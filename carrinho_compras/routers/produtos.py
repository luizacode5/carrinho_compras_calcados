from fastapi import APIRouter

rota_produtos = APIRouter(prefix="/produtos")


from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError, PyMongoError

from carrinho_compras.persistence.produtos import AdaptadorProduto
from carrinho_compras.persistence.excecoes import ObjetoInvalido, ObjetoNaoModificado, ObjetoDuplicado
from carrinho_compras.schemas.produtos import Produto


rota_produtos = APIRouter(prefix="/produtos")


@rota_produtos.post("/", status_code=201, response_model=Produto)
async def criar_produto(
    produto: Produto,
    adaptador: AdaptadorProduto = Depends(),
):
    try:
        return await adaptador.cria(produto)
    except ObjetoDuplicado:
        raise HTTPException(status_code=409, detail="Produto já existe")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Falha ao inserir")

@rota_produtos.get("/sku", response_model=Produto)
async def retornar_produto_sku(
    sku: str,
    adaptador: AdaptadorProduto = Depends(),
):
    produto = await adaptador.pega(sku,chave ='sku')
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@rota_produtos.get("/nome", response_model=Produto)
async def retornar_produto_nome(
    nome: str,
    adaptador: AdaptadorProduto = Depends(),
):
    produto = await adaptador.pega(nome,chave='nome')
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@rota_produtos.get("/codigo", response_model=Produto)
async def retornar_produto_codigo_cor_tamanho(
    codigo: str,
    cor: str,
    tamanho: int,
    adaptador: AdaptadorProduto = Depends(),
):
    produto = await adaptador.pega_codigo_cor_tamanho(codigo, cor, tamanho)
    print(1111, codigo, cor, tamanho)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@rota_produtos.delete("/", status_code=204)
async def deletar_produto(
    sku: str,
    adaptador: AdaptadorProduto = Depends(),):
    await adaptador.deleta(sku)
