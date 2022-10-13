from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from pymongo.errors import DuplicateKeyError, PyMongoError

from carrinho_compras.configuracoes import configuracao
from carrinho_compras.controller.clientes import (authenticate_user,
                                                  create_access_token,
                                                  get_current_user)
from carrinho_compras.persistence.clientes import AdaptadorCliente
from carrinho_compras.persistence.excecoes import ObjetoNaoModificado
from carrinho_compras.schemas.clientes import Cliente, ClienteInDB, Token

rota_clientes = APIRouter(prefix="/clientes", tags=["Clientes"])

rota_autenticacao = APIRouter()


@rota_clientes.post("/", status_code=201, response_model=Cliente)
async def criar_usuário(
    usuario: ClienteInDB,
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
    current_user: Cliente = Depends(get_current_user),
):
    try:
        await adaptador.deleta(email)
    except ObjetoNaoModificado:
        raise HTTPException(status_code=400, detail="Cliente não modificado")
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Falha ao deletar")


@rota_autenticacao.post(
    "/token", response_model=Token
)  # endpoint que dado um usuario e uma senha retona o token
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    adaptador: AdaptadorCliente = Depends(),
):
    user = await authenticate_user(adaptador, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=configuracao.access_token_expire_minutes
    )  # define um tempo para expirar o token
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
