import asyncio
from math import prod
import pytest
from carrinho_compras.persistence.persistence_bd import cliente_mongo
import requests

#limpar base de dados antes de cada teste
@pytest.fixture(autouse=True)
def resource():
    drop_command = cliente_mongo.drop_database('carrinho')
    asyncio.get_event_loop().run_until_complete(drop_command)
    yield


def test_criar_produto_pegar():
    produto = {
        'nome': 'SANDÁLIA VIKKI SALTO ALTO COURO PRETA E DOURADA',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 490 ,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 2
    }
    insert_response = requests.post("http://localhost:8000/produtos/", json=produto)

    get_by_code_response = requests.get(f"http://localhost:8000/produtos/sku/?sku={produto['sku']}")
    assert get_by_code_response.json()['descricao']== produto['descricao']

    get_by_name_response = requests.get(f"http://localhost:8000/produtos/nome/?nome={produto['nome']}")
    assert get_by_name_response.json()['descricao']== produto['descricao']

#teste para regra: nao pode existir produto sem nome
def test_criar_produto_sem_nome():
    produto = {
        'nome': '',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 490 ,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 2
    }
    insert_response = requests.post("http://localhost:8000/produtos/", json=produto)
    assert insert_response.json() == {'detail': 'Campos obigatórios não foram prenchidos coretamente'}
#teste para regra: nao pode existir produto com preco menor do que R$0,01
def test_criar_produto_sem_preco():
    produto = {
        'nome': 'SANDÁLIA VIKKI SALTO ALTO COURO PRETA E DOURADA',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 0 ,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 2
    }
    insert_response = requests.post("http://localhost:8000/produtos/", json=produto)
    assert insert_response.json() == {'detail': 'Campos obigatórios não foram prenchidos coretamente'}


#teste para regra: estoque precisa ser maior do que zero
def test_criar_produto_sem_estoque():
    produto = {
        'nome': 'SANDÁLIA VIKKI SALTO ALTO COURO PRETA E DOURADA',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 490,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 0
    }
    insert_response = requests.post("http://localhost:8000/produtos/", json=produto)
    assert insert_response.json() == {'detail': 'Campos obigatórios não foram prenchidos coretamente'}  

#teste para regra: codigo nao pode ser alterado

#teste para regra: produto não pode ser duplicado
def test_criar_produto_duplicado():
    produto = {
        'nome': 'SANDÁLIA VIKKI SALTO ALTO COURO PRETA E DOURADA',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 490 ,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 2
    }
    first_insert = requests.post("http://localhost:8000/produtos/", json=produto)
    assert first_insert.status_code == 201
    second_insert = requests.post("http://localhost:8000/produtos/", json=produto)
    assert second_insert.status_code == 409

#teste para regra: produto deletado
def test_produto_deletado():
    produto = {
        'nome': 'SANDÁLIA VIKKI SALTO ALTO COURO PRETA E DOURADA',
        'sku': 'S2116100010039',
        'categoria':'sandálias',
        'material': 'Couro',
        'descricao': 'Sexy, sofisticada e poderosa. Essa sandália de couro é um acontecimento! A amarração no tornozelo garante um toque de atitude extra,'
         'mas se você preferir um estilo mais clássico, é possível remover as tiras, ficando apenas com o fecho da fivela. Incrível, né', 
        'marca':'Schutz',
        'preco': 490 ,
        'image': 'y',
        'cor': 'preto',
        'tamanho': 35,
        'estoque': 2
    }

    insert_response = requests.post("http://localhost:8000/produtos/", json=produto)

    get_by_code_response = requests.get(f"http://localhost:8000/produtos/sku/?sku={produto['sku']}")
    assert get_by_code_response.json()['descricao']== produto['descricao']

    insert_response = requests.delete("http://localhost:8000/produtos/?sku=S2116100010039", json=produto)
    assert insert_response.status_code == 204

    get_by_code_response = requests.get(f"http://localhost:8000/produtos/sku/?sku={produto['sku']}")
    assert get_by_code_response.status_code == 404