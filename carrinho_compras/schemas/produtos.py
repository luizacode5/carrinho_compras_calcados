from typing import Optional

from pydantic import BaseModel, Field, condecimal

# Classe representando os dados do produto


class Produto(BaseModel):
    nome: str
    sku: str
    codigo: str
    categoria: str
    material: str
    descricao: Optional[str] = None
    marca: str
    preco: condecimal(max_digits=10, gt=0.01, decimal_places=2)
    image: str
    cor: str
    tamanho: int
    estoque: int = Field(gt=0)
