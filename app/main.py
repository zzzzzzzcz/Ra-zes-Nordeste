from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

from app.core.config import settings
from app.core.exceptions import RaizesException
from app.infrastructure.database.connection import engine, Base
from app.api.routers import auth, produtos, pedidos, pagamentos, estoque, fidelidade

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## API da Rede Raízes do Nordeste 🌾
    
    Sistema de gerenciamento de pedidos para rede de lanchonetes nordestinas.
    
    ### Funcionalidades principais:
    - 🔐 Autenticação JWT com perfis de acesso
    - 🛒 Gestão de pedidos multicanal (APP, TOTEM, BALCÃO, WEB, PICKUP)
    - 📦 Controle de estoque por unidade
    - 💳 Integração com pagamento mock
    - ⭐ Programa de fidelização
    - 📊 Logs de auditoria (LGPD)
    
    ### Perfis de usuário:
    - **CLIENTE**: realizar pedidos, consultar fidelidade
    - **ATENDENTE**: atualizar status de pedidos
    - **COZINHA**: atualizar status de preparo
    - **GERENTE**: gestão de estoque, relatórios
    - **ADMIN**: acesso total
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tratamento global de exceções
@app.exception_handler(RaizesException)
async def raizes_exception_handler(request: Request, exc: RaizesException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            **exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url.path),
            "request_id": str(uuid.uuid4())
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "ERRO_INTERNO",
            "message": "Erro interno do servidor.",
            "details": [{"issue": str(exc)}] if settings.DEBUG else [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url.path),
            "request_id": str(uuid.uuid4())
        }
    )

# Routers
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(estoque.router)
app.include_router(fidelidade.router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }