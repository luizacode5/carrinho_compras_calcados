from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal

# Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
    rua: str
    cep: str
    cidade: str
    estado: str


# Classe representando os dados do cliente
class Usuario(BaseModel):
    nome: str
    endereco: Optional[List[Endereco]] = Field(default_factory=list)
    email: EmailStr
    senha: str = Field(min_length=3)