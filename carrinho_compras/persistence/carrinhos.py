import json
from bson import json_util
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from bson import ObjectId

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.persistence.persistence_bd import obter_colecao
from carrinho_compras.schemas.carrinhos import CarrinhoItemSchema


COLECAO_CARRINHOS = obter_colecao("carrinho")
COLECAO_PEDIDOS = obter_colecao("pedido")

async def insere_carrinho(carrinho: CarrinhoSchema):
    try:
        dados_carrinho = carrinho.dict()
        resultado = await COLECAO_CARRINHOS.insert_one(dados_carrinho)

        if resultado.inserted_id:
            return True
        return False
        
    except Exception as e:
        print(f"insere_carrinho.erro: {e}")
        # logger.exception(f'insere_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def adiciona_itens_carrinho(email_cliente, produtos: list[CarrinhoItemSchema]):
    try:
        produtos_carrinho = produtos.dict()

        resultado  = await COLECAO_CARRINHOS.update_many(
            {"email_cliente": email_cliente},
            {"$addToSet": {
                "itens":
                {
                    "$each": [produtos_carrinho]
                }
            }}
        )

        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        print(f"adiciona_itens_carrinho.erro: {e}")
        # logger.exception(f'adiciona_itens_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def altera_item_carrinho(produto: CarrinhoItemSchema, email_cliente):
    try:
        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": email_cliente,
             "itens": {"$elemMatch":  {"codigo": produto.codigo,
                                        "cor": produto.cor, 
                                        "numeracao": produto.numeracao
                                        }
                    }
            },
            {"$set": {"itens.$.quantidade": produto.quantidade,
                        "itens.$.data_atualizacao": produto.data_atualizacao,
                        "itens.$.presente": produto.presente }
            }
        )

        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        print(f"altera_item_carrinho.erro: {e}")
        # logger.exception(f'altera_item_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def exclui_item_carrinho(insere_carrinho: CarrinhoItemSchema, email_cliente):
    try:
        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": email_cliente},
            {"$pull": {"itens": {"codigo": insere_carrinho.codigo,
                                "cor": insere_carrinho.cor, 
                                "numeracao": insere_carrinho.numeracao
                                }
                }
            }
        )
        if resultado.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"exclui_item_carrinho.erro: {e}")
        # logger.exception(f'exclui_item_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def atualiza_carrinho(carrinho: CarrinhoSchema):
    try:
        data_carrinho = carrinho.dict(exclude={"itens"})
        campos_alterar = {k: v for k, v in data_carrinho.items() if v is not None}

        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": carrinho.email_cliente},
            {"$set": campos_alterar},
        )

        if resultado.modified_count:
            return True
        return False

    except Exception as e:
        print(f"atualiza_carrinho.erro: {e}")
        # logger.exception(f'atualiza_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def insere_pedido(pedido: PedidoSchema):
    try:
        dados_pedido = pedido.dict()
        
        resultado = await COLECAO_PEDIDOS.insert_one(dados_pedido)

        if resultado.inserted_id:
            return resultado.inserted_id
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"insere_pedido.erro: {e}")
        # logger.exception(f'insere_pedido.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
async def exclui_carrinho(email_cliente: str):
    try:
        resultado = await COLECAO_CARRINHOS.delete_one(
            {"email_cliente": email_cliente}
        )

        if resultado.deleted_count:
            return True
        return False

    except Exception as e:
        print(f"exclui_carrinho.erro: {e}")
        # logger.exception(f'exclui_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível excluir o carrinho")


async def busca_carrinho_cliente(email_cliente: str):
    try:
        resultado = await COLECAO_CARRINHOS.find_one(
            {"email_cliente" : email_cliente}
            )

        if resultado:
            carrinho = CarrinhoSchema(**resultado)
            return carrinho
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado carrinho para o cliente informado")

    except Exception as e:
        print(f"busca_carrinho_cliente.erro: {e}")
        # logger.exception(f'busca_carrinho_cliente.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
async def busca_pedido_por_id(id_pedido: str):
    try:
        resultado = await COLECAO_PEDIDOS.find_one(
            {"_id" : ObjectId(id_pedido)}
            )

        if resultado:
            pedido = PedidoSchema(**resultado)
            return pedido
        return False

    except Exception as e:
        print(f"busca_pedido_por_id.erro: {e}")
        # logger.exception(f'busca_pedido_por_id.erro: {e}')
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def busca_pedidos_por_cliente(email_cliente: str):
    try:
        lista_pedidos = ListaPedidos()
        cursor_pesquisa = await COLECAO_PEDIDOS.find(
            {"email_cliente" : email_cliente}
            )
        
        async for pedido_resultado in cursor_pesquisa:
            pedido = PedidoSchema(**pedido_resultado)
            lista_pedidos.append(pedido)
        return lista_pedidos
        
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado carrinho para o cliente informado")

    except Exception as e:
        print(f"busca_pedidos_por_cliente.erro: {e}")
        # logger.exception(f'busca_pedidos_por_cliente.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)



async def busca_carrinhos_por_produto(codigo_produto: str):
    try:
        return {"sucesso": "busca_carrinhos_por_produto"}
    except Exception as e:
        print(f"busca_carrinhos_por_produto.erro: {e}")
        # logger.exception(f'busca_carrinhos_por_produto.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def busca_produtos_populares():
    try:
        return {"sucesso": "busca_produtos_populares"}
    except Exception as e:
        print(f"busca_produtos_populares.erro: {e}")
        # logger.exception(f'busca_produtos_populares.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def busca_carrinhos_abandonados():
    try:
        return {"sucesso": "busca_carrinhos_abandonados"}
    except Exception as e:
        print(f"busca_carrinhos_abandonados.erro: {e}")
        # logger.exception(f'busca_carrinhos_abandonados.erro: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)