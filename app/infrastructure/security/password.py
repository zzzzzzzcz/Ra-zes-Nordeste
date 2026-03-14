from passlib.context import CryptContext

# Versão compatível com bcrypt 4.x
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def hash_password(password: str) -> str:
    """Gera hash bcrypt da senha (trunca em 72 bytes se necessário)"""
    # bcrypt tem limite de 72 bytes — truncamos para evitar erro
    if isinstance(password, str):
        password = password.encode("utf-8")
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)