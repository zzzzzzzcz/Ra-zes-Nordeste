from enum import Enum

class PerfilEnum(str, Enum):
    CLIENTE = "CLIENTE"
    ATENDENTE = "ATENDENTE"
    COZINHA = "COZINHA"
    GERENTE = "GERENTE"
    ADMIN = "ADMIN"

class CanalPedidoEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    WEB = "WEB"
    PICKUP = "PICKUP"

class StatusPedidoEnum(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGAMENTO_APROVADO = "PAGAMENTO_APROVADO"
    PAGAMENTO_NEGADO = "PAGAMENTO_NEGADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class StatusPagamentoEnum(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    NEGADO = "NEGADO"
    ESTORNADO = "ESTORNADO"

class FormaPagamentoEnum(str, Enum):
    DINHEIRO = "DINHEIRO"
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    PIX = "PIX"
    MOCK = "MOCK"

class TipoMovimentacaoEstoqueEnum(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    AJUSTE = "AJUSTE"

class CategoriaEnum(str, Enum):
    SALGADO = "SALGADO"
    DOCE = "DOCE"
    BEBIDA = "BEBIDA"
    CAFE_MANHA = "CAFE_MANHA"
    ALMOCO = "ALMOCO"