# Projeto Carrinho de Compras

 ## 💙 Autores:    

- [Bruna Cotrim](https://github.com/brunacotrim), 
- [Daiani Bussanello](https://github.com/daianibusa),
- [Lívia dos Santos Pereira](https://github.com/liviaspereira), 
- [Lorrayne Silva](https://github.com/lorsilv), 
- [Stephanie Zimmermann](https://github.com/Stephaniezm)

## 📌 Introdução: 
Projeto desenvolvido com base nos conhecimento adquiridos atráves do curso de Python oferecido pelo LuizaCode 5ª edição. 

Foi criado um conjunto de APIs REst em python para um carrinho de compras, utilizando o
framework FastAPI com seus registros salvos no banco de dados MongoDB.

* [Python 3.10.7](https://www.python.org/downloads/release/python-3107/)
* [FastAPI 0.85.0](https://fastapi.tiangolo.com/)
* [MongoDB](https://www.mongodb.com/)
* [Docker](https://www.docker.com/)

## 📖 Bibliotecas utilizadas:

- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic](https://pydantic-docs.helpmanual.io/install/)
- [Motor](https://motor.readthedocs.io/en/stable/)

## 🛠 Como rodar o projeto:

Para executar:
```bash
sudo docker-compose up -d --build
```

Para parar:
```bash
sudo docker-compose down
```

Para ver os logs:
```bash
sudo docker-compose logs -f
```

Para utilizar os endpoints de Criar Endereço, Deletar Endereço e Deletar Cliente é necessário autenticação.
Para fazer a autenticação é necessãrio primeiro criar um cliente da maneira normal, e então obter um token fazendo um POST no endpoint `/token` com o email e a senha, utilizando FORM, por exemplo, para um Cliente com email `user@email.com` e senha `string`.

```bash
curl -X POST http://localhost:8000/token -F username='user@email.com' -F password='string'
```

Esse endpoint então retornará o token de acesso, o token então deve ser utilizado para utilização dos endpoints protegidos, sendo adicionado no endpoint da seguinte maneira, para o exemplo de adicionar um endereço a um cliente:

```bash
curl -X 'POST' \
  'http://localhost:8000/enderecos/?email=user%40email.com' \
  -H 'Authorization: Bearer TOKEN_OBTIDO_ANTERIORMENTE_AQUI' \
  -H 'Content-Type: application/json' \
  -d '{
  "rua": "string",
  "cep": "string",
  "cidade": "string",
  "estado": "string"
}'
```

Também é possível fazer essas operações de maneira mais simples utilizando o `/docs` onde possui um botão `Authorize` que já coloca o token automaticamente em todas as operações que o necessitam estando na página.

## Deploy no Heroku

https://carrinho-compras-luiza-code.herokuapp.com/docs#/


###### OBS: Ainda não está funcionando completamente, mudanças ainda serão realizadas.

## 💻 Requisito Funcionais e entregas extras:

### 🙆🏽‍♀️ Clientes
- [x] Cadastrar clientes
- [x] Cadastrar endereço
- [x] Pesquisar cliente
- [x] Pesquisar endereço
- [x] Remover cliente
- [x] Remover endereço

### 👞 Produto
- [x] Cadastrar produto
- [x] Atualizar dados de produto
- [x] Pesquisar produto
- [x] Pesquisar produto pelo nome
- [x] Remover um produto

### 🛒 Carrinho
- [x] Criar carrinho de compras e adicionar itens
- [x] Atualizar os dados do carrinho
- [x] Remover itens
- [x] Remover carrinho
- [x] Busca carrinho por cliente
- [x] Consultar carrinhos por produto
- [x] Consultar carrinhos abandonados
- [x] Consultar produtos "em alta"/"populares" nos carrinhos
- [x] Fechar carrinho (pedido)

- [x] Consultar pedido (carrinho fechado) por id
- [x] Consultar pedidos por cliente
- [x] Consultar pedidos por produto
- [x] Consultar produtos mais vendidos
- [x] Consultar quantidade e valor total de pedidos por cliente

## ✨ Entregas extras:
- [x] Especificação do produto
- [x] Documentação a API Rest com Swagger/OpenAPI
- [x] Readme
- [x] Testes unitários (parcial)
- [x] Autenticação
- [x] Mensagens de log
- [x] Arquivo Dockerfile e docker-compose
- [x] Deploy
