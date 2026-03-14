import random
import uuid
from datetime import datetime
from typing import Dict, Any

class PagamentoMockService:
    """
    Simula um gateway de pagamento externo.
    Retorna aprovado ou negado aleatoriamente.
    """
    
    @staticmethod
    def processar_pagamento(
        valor: float,
        forma_pagamento: str,
        pedido_codigo: str
    ) -> Dict[str, Any]:
        """
        Simula processamento de pagamento
        
        Returns:
            dict com: status, transacao_id, mensagem, timestamp
        """
        
        # Simula 80% de aprovação, 20% de negação
        aprovado = random.random() < 0.8
        
        transacao_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        if aprovado:
            return {
                "status": "APROVADO",
                "transacao_id": transacao_id,
                "mensagem": "Pagamento aprovado com sucesso.",
                "valor": valor,
                "forma_pagamento": forma_pagamento,
                "pedido_codigo": pedido_codigo,
                "timestamp": datetime.utcnow().isoformat(),
                "gateway": "MOCK_PAYMENT_GATEWAY_V1"
            }
        else:
            return {
                "status": "NEGADO",
                "transacao_id": transacao_id,
                "mensagem": "Pagamento negado. Saldo insuficiente ou cartão bloqueado.",
                "valor": valor,
                "forma_pagamento": forma_pagamento,
                "pedido_codigo": pedido_codigo,
                "timestamp": datetime.utcnow().isoformat(),
                "gateway": "MOCK_PAYMENT_GATEWAY_V1",
                "codigo_erro": "ERR_" + str(random.randint(1000, 9999))
            }