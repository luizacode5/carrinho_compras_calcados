from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from pymongo.errors import PyMongoError

from carrinho_compras.persistence.clientes import AdaptadorCliente
from carrinho_compras.persistence.excecoes import (ObjetoNaoEncontrado,
                                                   ObjetoNaoModificado)
from carrinho_compras.schemas.clientes import Endereco

rota_enderecos = APIRouter(
    prefix="/enderecos",
    tags=["Endereços"]
)


@rota_enderecos.post("/", status_code=201, response_model=Endereco)
async def criar_endereco(
    email: EmailStr,
    endereco: Endereco,
    adaptador: AdaptadorCliente = Depends(),
):
    try:
        return await adaptador.adiciona_endereco(email, endereco)

    except ObjetoNaoEncontrado:
        raise HTTPException(status_code=404, detail="Usuário não encontado")
    except ObjetoNaoModificado:
        raise HTTPException(status_code=200, detail="Nada foi modificados")
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Falha ao inserir")


@rota_enderecos.delete("/")
async def deletar_endereco(
    endereco: Endereco,
    email: EmailStr,
    adaptador: AdaptadorCliente = Depends(),
):
    try:
        await adaptador.remover_endereco(endereco, email)

    except ObjetoNaoModificado:
        raise HTTPException(status_code=400, detail="Endereco não modificado")
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Falha ao deletar")
