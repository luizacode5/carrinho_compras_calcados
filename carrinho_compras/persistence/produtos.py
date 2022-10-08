
from typing import List

from carrinho_compras.persistence.base import AdaptadorBase
from carrinho_compras.persistence.excecoes import (ObjetoDuplicado, ObjetoInvalido)
from carrinho_compras.persistence.persistence_bd import obter_colecao
from carrinho_compras.schemas.produtos import Produto

COLECAO_PRODUTOS = obter_colecao("produtos")


class AdaptadorProduto(AdaptadorBase):
    def __init__(self):
        self.colecao = COLECAO_PRODUTOS

    async def cria(self, produto: Produto) -> Produto:
        produto_existente = await self.pega_sku(produto.sku)
        #testa se sku já existe
        if produto_existente:
            raise ObjetoDuplicado
        #testa se produto não tem nome
        if not produto.nome:
            raise ObjetoInvalido
        #testa se produto tem preco menor do que R$0,01
        if produto.preco < 0.01:
            raise ObjetoInvalido
        #testa se estoque está zerado
        if produto.estoque < 1:
            raise ObjetoInvalido
        return await super().cria(produto)

    async def pega_sku(self, sku: str) -> Produto:
        return await super().pega(sku, chave="sku")
    
    async def pega_nome(self, nome: str) -> Produto:
        return await super().pega(nome, chave="nome")

    async def pega_todos(
        self, pula: int = 0, limite: int = 10
    ) -> List[Produto]:
        return await super().pega_tudo(pula=pula, limite=limite)

    async def deleta(self, sku: str):
        return await super().deleta(sku, chave="sku")
    
