from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from carrinho_compras.schemas.uteis import *


class CarrinhoItemBase(BaseModel):
    codigo: str = Field(description="Código do produto")
    cor: str = Field(description="Cor/modelo do produto")
    numeracao: str = Field(description="Numeração do produto")
    quantidade: int = Field(1, ge=1, description="Quantidade do produto no carrinho")
    presente: bool = Field(False, description="É presente")


class CarrinhoBase(BaseModel):
    email_cliente: str = Field(description="E-mail do cliente")
    codigo: Optional[int] = Field(description="Código do pedido/carrinho")
    cep: Optional[int] = Field(description="CEP do endereço de entrega")
    forma_pagamento: Optional[str] = Field(description="Forma de pagamento")
    tipo_entrega: Optional[str] = Field(description="Tipo de entrega")
    valor_frete: Optional[float] = Field(0, description="Valor do frete")


class CarrinhoItemSchema(CarrinhoItemBase):
    preco_unitario: Optional[float] = Field(description="Preço unitário do produto")
    data_criacao: Optional[datetime] = Field(description="Data de inserção do item")
    data_atualizacao: Optional[datetime] = Field(description="Data da última atualização do item")


class CarrinhoSchema(CarrinhoBase):
    valor_total: Optional[float] = Field(description="Valor total líquido do carrinho")
    quantidade_total: Optional[int] = Field(description="Quantidade total de produtos")
    data_criacao_carrinho: Optional[datetime] = Field(description="Data de criação do carrinho")
    data_atualizacao: Optional[datetime] = Field(description="Data da última atualização")


class CarrinhoCompleto(CarrinhoSchema):
    produtos: Optional[list[CarrinhoItemSchema]] = Field(description="Lista de produtos")


class ListaCarrinhos(ConsultaPaginada):
    carrinhos: Optional[list[CarrinhoCompleto]] = Field([], description="Lista de carrinhos")


class CarrinhoRequest(CarrinhoBase):
    produto: Optional[CarrinhoItemBase] = Field(description="Dados do produto")

    class Config:
        schema_extra = {
            "example": {
                "email_cliente": "email@email.com",
                "codigo": 123456,
                "cep": 38408975,
                "forma_pagamento" : "Cartão",
                "tipo_entrega" : "Transportadora",
                "valor_frete" : 15.65,
                "produto":{
                            "codigo": "111",
                            "cor": "Vermelho",
                            "numeracao": "38",
                            "quantidade": 2,
                            "presente": False
                        }
                }
            }
            
class CarrinhoAtualizacao(CarrinhoSchema):
    produto: Optional[CarrinhoItemSchema] = Field(description="Dados do produto")


class ExclusaoProdutoRequest(BaseModel):
    codigo: str = Field(description="Código do produto")
    cor: str = Field(description="Cor/modelo do produto")
    numeracao: str = Field(description="Numeração do produto")

    class Config:
        schema_extra = {
            "example": {
                "codigo": "111",
                "cor": "Vermelho",
                "numeracao": "38"
            }
        }


class ProdutosPopulares(ConsultaPaginada):
    produtos: Optional[list[QuantidadeTotalPorProduto]] = Field(
            description="Lista de produtos mais adicionados ao carrinho")
