from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import Usuario
from app.application.services.pagamento_service import PagamentoService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post(
    "/processar/{pedido_id}",
    summary="Processar pagamento (mock)",
    description="Simula processamento de pagamento via gateway externo"
)
def processar_pagamento(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    **Processar pagamento mock ⭐**
    
    - Simula chamada a gateway externo
    - Retorna aprovado (80%) ou negado (20%) aleatoriamente
    - Atualiza status do pedido
    - Registra transacao_id e payload completo
    
    **Path params:**
    - pedido_id: ID do pedido
    
    **Response (aprovado):**
```json
    {
        "pagamento_id": 1,
        "status": "APROVADO",
        "transacao_id": "TXN-ABC123DEF456",
        "mensagem": "Pagamento aprovado com sucesso.",
        "pedido_status": "PAGAMENTO_APROVADO"
    }
```
    
    **Response (negado):**
```json
    {
        "pagamento_id": 1,
        "status": "NEGADO",
        "transacao_id": "TXN-XYZ789GHI012",
        "mensagem": "Pagamento negado. Saldo insuficiente ou cartão bloqueado.",
        "pedido_status": "PAGAMENTO_NEGADO"
    }
```
    
    **Códigos de status:**
    - 200: Pagamento processado (aprovado ou negado)
    - 401: Não autenticado
    - 404: Pedido/Pagamento não encontrado
    - 422: Pagamento já processado
    """
    resultado = PagamentoService.processar_pagamento(db, pedido_id, current_user.id)
    return resultado