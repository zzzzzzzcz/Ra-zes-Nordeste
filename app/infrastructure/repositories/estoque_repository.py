from sqlalchemy.orm import Session
from app.infrastructure.database.models import Estoque, MovimentacaoEstoque
from typing import Optional

class EstoqueRepository:
    
    @staticmethod
    def get_by_unidade_produto(
        db: Session,
        unidade_id: int,
        produto_id: int
    ) -> Optional[Estoque]:
        return db.query(Estoque).filter(
            Estoque.unidade_id == unidade_id,
            Estoque.produto_id == produto_id
        ).first()
    
    @staticmethod
    def create(db: Session, estoque: Estoque) -> Estoque:
        db.add(estoque)
        db.commit()
        db.refresh(estoque)
        return estoque
    
    @staticmethod
    def update(db: Session, estoque: Estoque) -> Estoque:
        db.commit()
        db.refresh(estoque)
        return estoque
    
    @staticmethod
    def criar_movimentacao(
        db: Session,
        movimentacao: MovimentacaoEstoque
    ) -> MovimentacaoEstoque:
        db.add(movimentacao)
        db.commit()
        db.refresh(movimentacao)
        return movimentacao
    
    @staticmethod
    def get_estoque_unidade(db: Session, unidade_id: int, skip: int = 0, limit: int = 100):
        return db.query(Estoque).filter(
            Estoque.unidade_id == unidade_id
        ).offset(skip).limit(limit).all()