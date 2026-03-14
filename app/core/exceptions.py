from fastapi import HTTPException, status

class RaizesException(HTTPException):
    """Exceção base customizada"""
    pass

class CredenciaisInvalidasException(RaizesException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "CREDENCIAIS_INVALIDAS",
                "message": "E-mail ou senha inválidos.",
                "details": []
            }
        )

class NaoAutenticadoException(RaizesException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "NAO_AUTENTICADO",
                "message": "Token não fornecido ou inválido.",
                "details": []
            }
        )

class SemPermissaoException(RaizesException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "SEM_PERMISSAO",
                "message": "Você não tem permissão para acessar este recurso.",
                "details": []
            }
        )

class NaoEncontradoException(RaizesException):
    def __init__(self, recurso: str = "Recurso"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "NAO_ENCONTRADO",
                "message": f"{recurso} não encontrado.",
                "details": []
            }
        )

class EstoqueInsuficienteException(RaizesException):
    def __init__(self, detalhes: list = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "ESTOQUE_INSUFICIENTE",
                "message": "Não há quantidade suficiente para um ou mais itens.",
                "details": detalhes or []
            }
        )

class ValidacaoException(RaizesException):
    def __init__(self, detalhes: list):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "VALIDACAO_FALHOU",
                "message": "Os dados fornecidos são inválidos.",
                "details": detalhes
            }
        )