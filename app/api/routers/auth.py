from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services.auth_service import AuthService
from app.application.dtos.auth_schemas import (
    LoginRequest, 
    LoginResponse, 
    UsuarioCreate, 
    UsuarioResponse
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuário",
    description="Autentica usuário com e-mail e senha, retornando token JWT"
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    **Endpoint de login**
    
    - Valida credenciais
    - Retorna token JWT
    - Token expira em 30 minutos (padrão)
    
    **Exemplo de request:**
```json

{
    "email": "cliente@exemplo.com",
    "senha": "Senha@123"
}

**Códigos de status:**
    - 200: Login bem-sucedido
    - 401: Credenciais inválidas
    - 422: Dados inválidos
    """
    return AuthService.login(db, request)

@router.post(
    "/registrar",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria novo usuário no sistema"
)
def registrar(request: UsuarioCreate, db: Session = Depends(get_db)):
    """
    **Registro de novo usuário**
    
    - Valida e-mail único
    - Cria hash da senha
    - Se perfil CLIENTE e consentimento_lgpd=true, cria registro de fidelidade
    
    **Exemplo de request:**
```json
{
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "senha": "Senha@123",
    "cpf": "123.456.789-00",
    "telefone": "(81) 99999-9999",
    "perfil": "CLIENTE",
    "consentimento_lgpd": true
}

**Códigos de status:**
    - 201: Usuário criado
    - 422: E-mail já cadastrado ou dados inválidos
    """
    return AuthService.registrar_usuario(db, request)