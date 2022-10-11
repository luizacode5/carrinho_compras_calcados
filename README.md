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
- [ ] Atualizar dados de produto
- [x] Pesquisar produto
- [x] Pesquisar produto pelo nome
- [x] Remover um produto

### 🛒 Carrinho
- [ ] Abrir carrinho de compras
- [ ] Adicionar itens no carrinho
- [ ] Remover itens
- [ ] Consultar o carrinho
- [ ] Consultar o carrinho fechado
- [ ] Consultar os produtor e quantidades do carrinho fechado
- [ ] Consultar quantos carrinhos o cliente possui
- [ ] Fechar o carrinho
- [ ] Excluir o carrinho

## ✨ Entregas extras:
- [ ] Especificação do produto
- [ ] Documentação a API Rest com Swagger/OpenAPI
- [ ] Readme
- [ ] Testes unitários
- [ ] Autenticação
- [ ] Mensagens de log
- [ ] Deploy
- [ ] Arquivo Dockerfile e docker-compose
