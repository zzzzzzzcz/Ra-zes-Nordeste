from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, Numeric, ForeignKey, Text, JSON
)
from sqlalchemy import Enum as SAEnum   # ← alias para não conflitar com enum do Python
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.database.connection import Base
from app.domain.enums import (
    PerfilEnum, CanalPedidoEnum, StatusPedidoEnum,
    StatusPagamentoEnum, FormaPagamentoEnum,
    TipoMovimentacaoEstoqueEnum, CategoriaEnum
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id                  = Column(Integer, primary_key=True, index=True)
    nome                = Column(String(255), nullable=False)
    email               = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash          = Column(String(255), nullable=False)
    cpf                 = Column(String(14), unique=True, nullable=True)
    telefone            = Column(String(20), nullable=True)
    perfil              = Column(SAEnum(PerfilEnum), nullable=False, default=PerfilEnum.CLIENTE)
    ativo               = Column(Boolean, default=True)
    consentimento_lgpd  = Column(Boolean, default=False)
    data_consentimento  = Column(DateTime, nullable=True)
    created_at          = Column(DateTime, default=datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pedidos    = relationship("Pedido", back_populates="usuario")
    fidelidade = relationship("Fidelidade", back_populates="usuario", uselist=False)
    logs       = relationship("LogAuditoria", back_populates="usuario")


class Unidade(Base):
    __tablename__ = "unidades"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(255), nullable=False)
    cnpj      = Column(String(18), unique=True, nullable=False)
    endereco  = Column(Text, nullable=True)
    cidade    = Column(String(100), nullable=False)
    estado    = Column(String(2), nullable=False)
    telefone  = Column(String(20), nullable=True)
    ativa     = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pedidos          = relationship("Pedido", back_populates="unidade")
    estoques         = relationship("Estoque", back_populates="unidade")
    produtos_unidade = relationship("ProdutoUnidade", back_populates="unidade")


class Produto(Base):
    __tablename__ = "produtos"

    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column(String(255), nullable=False)
    descricao   = Column(Text, nullable=True)
    categoria   = Column(SAEnum(CategoriaEnum), nullable=False)
    imagem_url  = Column(String(500), nullable=True)
    ativo       = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    estoques         = relationship("Estoque", back_populates="produto")
    produtos_unidade = relationship("ProdutoUnidade", back_populates="produto")
    itens_pedido     = relationship("ItemPedido", back_populates="produto")


class ProdutoUnidade(Base):
    __tablename__ = "produtos_unidade"

    id          = Column(Integer, primary_key=True, index=True)
    unidade_id  = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    produto_id  = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    preco       = Column(Numeric(10, 2), nullable=False)
    disponivel  = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    unidade = relationship("Unidade", back_populates="produtos_unidade")
    produto = relationship("Produto", back_populates="produtos_unidade")


class Estoque(Base):
    __tablename__ = "estoque"

    id          = Column(Integer, primary_key=True, index=True)
    unidade_id  = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    produto_id  = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade  = Column(Integer, default=0)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    unidade       = relationship("Unidade", back_populates="estoques")
    produto       = relationship("Produto", back_populates="estoques")
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="estoque")


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"

    id          = Column(Integer, primary_key=True, index=True)
    estoque_id  = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    tipo        = Column(SAEnum(TipoMovimentacaoEstoqueEnum), nullable=False)
    quantidade  = Column(Integer, nullable=False)
    observacao  = Column(Text, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    estoque = relationship("Estoque", back_populates="movimentacoes")


class Pedido(Base):
    __tablename__ = "pedidos"

    id           = Column(Integer, primary_key=True, index=True)
    codigo       = Column(String(50), unique=True, index=True, nullable=False)
    usuario_id   = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id   = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    canal_pedido = Column(SAEnum(CanalPedidoEnum), nullable=False)   # ⭐ OBRIGATÓRIO
    status       = Column(SAEnum(StatusPedidoEnum), default=StatusPedidoEnum.AGUARDANDO_PAGAMENTO)
    valor_total  = Column(Numeric(10, 2), default=0)
    observacao   = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario  = relationship("Usuario", back_populates="pedidos")
    unidade  = relationship("Unidade", back_populates="pedidos")
    itens    = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id             = Column(Integer, primary_key=True, index=True)
    pedido_id      = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id     = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade     = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal       = Column(Numeric(10, 2), nullable=False)

    pedido  = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id               = Column(Integer, primary_key=True, index=True)
    pedido_id        = Column(Integer, ForeignKey("pedidos.id"), nullable=False, unique=True)
    forma_pagamento  = Column(SAEnum(FormaPagamentoEnum), nullable=False)
    status           = Column(SAEnum(StatusPagamentoEnum), default=StatusPagamentoEnum.PENDENTE)
    transacao_id     = Column(String(255), nullable=True)
    valor            = Column(Numeric(10, 2), nullable=False)
    resposta_gateway = Column(JSON, nullable=True)
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pedido = relationship("Pedido", back_populates="pagamento")


class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id               = Column(Integer, primary_key=True, index=True)
    usuario_id       = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True)
    saldo_pontos     = Column(Integer, default=0)
    total_acumulado  = Column(Integer, default=0)
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario   = relationship("Usuario", back_populates="fidelidade")
    historico = relationship("HistoricoFidelidade", back_populates="fidelidade")


class HistoricoFidelidade(Base):
    __tablename__ = "historico_fidelidade"

    id           = Column(Integer, primary_key=True, index=True)
    fidelidade_id = Column(Integer, ForeignKey("fidelidade.id"), nullable=False)
    tipo         = Column(String(50), nullable=False)
    pontos       = Column(Integer, nullable=False)
    descricao    = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    fidelidade = relationship("Fidelidade", back_populates="historico")


class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    acao        = Column(String(100), nullable=False)
    entidade    = Column(String(100), nullable=False)
    entidade_id = Column(Integer, nullable=True)
    dados       = Column(JSON, nullable=True)
    ip_address  = Column(String(50), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="logs")