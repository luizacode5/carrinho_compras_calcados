from fastapi import APIRouter, status, HTTPException

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.controller import carrinhos, excecoes
from carrinho_compras.documentacao.carrinhos import *


rota_carrinhos = APIRouter(
    prefix="/carrinho",
    tags=["Carrinho"]
)

@rota_carrinhos.post('/',
    summary="Cria carrinho e adiciona/atualiza produtos",
    description=POST_CARRINHO_DESCRICAO,
    responses= {
        200: {"description": "Produto excluído com sucesso",
            "content": POST_CARRINHO_DESCRICAO},
        422: {"description": "Não foi possível processar as \
            instruções contidas na requisição"},
        500: {"description": "Erro interno no servidor"}
    },
    response_model=CarrinhoSchema,
    # response_model=CarrinhoResponse,
    status_code=status.HTTP_201_CREATED)
async def adiciona_itens_carrinho(carrinho: CarrinhoBase):
    try:
        resultado = await carrinhos.adiciona_itens_carrinho(carrinho)
    except excecoes.ObjetoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Carrinho não encontado")
    except excecoes.ObjetoNaoModificado:
        raise HTTPException(status_code=200, detail="Nada foi modificados")
    except excecoes.PyMongoError:
        raise HTTPException(status_code=400, detail="Falha ao inserir")

@rota_carrinhos.delete('/delete_item',
    summary="Exclui produto do carrinho",
    description=DELETE_ITEM_CARRINHO_DESCRICAO,
    status_code=status.HTTP_200_OK)
async def exclui_item_carrinho(produto: ExclusaoProdutoRequest, email_cliente: str):
    await carrinhos.exclui_item_carrinho(produto, email_cliente)
    return

@rota_carrinhos.delete('/delete',
    summary="Exclui carrinho",
    description=DELETE_CARRINHO_DESCRICAO,
    status_code=status.HTTP_200_OK)
async def exclui_carrinho(email_cliente: str):
    resultado = await carrinhos.exclui_carrinho(email_cliente)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O cliente não possui carrinho aberto")
    return

@rota_carrinhos.put('/fechar',
    summary="Gera pedido a partir do carrinho",
    description=PUT_FECHA_CARRINHO_DESCRICAO,
    response_model=PedidoSchema,
    status_code=status.HTTP_200_OK)
async def fecha_carrinho(email_cliente: str):
    resultado = await carrinhos.fecha_carrinho(email_cliente)
    return resultado

@rota_carrinhos.get('/cliente',
    summary="Busca carrinho por cliente",
    description=GET_CARRINHO_CLIENTE_DESCRICAO,
    response_model=CarrinhoSchema,
    status_code=status.HTTP_200_OK)
async def busca_carrinho_cliente(email_cliente: str):
    resultado = await carrinhos.busca_carrinho_cliente(email_cliente)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado carrinho para o cliente")
    return resultado

@rota_carrinhos.get('/pedido',
    summary="Busca pedido por id",
    description=GET_PEDIDO_POR_ID_DESCRICAO,
    response_model=PedidoSchema,
    status_code=status.HTTP_200_OK)
async def busca_pedido_por_id(id_pedido: str):
    resultado = await carrinhos.busca_pedido_por_id(id_pedido)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado pedido com o id informado")
    return resultado

@rota_carrinhos.get('/pedido/cliente',
    summary="Busca pedidos do cliente",
    description=GET_PEDIDOS_CLIENTE_DESCRICAO,
    response_model=ListaPedidos,
    status_code=status.HTTP_200_OK)
async def busca_pedidos_por_cliente(email_cliente: str):
    resultado = await carrinhos.busca_pedidos_por_cliente(email_cliente)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foram encontrados pedidos para o cliente")
    return resultado


@rota_carrinhos.get('/produto',
    summary="Busca carrinhos que contém o produto",
    description=GET_CARRINHOS_COM_PRODUTO_DESCRICAO,
    response_model=ConsultaCarrinhos,
    status_code=status.HTTP_200_OK)
async def busca_carrinhos_por_produto(codigo_produto: str):
    resultado = await carrinhos.busca_carrinhos_por_produto(codigo_produto)
    return resultado

@rota_carrinhos.get('/produtos_populares',
    summary="Busca produtos mais frequentes nos carrinhos abertos",
    description=GET_PRODUTOS_POPULARES_CARRINHOS_DESCRICAO,
    response_model=ConsultaProdutoCarrinho,
    status_code=status.HTTP_200_OK)
async def busca_produtos_populares():
    resultado = await carrinhos.busca_produtos_populares()
    return resultado

@rota_carrinhos.get('/abandonados',
    summary="Busca carrinhos abandonados",
    description=GET_CARRINHOS_ABANDONADOS_DESCRICAO,
    response_model=ConsultaCarrinhos,
    status_code=status.HTTP_200_OK)
async def busca_carrinhos_abandonados():
    resultado = await carrinhos.busca_carrinhos_abandonados()
    return resultado