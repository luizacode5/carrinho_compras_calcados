from fastapi import HTTPException, status
import logging
from bson import ObjectId
from pymongo import DESCENDING

from carrinho_compras.schemas.pedidos import *
from carrinho_compras.persistence.persistence_bd import obter_colecao


COLECAO_PEDIDOS = obter_colecao("pedido")

async def insere_pedido(pedido: PedidoSchema):
    try:
        dados_pedido = pedido.dict()

        resultado = await COLECAO_PEDIDOS.insert_one(dados_pedido)

        if resultado.inserted_id:
            return resultado.inserted_id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Não foi possível fechar o pedido")

    except Exception as e:
        logging.exception(f'insere_pedido.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível inserir o pedido")

async def busca_pedido_por_id(id_pedido: str) -> PedidoSchema:
    try:
        resultado = await COLECAO_PEDIDOS.find_one(
            {"_id" : ObjectId(id_pedido)}
        )

        if resultado:
            pedido = PedidoSchema(**resultado)
            pedido.id_pedido = str(resultado["_id"])
            return pedido
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="O pedido não foi encontrado")

    except Exception as e:
        logging.exception(f'busca_pedido_por_id.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível consultar o pedido")


async def busca_pedidos_por_cliente(
    email_cliente: EmailStr,
    registros_pular: int,
    qtde_por_pagina: int
    ) -> ListaPedidos:
    try:
        lista_pedidos = ListaPedidos()

        cursor_pesquisa = COLECAO_PEDIDOS \
            .find({"email_cliente": email_cliente}) \
            .skip(registros_pular) \
            .limit(qtde_por_pagina) \
            .sort("data_criacao_pedido", DESCENDING)

        async for pedidos_resultado in cursor_pesquisa:
            pedido = PedidoSchema(**pedidos_resultado)
            pedido.id_pedido = str(pedidos_resultado["_id"])
            lista_pedidos.pedidos.append(pedido)

        return lista_pedidos

    except Exception as e:
        logging.exception(f'busca_pedidos_por_cliente.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de pedidos por cliente")

async def busca_pedidos_por_produto(
    filtro_produto: dict, 
    registros_pular: int, 
    qtde_por_pagina: int
    ) -> ListaPedidos:
    try:
        lista_pedidos = ListaPedidos()

        cursor_pesquisa = COLECAO_PEDIDOS \
            .find({"produtos": 
                        {"$elemMatch": filtro_produto}}) \
            .skip(registros_pular) \
            .limit(qtde_por_pagina) \
            .sort("data_criacao_pedido", DESCENDING)

        async for pedidos_resultado in cursor_pesquisa:
            pedido = PedidoSchema(**pedidos_resultado)
            lista_pedidos.pedidos.append(pedido)

        return lista_pedidos

    except Exception as e:
        logging.exception(f'busca_pedidos_por_produto.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de pedidos por produto")

async def busca_produtos_mais_vendidos(
    registros_pular: int,
    qtde_por_pagina: int
    ) -> ProdutosMaisVendidos:
    try:
        lista_produtos = ProdutosMaisVendidos()
        lista_produtos.produtos = []

        cursor_pesquisa = COLECAO_PEDIDOS \
            .aggregate( [   
                    {"$unwind": "$produtos" }, 
                    {"$group": {"_id": {"codigo": "$produtos.codigo",  
                                        "cor": "$produtos.cor", 
                                        "tamanho": "$produtos.tamanho"},  
                    "quantidade_total": {"$sum": "$produtos.quantidade" }}}, 
                    {"$sort":{"quantidade_total": DESCENDING}},
                    {"$skip":registros_pular},
                    {"$limit":qtde_por_pagina}
            ])

        async for produtos_resultado in cursor_pesquisa:
            produto = QuantidadeTotalPorProduto(**produtos_resultado["_id"])
            produto.quantidade_total = produtos_resultado["quantidade_total"]
            lista_produtos.produtos.append(produto)

        return lista_produtos
    except Exception as e:
        logging.exception(f'busca_produtos_mais_vendidos.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de produtos mais vendidos")

async def busca_total_pedidos_por_cliente(
    registros_pular: int,
    qtde_por_pagina: int,
    ordenacao_filtro: str
    ) -> TotalPedidoClientes:
    try:
        lista_clientes = TotalPedidoClientes()
        lista_clientes.clientes = []

        cursor_pesquisa = COLECAO_PEDIDOS \
            .aggregate( [
                    {"$group": {"_id": "$email_cliente",  
                    "quantidade_total": {"$count": {}},
                    "valor_total": {"$sum": "$valor_total"}}}, 
                    {"$sort":{ordenacao_filtro: DESCENDING}},
                    {"$skip":registros_pular},
                    {"$limit":qtde_por_pagina}
            ] )

        async for clientes_resultado in cursor_pesquisa:
            cliente = TotalPedidosPorCliente()
            cliente.email_cliente = clientes_resultado["_id"]
            cliente.quantidade_total = round(clientes_resultado["quantidade_total"], 2)
            cliente.valor_total = round(clientes_resultado["valor_total"], 2)
            lista_clientes.clientes.append(cliente)

        return lista_clientes
    except Exception as e:
        logging.exception(f'busca_total_pedidos_por_cliente.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de totais de pedidos por cliente")