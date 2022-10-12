from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from pymongo.errors import DuplicateKeyError, PyMongoError

from carrinho_compras.persistence.clientes import AdaptadorCliente
from carrinho_compras.persistence.excecoes import ObjetoNaoModificado
from carrinho_compras.schemas.clientes import Cliente

rota_clientes = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@rota_clientes.post("/", status_code=201, response_model=Cliente)
async def criar_usuário(
    usuario: Cliente,
    adaptador: AdaptadorCliente = Depends(),
):
    try:
        return await adaptador.cria(usuario)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Usuário já existe")
    except Exception:
        raise HTTPException(status_code=400, detail="Falha ao inserir")


@rota_clientes.get("/", response_model=Cliente)
async def retornar_usuario(
    email: EmailStr,
    adaptador: AdaptadorCliente = Depends(),
):
    usuario = await adaptador.pega(email)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@rota_clientes.delete("/", status_code=204)
async def deletar_usuario(
    email: EmailStr,
    adaptador: AdaptadorCliente = Depends(),
):
    try:
        await adaptador.deleta(email)
    except ObjetoNaoModificado:
        raise HTTPException(status_code=400, detail="Cliente não modificado")
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Falha ao deletar")
