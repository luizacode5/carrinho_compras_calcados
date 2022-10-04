from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

from carrinho_compras.configuracoes import configuracao


def iniciar_cliente_mongo() -> AsyncIOMotorClient:
    cliente_mongo = AsyncIOMotorClient(configuracao.database_uri)
    return cliente_mongo


cliente_mongo = iniciar_cliente_mongo()


def obter_base_dados() -> AsyncIOMotorDatabase:
    return cliente_mongo.carrinho


def obter_colecao(nome_colecao: str) -> AsyncIOMotorCollection:
    bd = obter_base_dados()
    colecao = bd[nome_colecao]

    return colecao
