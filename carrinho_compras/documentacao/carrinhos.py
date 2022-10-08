

POST_CARRINHO_DESCRICAO = """
Adiciona um ou mais produtos ao carrinho do cliente.   
Cria um carrinho aberto para o cliente, caso ainda não exista.  
Substitui o produto no carrinho, caso já exista o mesmo produto no carrinho.   

Informações do carrinho:   
- `email_cliente`: E-mail do cliente, que já deve estar previamente cadastrado.
- `codigo`: Código do carrinho. Informação opcional.  
- `cep`: CEP do endereço de entrega do cliente. Informação opcional.  
- `forma_pagamento`: Forma de pagamento escolhida pelo cliente. Informação opcional.  
- `tipo_entrega`: Tipo de entrega escolhido pelo cliente. Informação opcional.  
- `valor_frete`: Valor do frete do carrinho. Informação opcional.  

Produtos:
- `codigo`: Código único do produto.
- `cor`: Cor/modelo do produto escolhido pelo cliente.
- `numeracao`: Número da grade do calçado selecionado pelo cliente.
- `quantidade`: Quantidade do produto adicionada ao carrinho. Precisa ser um valor inteiro maior que zero.
- `presente`: Informação opcional, que indica se o produto deve ser embalado para presente. Caso não informado, será igual a 'False'.

Se o item for adicionado corretamente ao carrinho, a API retornará sucesso (código HTTP 201), e no corpo da resposta serão retornados os dados completos do carrinho.
"""

DELETE_ITEM_CARRINHO_DESCRICAO = """
Exclui um produto específico do carrinho do cliente.   
Caso o produto excluído seja o único produto existente no carrinho, o carrinho também é excluído.  

Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.
- `codigo`: Código único do produto que será excluído.
- `cor`: Cor/modelo do produto.
- `numeracao`: Númeração do produto. 

Se o produto for excluído corretamente do carrinho, a API retornará sucesso (código HTTP 200).
"""

DELETE_CARRINHO_DESCRICAO = """
Exclui completamente o carrinho do cliente.

Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.

Se o carrinho for excluído corretamente, a API retornará sucesso (código HTTP 200).
"""

PUT_FECHA_CARRINHO_DESCRICAO = """
Gera um pedido com base no carrinho do cliente.
Exclui o carrinho do cliente.   

Para fechar um carrinho, é necessário que todas as informações do carrinho tenham sido preenchidas.

Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.  

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os dados do pedido.
"""

GET_CARRINHO_CLIENTE_DESCRICAO = """
Retorna os dados do carrinho aberto do cliente, caso exista.   

Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.  

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os dados do carrinho.
"""

GET_CARRINHOS_COM_PRODUTO_DESCRICAO = """
Retorna os carrinhos abertos que contém o produto especificado.   

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os carrinhos.
"""

GET_PRODUTOS_POPULARES_CARRINHOS_DESCRICAO = """
Retorna uma lista dos produtos que são mais frequentemente nos carrinhos abertos.   

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta será retornada a lista de produtos.
"""

GET_CARRINHOS_ABANDONADOS_DESCRICAO = """
Retorna uma lista com os carrinhos abandonados a mais tempo.   

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os carrinhos abandonados.
"""

GET_PEDIDO_POR_ID_DESCRICAO = """
Retorna os dados do pedido do cliente, de acordo com o id de pedido informado.   

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os dados do pedido.
"""

GET_PEDIDOS_CLIENTE_DESCRICAO = """
Retorna os pedidos do cliente, de acordo com o email do cliente.   

Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os pedidos do cliente.
"""