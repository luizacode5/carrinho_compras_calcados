from pydantic import BaseModel, Field
from typing import Optional


class CarrinhoItemBase(BaseModel):
    codigo: str = Field(description="Código único do produto")
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
    valor_frete: Optional[float] = Field(description="Valor do frete")

    # valor_desconto: Optional[float] = Field(description="Valor de desconto")
    # nome_campanha: Optional[float] = Field(description="Nome da campanha/oferta")
    # endereco_entrega: Optional[Endereco] = Field(description="Endereço de entrega")

    itens: Optional[list[CarrinhoItemBase]] = []
    # itens: Optional[list[CarrinhoItemRequest]] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "email_cliente": "email@email.com",
                "codigo": 123456,
                "cep": 38408975,
                "forma_pagamento" : "Cartão",
                "tipo_entrega" : "Transportadora",
                "valor_frete" : 15.65,
                "itens": [
                        {
                            "codigo": "111",
                            "cor": "Vermelho",
                            "numeracao": "38",
                            "quantidade": 2,
                            "presente": False
                        },
                        {
                            "codigo": "222",
                            "cor": "Azul",
                            "numeracao": "38",
                            "quantidade": 1,
                            "presente": True
                        }
                    ]
                }
            }


class CarrinhoItemSchema(CarrinhoItemBase):
    preco_unitario: Optional[float] = Field(description="Preço unitário do produto")
    data_criacao: Optional[str] = Field(description="Data de inserção do item")
    data_atualizacao: Optional[str] = Field(description="Data da última atualização do item")


class CarrinhoSchema(CarrinhoBase):
    valor_total: Optional[float] = Field(description="Valor total")
    quantidade_total: Optional[int] = Field(description="Quantidade total de produtos")
    data_criacao_carrinho: Optional[str] = Field(description="Data de criação do carrinho")
    data_atualizacao: Optional[str] = Field(description="Data da última atualização")
    # itens: Optional[list[CarrinhoItemSchema]] = Field(default_factory=list)
    itens: Optional[list[CarrinhoItemSchema]] = []


class CarrinhoItemResponse(BaseModel):
    detalhes: Optional[list[CarrinhoItemBase]] = Field(description="Produtos inseridos/alterados")


class CarrinhoResponse(CarrinhoBase):
    produtos_nao_processados: Optional[list[CarrinhoItemResponse]] = Field(description="Produtos não processados")


class PedidoSchema(CarrinhoSchema):
    status: Optional[str] = Field(description="Status do pedido")
    data_criacao_pedido: Optional[str] = Field(description="Data de criação do pedido")
    pagamento_aprovado: Optional[bool] = Field(False, description="Pagamento aprovado")


class ListaPedidos(BaseModel):
    pedidos: Optional[list[PedidoSchema]] = []


class ExclusaoProdutoRequest(BaseModel):
    codigo: str = Field(description="Código único do produto")
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


class ConsultaCarrinhos(BaseModel):
    carrinhos: Optional[list[CarrinhoSchema]] = []


class OcorrenciaVariacaoProduto(BaseModel):
    cor: str = Field(description="Cor/modelo do produto")
    numeracao: str = Field(description="Numeração do produto")
    quantidade: int = Field(1, ge=1, description="Quantidade de ocorrências")

class ConsultaProdutoCarrinho(BaseModel):
    codigo: str = Field(description="Código único do produto")
    descricao: str = Field(description="Nome do produto")
    variacoes: Optional[list[OcorrenciaVariacaoProduto]] = Field(description="Variações dos produtos")


class AtualizaCarrinhoExclusaoItem(BaseModel):
    email_cliente: Optional[str] = Field(description="E-mail do cliente")
    valor_total: Optional[float] = Field(description="Valor total")
    quantidade_total: Optional[int] = Field(description="Quantidade total de itens")
    data_atualizacao: Optional[str] = Field(description="Data da última atualização")