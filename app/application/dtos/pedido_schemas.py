from pydantic import BaseModel, Field, validator
from typing import List
from decimal import Decimal
from datetime import datetime
from app.domain.enums import CanalPedidoEnum, StatusPedidoEnum, FormaPagamentoEnum

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)

class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedidoEnum  # ⭐ OBRIGATÓRIO
    itens: List[ItemPedidoCreate] = Field(..., min_length=1)
    forma_pagamento: FormaPagamentoEnum
    observacao: str | None = None

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    produto_nome: str
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    id: int
    codigo: str
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    status: StatusPedidoEnum
    valor_total: Decimal
    itens: List[ItemPedidoResponse]
    observacao: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AtualizarStatusRequest(BaseModel):
    status: StatusPedidoEnum