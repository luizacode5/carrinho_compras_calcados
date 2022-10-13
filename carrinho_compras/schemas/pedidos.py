from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.schemas.uteis import *


class PedidoSchema(CarrinhoCompleto):
    id_pedido: Optional[str] = Field(description="ID do pedido")
    status: Optional[str] = Field(description="Status do pedido")
    data_criacao_pedido: Optional[datetime] = Field(
        description="Data de criação do pedido"
    )
    pagamento_aprovado: Optional[bool] = Field(False, description="Pagamento aprovado")


class ListaPedidos(ConsultaPaginada):
    pedidos: Optional[list[PedidoSchema]] = Field([], description="Lista de pedidos")


class ProdutosMaisVendidos(ConsultaPaginada):
    produtos: Optional[list[QuantidadeTotalPorProduto]] = Field(
        description="Lista de produtos mais vendidos"
    )


class TotalPedidosPorCliente(BaseModel):
    email_cliente: Optional[EmailStr] = Field(description="E-mail do cliente")
    quantidade_total: Optional[str] = Field(description="Quantidade total de pedidos")
    valor_total: Optional[str] = Field(description="Valor total de pedidos")


class TotalPedidoClientes(ConsultaPaginada):
    clientes: Optional[list[TotalPedidosPorCliente]] = Field(
        [], description="Lista de pedidos"
    )
