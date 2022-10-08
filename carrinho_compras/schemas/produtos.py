from typing import Optional

from pydantic import BaseModel


# Classe representando os dados do produto

class Produto(BaseModel):
    nome: str
    sku: str
    categoria: str
    material:str
    descricao: Optional[str]
    marca: str
    preco: float
    image: str
    cor: str
    tamanho: int
    estoque: int