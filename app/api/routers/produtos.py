from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.infrastructure.database.models import Usuario
from app.api.dependencies import get_current_user
from app.core.exceptions import NaoEncontradoException

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get(
    "",
    summary="Listar produtos",
    description="Lista todos os produtos ativos do sistema"
)
def listar_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    **Lista produtos**
    
    - Retorna apenas produtos ativos
    - Suporta paginação
    
    **Query params:**
    - skip: número de registros a pular (padrão: 0)
    - limit: quantidade de registros (padrão: 10, máx: 100)
    
    **Códigos de status:**
    - 200: Lista retornada com sucesso
    """
    produtos = ProdutoRepository.get_all(db, skip=skip, limit=limit)
    return {
        "total": len(produtos),
        "skip": skip,
        "limit": limit,
        "produtos": produtos
    }

@router.get(
    "/{produto_id}",
    summary="Buscar produto por ID"
)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    **Busca produto específico**
    
    **Path params:**
    - produto_id: ID do produto
    
    **Códigos de status:**
    - 200: Produto encontrado
    - 404: Produto não encontrado
    """
    produto = ProdutoRepository.get_by_id(db, produto_id)
    if not produto:
        raise NaoEncontradoException("Produto")
    return produto

@router.get(
    "/unidade/{unidade_id}",
    summary="Listar produtos de uma unidade",
    description="Lista produtos disponíveis em uma unidade específica com preços"
)
def listar_produtos_unidade(unidade_id: int, db: Session = Depends(get_db)):
    """
    **Cardápio da unidade**
    
    - Retorna apenas produtos disponíveis na unidade
    - Inclui preço específico da unidade
    
    **Path params:**
    - unidade_id: ID da unidade
    
    **Códigos de status:**
    - 200: Lista retornada
    """
    produtos_unidade = ProdutoRepository.get_produtos_unidade(db, unidade_id)
    
    return {
        "unidade_id": unidade_id,
        "total": len(produtos_unidade),
        "produtos": [
            {
                "id": pu.produto.id,
                "nome": pu.produto.nome,
                "descricao": pu.produto.descricao,
                "categoria": pu.produto.categoria.value,
                "preco": float(pu.preco),
                "disponivel": pu.disponivel
            }
            for pu in produtos_unidade
        ]
    }