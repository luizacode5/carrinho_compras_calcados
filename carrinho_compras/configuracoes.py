from typing import Optional

from pydantic import BaseSettings


class Configuracao(BaseSettings):
    database_uri: Optional[str] = None
    secret_key: str
    algorithm: str
    access_token_expire_minutes: Optional[int] = 30


def iniciar_configuracao():
    return Configuracao()


configuracao = iniciar_configuracao()
