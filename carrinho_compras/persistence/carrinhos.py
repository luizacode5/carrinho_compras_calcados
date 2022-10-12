from fastapi import HTTPException, status
import logging
from pymongo import ASCENDING, DESCENDING

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.persistence.persistence_bd import obter_colecao


COLECAO_CARRINHOS = obter_colecao("carrinhos")

async def insere_carrinho(carrinho: CarrinhoAtualizacao):
    try:
        dados_carrinho = carrinho.dict(exclude={"produto"})
        
        if carrinho.produto:
            dados_carrinho["produtos"] = [carrinho.produto.dict()]

        resultado = await COLECAO_CARRINHOS.insert_one(dados_carrinho)

        if resultado.inserted_id:
            return True
        return False
        
    except Exception as e:
        logging.exception(f'insere_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível criar o carrinho")

async def atualiza_carrinho(carrinho: CarrinhoAtualizacao):
    try:
        data_carrinho = carrinho.dict(exclude={"produto"})
        campos_alterar = {k: v for k, v in data_carrinho.items() if v is not None}

        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": carrinho.email_cliente},
            {"$set": campos_alterar},
        )

        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        logging.exception(f'atualiza_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível atualizar o carrinho")  

async def insere_produto_carrinho(carrinho: CarrinhoAtualizacao):
    try:
        dados_produto = carrinho.produto.dict()

        resultado  = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": carrinho.email_cliente},
            {"$set": {"valor_total": carrinho.valor_total,
                    "quantidade_total": carrinho.quantidade_total,
                    "valor_frete": carrinho.valor_frete,
                    "data_atualizacao": carrinho.data_atualizacao},
            "$addToSet": {"produtos": dados_produto}
            }
        )

        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        logging.exception(f'insere_produto_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível inserir o produto no carrinho")  

async def atualiza_produto_carrinho(carrinho: CarrinhoAtualizacao):
    try:
        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": carrinho.email_cliente,
             "produtos": {"$elemMatch":  {"codigo": carrinho.produto.codigo,
                                        "cor": carrinho.produto.cor, 
                                        "tamanho": carrinho.produto.tamanho}
                        }
            },
            {"$set": {"valor_total": carrinho.valor_total,
                        "quantidade_total": carrinho.quantidade_total,
                        "valor_frete": carrinho.valor_frete,
                        "data_atualizacao": carrinho.data_atualizacao,
                        "produtos.$.quantidade": carrinho.produto.quantidade,
                        "produtos.$.data_atualizacao": carrinho.produto.data_atualizacao,
                        "produtos.$.presente": carrinho.produto.presente}
            }
        )
        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        logging.exception(f'atualiza_produto_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível atualizar o produto no carrinho")  

async def exclui_item_carrinho(carrinho: CarrinhoAtualizacao):
    try:
        resultado = await COLECAO_CARRINHOS.update_one(
            {"email_cliente": carrinho.email_cliente},
            {"$set": {"valor_total": carrinho.valor_total,
                        "quantidade_total": carrinho.quantidade_total,
                        "data_atualizacao": carrinho.data_atualizacao},
            "$pull": {"produtos": {"codigo": carrinho.produto.codigo,
                                    "cor": carrinho.produto.cor, 
                                    "tamanho": carrinho.produto.tamanho}
                    }
            }
        )
        if resultado.modified_count > 0:
            return True
        return False

    except Exception as e:
        logging.exception(f'exclui_item_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível excluir o produto do carrinho")
        
async def exclui_carrinho(email_cliente: EmailStr):
    try:
        resultado = await COLECAO_CARRINHOS.delete_one(
            {"email_cliente": email_cliente}
        )

        if resultado.deleted_count > 0:
            return True
        return False

    except Exception as e:
        logging.exception(f'exclui_carrinho.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível excluir o carrinho")

async def busca_carrinho_cliente(email_cliente: EmailStr) -> CarrinhoCompleto:
    try:
        resultado = await COLECAO_CARRINHOS.find_one(
            {"email_cliente" : email_cliente}
        )

        if resultado:
            carrinho = CarrinhoCompleto(**resultado)
            return carrinho

    except Exception as e:
        logging.exception(f'busca_carrinho_cliente.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível consultar o carrinho do cliente")

async def busca_carrinhos_por_produto(
    filtro_produto: dict, 
    registros_pular: int, 
    qtde_por_pagina: int
    ) -> ListaCarrinhos:
    try:
        lista_carrinhos = ListaCarrinhos()

        cursor_pesquisa = COLECAO_CARRINHOS \
            .find({"produtos": 
                        {"$elemMatch": filtro_produto}}) \
            .skip(registros_pular) \
            .limit(qtde_por_pagina) \
            .sort("data_criacao_carrinho", DESCENDING)

        async for carrinhos_resultado in cursor_pesquisa:
            carrinho = CarrinhoCompleto(**carrinhos_resultado)
            lista_carrinhos.carrinhos.append(carrinho)

        return lista_carrinhos

    except Exception as e:
        logging.exception(f'busca_carrinhos_por_produto.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de carrinhos por produto")

async def busca_produtos_populares(
    registros_pular: int,
    qtde_por_pagina: int
    ) -> ProdutosPopulares:
    try:
        lista_produtos = ProdutosPopulares()
        lista_produtos.produtos = []

        cursor_pesquisa = COLECAO_CARRINHOS \
            .aggregate( [   
                    {"$unwind": "$produtos" }, 
                    {"$group": { "_id": {"codigo": "$produtos.codigo",  
                                        "cor": "$produtos.cor", 
                                        "tamanho": "$produtos.tamanho"},  
                    "quantidade_total": { "$sum": "$produtos.quantidade" }}}, 
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
        logging.exception(f'busca_produtos_populares.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de produtos populares")

async def busca_carrinhos_abandonados(
    registros_pular: int, 
    qtde_por_pagina: int
    ) -> ListaCarrinhos:
    try:
        lista_carrinhos = ListaCarrinhos()

        cursor_pesquisa = COLECAO_CARRINHOS \
            .find({}) \
            .skip(registros_pular) \
            .limit(qtde_por_pagina) \
            .sort("data_criacao_carrinho", ASCENDING)
        
        async for carrinhos_resultado in cursor_pesquisa:
            carrinho = CarrinhoCompleto(**carrinhos_resultado)
            lista_carrinhos.carrinhos.append(carrinho)

        return lista_carrinhos
    except Exception as e:
        logging.exception(f'busca_carrinhos_abandonados.erro: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível realizar a consulta de carrinhos abandonados")
