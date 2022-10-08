class ObjetoNaoEncontrado(Exception):
    """Quando for feito uma update e o matched_count == 0"""


class ObjetoNaoModificado(Exception):
    """Quando o update for igual a um existente"""

class ObjetoNaoAtendeRequisitos(Exception):
    """Quando não são atendidos os requisitos necessários para que a ação seja executada"""