from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import Usuario, Estoque, MovimentacaoEstoque
from app.infrastructure.repositories.estoque_repository import EstoqueRepository
from app.domain.enums import TipoMovimentacaoEstoqueEnum, PerfilEnum
from app.api.dependencies import require_roles
from app.core.exceptions import NaoEncontradoException

router = APIRouter(prefix="/estoque", tags=["Estoque"])

class MovimentacaoRequest(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    tipo: TipoMovimentacaoEstoqueEnum
    observacao: str | None = None

@router.get(
    "/unidade/{unidade_id}",
    summary="Consultar estoque da unidade"
)
def consultar_estoque_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles([PerfilEnum.GERENTE, PerfilEnum.ADMIN]))
):
    """
    **Consulta estoque de uma unidade**
    
    - Requer permissão de Gerente ou Admin
    
    **Códigos de status:**
    - 200: Estoque retornado
    - 401: Não autenticado
    - 403: Sem permissão
    """
    estoques = EstoqueRepository.get_estoque_unidade(db, unidade_id)
    
    return {
        "unidade_id": unidade_id,
        "total_itens": len(estoques),
        "estoque": [
            {
                "produto_id": e.produto_id,
                "produto_nome": e.produto.nome,
                "quantidade": e.quantidade,
                "updated_at": e.updated_at
            }
            for e in estoques
        ]
    }

@router.post(
    "/movimentar",
    status_code=status.HTTP_201_CREATED,
    summary="Movimentar estoque",
    description="Registra entrada, saída ou ajuste de estoque"
)
def movimentar_estoque(
    unidade_id: int,
    request: MovimentacaoRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles([PerfilEnum.GERENTE, PerfilEnum.ADMIN]))
):
    """
    **Movimentação de estoque**
    
    - ENTRADA: adiciona quantidade
    - SAIDA: remove quantidade
    - AJUSTE: define quantidade exata
    
    **Exemplo de request:**
```json
    {
        "produto_id": 1,
        "quantidade": 50,
        "tipo": "ENTRADA",
        "observacao": "Recebimento fornecedor"
    }
```
    
    **Códigos de status:**
    - 201: Movimentação registrada
    - 401: Não autenticado
    - 403: Sem permissão
    """
    # Buscar ou criar estoque
    estoque = EstoqueRepository.get_by_unidade_produto(
        db, unidade_id, request.produto_id
    )
    
    if not estoque:
        estoque = Estoque(
            unidade_id=unidade_id,
            produto_id=request.produto_id,
            quantidade=0
        )
        estoque = EstoqueRepository.create(db, estoque)
    
    # Aplicar movimentação
    if request.tipo == TipoMovimentacaoEstoqueEnum.ENTRADA:
        estoque.quantidade += request.quantidade
    elif request.tipo == TipoMovimentacaoEstoqueEnum.SAIDA:
        estoque.quantidade -= request.quantidade
    elif request.tipo == TipoMovimentacaoEstoqueEnum.AJUSTE:
        estoque.quantidade = request.quantidade
    
    estoque = EstoqueRepository.update(db, estoque)
    
    # Registrar movimentação
    movimentacao = MovimentacaoEstoque(
        estoque_id=estoque.id,
        tipo=request.tipo,
        quantidade=request.quantidade,
        observacao=request.observacao
    )
    EstoqueRepository.criar_movimentacao(db, movimentacao)
    
    return {
        "mensagem": "Movimentação registrada com sucesso",
        "estoque": {
            "produto_id": estoque.produto_id,
            "unidade_id": estoque.unidade_id,
            "quantidade_atual": estoque.quantidade
        }
    }