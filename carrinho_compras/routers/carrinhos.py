from fastapi import APIRouter, HTTPException, Query, status

from carrinho_compras.controller import carrinhos
from carrinho_compras.documentacao.carrinhos import *
from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.schemas.pedidos import *

rota_carrinhos = APIRouter(prefix="/carrinho", tags=["Carrinho"])


@rota_carrinhos.post(
    "/",
    summary="Cria carrinho e adiciona/atualiza produto",
    description=POST_CARRINHO_DESCRICAO,
    response_model=CarrinhoCompleto,
    status_code=status.HTTP_201_CREATED,
)
async def adiciona_itens_carrinho(carrinho: CarrinhoRequest):
    await carrinhos.adiciona_itens_carrinho(carrinho)
    resultado = await carrinhos.busca_carrinho_cliente(carrinho.email_cliente)
    return resultado


@rota_carrinhos.put(
    "/",
    summary="Atualiza o carrinho",
    description=PUT_CARRINHO_DESCRICAO,
    response_model=CarrinhoCompleto,
    status_code=status.HTTP_202_ACCEPTED,
)
async def atualiza_carrinho(carrinho: CarrinhoRequest):
    resultado = await carrinhos.atualiza_carrinho(carrinho)
    return resultado


@rota_carrinhos.delete(
    "/delete_item",
    summary="Exclui produto do carrinho",
    description=DELETE_ITEM_CARRINHO_DESCRICAO,
    status_code=status.HTTP_202_ACCEPTED,
)
async def exclui_item_carrinho(
    produto: ExclusaoProdutoRequest,
    email_cliente: EmailStr = Query(description="Email do cliente"),
):
    resultado = await carrinhos.exclui_item_carrinho(produto, email_cliente)
    return resultado


@rota_carrinhos.delete(
    "/delete",
    summary="Exclui carrinho",
    description=DELETE_CARRINHO_DESCRICAO,
    status_code=status.HTTP_202_ACCEPTED,
)
async def exclui_carrinho(
    email_cliente: EmailStr = Query(description="Email do cliente"),
):
    resultado = await carrinhos.exclui_carrinho(email_cliente)
    return resultado


@rota_carrinhos.get(
    "/cliente",
    summary="Busca carrinho por cliente",
    description=GET_CARRINHO_CLIENTE_DESCRICAO,
    response_model=CarrinhoCompleto,
    status_code=status.HTTP_200_OK,
)
async def busca_carrinho_cliente(
    email_cliente: EmailStr = Query(description="Email do cliente"),
):
    resultado = await carrinhos.busca_carrinho_cliente(email_cliente)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="N??o foi encontrado carrinho para o cliente",
        )
    return resultado


@rota_carrinhos.put(
    "/fechar",
    summary="Gera pedido a partir do carrinho",
    description=PUT_FECHA_CARRINHO_DESCRICAO,
    response_model=PedidoSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def fecha_carrinho(
    email_cliente: EmailStr = Query(description="Email do cliente"),
):
    resultado = await carrinhos.fecha_carrinho(email_cliente)
    return resultado


@rota_carrinhos.get(
    "/produto",
    summary="Busca carrinhos que cont??m determinado produto",
    description=GET_CARRINHOS_COM_PRODUTO_DESCRICAO,
    response_model=ListaCarrinhos,
    status_code=status.HTTP_200_OK,
)
async def busca_carrinhos_por_produto(
    codigo_produto: str = Query(default=None, description="C??digo do produto"),
    cor_produto: str = Query(default=None, description="Cor do produto"),
    tamanho_produto: str = Query(
        default=None, description="Tamanho/numera????o do produto"
    ),
    numero_pagina: int = Query(default=0, description="N??mero da p??gina"),
    qtde_por_pagina: int = Query(
        default=50, description="Quantidade de registros por p??gina. Valor m??ximo: 50"
    ),
):
    resultado = await carrinhos.busca_carrinhos_por_produto(
        codigo_produto, cor_produto, tamanho_produto, numero_pagina, qtde_por_pagina
    )
    return resultado


@rota_carrinhos.get(
    "/produtos_populares",
    summary="Busca produtos mais frequentes nos carrinhos abertos",
    description=GET_PRODUTOS_POPULARES_CARRINHOS_DESCRICAO,
    response_model=ProdutosPopulares,
    status_code=status.HTTP_200_OK,
)
async def busca_produtos_populares(
    numero_pagina: int = Query(default=0, description="N??mero da p??gina"),
    qtde_por_pagina: int = Query(
        default=50, description="Quantidade de registros por p??gina. Valor m??ximo: 50"
    ),
):
    resultado = await carrinhos.busca_produtos_populares(numero_pagina, qtde_por_pagina)
    return resultado


@rota_carrinhos.get(
    "/abandonados",
    summary="Busca carrinhos abandonados",
    description=GET_CARRINHOS_ABANDONADOS_DESCRICAO,
    response_model=ListaCarrinhos,
    status_code=status.HTTP_200_OK,
)
async def busca_carrinhos_abandonados(
    numero_pagina: int = Query(default=0, description="N??mero da p??gina"),
    qtde_por_pagina: int = Query(
        default=50, description="Quantidade de registros por p??gina. Valor m??ximo: 50"
    ),
):
    resultado = await carrinhos.busca_carrinhos_abandonados(
        numero_pagina, qtde_por_pagina
    )
    return resultado
