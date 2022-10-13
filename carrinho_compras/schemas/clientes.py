from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
    rua: str
    cep: str
    cidade: str
    estado: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Classe representando os dados do cliente
class Cliente(BaseModel):
    nome: str = Field(description="Nome do Cliente")
    endereco: Optional[List[Endereco]] = Field(default_factory=list, description="Como o endereço é opcional, caso não seja passado nada, uma lista vazia é criada")
    email: EmailStr = Field(description="O email deve ser único, um mesmo email para mais de um cliente não é permitido")


class ClienteInDB(Cliente):
    senha: str = Field(min_length=3, description="É necessário uma senha com mais de 3 caracter")