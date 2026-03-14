from pydantic import BaseModel, EmailStr, Field
from app.domain.enums import PerfilEnum
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: dict

class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    senha: str = Field(..., min_length=6)
    cpf: str | None = None
    telefone: str | None = None
    perfil: PerfilEnum = PerfilEnum.CLIENTE
    consentimento_lgpd: bool = False

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: PerfilEnum
    ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True