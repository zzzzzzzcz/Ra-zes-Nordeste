from sqlalchemy.orm import Session
from app.infrastructure.database.models import Fidelidade, HistoricoFidelidade
from typing import Optional

class FidelidadeRepository:
    
    @staticmethod
    def get_by_usuario_id(db: Session, usuario_id: int) -> Optional[Fidelidade]:
        return db.query(Fidelidade).filter(
            Fidelidade.usuario_id == usuario_id
        ).first()
    
    @staticmethod
    def create(db: Session, fidelidade: Fidelidade) -> Fidelidade:
        db.add(fidelidade)
        db.commit()
        db.refresh(fidelidade)
        return fidelidade
    
    @staticmethod
    def update(db: Session, fidelidade: Fidelidade) -> Fidelidade:
        db.commit()
        db.refresh(fidelidade)
        return fidelidade
    
    @staticmethod
    def criar_historico(
        db: Session,
        historico: HistoricoFidelidade
    ) -> HistoricoFidelidade:
        db.add(historico)
        db.commit()
        db.refresh(historico)
        return historico