class ObjetoNaoEncontrado(Exception):
    """Quando for feito uma update e o matched_count == 0"""


class ObjetoNaoModificado(Exception):
    """Quando o update for igual a um existente"""


class ObjetoInvalido(Exception):
    """Quando o produto não atender os requisitos mínimos"""


class ObjetoDuplicado(Exception):
    """Quando o produto for duplicado"""
