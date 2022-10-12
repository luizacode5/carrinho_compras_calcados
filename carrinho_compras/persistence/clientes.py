from typing import List

from pydantic import EmailStr

from carrinho_compras.persistence.base import AdaptadorBase
from carrinho_compras.persistence.excecoes import (ObjetoNaoEncontrado,
                                                   ObjetoNaoModificado)
from carrinho_compras.persistence.persistence_bd import obter_colecao
from carrinho_compras.schemas.clientes import Cliente, Endereco

COLECAO_CLIENTES = obter_colecao("clientes")


class AdaptadorCliente(AdaptadorBase):
    def __init__(self):
        self.colecao = COLECAO_CLIENTES

    async def cria(self, dados: Cliente) -> Cliente:
        return await super().cria(dados)

    async def adiciona_endereco(
        self,
        email: EmailStr,
        endereco: Endereco,
    ) -> Cliente:
        return await super().atualiza_item_lista(
            endereco, email, "email", chave_de_atualizacao="endereco"
        )

    async def pega(self, email: EmailStr) -> Cliente:
        return await super().pega(email, chave="email")

    async def pega_todos(
        self, pula: int = 0, limite: int = 10
    ) -> List[Cliente]:
        return await super().pega_tudo(pula=pula, limite=limite)

    async def deleta(self, email: EmailStr):
        return await super().deleta(email, chave="email")

    async def remover_endereco(self, endereco: Endereco, email):
        atualizados = await self.colecao.update_one(
            {"email": email},
            {
                "$pull": {
                    "endereco": {
                        "rua": endereco.rua,
                        "cep": endereco.cep,
                        "cidade": endereco.cidade,
                        "estado": endereco.estado,
                    }
                }
            },
        )
        if atualizados.matched_count == 0:
            raise ObjetoNaoEncontrado
        if atualizados.modified_count == 0:
            raise ObjetoNaoModificado
        return endereco
