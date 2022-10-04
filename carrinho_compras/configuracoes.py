from typing import Optional

from pydantic import BaseSettings


class Configuracao(BaseSettings):
    database_uri: Optional[str] = None


def iniciar_configuracao():
    return Configuracao()


configuracao = iniciar_configuracao()
