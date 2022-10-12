from datetime import datetime
from fastapi import HTTPException, status

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.schemas.pedidos import *
from carrinho_compras.schemas.produtos import *
from carrinho_compras.controller import pedidos, uteis
from carrinho_compras.persistence import carrinhos
from carrinho_compras.persistence.clientes import AdaptadorCliente
from carrinho_compras.persistence.produtos import AdaptadorProduto


async def adiciona_itens_carrinho(carrinho: CarrinhoRequest) -> CarrinhoCompleto:

    produto = AdaptadorProduto()

    if carrinho.produto:
        dados_produto = await produto.pega_codigo_cor_tamanho(
            carrinho.produto.codigo,
            carrinho.produto.cor,
            carrinho.produto.tamanho
            )
        if not dados_produto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não foi encontrado o cadastro deste produto na base de dados")
        dados_produto = Produto(**dados_produto)
        if dados_produto.estoque < carrinho.produto.quantidade:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail="O produto não possui a quantidade solicitada em estoque")    

    dados_carrinho = await busca_carrinho_cliente(carrinho.email_cliente)

    if not dados_carrinho:
        adaptador = AdaptadorCliente()
        existe_cliente = await adaptador.pega(carrinho.email_cliente)
        if not existe_cliente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não há cliente cadastrado com o e-mail informado")
    
    carrinho_atualizado = CarrinhoAtualizacao(
        email_cliente = carrinho.email_cliente,
        codigo = carrinho.codigo,
        cep = carrinho.cep,
        forma_pagamento = carrinho.forma_pagamento,
        tipo_entrega = carrinho.tipo_entrega,
        valor_frete = carrinho.valor_frete,
        data_atualizacao = datetime.now(),
        valor_total = 0.0,
        quantidade_total = 0
    )
    
    if not carrinho.produto and not dados_carrinho:
        carrinho_atualizado.data_criacao_carrinho = datetime.now()
        await carrinhos.insere_carrinho(carrinho_atualizado)
        return
    
    if not carrinho.produto and dados_carrinho:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail="Já existe um carrinho para este cliente")
    
    valor_total = round(carrinho.produto.quantidade \
                * float(dados_produto.preco) \
                + carrinho.valor_frete, 2)

    produto_atualizado = CarrinhoItemSchema(
        sku = dados_produto.sku,
        codigo = carrinho.produto.codigo,
        cor = carrinho.produto.cor,
        tamanho = carrinho.produto.tamanho,
        quantidade = carrinho.produto.quantidade,
        presente = carrinho.produto.presente,
        data_atualizacao = datetime.now(),
        preco_unitario = round(float(dados_produto.preco), 2)
    )

    carrinho_atualizado.quantidade_total = carrinho.produto.quantidade
    carrinho_atualizado.valor_total = valor_total
    carrinho_atualizado.produto = produto_atualizado

    if not dados_carrinho:
        carrinho_atualizado.data_criacao_carrinho = datetime.now()
        carrinho_atualizado.produto.data_criacao = datetime.now()
        await carrinhos.insere_carrinho(carrinho_atualizado)
        return
        
    if dados_carrinho.produtos:
        carrinho_atualizado.valor_total = round(carrinho_atualizado.valor_total \
                                        + dados_carrinho.valor_total \
                                        - dados_carrinho.valor_frete, 2)
        carrinho_atualizado.quantidade_total += dados_carrinho.quantidade_total
        
        dados_produto_carrinho = await busca_produto_carrinho(dados_carrinho.produtos, produto_atualizado)

        if dados_produto_carrinho:
            carrinho_atualizado.valor_total = round(carrinho_atualizado.valor_total \
                                            - dados_produto_carrinho.quantidade \
                                            * dados_produto_carrinho.preco_unitario, 2)
            carrinho_atualizado.quantidade_total -= dados_produto_carrinho.quantidade

            await carrinhos.atualiza_produto_carrinho(carrinho_atualizado)
            return
    
    carrinho_atualizado.produto.data_criacao = datetime.now()
    await carrinhos.insere_produto_carrinho(carrinho_atualizado)

async def atualiza_carrinho(carrinho: CarrinhoRequest) -> CarrinhoCompleto:
    dados_carrinho = await busca_carrinho_cliente(carrinho.email_cliente)
    if not dados_carrinho:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não foi encontrado carrinho para o cliente informado")
 
    carrinho_atualizado = CarrinhoAtualizacao(
        email_cliente = carrinho.email_cliente,
        codigo = carrinho.codigo,
        cep = carrinho.cep,
        forma_pagamento = carrinho.forma_pagamento,
        tipo_entrega = carrinho.tipo_entrega,
        valor_frete = carrinho.valor_frete,
        data_atualizacao = datetime.now()
    )

    if carrinho.valor_frete != dados_carrinho.valor_frete:
        carrinho_atualizado.valor_total = round(dados_carrinho.valor_total \
                                        + carrinho.valor_frete \
                                        - dados_carrinho.valor_frete, 2)

    await carrinhos.atualiza_carrinho(carrinho_atualizado)

    dados_carrinho = await busca_carrinho_cliente(carrinho.email_cliente)
    return dados_carrinho

async def busca_carrinho_cliente(email_cliente: EmailStr) -> CarrinhoCompleto:
    dados_carrinho = await carrinhos.busca_carrinho_cliente(email_cliente)
    return dados_carrinho

async def exclui_carrinho(email_cliente: EmailStr):
    resultado = await carrinhos.exclui_carrinho(email_cliente)
    if resultado:
        return {"detail": "Carrinho excluído com sucesso"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail="O cliente não possui carrinho aberto")

async def busca_produto_carrinho(
    produtos_carrinho: list[CarrinhoItemSchema], 
    produto_procurado: CarrinhoItemSchema):

    for produto in produtos_carrinho:
        if produto.codigo == produto_procurado.codigo and \
            produto.cor == produto_procurado.cor and \
            produto.tamanho == produto_procurado.tamanho:

            return produto
    return

async def exclui_item_carrinho(
    produto_excluir: ExclusaoProdutoRequest, 
    email_cliente: EmailStr
    ):

    dados_carrinho = await busca_carrinho_cliente(email_cliente)
    if not dados_carrinho:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não foi encontrado carrinho para o cliente")

    if not dados_carrinho.produtos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Produto não encontrado no carrinho")
    
    dados_produto_carrinho = await busca_produto_carrinho(
        dados_carrinho.produtos, 
        produto_excluir
        )

    if not dados_produto_carrinho:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Produto não encontrado no carrinho")
        
    if len(dados_carrinho.produtos) == 1:
        resultado = await exclui_carrinho(email_cliente)
    
    else:
        valor_total = round(dados_carrinho.valor_total \
                    - dados_produto_carrinho.preco_unitario \
                    * dados_produto_carrinho.quantidade, 2)
        
        quantidade_total = dados_carrinho.quantidade_total \
                         - dados_produto_carrinho.quantidade

        carrinho_atualizar = CarrinhoAtualizacao(
            email_cliente = email_cliente,
            valor_total = valor_total,
            quantidade_total = quantidade_total,
            data_atualizacao = datetime.now(),
            produto = produto_excluir
        )
        resultado = await carrinhos.exclui_item_carrinho(carrinho_atualizar)

    if resultado:
        return {"detail": "Produto excluído do carrinho com sucesso"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Não foi possível excluir o produto do carrinho")

async def fecha_carrinho(email_cliente: EmailStr) -> PedidoSchema:
    dados_carrinho = await busca_carrinho_cliente(email_cliente)
    
    if not dados_carrinho:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não foi encontrado carrinho para o cliente informado")

    if not dados_carrinho.produtos:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="O carrinho está vazio")

    pedido = PedidoSchema(**dados_carrinho.dict())

    pedido.data_atualizacao = datetime.now()
    pedido.data_criacao_pedido = datetime.now()
    pedido.status = "Pedido Recebido"

    # baixa_estoque = await produtos.baixa_estoque_pedido(dados_carrinho)
    # if not baixa_estoque:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
    #   detail="Não foi possível realizar a baixa do estoque dos produtos do carrinho")

    id_pedido = await pedidos.insere_pedido(pedido)
    await carrinhos.exclui_carrinho(email_cliente)
    dados_pedido = await pedidos.busca_pedido_por_id(id_pedido)
    return dados_pedido

async def busca_carrinhos_por_produto(
    codigo_produto: str,
    cor_produto: str,
    tamanho_produto: int,
    numero_pagina: int,
    qtde_por_pagina: int) -> ListaCarrinhos:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, 
        qtde_por_pagina
        )
    
    filtro_produto = await uteis.gera_filtro_produto(codigo_produto, cor_produto, tamanho_produto)

    resultado = await carrinhos.busca_carrinhos_por_produto(
        filtro_produto,
        registros_pular, 
        qtde_por_pagina
        )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina

    if resultado:
        return resultado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="Não foram encontrados carrinhos com o produto")

async def busca_produtos_populares(
    numero_pagina: int, 
    qtde_por_pagina: int
    ) -> ProdutosPopulares:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, 
        qtde_por_pagina
        )

    resultado = await carrinhos.busca_produtos_populares(
        registros_pular, 
        qtde_por_pagina
        )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina
    
    if resultado:
        return resultado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="Não foram encontrados registros para os parâmetros especificados")

async def busca_carrinhos_abandonados(
    numero_pagina: int, 
    qtde_por_pagina: int
    ) -> ListaCarrinhos:

    registros_pular, qtde_por_pagina = await uteis.ajusta_paginacao(
        numero_pagina, 
        qtde_por_pagina)

    resultado = await carrinhos.busca_carrinhos_abandonados(
        registros_pular, 
        qtde_por_pagina
        )
    if numero_pagina == 0:
        numero_pagina = 1
    resultado.numero_pagina = numero_pagina
    resultado.qtde_por_pagina = qtde_por_pagina

    if resultado:
        return resultado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="Não foram encontrados registros para os parâmetros especificados")
