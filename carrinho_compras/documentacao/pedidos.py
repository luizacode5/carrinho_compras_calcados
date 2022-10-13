GET_PEDIDO_POR_ID_DESCRICAO = """
Retorna os dados do pedido, de acordo com o id do pedido informado.   
   
Informações necessárias para processar a solicitação:   
- `id_pedido`: Id do pedido que deseja consultar.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os dados do pedido.   
"""

GET_PEDIDOS_CLIENTE_DESCRICAO = """
Retorna os pedidos do cliente, de acordo com o email informado.   
   
Informações necessárias para processar a solicitação:   
- `email_cliente`: E-mail do cliente.   
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os pedidos do cliente.   
"""

GET_PEDIDOS_COM_PRODUTO_DESCRICAO = """
Retorna os pedidos que contém o produto especificado.   
Os dados são ordenados em ordem decrescente de data de criação do pedido.   
   
Opções de filtro de dados:   
- *É obrigatório o preenchimento de pelo menos um dos filtros de produto.   
- `codigo_produto`: Código do produto.   
- `cor_produto`: Cor/modelo do produto. É case-insensitive. Filtra registros que contém o texto informado.     
- `tamanho_produto`: Número da grade do calçado.   
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.    
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta serão retornados os pedidos.   
"""

GET_PRODUTOS_MAIS_VENDIDOS_DESCRICAO = """
Retorna uma lista com a quantidade vendida de cada produto, ordenando os registros do produto mais vendido para o menos vendido.    
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta será retornada a lista de produtos, com a quantidade total de cada um.   
"""

GET_TOTAIS_PEDIDOS_POR_CLIENTE_DESCRICAO = """
Retorna uma lista com os clientes e a quantidade e o valor total de pedidos de cada um.    
   
Filtros de paginação:   
- `numero_pagina`: Número da página a ser pesquisada. É opcional. Se não for informado, traz a primeira página.   
- `qtde_por_pagina`: Quantidade de registros a serem exibidos por página.  É opcional e limitado a 50 registros.   
   
Se o processo for realizado corretamente, a API retornará sucesso (código HTTP 200), e no corpo da resposta será retornada uma lista de clientes com os totalizadores.   
"""
