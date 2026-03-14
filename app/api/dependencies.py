from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.security.jwt_handler import decode_access_token
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.database.models import Usuario
from app.core.exceptions import NaoAutenticadoException, SemPermissaoException

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    token = credentials.credentials
    payload = decode_access_token(token)
    usuario_id = payload.get('sub')
    if not usuario_id:
        raise NaoAutenticadoException()
    usuario = UsuarioRepository.get_by_id(db, int(usuario_id))
    if not usuario:
        raise NaoAutenticadoException()
    return usuario

def require_roles(roles: list):
    def role_checker(
        current_user: Usuario = Depends(get_current_user)
    ) -> Usuario:
        if current_user.perfil not in roles:
            raise SemPermissaoException()
        return current_user
    return role_checker
