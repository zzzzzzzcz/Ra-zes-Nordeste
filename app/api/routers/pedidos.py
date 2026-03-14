from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import Usuario
from app.infrastructure.repositories.pedido_repository import PedidoRepository
from app.application.services.pedido_service import PedidoService
from app.application.services.fidelidade_service import FidelidadeService
from app.application.dtos.pedido_schemas import (
    PedidoCreate, 
    PedidoResponse,
    AtualizarStatusRequest
)
from app.domain.enums import StatusPedidoEnum, CanalPedidoEnum, PerfilEnum
from app.api.dependencies import get_current_user, require_roles
from app.core.exceptions import NaoEncontradoException

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar pedido",
    description="Cria novo pedido validando estoque e calculando total"
)
def criar_pedido(
    request: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Criar pedido (fluxo crítico) ⭐**
    
    - Valida disponibilidade dos produtos na unidade
    - Verifica estoque
    - Calcula valor total
    - Cria registro de pagamento pendente
    - **Requer campo obrigatório: canal_pedido**
    
    **Exemplo de request:**
```json
    {
        "unidade_id": 1,
        "canal_pedido": "TOTEM",
        "itens": [
            {"produto_id": 1, "quantidade": 2},
            {"produto_id": 3, "quantidade": 1}
        ],
        "forma_pagamento": "PIX",
        "observacao": "Sem cebola"
    }
```
    
    **Códigos de status:**
    - 201: Pedido criado
    - 401: Não autenticado
    - 404: Produto/Unidade não encontrado
    - 409: Estoque insuficiente
    - 422: Dados inválidos (ex: canal_pedido ausente)
    """
    pedido = PedidoService.criar_pedido(db, current_user.id, request)
    
    # Acumular pontos fidelidade (1 ponto a cada R$ 10)
    if current_user.perfil == PerfilEnum.CLIENTE:
        pontos = int(float(pedido.valor_total) // 10)
        if pontos > 0:
            FidelidadeService.acumular_pontos(
                db, 
                current_user.id, 
                pontos,
                f"Pedido {pedido.codigo}"
            )
    
    return PedidoService.converter_para_response(pedido)

@router.get(
    "",
    summary="Listar pedidos",
    description="Lista pedidos com filtros opcionais"
)
def listar_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[StatusPedidoEnum] = None,
    canal_pedido: Optional[CanalPedidoEnum] = None,  # ⭐ Filtro por canal
    unidade_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Lista pedidos com filtros**
    
    **Query params:**
    - skip, limit: paginação
    - status: filtrar por status (ex: AGUARDANDO_PAGAMENTO)
    - canal_pedido: filtrar por canal (ex: TOTEM, APP, BALCAO) ⭐
    - unidade_id: filtrar por unidade
    
    **Exemplo:**
```
    GET /pedidos?canal_pedido=TOTEM&status=PRONTO
```
    
    **Códigos de status:**
    - 200: Lista retornada
    - 401: Não autenticado
    """
    pedidos = PedidoRepository.get_all(
        db, 
        skip=skip, 
        limit=limit,
        status=status,
        canal_pedido=canal_pedido,
        unidade_id=unidade_id
    )
    
    return {
        "total": len(pedidos),
        "skip": skip,
        "limit": limit,
        "filtros": {
            "status": status.value if status else None,
            "canal_pedido": canal_pedido.value if canal_pedido else None,
            "unidade_id": unidade_id
        },
        "pedidos": [
            PedidoService.converter_para_response(p) for p in pedidos
        ]
    }

@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
    summary="Buscar pedido por ID"
)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Busca pedido específico**
    
    **Códigos de status:**
    - 200: Pedido encontrado
    - 401: Não autenticado
    - 404: Pedido não encontrado
    """
    pedido = PedidoRepository.get_by_id(db, pedido_id)
    if not pedido:
        raise NaoEncontradoException("Pedido")
    
    return PedidoService.converter_para_response(pedido)

@router.patch(
    "/{pedido_id}/status",
    summary="Atualizar status do pedido",
    description="Atualiza status do pedido (requer permissão)"
)
def atualizar_status(
    pedido_id: int,
    request: AtualizarStatusRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles([PerfilEnum.ATENDENTE, PerfilEnum.COZINHA, PerfilEnum.GERENTE, PerfilEnum.ADMIN]))
):
    """
    **Atualiza status do pedido**
    
    - Atendentes/Cozinha/Gerentes/Admins podem atualizar
    - Ao passar para EM_PREPARO, dá baixa no estoque
    - Registra log de auditoria
    
    **Exemplo de request:**
```json
    {
        "status": "EM_PREPARO"
    }
```
    
    **Fluxo de status:**
    - AGUARDANDO_PAGAMENTO → PAGAMENTO_APROVADO/NEGADO
    - PAGAMENTO_APROVADO → EM_PREPARO → PRONTO → ENTREGUE
    - Qualquer status → CANCELADO
    
    **Códigos de status:**
    - 200: Status atualizado
    - 401: Não autenticado
    - 403: Sem permissão
    - 404: Pedido não encontrado
    """
    pedido = PedidoService.atualizar_status(
        db, 
        pedido_id, 
        request.status,
        current_user.id
    )
    
    return PedidoService.converter_para_response(pedido)