import asyncio

from carrinho_compras.persistence.clientes import AdaptadorCliente
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

seguranca = HTTPBasic()


def pegar_cliente(cliente):
    try:
        usuario = asyncio.run(AdaptadorCliente().pega(cliente))
        print(cliente)
        print(usuario)
        if usuario is None:
            print("Usuário não encontrado!")
    except Exception as e:
        print(e)
    return usuario["email"], usuario["senha"]


def confere_credencial(credenciais: HTTPBasicCredentials = Depends(seguranca)):
    credencial_usuario = credenciais.username
    credencial_senha = credenciais.password
    try:
        usuario, senha = pegar_cliente(credencial_usuario)
        print(usuario)
        if usuario == credencial_usuario:
            if senha == credencial_senha:
                return usuario
    except Exception as e:
        print(e)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuário ou senha inválidos!',
        headers={"WWW-Authenticate": "Basic"}
    )


def autenticacao(credenciais: str = Depends(confere_credencial)):
    return "Autenticação realizada!"


# Para testar pode ser incluída uma rota como no exemplo abaixo ou chamar a função autenticação em uma rota já existente:
# @rota_clientes.get("/teste")
# async def teste(credenciais: str = Depends(autenticacao)):
#    return "Oi"
