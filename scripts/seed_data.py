"""
Script para popular o banco com dados iniciais
Execute: python scripts/seed_data.py
"""

# ✅ FIX: Garante que o Python encontra o pacote 'app'
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Agora as importações funcionam normalmente
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import SessionLocal, engine, Base
from app.infrastructure.database.models import (
    Usuario, Unidade, Produto, ProdutoUnidade,
    Estoque, MovimentacaoEstoque, Fidelidade, HistoricoFidelidade
)
from app.infrastructure.security.password import hash_password
from app.domain.enums import (
    PerfilEnum, CategoriaEnum, TipoMovimentacaoEstoqueEnum
)
from decimal import Decimal


def seed_database():
    """Popula banco com dados de exemplo"""

    # Criar tabelas
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("🌱 Iniciando seed do banco de dados...")

        # ─────────────────────────────────────────
        # 1. USUÁRIOS
        # ─────────────────────────────────────────
        print("\n📝 Criando usuários...")

        usuarios = [
            Usuario(
                nome="Admin Sistema",
                email="admin@raizes.com",
                senha_hash=hash_password("Admin@123"),
                perfil=PerfilEnum.ADMIN,
                ativo=True,
                consentimento_lgpd=True
            ),
            Usuario(
                nome="Gerente Recife",
                email="gerente@raizes.com",
                senha_hash=hash_password("Gerente@123"),
                perfil=PerfilEnum.GERENTE,
                ativo=True,
                consentimento_lgpd=True
            ),
            Usuario(
                nome="Atendente João",
                email="atendente@raizes.com",
                senha_hash=hash_password("Atendente@123"),
                perfil=PerfilEnum.ATENDENTE,
                ativo=True
            ),
            Usuario(
                nome="Cozinha Maria",
                email="cozinha@raizes.com",
                senha_hash=hash_password("Cozinha@123"),
                perfil=PerfilEnum.COZINHA,
                ativo=True
            ),
            Usuario(
                nome="Cliente Ana Silva",
                email="ana@exemplo.com",
                senha_hash=hash_password("Cliente@123"),
                cpf="123.456.789-00",
                telefone="(81) 99999-1111",
                perfil=PerfilEnum.CLIENTE,
                ativo=True,
                consentimento_lgpd=True
            ),
            Usuario(
                nome="Cliente Pedro Santos",
                email="pedro@exemplo.com",
                senha_hash=hash_password("Cliente@123"),
                cpf="987.654.321-00",
                telefone="(81) 99999-2222",
                perfil=PerfilEnum.CLIENTE,
                ativo=True,
                consentimento_lgpd=True
            ),
        ]

        for usuario in usuarios:
            db.add(usuario)
        db.commit()
        print(f"✅ {len(usuarios)} usuários criados")

        # ─────────────────────────────────────────
        # 2. UNIDADES
        # ─────────────────────────────────────────
        print("\n🏪 Criando unidades...")

        unidades = [
            Unidade(
                nome="Raízes Boa Viagem",
                cnpj="12.345.678/0001-01",
                endereco="Av. Boa Viagem, 1000",
                cidade="Recife",
                estado="PE",
                telefone="(81) 3333-1111",
                ativa=True
            ),
            Unidade(
                nome="Raízes Shopping Recife",
                cnpj="12.345.678/0002-02",
                endereco="Shopping Recife, Loja 201",
                cidade="Recife",
                estado="PE",
                telefone="(81) 3333-2222",
                ativa=True
            ),
            Unidade(
                nome="Raízes Olinda",
                cnpj="12.345.678/0003-03",
                endereco="Rua do Amparo, 50",
                cidade="Olinda",
                estado="PE",
                telefone="(81) 3333-3333",
                ativa=True
            ),
        ]

        for unidade in unidades:
            db.add(unidade)
        db.commit()
        print(f"✅ {len(unidades)} unidades criadas")

        # ─────────────────────────────────────────
        # 3. PRODUTOS
        # ─────────────────────────────────────────
        print("\n🍽️ Criando produtos...")

        produtos = [
            Produto(nome="Cuscuz Recheado",        descricao="Cuscuz nordestino com queijo coalho",            categoria=CategoriaEnum.CAFE_MANHA, ativo=True),
            Produto(nome="Tapioca de Carne Seca",  descricao="Tapioca recheada com carne de sol desfiada",     categoria=CategoriaEnum.CAFE_MANHA, ativo=True),
            Produto(nome="Tapioca de Queijo",       descricao="Tapioca recheada com queijo coalho",             categoria=CategoriaEnum.CAFE_MANHA, ativo=True),
            Produto(nome="Bolo de Macaxeira",       descricao="Bolo caseiro de macaxeira com coco",             categoria=CategoriaEnum.DOCE,       ativo=True),
            Produto(nome="Café Nordestino",         descricao="Café passado na hora",                           categoria=CategoriaEnum.BEBIDA,     ativo=True),
            Produto(nome="Baião de Dois",           descricao="Arroz com feijão verde, queijo coalho e carne de sol", categoria=CategoriaEnum.ALMOCO, ativo=True),
            Produto(nome="Macaxeira Frita",         descricao="Porção de macaxeira frita crocante",             categoria=CategoriaEnum.SALGADO,    ativo=True),
            Produto(nome="Escondidinho de Carne Seca", descricao="Purê de macaxeira gratinado com carne de sol", categoria=CategoriaEnum.ALMOCO,    ativo=True),
            Produto(nome="Suco de Caju",            descricao="Suco natural de caju",                           categoria=CategoriaEnum.BEBIDA,     ativo=True),
            Produto(nome="Suco de Acerola",         descricao="Suco natural de acerola",                        categoria=CategoriaEnum.BEBIDA,     ativo=True),
            Produto(nome="Água de Coco",            descricao="Água de coco natural gelada",                    categoria=CategoriaEnum.BEBIDA,     ativo=True),
            Produto(nome="Cocada Branca",           descricao="Cocada tradicional",                             categoria=CategoriaEnum.DOCE,       ativo=True),
            Produto(nome="Bolo de Rolo",            descricao="Bolo de rolo recheado com goiabada",             categoria=CategoriaEnum.DOCE,       ativo=True),
        ]

        for produto in produtos:
            db.add(produto)
        db.commit()
        print(f"✅ {len(produtos)} produtos criados")

        # ─────────────────────────────────────────
        # 4. PRODUTOS POR UNIDADE
        # ─────────────────────────────────────────
        print("\n💰 Vinculando produtos às unidades com preços...")

        unidades_db = db.query(Unidade).all()
        produtos_db = db.query(Produto).all()

        precos_base = {
            "Cuscuz Recheado":           Decimal("15.90"),
            "Tapioca de Carne Seca":     Decimal("18.90"),
            "Tapioca de Queijo":         Decimal("14.90"),
            "Bolo de Macaxeira":         Decimal("8.90"),
            "Café Nordestino":           Decimal("5.00"),
            "Baião de Dois":             Decimal("25.90"),
            "Macaxeira Frita":           Decimal("12.90"),
            "Escondidinho de Carne Seca": Decimal("28.90"),
            "Suco de Caju":              Decimal("8.90"),
            "Suco de Acerola":           Decimal("8.90"),
            "Água de Coco":              Decimal("6.90"),
            "Cocada Branca":             Decimal("4.90"),
            "Bolo de Rolo":              Decimal("12.90"),
        }

        produtos_unidade_count = 0
        for unidade in unidades_db:
            for produto in produtos_db:
                preco = precos_base.get(produto.nome, Decimal("10.00"))
                if "Shopping" in unidade.nome:
                    preco = (preco * Decimal("1.15")).quantize(Decimal("0.01"))

                pu = ProdutoUnidade(
                    unidade_id=unidade.id,
                    produto_id=produto.id,
                    preco=preco,
                    disponivel=True
                )
                db.add(pu)
                produtos_unidade_count += 1

        db.commit()
        print(f"✅ {produtos_unidade_count} vinculações produto-unidade criadas")

        # ─────────────────────────────────────────
        # 5. ESTOQUE
        # ─────────────────────────────────────────
        print("\n📦 Criando registros de estoque...")

        estoque_count = 0
        for unidade in unidades_db:
            for produto in produtos_db:
                estoque = Estoque(
                    unidade_id=unidade.id,
                    produto_id=produto.id,
                    quantidade=100
                )
                db.add(estoque)
                estoque_count += 1

        db.commit()
        print(f"✅ {estoque_count} registros de estoque criados")

        # ─────────────────────────────────────────
        # 6. FIDELIDADE
        # ─────────────────────────────────────────
        print("\n⭐ Criando programas de fidelidade...")

        clientes = db.query(Usuario).filter(
            Usuario.perfil == PerfilEnum.CLIENTE
        ).all()

        fid_count = 0
        for cliente in clientes:
            fidelidade = Fidelidade(
                usuario_id=cliente.id,
                saldo_pontos=50,
                total_acumulado=50
            )
            db.add(fidelidade)
            db.flush()   # garante fidelidade.id disponível

            historico = HistoricoFidelidade(
                fidelidade_id=fidelidade.id,
                tipo="ACUMULO",
                pontos=50,
                descricao="Bônus de boas-vindas"
            )
            db.add(historico)
            fid_count += 1

        db.commit()
        print(f"✅ {fid_count} programas de fidelidade criados")

        # ─────────────────────────────────────────
        # RESUMO
        # ─────────────────────────────────────────
        print("\n✨ Seed concluído com sucesso!")
        print("\n📊 Resumo:")
        print(f"   - {len(usuarios)} usuários")
        print(f"   - {len(unidades)} unidades")
        print(f"   - {len(produtos)} produtos")
        print(f"   - {produtos_unidade_count} vinculações produto-unidade")
        print(f"   - {estoque_count} registros de estoque")
        print(f"   - {fid_count} programas de fidelidade")

        print("\n🔑 Credenciais de acesso:")
        print("   ADMIN    : admin@raizes.com     / Admin@123")
        print("   GERENTE  : gerente@raizes.com   / Gerente@123")
        print("   ATENDENTE: atendente@raizes.com / Atendente@123")
        print("   COZINHA  : cozinha@raizes.com   / Cozinha@123")
        print("   CLIENTE  : ana@exemplo.com      / Cliente@123")
        print("   CLIENTE  : pedro@exemplo.com    / Cliente@123")

    except Exception as e:
        print(f"\n❌ Erro durante seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()