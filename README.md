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
- [ ] Abrir carrinho de compras
- [ ] Adicionar itens no carrinho
- [ ] Remover itens
- [ ] Busca carrinho
- [ ] Busca carrinho fechado
- [ ] Busca produtos e quantidades do carrinho fechado
- [ ] Busca quantos carrinhos o cliente possui
- [x] Atualiza carrinho
- [ ] Fechar carrinho
- [x] Excluir carrinho

## ✨ Entregas extras:
- [x] Especificação do produto
- [x] Documentação a API Rest com Swagger/OpenAPI
- [x] Readme
- [ ] Testes unitários
- [x] Autenticação
- [ ] Mensagens de log
- [ ] Deploy
- [x] Arquivo Dockerfile e docker-compose
