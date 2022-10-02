from fastapi import FastAPI

from carrinho_compras.routers.carrinhos import rota_carrinhos
from carrinho_compras.routers.clientes import rota_clientes
from carrinho_compras.routers.enderecos import rota_enderecos
from carrinho_compras.routers.principal import rota_principal
from carrinho_compras.routers.produtos import rota_produtos


def configurar_rotas(app: FastAPI):
    app.include_router(rota_principal)
    app.include_router(rota_enderecos)
    app.include_router(rota_clientes)
    app.include_router(rota_produtos)
    app.include_router(rota_carrinhos)


def criar_aplicacao_fastapi():
    app = FastAPI()
    configurar_rotas(app)

    return app
