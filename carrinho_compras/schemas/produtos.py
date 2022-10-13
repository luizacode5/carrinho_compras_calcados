from typing import Optional

from pydantic import BaseModel, condecimal, Field

# Classe representando os dados do produto


class Produto(BaseModel):
    nome: str = Field(description="Nome do calçado")
    sku: str = Field(description="Código do Calçado")
    codigo: str = Field(description="Código do Produto")
    categoria: str = Field(description="Categoria do Calçado")
    material: str = Field(description="Material do Calçado")
    descricao: Optional[str] = Field(None, description="Descrição do Calçado") 
    marca: str = Field(description="Marca do Calçado")
    preco: condecimal(max_digits=10, gt=0.01, decimal_places=2) = Field(description="Preço do Calçado")
    image: str = Field(description="Imagem do Calçado")
    cor: str = Field(description="Cor do Calçado")
    tamanho: int = Field(description="Tamanho do calçado")
    estoque: int = Field(gt=0, description="Estoque")
