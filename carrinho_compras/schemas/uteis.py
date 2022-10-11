from pydantic import BaseModel, Field
from typing import Optional


class ConsultaPaginada(BaseModel):
    numero_pagina: Optional[int] = Field(description="Número da página pesquisada")
    qtde_por_pagina: Optional[int] = Field(description="Quantidade de registros por página")


class QuantidadeTotalPorProduto(BaseModel):
    codigo: str = Field(description="Código do produto")
    cor: str = Field(description="Cor do produto")
    numeracao: str = Field(description="Numeração do produto")
    quantidade_total: Optional[str] = Field(
        description="Somatório da quantidade do produto")
    
    class Config:
        schema_extra = {
            "produtos": [
                {
                    "codigo": "111",
                    "cor": "Vermelho",
                    "numeracao": "38",
                    "quantidade_total": "15"
                },
                {
                    "codigo": "111",
                    "cor": "Preto",
                    "numeracao": "35",
                    "quantidade_total": "8"
                },
                {
                    "codigo": "222",
                    "cor": "Vermelho",
                    "numeracao": "35",
                    "quantidade_total": "6"
                }
            ]
        }