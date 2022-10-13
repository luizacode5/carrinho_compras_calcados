import logging
from decimal import Decimal
from typing import Any, List

from bson.decimal128 import Decimal128
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError, PyMongoError

from carrinho_compras.persistence.excecoes import (ObjetoNaoEncontrado,
                                                   ObjetoNaoModificado)


def convert_decimal(dict_item):
    # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
    # Embedded dictionaries and lists are called recursively.
    if dict_item is None:
        return None

    for k, v in list(dict_item.items()):
        if isinstance(v, dict):
            convert_decimal(v)
        elif isinstance(v, list):
            for l in v:
                convert_decimal(l)
        elif isinstance(v, Decimal):
            dict_item[k] = Decimal128(str(v))

    return dict_item


class AdaptadorBase:
    async def cria(self, dados: BaseModel) -> BaseModel:
        try:
            await self.colecao.insert_one(convert_decimal(dados.dict()))
            return dados
        except DuplicateKeyError as e:
            logging.error(e)
            raise

    async def atualiza(
        self, dados: BaseModel, identificador: Any, chave: str
    ) -> BaseModel:
        atualizados = await self.colecao.update_one(
            {chave: identificador},
            {"$set": convert_decimal(dados.dict())},
        )
        if atualizados.matched_count == 0:
            raise ObjetoNaoEncontrado
        if atualizados.modified_count == 0:
            raise ObjetoNaoModificado
        return dados

    async def atualiza_item_lista(
        self,
        dados: BaseModel,
        identificador: Any,
        chave: str,
        chave_de_atualizacao: str,
    ) -> BaseModel:
        atualizados = await self.colecao.update_one(
            {chave: identificador},
            {"$addToSet": {chave_de_atualizacao: convert_decimal(dados.dict())}},
        )
        if atualizados.matched_count == 0:
            raise ObjetoNaoEncontrado
        if atualizados.modified_count == 0:
            raise ObjetoNaoModificado
        return dados

    async def pega(self, identificador: Any, chave: str) -> BaseModel:
        try:
            dados = await self.colecao.find_one({chave: identificador})
            return dados
        except Exception as e:
            logging.error(e)
            return

    async def pega_todos(self, pula: int = 0, limite: int = 10) -> List[BaseModel]:
        try:
            cursor = self.colecao.find().skip(pula).limit(limite)
            dados = await cursor.to_list(length=limite)
            return dados
        except Exception as e:
            logging.error(e)
            return

    async def deleta(self, identificador: Any, chave: str):
        try:
            dados = await self.colecao.delete_one({chave: identificador})
            if dados.deleted_count == 0:
                raise ObjetoNaoModificado
        except PyMongoError as e:
            logging.error(e)
            raise
