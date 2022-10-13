POST_CARRINHO_DESCRICAO = """
Cria um carrinho para o cliente, caso o cliente não tenha carrinho aberto.   
Adiciona um produto ao carrinho. Podem ser adicionados vários produtos ao carrinho, fazendo uma requisição para cada produto.   
Substitui o produto no carrinho, caso o carrinho já possua um produto semelhante, ou seja, produto com mesmo código, cor e tamanho.   
Não permite a alteração das informações principais do carrinho, com exceção do valor do frete, que normalmente varia de acordo com as alterações realizadas nos itens.   
   
Informações principais (cabeçalho):   
- `email_cliente`: E-mail do cliente, que já deve estar previamente cadastrado.   
- `codigo`: Código do carrinho. Informação opcional.   
- `cep`: CEP do endereço de entrega do cliente. Informação opcional.  
- `forma_pagamento`: Forma de pagamento escolhida pelo cliente. Informação opcional.   
- `tipo_entrega`: Tipo de entrega escolhido pelo cliente. Informação opcional.   
- `valor_frete`: Valor do frete do carrinho. Informação opcional.   
   
Produtos:   
- `codigo`: Código do produto.   
- `cor`: Cor/modelo do produto escolhido pelo cliente.   
- `tamanho`: Número da grade do calçado selecionado pelo cliente.   
- `quantidade`: Quantidade do produto adicionada ao carrinho. Precisa ser um valor inteiro maior que zero.   
- `presente`: Informação opcional, que indica se o produto deve ser embalado para presente. Caso não informado, será igual a 'False'.   
   
Se o item for adicionado corretamente ao carrinho, a API retornará sucesso (código HTTP 201).   
"""

PUT_CARRINHO_DESCRICAO = """
Atualiza as informações do cabeçalho do carrinho.   
   
Informações do carrinho:   
- `email_cliente`: E-mail do cliente, que já deve estar previamente cadastrado.   
- `codigo`: Código do carrinho. Informação opcional.   
- `cep`: CEP do endereço de entrega do cliente. Informação opcional.   
- `forma_pagamento`: Forma de pagamento escolhida pelo cliente. Informação opcional.   
- `tipo_entrega`: Tipo de entrega escolhido pelo cliente. Informação opcional.   
- `valor_frete`: Valor do frete do carrinho. Informação opcional.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200).   
"""

DELETE_ITEM_CARRINHO_DESCRICAO = """
Exclui um produto específico do carrinho do cliente.   
Caso o produto excluído seja o único produto existente no carrinho, o carrinho também é excluído.   
   
Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.   
- `codigo`: Código do produto que será excluído.   
- `cor`: Cor/modelo do produto.   
- `tamanho`: Númeração do produto.   
   
Se o produto for excluído corretamente do carrinho, a API retornará sucesso (código HTTP 200).   
"""

DELETE_CARRINHO_DESCRICAO = """
Exclui completamente o carrinho do cliente.   
   
Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.   
   
Se o carrinho for excluído corretamente, a API retornará sucesso (código HTTP 200).   
"""

GET_CARRINHO_CLIENTE_DESCRICAO = """
Retorna os dados do carrinho aberto do cliente, caso exista.   
   
Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os dados do carrinho.   
"""

PUT_FECHA_CARRINHO_DESCRICAO = """
Gera um pedido com base no carrinho do cliente.   
Exclui o carrinho do cliente.   
   
Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente ao qual o carrinho está vinculado.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 201), e no corpo da resposta serão retornados os dados do pedido.   
"""

GET_CARRINHOS_COM_PRODUTO_DESCRICAO = """
Retorna os carrinhos abertos que contém o produto especificado.   
Os dados são ordenados em ordem decrescente de data de criação do carrinho.   
   
Opções de filtro de dados:   
- *É obrigatório o preenchimento de pelo menos um dos filtros de produto.   
- `codigo_produto`: Código do produto.   
- `cor_produto`: Cor/modelo do produto escolhido pelo cliente. É case-insensitive. Filtra registros que contém o texto informado.    
- `tamanho_produto`: Número da grade do calçado selecionado pelo cliente.   
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.    
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os carrinhos.   
"""

GET_PRODUTOS_POPULARES_CARRINHOS_DESCRICAO = """
Retorna uma lista com a soma da quantidade de cada produto que está nos carrinhos abertos.   
Os produtos são exibidos em ordem descrecente da quantidade total, de forma que é possível saber os produtos que são mais "populares", ou que estão "em alta" nos carrinhos.   
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta será retornada a lista de produtos, com a quantidade total de cada um.   
"""

GET_CARRINHOS_ABANDONADOS_DESCRICAO = """
Retorna uma lista com os carrinhos abandonados, ou seja, carrinhos que ainda não foram convertidos em vendas.   
Os dados são ordenados em ordem decrescente de data de criação do carrinho.   
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os carrinhos abandonados.   
"""
