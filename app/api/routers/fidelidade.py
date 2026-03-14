from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import Usuario
from app.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from app.application.services.fidelidade_service import FidelidadeService
from app.api.dependencies import get_current_user
from app.core.exceptions import NaoEncontradoException

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])

class ResgatePontosRequest(BaseModel):
    pontos: int = Field(..., gt=0)
    descricao: str | None = None

@router.get(
    "/saldo",
    summary="Consultar saldo de pontos"
)
def consultar_saldo(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Consulta saldo de pontos do usuário**
    
    - Retorna saldo atual e total acumulado
    
    **Códigos de status:**
    - 200: Saldo retornado
    - 401: Não autenticado
    - 404: Programa de fidelidade não encontrado
    """
    fidelidade = FidelidadeRepository.get_by_usuario_id(db, current_user.id)
    
    if not fidelidade:
        raise NaoEncontradoException("Programa de fidelidade")
    
    return {
        "usuario_id": current_user.id,
        "saldo_pontos": fidelidade.saldo_pontos,
        "total_acumulado": fidelidade.total_acumulado,
        "created_at": fidelidade.created_at
    }

@router.get(
    "/historico",
    summary="Histórico de pontos"
)
def historico_pontos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Histórico de acúmulos e resgates**
    
    **Códigos de status:**
    - 200: Histórico retornado
    - 401: Não autenticado
    - 404: Programa de fidelidade não encontrado
    """
    fidelidade = FidelidadeRepository.get_by_usuario_id(db, current_user.id)
    
    if not fidelidade:
        raise NaoEncontradoException("Programa de fidelidade")
    
    return {
        "usuario_id": current_user.id,
        "saldo_atual": fidelidade.saldo_pontos,
        "historico": [
            {
                "id": h.id,
                "tipo": h.tipo,
                "pontos": h.pontos,
                "descricao": h.descricao,
                "created_at": h.created_at
            }
            for h in fidelidade.historico
        ]
    }

@router.post(
    "/resgatar",
    summary="Resgatar pontos"
)
def resgatar_pontos(
    request: ResgatePontosRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Resgate de pontos**
    
    - Valida saldo disponível
    - Registra histórico
    
    **Exemplo de request:**
```json
    {
        "pontos": 100,
        "descricao": "Desconto no pedido PED-ABC123"
    }
```
    
    **Códigos de status:**
    - 200: Resgate realizado
    - 401: Não autenticado
    - 404: Programa de fidelidade não encontrado
    - 422: Saldo insuficiente
    """
    fidelidade = FidelidadeService.resgatar_pontos(
        db,
        current_user.id,
        request.pontos,
        request.descricao
    )
    
    return {
        "mensagem": "Pontos resgatados com sucesso",
        "pontos_resgatados": request.pontos,
        "saldo_atual": fidelidade.saldo_pontos
    }