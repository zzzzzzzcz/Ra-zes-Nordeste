from sqlalchemy.orm import Session
from decimal import Decimal
import uuid
from datetime import datetime

from app.infrastructure.database.models import Pedido, ItemPedido, Pagamento, LogAuditoria
from app.infrastructure.repositories.pedido_repository import PedidoRepository
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.infrastructure.repositories.estoque_repository import EstoqueRepository
from app.application.dtos.pedido_schemas import PedidoCreate, PedidoResponse, ItemPedidoResponse
from app.domain.enums import StatusPedidoEnum, StatusPagamentoEnum
from app.core.exceptions import NaoEncontradoException, EstoqueInsuficienteException, ValidacaoException

class PedidoService:
    
    @staticmethod
    def criar_pedido(db: Session, usuario_id: int, request: PedidoCreate) -> Pedido:
        """Cria novo pedido validando estoque"""
        
        # Validar itens e calcular total
        itens_validados = []
        valor_total = Decimal("0.00")
        erros_estoque = []
        
        for item in request.itens:
            # Buscar produto na unidade
            produto_unidade = ProdutoRepository.get_produto_unidade(
                db, request.unidade_id, item.produto_id
            )
            
            if not produto_unidade:
                raise NaoEncontradoException(f"Produto {item.produto_id} não disponível nesta unidade")
            
            # Verificar estoque
            estoque = EstoqueRepository.get_by_unidade_produto(
                db, request.unidade_id, item.produto_id
            )
            
            if not estoque or estoque.quantidade < item.quantidade:
                erros_estoque.append({
                    "field": f"itens[{item.produto_id}].quantidade",
                    "issue": f"Disponível: {estoque.quantidade if estoque else 0}"
                })
                continue
            
            # Calcular subtotal
            subtotal = produto_unidade.preco * item.quantidade
            valor_total += subtotal
            
            itens_validados.append({
                "produto_id": item.produto_id,
                "quantidade": item.quantidade,
                "preco_unitario": produto_unidade.preco,
                "subtotal": subtotal
            })
        
        if erros_estoque:
            raise EstoqueInsuficienteException(erros_estoque)
        
        # Gerar código único do pedido
        codigo = f"PED-{uuid.uuid4().hex[:8].upper()}"
        
        # Criar pedido
        novo_pedido = Pedido(
            codigo=codigo,
            usuario_id=usuario_id,
            unidade_id=request.unidade_id,
            canal_pedido=request.canal_pedido,  # ⭐ OBRIGATÓRIO
            status=StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
            valor_total=valor_total,
            observacao=request.observacao
        )
        
        pedido_criado = PedidoRepository.create(db, novo_pedido)
        
        # Criar itens do pedido
        for item_data in itens_validados:
            item_pedido = ItemPedido(
                pedido_id=pedido_criado.id,
                **item_data
            )
            db.add(item_pedido)
        
        # Criar registro de pagamento pendente
        pagamento = Pagamento(
            pedido_id=pedido_criado.id,
            forma_pagamento=request.forma_pagamento,
            status=StatusPagamentoEnum.PENDENTE,
            valor=valor_total
        )
        db.add(pagamento)
        
        # Log de auditoria
        log = LogAuditoria(
            usuario_id=usuario_id,
            acao="CRIAR_PEDIDO",
            entidade="Pedido",
            entidade_id=pedido_criado.id,
            dados={
                "codigo": codigo,
                "canal": request.canal_pedido.value,
                "valor": float(valor_total)
            }
        )
        db.add(log)
        
        db.commit()
        db.refresh(pedido_criado)
        
        return pedido_criado
    
    @staticmethod
    def atualizar_status(
        db: Session,
        pedido_id: int,
        novo_status: StatusPedidoEnum,
        usuario_id: int
    ) -> Pedido:
        """Atualiza status do pedido"""
        
        pedido = PedidoRepository.get_by_id(db, pedido_id)
        
        if not pedido:
            raise NaoEncontradoException("Pedido")
        
        status_anterior = pedido.status
        pedido.status = novo_status
        
        # Se status for EM_PREPARO, dar baixa no estoque
        if novo_status == StatusPedidoEnum.EM_PREPARO and status_anterior == StatusPedidoEnum.PAGAMENTO_APROVADO:
            for item in pedido.itens:
                estoque = EstoqueRepository.get_by_unidade_produto(
                    db, pedido.unidade_id, item.produto_id
                )
                if estoque:
                    estoque.quantidade -= item.quantidade
                    EstoqueRepository.update(db, estoque)
        
        # Log de auditoria
        log = LogAuditoria(
            usuario_id=usuario_id,
            acao="ATUALIZAR_STATUS_PEDIDO",
            entidade="Pedido",
            entidade_id=pedido.id,
            dados={
                "status_anterior": status_anterior.value,
                "status_novo": novo_status.value
            }
        )
        db.add(log)
        
        pedido_atualizado = PedidoRepository.update(db, pedido)
        db.commit()
        
        return pedido_atualizado
    
    @staticmethod
    def converter_para_response(pedido: Pedido) -> PedidoResponse:
        """Converte model para response DTO"""
        return PedidoResponse(
            id=pedido.id,
            codigo=pedido.codigo,
            usuario_id=pedido.usuario_id,
            unidade_id=pedido.unidade_id,
            canal_pedido=pedido.canal_pedido,
            status=pedido.status,
            valor_total=pedido.valor_total,
            observacao=pedido.observacao,
            created_at=pedido.created_at,
            itens=[
                ItemPedidoResponse(
                    id=item.id,
                    produto_id=item.produto_id,
                    produto_nome=item.produto.nome,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                    subtotal=item.subtotal
                )
                for item in pedido.itens
            ]
        )