from sqlalchemy.orm import Session
from app.infrastructure.database.models import Fidelidade, HistoricoFidelidade
from app.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from app.core.exceptions import NaoEncontradoException, ValidacaoException

class FidelidadeService:
    
    @staticmethod
    def acumular_pontos(db: Session, usuario_id: int, pontos: int, descricao: str = None):
        """Acumula pontos de fidelidade"""
        
        fidelidade = FidelidadeRepository.get_by_usuario_id(db, usuario_id)
        
        if not fidelidade:
            # Criar se não existir
            fidelidade = Fidelidade(usuario_id=usuario_id)
            fidelidade = FidelidadeRepository.create(db, fidelidade)
        
        fidelidade.saldo_pontos += pontos
        fidelidade.total_acumulado += pontos
        
        # Criar histórico
        historico = HistoricoFidelidade(
            fidelidade_id=fidelidade.id,
            tipo="ACUMULO",
            pontos=pontos,
            descricao=descricao or f"Acúmulo de {pontos} pontos"
        )
        FidelidadeRepository.criar_historico(db, historico)
        FidelidadeRepository.update(db, fidelidade)
        
        return fidelidade
    
    @staticmethod
    def resgatar_pontos(db: Session, usuario_id: int, pontos: int, descricao: str = None):
        """Resgata pontos de fidelidade"""
        
        fidelidade = FidelidadeRepository.get_by_usuario_id(db, usuario_id)
        
        if not fidelidade:
            raise NaoEncontradoException("Programa de fidelidade não encontrado para este usuário")
        
        if fidelidade.saldo_pontos < pontos:
            raise ValidacaoException([{
                "field": "pontos",
                "issue": f"Saldo insuficiente. Disponível: {fidelidade.saldo_pontos}"
            }])
        
        fidelidade.saldo_pontos -= pontos
        
        # Criar histórico
        historico = HistoricoFidelidade(
            fidelidade_id=fidelidade.id,
            tipo="RESGATE",
            pontos=-pontos,
            descricao=descricao or f"Resgate de {pontos} pontos"
        )
        FidelidadeRepository.criar_historico(db, historico)
        FidelidadeRepository.update(db, fidelidade)
        
        return fidelidade