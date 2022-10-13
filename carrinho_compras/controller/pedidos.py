from fastapi import HTTPException, status

from carrinho_compras.controller import uteis
from carrinho_compras.persistence import pedidos
from carrinho_compras.schemas.pedidos import *


async def insere_pedido(pedido: PedidoSchema):
    resultado = await pedidos.insere_pedido(pedido)
    return resultado


async def busca_pedido_por_id(id_pedido: str):
    resultado = await pedidos.busca_pedido_por_id(id_pedido)
    return resultado


async def busca_pedidos_por_cliente(
    email_cliente: EmailStr, numero_pagina: int, qtde_por_pagina: int
) -> ListaPedidos:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, qtde_por_pagina
    )

    lista_pedidos = await pedidos.busca_pedidos_por_cliente(
        email_cliente, registros_pular, qtde_por_pagina
    )

    if len(lista_pedidos.pedidos) != 0:
        if numero_pagina == 0:
            numero_pagina = 1
        lista_pedidos.numero_pagina = numero_pagina
        lista_pedidos.qtde_por_pagina = qtde_por_pagina
        return lista_pedidos

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não foram encontrados pedidos para o cliente",
    )


async def busca_pedidos_por_produto(
    codigo_produto: str,
    cor_produto: str,
    tamanho_produto: int,
    numero_pagina: int,
    qtde_por_pagina: int,
) -> ListaPedidos:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, qtde_por_pagina
    )

    filtro_produto = await uteis.gera_filtro_produto(
        codigo_produto, cor_produto, tamanho_produto
    )

    resultado = await pedidos.busca_pedidos_por_produto(
        filtro_produto, registros_pular, qtde_por_pagina
    )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina

    if resultado:
        return resultado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não foram encontrados pedidos com o produto",
    )


async def busca_produtos_mais_vendidos(
    numero_pagina: int, qtde_por_pagina: int
) -> ProdutosMaisVendidos:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, qtde_por_pagina
    )

    resultado = await pedidos.busca_produtos_mais_vendidos(
        registros_pular, qtde_por_pagina
    )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina

    if resultado:
        return resultado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não foram encontrados registros para os parâmetros especificados",
    )


async def busca_total_pedidos_por_cliente(
    numero_pagina: int, qtde_por_pagina: int, ordenacao: str
) -> TotalPedidoClientes:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, qtde_por_pagina
    )

    if ordenacao.upper() == "QUANTIDADE":
        ordenacao_filtro = "quantidade_total"
    elif ordenacao.upper() == "VALOR":
        ordenacao_filtro = "valor_total"

    resultado = await pedidos.busca_total_pedidos_por_cliente(
        registros_pular, qtde_por_pagina, ordenacao_filtro
    )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina

    if resultado:
        return resultado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não foram encontrados registros para os parâmetros especificados",
    )
