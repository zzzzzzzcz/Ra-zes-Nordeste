from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database.models import Pedido, ItemPedido
from app.domain.enums import StatusPedidoEnum, CanalPedidoEnum
from typing import Optional, List

class PedidoRepository:
    
    @staticmethod
    def create(db: Session, pedido: Pedido) -> Pedido:
        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        return pedido
    
    @staticmethod
    def get_by_id(db: Session, pedido_id: int) -> Optional[Pedido]:
        return db.query(Pedido)\
            .options(joinedload(Pedido.itens).joinedload(ItemPedido.produto))\
            .filter(Pedido.id == pedido_id)\
            .first()
    
    @staticmethod
    def get_by_codigo(db: Session, codigo: str) -> Optional[Pedido]:
        return db.query(Pedido)\
            .options(joinedload(Pedido.itens).joinedload(ItemPedido.produto))\
            .filter(Pedido.codigo == codigo)\
            .first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[StatusPedidoEnum] = None,
        canal_pedido: Optional[CanalPedidoEnum] = None,
        unidade_id: Optional[int] = None
    ) -> List[Pedido]:
        query = db.query(Pedido).options(
            joinedload(Pedido.itens).joinedload(ItemPedido.produto)
        )
        
        if status:
            query = query.filter(Pedido.status == status)
        
        if canal_pedido:
            query = query.filter(Pedido.canal_pedido == canal_pedido)
        
        if unidade_id:
            query = query.filter(Pedido.unidade_id == unidade_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, pedido: Pedido) -> Pedido:
        db.commit()
        db.refresh(pedido)
        return pedido