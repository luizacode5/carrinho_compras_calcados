from fastapi import FastAPI

from carrinho_compras.routers.carrinhos import rota_carrinhos
from carrinho_compras.routers.clientes import rota_clientes
from carrinho_compras.routers.enderecos import rota_enderecos
from carrinho_compras.routers.principal import rota_principal
from carrinho_compras.routers.produtos import rota_produtos
from carrinho_compras.routers.pedidos import rota_pedidos


def configurar_rotas(app: FastAPI):
    app.include_router(rota_principal)
    app.include_router(rota_enderecos)
    app.include_router(rota_clientes)
    app.include_router(rota_produtos)
    app.include_router(rota_carrinhos)
    app.include_router(rota_pedidos)


def criar_aplicacao_fastapi():
    descricao_api = "Esta API é responsável pelos carrinhos de compra, cadastro \
     de produtos e clientes para lojas online que vendem calçados."

    app = FastAPI(title="API de Carrinho de Compras para Calçados ",
        description=descricao_api)
    configurar_rotas(app)

    return app
