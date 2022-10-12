from fastapi import APIRouter, status, HTTPException, Query

from carrinho_compras.schemas.pedidos import *
from carrinho_compras.controller import pedidos
from carrinho_compras.documentacao.pedidos import *


rota_pedidos = APIRouter(
    prefix="/pedido",
    tags=["Pedido"]
)

@rota_pedidos.get('/',
    summary="Busca pedido por id",
    description=GET_PEDIDO_POR_ID_DESCRICAO,
    response_model=PedidoSchema,
    status_code=status.HTTP_200_OK)
async def busca_pedido_por_id(
    id_pedido: str = Query(description="Id do pedido")):
    resultado = await pedidos.busca_pedido_por_id(id_pedido)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Não foi encontrado pedido com o id informado")
    return resultado

@rota_pedidos.get('/cliente',
    summary="Busca pedidos do cliente",
    description=GET_PEDIDOS_CLIENTE_DESCRICAO,
    response_model=ListaPedidos,
    status_code=status.HTTP_200_OK)
async def busca_pedidos_por_cliente(
    email_cliente: EmailStr = Query(description="Email do cliente"),
    numero_pagina: int = Query(default=0, description="Número da página"),
    qtde_por_pagina: int = Query(default=50,
        description="Quantidade de registros por página. Valor máximo: 50")):
    resultado = await pedidos.busca_pedidos_por_cliente(
        email_cliente,
        numero_pagina,
        qtde_por_pagina)
    return resultado

@rota_pedidos.get('/produto',
    summary="Busca pedidos que contém determinado produto",
    description=GET_PEDIDOS_COM_PRODUTO_DESCRICAO,
    response_model=ListaPedidos,
    status_code=status.HTTP_200_OK)
async def busca_pedidos_por_produto(
    codigo_produto: str = Query(default=None, description="Código do produto"),
    cor_produto: str = Query(default=None, description="Cor do produto"),
    numeracao_produto: str = Query(default=None, description="Numeração do produto"),
    numero_pagina: int = Query(default=0, description="Número da página"),
    qtde_por_pagina: int = Query(default=50,
        description="Quantidade de registros por página. Valor máximo: 50")):
    resultado = await pedidos.busca_pedidos_por_produto(
        codigo_produto,
        cor_produto,
        numeracao_produto,
        numero_pagina,
        qtde_por_pagina)
    return resultado

@rota_pedidos.get('/mais_vendidos',
    summary="Busca produtos mais vendidos",
    description=GET_PRODUTOS_MAIS_VENDIDOS_DESCRICAO,
    response_model=ProdutosMaisVendidos,
    status_code=status.HTTP_200_OK)
async def busca_produtos_mais_vendidos(
    numero_pagina: int = Query(default=0, description="Número da página"),
    qtde_por_pagina: int = Query(default=50,
        description="Quantidade de registros por página. Valor máximo: 50")):
    resultado = await pedidos.busca_produtos_mais_vendidos(
        numero_pagina, 
        qtde_por_pagina)
    return resultado

@rota_pedidos.get('/total_cliente',
    summary="Busca total de pedidos por cliente",
    description=GET_TOTAIS_PEDIDOS_POR_CLIENTE_DESCRICAO,
    response_model=TotalPedidoClientes,
    status_code=status.HTTP_200_OK)
async def busca_total_pedidos_por_cliente(
    ordenacao: str = Query(default="quantidade",
        description='Ordenação. Usar "quantidade" ou "valor"'),
    numero_pagina: int = Query(default=0, description="Número da página"),
    qtde_por_pagina: int = Query(default=50,
        description="Quantidade de registros por página. Valor máximo: 50")):
    resultado = await pedidos.busca_total_pedidos_por_cliente(
        numero_pagina, 
        qtde_por_pagina,
        ordenacao)
    return resultado