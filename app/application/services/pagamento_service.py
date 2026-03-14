from sqlalchemy.orm import Session
from app.infrastructure.database.models import Pagamento, Pedido, LogAuditoria
from app.infrastructure.external.pagamento_mock import PagamentoMockService
from app.domain.enums import StatusPagamentoEnum, StatusPedidoEnum
from app.core.exceptions import NaoEncontradoException, ValidacaoException

class PagamentoService:
    
    @staticmethod
    def processar_pagamento(db: Session, pedido_id: int, usuario_id: int) -> dict:
        """Processa pagamento via gateway mock"""
        
        # Buscar pedido
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        
        if not pedido:
            raise NaoEncontradoException("Pedido")
        
        # Buscar pagamento
        pagamento = db.query(Pagamento).filter(
            Pagamento.pedido_id == pedido_id
        ).first()
        
        if not pagamento:
            raise NaoEncontradoException("Pagamento")
        
        if pagamento.status != StatusPagamentoEnum.PENDENTE:
            raise ValidacaoException([{
                "field": "pagamento",
                "issue": f"Pagamento já processado com status: {pagamento.status.value}"
            }])
        
        # Chamar gateway mock
        resposta_gateway = PagamentoMockService.processar_pagamento(
            valor=float(pedido.valor_total),
            forma_pagamento=pagamento.forma_pagamento.value,
            pedido_codigo=pedido.codigo
        )
        
        # Atualizar pagamento
        pagamento.transacao_id = resposta_gateway["transacao_id"]
        pagamento.resposta_gateway = resposta_gateway
        
        if resposta_gateway["status"] == "APROVADO":
            pagamento.status = StatusPagamentoEnum.APROVADO
            pedido.status = StatusPedidoEnum.PAGAMENTO_APROVADO
        else:
            pagamento.status = StatusPagamentoEnum.NEGADO
            pedido.status = StatusPedidoEnum.PAGAMENTO_NEGADO
        
        # Log de auditoria
        log = LogAuditoria(
            usuario_id=usuario_id,
            acao="PROCESSAR_PAGAMENTO",
            entidade="Pagamento",
            entidade_id=pagamento.id,
            dados={
                "pedido_codigo": pedido.codigo,
                "status": pagamento.status.value,
                "transacao_id": pagamento.transacao_id
            }
        )
        db.add(log)
        
        db.commit()
        db.refresh(pagamento)
        
        return {
            "pagamento_id": pagamento.id,
            "status": pagamento.status.value,
            "transacao_id": pagamento.transacao_id,
            "mensagem": resposta_gateway["mensagem"],
            "pedido_status": pedido.status.value
        }