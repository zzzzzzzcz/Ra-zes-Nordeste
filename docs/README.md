# 🌾 Raízes do Nordeste - API Back-End

> **Projeto Multidisciplinar - Trilha Back-End**  
> Sistema de gerenciamento de pedidos para rede de lanchonetes nordestinas com suporte a múltiplos canais de atendimento.

---

## 📋 Sobre o Projeto

API REST completa para a rede **Raízes do Nordeste**, desenvolvida como projeto final do curso, simulando um cenário real de mercado com:

- ✅ Autenticação JWT com perfis de acesso (RBAC)
- ✅ Gestão de pedidos multicanal (APP, TOTEM, BALCÃO, WEB, PICKUP)
- ✅ Controle de estoque por unidade
- ✅ Integração com gateway de pagamento (mock)
- ✅ Programa de fidelização com pontos
- ✅ Logs de auditoria (conformidade LGPD)
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Arquitetura em camadas
- ✅ Testes automatizados com Postman

---

## 🏗️ Arquitetura

### Estrutura em Camadas
```
app/
├── domain/          # Entidades e regras de negócio
├── application/     # Casos de uso e DTOs
├── infrastructure/  # Persistência, segurança, integrações
├── api/            # Controllers e rotas
└── core/           # Configurações e exceções
```

### Tecnologias Utilizadas

- **Framework**: FastAPI 0.104
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Migrations**: Alembic
- **Autenticação**: JWT (python-jose)
- **Senha**: bcrypt (passlib)
- **Validação**: Pydantic v2
- **Testes**: Pytest + Postman

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes)
- Git

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/raizes-nordeste-api.git
cd raizes-nordeste-api
```

### Passo 2: Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:
```bash
# Database
DATABASE_URL=sqlite:///./raizes_nordeste.db

# Security (IMPORTANTE: Mude a SECRET_KEY em produção!)
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-isso
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME="Raízes do Nordeste API"
APP_VERSION=1.0.0
DEBUG=True
```

**⚠️ IMPORTANTE**: Gere uma SECRET_KEY segura:
```bash
# No terminal Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Passo 5: Criar o Banco de Dados

#### Opção A: Migrations com Alembic (recomendado)
```bash
# Inicializar Alembic (já configurado)
alembic upgrade head
```

#### Opção B: Criar tabelas diretamente

As tabelas serão criadas automaticamente ao executar o seed.

### Passo 6: Popular o Banco (Seed)
```bash
python scripts/seed_data.py
```

**Saída esperada:**
```
🌱 Iniciando seed do banco de dados...

📝 Criando usuários...
✅ 6 usuários criados

🏪 Criando unidades...
✅ 3 unidades criadas

🍽️ Criando produtos...
✅ 13 produtos criados

💰 Vinculando produtos às unidades com preços...
✅ 39 vinculações produto-unidade criadas

📦 Criando registros de estoque...
✅ 39 registros de estoque criados

⭐ Criando programas de fidelidade...
✅ 2 programas de fidelidade criados

✨ Seed concluído com sucesso!

📊 Resumo:
   - 6 usuários
   - 3 unidades
   - 13 produtos
   - 39 vinculações produto-unidade
   - 39 registros de estoque
   - 2 programas de fidelidade

🔑 Credenciais de acesso:
   ADMIN: admin@raizes.com / Admin@123
   GERENTE: gerente@raizes.com / Gerente@123
   ATENDENTE: atendente@raizes.com / Atendente@123
   COZINHA: cozinha@raizes.com / Cozinha@123
   CLIENTE: ana@exemplo.com / Cliente@123
   CLIENTE: pedro@exemplo.com / Cliente@123
```

### Passo 7: Iniciar o Servidor
```bash
uvicorn app.main:app --reload
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📚 Documentação da API

### Swagger UI (Interativo)

Acesse: **http://localhost:8000/docs**

![Swagger Screenshot](docs/swagger-preview.png)

### ReDoc (Alternativo)

Acesse: **http://localhost:8000/redoc**

---

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Como Autenticar

1. **Faça login** no endpoint `/auth/login`:
```bash
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "ana@exemplo.com",
  "senha": "Cliente@123"
}
```

2. **Copie o `access_token`** da resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "user": {
    "id": 5,
    "nome": "Cliente Ana Silva",
    "email": "ana@exemplo.com",
    "perfil": "CLIENTE"
  }
}
```

3. **Use o token** nas requisições protegidas:
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Perfis de Acesso

| Perfil | Permissões |
|--------|-----------|
| **CLIENTE** | Criar pedidos, consultar fidelidade |
| **ATENDENTE** | Atualizar status de pedidos |
| **COZINHA** | Atualizar status de preparo |
| **GERENTE** | Gestão de estoque, relatórios |
| **ADMIN** | Acesso total ao sistema |

---

## 📡 Principais Endpoints

### 🔐 Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/login` | Login de usuário | ❌ |
| POST | `/auth/registrar` | Cadastro de novo usuário | ❌ |

### 🍽️ Produtos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/produtos` | Listar todos os produtos | ❌ |
| GET | `/produtos/{id}` | Buscar produto por ID | ❌ |
| GET | `/produtos/unidade/{unidade_id}` | Cardápio da unidade | ❌ |

### 🛒 Pedidos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/pedidos` | **Criar pedido** ⭐ | ✅ |
| GET | `/pedidos` | Listar pedidos (com filtros) | ✅ |
| GET | `/pedidos/{id}` | Buscar pedido por ID | ✅ |
| PATCH | `/pedidos/{id}/status` | Atualizar status | ✅ (Atendente+) |

### 💳 Pagamentos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/pagamentos/processar/{pedido_id}` | **Processar pagamento mock** ⭐ | ✅ |

### 📦 Estoque

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/estoque/unidade/{unidade_id}` | Consultar estoque | ✅ (Gerente+) |
| POST | `/estoque/movimentar` | Movimentar estoque | ✅ (Gerente+) |

### ⭐ Fidelidade

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/fidelidade/saldo` | Consultar saldo de pontos | ✅ |
| GET | `/fidelidade/historico` | Histórico de pontos | ✅ |
| POST | `/fidelidade/resgatar` | Resgatar pontos | ✅ |

---

## 🎯 Fluxo Crítico Completo

### Criar Pedido → Processar Pagamento → Atualizar Status
```bash
# 1. Login
POST /auth/login
{
  "email": "ana@exemplo.com",
  "senha": "Cliente@123"
}
# Resposta: { "access_token": "..." }

# 2. Criar Pedido (⭐ campo canal_pedido OBRIGATÓRIO)
POST /pedidos
Authorization: Bearer {token}
{
  "unidade_id": 1,
  "canal_pedido": "TOTEM",
  "itens": [
    {"produto_id": 1, "quantidade": 2},
    {"produto_id": 5, "quantidade": 1}
  ],
  "forma_pagamento": "PIX",
  "observacao": "Sem cebola"
}
# Resposta: { "id": 1, "codigo": "PED-ABC123", "status": "AGUARDANDO_PAGAMENTO", ... }

# 3. Processar Pagamento Mock
POST /pagamentos/processar/1
Authorization: Bearer {token}
# Resposta: {
#   "status": "APROVADO",
#   "transacao_id": "TXN-XYZ789",
#   "pedido_status": "PAGAMENTO_APROVADO"
# }

# 4. Atualizar Status (login como ATENDENTE ou COZINHA)
PATCH /pedidos/1/status
Authorization: Bearer {token_atendente}
{
  "status": "EM_PREPARO"
}
# Resposta: { "status": "EM_PREPARO", ... }

# 5. Finalizar Pedido
PATCH /pedidos/1/status
{
  "status": "PRONTO"
}

PATCH /pedidos/1/status
{
  "status": "ENTREGUE"
}
```

---

## ✅ Testes

### Importar Coleção Postman

1. Abra o **Postman**
2. Clique em **Import**
3. Selecione o arquivo: `tests/Raizes_Nordeste_API.postman_collection.json`
4. Configure a variável `base_url` como `http://localhost:8000`

### Executar Testes

A coleção contém **12 cenários de teste**:

| ID | Cenário | Endpoint | Esperado |
|----|---------|----------|----------|
| T01 | Login válido | POST /auth/login | 200 + token |
| T02 | Login com senha inválida | POST /auth/login | 401 |
| T03 | Registrar novo cliente | POST /auth/registrar | 201 |
| T04 | Listar produtos | GET /produtos | 200 |
| T05 | Cardápio da unidade | GET /produtos/unidade/1 | 200 |
| T06 | Criar pedido válido (TOTEM) | POST /pedidos | 201 + canal_pedido |
| T07 | Criar pedido sem token | POST /pedidos | 401 |
| T08 | Criar pedido sem canal_pedido | POST /pedidos | 422 |
| T09 | Filtrar pedidos por canal | GET /pedidos?canal_pedido=TOTEM | 200 |
| T10 | Buscar pedido por ID | GET /pedidos/{id} | 200 |
| T11 | Processar pagamento mock | POST /pagamentos/processar/{id} | 200 |
| T12 | Consultar saldo fidelidade | GET /fidelidade/saldo | 200 |

**Ordem de execução recomendada:**

1. Execute **T01** primeiro para obter o token
2. Execute os demais testes em sequência
3. **T06** cria um pedido e salva o ID para os próximos testes

### Testes Automatizados (Pytest)
```bash
# Rodar todos os testes
pytest

# Rodar com coverage
pytest --cov=app tests/

# Rodar teste específico
pytest tests/test_auth.py -v
```

---

## 🔒 Segurança e LGPD

### Medidas Implementadas

✅ **Autenticação JWT**: Token expira em 30 minutos  
✅ **Hash de Senha**: bcrypt com salt automático  
✅ **Autorização por Perfis**: RBAC (Role-Based Access Control)  
✅ **Consentimento LGPD**: Campo `consentimento_lgpd` obrigatório para fidelidade  
✅ **Logs de Auditoria**: Registro de ações sensíveis (tabela `logs_auditoria`)  
✅ **Dados Sensíveis**: Senhas nunca retornadas em responses  
✅ **Validação de Entrada**: Pydantic valida todos os requests  
✅ **Padrão de Erro**: Respostas sem exposição indevida de dados internos  

### Dados Pessoais Coletados

| Campo | Finalidade | Base Legal |
|-------|-----------|-----------|
| Nome | Identificação do usuário | Execução de contrato |
| E-mail | Login e comunicação | Execução de contrato |
| CPF | Identificação fiscal (opcional) | Consentimento |
| Telefone | Contato (opcional) | Consentimento |
| Histórico de Pedidos | Operação do serviço | Execução de contrato |
| Pontos de Fidelidade | Programa de benefícios | Consentimento explícito |

### Logs de Auditoria

Ações registradas automaticamente:

- Criação de pedidos
- Processamento de pagamentos
- Atualização de status
- Movimentação de estoque (por gerentes)

**Exemplo de log:**
```json
{
  "usuario_id": 5,
  "acao": "CRIAR_PEDIDO",
  "entidade": "Pedido",
  "entidade_id": 1,
  "dados": {
    "codigo": "PED-ABC123",
    "canal": "TOTEM",
    "valor": 45.70
  },
  "created_at": "2026-02-09T10:30:00"
}
```

---

## 📊 Diagramas

### DER (Diagrama Entidade-Relacionamento)

![DER](docs/diagrama-der.png)

**Principais Entidades:**

- `usuarios`: Cadastro de usuários com perfis
- `unidades`: Lojas da rede
- `produtos`: Catálogo de produtos
- `produtos_unidade`: Produtos disponíveis por loja (com preço)
- `pedidos`: Pedidos com campo **canal_pedido** obrigatório ⭐
- `itens_pedido`: Itens de cada pedido
- `pagamentos`: Registro de transações (mock)
- `estoque`: Estoque por unidade e produto
- `fidelidade`: Pontos de cada cliente
- `logs_auditoria`: Rastreabilidade de ações

### Diagrama de Classes (Domínio)
```
┌─────────────┐         ┌─────────────┐
│   Usuario   │         │   Unidade   │
├─────────────┤         ├─────────────┤
│ id          │         │ id          │
│ email       │         │ nome        │
│ senha_hash  │         │ cnpj        │
│ perfil      │         │ cidade      │
└─────────────┘         └─────────────┘
       │                       │
       │ 1                     │ 1
       │                       │
       │ *                     │ *
┌─────────────┐         ┌─────────────┐
│   Pedido    │────────▶│   Estoque   │
├─────────────┤    *    ├─────────────┤
│ id          │         │ produto_id  │
│ codigo      │         │ unidade_id  │
│ canal_pedido│ ⭐      │ quantidade  │
│ status      │         └─────────────┘
│ valor_total │
└─────────────┘
       │ 1
       │
       │ *
┌─────────────┐
│ ItemPedido  │
├─────────────┤
│ produto_id  │
│ quantidade  │
│ preco_unit  │
└─────────────┘
```

---

## 🎨 Multicanalidade (Requisito Obrigatório)

### Campo `canal_pedido`

**Enum**: `CanalPedidoEnum`

Valores aceitos:
- `APP` - Aplicativo mobile
- `TOTEM` - Totem de autoatendimento
- `BALCAO` - Atendimento presencial no balcão
- `WEB` - Site web
- `PICKUP` - Retirada rápida

### Validação

✅ Campo **obrigatório** na criação do pedido  
✅ Validação no nível de schema (Pydantic)  
✅ Armazenado no banco de dados  
✅ Filtro disponível na listagem: `/pedidos?canal_pedido=TOTEM`  

### Rastreabilidade

Permite:
- Identificar qual canal gerou mais vendas
- Relatórios de desempenho por canal
- Auditoria operacional
- Análise de comportamento do cliente

---

## 🔄 Integração com Pagamento Mock

### Como Funciona

1. Cliente cria pedido → Status: `AGUARDANDO_PAGAMENTO`
2. Sistema chama `/pagamentos/processar/{pedido_id}`
3. **Mock retorna aleatoriamente**:
   - 80% chance: `APROVADO` → Status: `PAGAMENTO_APROVADO`
   - 20% chance: `NEGADO` → Status: `PAGAMENTO_NEGADO`
4. Resposta completa é armazenada em `pagamentos.resposta_gateway`

### Payload do Mock (Aprovado)
```json
{
  "status": "APROVADO",
  "transacao_id": "TXN-A1B2C3D4E5F6",
  "mensagem": "Pagamento aprovado com sucesso.",
  "valor": 45.70,
  "forma_pagamento": "PIX",
  "pedido_codigo": "PED-ABC123",
  "timestamp": "2026-02-09T10:35:22.123456",
  "gateway": "MOCK_PAYMENT_GATEWAY_V1"
}
```

### Payload do Mock (Negado)
```json
{
  "status": "NEGADO",
  "transacao_id": "TXN-X9Y8Z7W6V5U4",
  "mensagem": "Pagamento negado. Saldo insuficiente ou cartão bloqueado.",
  "valor": 45.70,
  "forma_pagamento": "PIX",
  "pedido_codigo": "PED-ABC123",
  "timestamp": "2026-02-09T10:35:22.123456",
  "gateway": "MOCK_PAYMENT_GATEWAY_V1",
  "codigo_erro": "ERR_7253"
}
```

---

## 📝 Padrão de Erro

Todos os erros seguem o mesmo formato JSON:
```json
{
  "error": "NOME_DO_ERRO",
  "message": "Mensagem legível para o usuário",
  "details": [
    {
      "field": "campo_com_erro",
      "issue": "descrição do problema"
    }
  ],
  "timestamp": "2026-02-09T10:30:00.000000Z",
  "path": "/pedidos",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Principais Códigos de Erro

| Código | Nome | Descrição |
|--------|------|-----------|
| 400 | BAD_REQUEST | Requisição malformada |
| 401 | NAO_AUTENTICADO | Token ausente ou inválido |
| 403 | SEM_PERMISSAO | Usuário sem permissão |
| 404 | NAO_ENCONTRADO | Recurso não existe |
| 409 | ESTOQUE_INSUFICIENTE | Produto indisponível |
| 422 | VALIDACAO_FALHOU | Dados inválidos |
| 500 | ERRO_INTERNO | Erro no servidor |

---

## 🗂️ Estrutura de Pastas Completa
```
raizes-nordeste-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicação FastAPI
│   │
│   ├── domain/                    # DOMÍNIO
│   │   ├── __init__.py
│   │   └── enums.py              # Enums do sistema
│   │
│   ├── application/               # APLICAÇÃO
│   │   ├── __init__.py
│   │   ├── services/             # Casos de uso
│   │   │   ├── auth_service.py
│   │   │   ├── pedido_service.py
│   │   │   ├── pagamento_service.py
│   │   │   └── fidelidade_service.py
│   │   └── dtos/                 # Schemas request/response
│   │       ├── auth_schemas.py
│   │       └── pedido_schemas.py
│   │
│   ├── infrastructure/            # INFRAESTRUTURA
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── models.py         # Models SQLAlchemy
│   │   ├── repositories/
│   │   │   ├── usuario_repository.py
│   │   │   ├── pedido_repository.py
│   │   │   ├── estoque_repository.py
│   │   │   ├── produto_repository.py
│   │   │   └── fidelidade_repository.py
│   │   ├── security/
│   │   │   ├── password.py
│   │   │   └── jwt_handler.py
│   │   └── external/
│   │       └── pagamento_mock.py
│   │
│   ├── api/                       # API
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Injeção de dependências
│   │   └── routers/              # Endpoints
│   │       ├── auth.py
│   │       ├── produtos.py
│   │       ├── pedidos.py
│   │       ├── pagamentos.py
│   │       ├── estoque.py
│   │       └── fidelidade.py
│   │
│   └── core/
│       ├── config.py             # Configurações
│       └── exceptions.py         # Exceções customizadas
│
├── migrations/                    # Migrations Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── scripts/
│   └── seed_data.py              # Popular banco
│
├── tests/
│   ├── test_auth.py
│   ├── test_pedidos.py
│   └── Raizes_Nordeste_API.postman_collection.json
│
├── docs/
│   ├── diagrama-der.png
│   └── swagger-preview.png
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🚢 Deploy (Produção)

### PostgreSQL

Altere o `.env`:
```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/raizes_nordeste
```

### Executar Migrations
```bash
alembic upgrade head
python scripts/seed_data.py
```

### Servidor de Produção
```bash
# Gunicorn com Uvicorn workers
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📞 Suporte

- **Repositório**: https://github.com/seu-usuario/raizes-nordeste-api
- **Issues**: https://github.com/seu-usuario/raizes-nordeste-api/issues
- **E-mail**: seu-email@exemplo.com

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte do Projeto Multidisciplinar.

---

## 👨‍💻 Autor

**Seu Nome**  
RU: 1234567  
Curso: Análise e Desenvolvimento de Sistemas  
Trilha: Back-End  

---

## 🎓 Agradecimentos

- Professores da disciplina de Projeto Multidisciplinar
- Equipe Univirtus
- Comunidade FastAPI

---

**Última atualização**: 09/02/2026