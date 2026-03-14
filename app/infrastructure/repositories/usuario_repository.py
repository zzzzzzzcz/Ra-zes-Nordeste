from sqlalchemy.orm import Session
from app.infrastructure.database.models import Usuario
from typing import Optional

class UsuarioRepository:
    
    @staticmethod
    def create(db: Session, usuario: Usuario) -> Usuario:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def get_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, usuario: Usuario) -> Usuario:
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def delete(db: Session, usuario: Usuario):
        db.delete(usuario)
        db.commit()