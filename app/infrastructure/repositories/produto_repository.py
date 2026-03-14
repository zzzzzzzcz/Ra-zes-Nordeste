from sqlalchemy.orm import Session
from app.infrastructure.database.models import Produto, ProdutoUnidade
from typing import Optional, List

class ProdutoRepository:
    
    @staticmethod
    def get_by_id(db: Session, produto_id: int) -> Optional[Produto]:
        return db.query(Produto).filter(Produto.id == produto_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Produto]:
        return db.query(Produto).filter(Produto.ativo == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_produtos_unidade(db: Session, unidade_id: int) -> List[ProdutoUnidade]:
        return db.query(ProdutoUnidade).filter(
            ProdutoUnidade.unidade_id == unidade_id,
            ProdutoUnidade.disponivel == True
        ).all()
    
    @staticmethod
    def get_produto_unidade(
        db: Session,
        unidade_id: int,
        produto_id: int
    ) -> Optional[ProdutoUnidade]:
        return db.query(ProdutoUnidade).filter(
            ProdutoUnidade.unidade_id == unidade_id,
            ProdutoUnidade.produto_id == produto_id
        ).first()