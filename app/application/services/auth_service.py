from sqlalchemy.orm import Session
from datetime import timedelta
from app.infrastructure.database.models import Usuario, Fidelidade
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.security.password import hash_password, verify_password
from app.infrastructure.security.jwt_handler import create_access_token
from app.application.dtos.auth_schemas import LoginRequest, LoginResponse, UsuarioCreate
from app.core.config import settings
from app.core.exceptions import CredenciaisInvalidasException, ValidacaoException

class AuthService:
    
    @staticmethod
    def login(db: Session, request: LoginRequest) -> LoginResponse:
        """Autentica usuário e retorna token JWT"""
        
        # Buscar usuário
        usuario = UsuarioRepository.get_by_email(db, request.email)
        
        if not usuario or not verify_password(request.senha, usuario.senha_hash):
            raise CredenciaisInvalidasException()
        
        if not usuario.ativo:
            raise ValidacaoException([{
                "field": "email",
                "issue": "Usuário desativado."
            }])
        
        # Criar token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email,
                "perfil": usuario.perfil.value
            },
            expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil.value
            }
        )
    
    @staticmethod
    def registrar_usuario(db: Session, request: UsuarioCreate) -> Usuario:
        """Registra novo usuário"""
        
        # Verificar se email já existe
        if UsuarioRepository.get_by_email(db, request.email):
            raise ValidacaoException([{
                "field": "email",
                "issue": "E-mail já cadastrado."
            }])
        
        # Criar usuário
        novo_usuario = Usuario(
            nome=request.nome,
            email=request.email,
            senha_hash=hash_password(request.senha),
            cpf=request.cpf,
            telefone=request.telefone,
            perfil=request.perfil,
            consentimento_lgpd=request.consentimento_lgpd,
            ativo=True
        )
        
        usuario_criado = UsuarioRepository.create(db, novo_usuario)
        
        # Criar registro de fidelidade se for cliente
        if request.perfil == "CLIENTE" and request.consentimento_lgpd:
            fidelidade = Fidelidade(usuario_id=usuario_criado.id)
            db.add(fidelidade)
            db.commit()
        
        return usuario_criado