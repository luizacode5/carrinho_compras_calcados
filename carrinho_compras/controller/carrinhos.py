from datetime import datetime
from fastapi import HTTPException, status

from carrinho_compras.schemas.carrinhos import *
from carrinho_compras.controller import clientes, produtos, excecoes
from carrinho_compras.persistence import carrinhos


def data_atual_formatada():
    return datetime.now().strftime("%d-%m-%Y %H:%M")

async def adiciona_itens_carrinho(carrinho: CarrinhoBase):

    carrinho_atualizado = CarrinhoSchema(
        email_cliente = carrinho.email_cliente,
        codigo = carrinho.codigo,
        cep = carrinho.cep,
        forma_pagamento = carrinho.forma_pagamento,
        tipo_entrega = carrinho.tipo_entrega,
        valor_frete = carrinho.valor_frete,
        data_atualizacao = data_atual_formatada(),
        valor_total = 0,
        quantidade_total = 0
    )

    dados_carrinho = await busca_carrinho_cliente(carrinho.email_cliente)

    if not dados_carrinho:
        existe_cliente = await clientes.busca_cliente_por_email(carrinho.email_cliente)
        if not existe_cliente:
            return "Não há cliente cadastrado com o e-mail informado"

        carrinho_atualizado.data_criacao_carrinho = data_atual_formatada()
        await carrinhos.insere_carrinho(carrinho_atualizado)

    else:
        carrinho_atualizado.valor_total = float(dados_carrinho.valor_total)
        carrinho_atualizado.quantidade_total = int(dados_carrinho.quantidade_total)

        resultado = await carrinhos.atualiza_carrinho(carrinho_atualizado)

    if not carrinho.itens:
        if resultado > 0:
            return {"Sucesso": "Carrinho criado/atualizado com sucesso!"}
        return {"Erro": "Não foi possível criar/atualizar o carrinho!"}

    for produto in carrinho.itens:

        produto_atualizado = CarrinhoItemSchema(
            codigo = produto.codigo,
            cor = produto.cor,
            numeracao = produto.numeracao,
            quantidade = produto.quantidade,
            presente = produto.presente,
            data_atualizacao = data_atual_formatada()
        )
        quantidade_substituida = 0
        preco_substituido = 0

        produto_disponivel = await produtos.consulta_produto_disponivel(produto_atualizado)
        if not produto_disponivel:
            # produto_atualizado.detalhes = produto_disponivel.get("detalhes")
            # produtos_nao_processados.append(produto_atualizado)
            continue
        
        produto_atualizado.preco_unitario = round(float(produto_disponivel.get("preco")), 2)
        produto_existe_carrinho = False

        if dados_carrinho and dados_carrinho.itens:

            dados_produto_carrinho = await busca_produto_carrinho(dados_carrinho.itens, produto)

            if dados_produto_carrinho != None:
                produto_existe_carrinho = True

                if produto.quantidade == dados_produto_carrinho.get("quantidade"):
                    continue
                
                resultado = await carrinhos.altera_item_carrinho(produto_atualizado, carrinho.email_cliente)

                quantidade_substituida = int(dados_produto_carrinho.get("quantidade"))
                preco_substituido = float(dados_produto_carrinho.get("quantidade")) \
                    * float(dados_produto_carrinho.get("preco_unitario"))
    
        if not produto_existe_carrinho:            
            produto_atualizado.data_criacao = data_atual_formatada()
            resultado = await carrinhos.adiciona_itens_carrinho(carrinho.email_cliente, produto_atualizado)
        
        if resultado:
            print("entrou resultado ok inserir ou atualizar prod")
            carrinho_atualizado.quantidade_total = int(carrinho_atualizado.quantidade_total) \
                + int(produto_atualizado.quantidade) \
                - quantidade_substituida
                
            carrinho_atualizado.valor_total = float(carrinho_atualizado.valor_total) \
                + float(produto_atualizado.quantidade) * float(produto_atualizado.preco_unitario) \
                - preco_substituido

            carrinho_atualizado.valor_total = round(carrinho_atualizado.valor_total, 2)
            
            resultado = await atualiza_carrinho(carrinho_atualizado)

        # if not resultado:
            # produto_atualizado.detalhes = "Não foi possível inserir/atualizar o produto no carrinho"
            # produtos_nao_processados.append(produto_atualizado)
        
    resultado = await carrinhos.busca_carrinho_cliente(carrinho.email_cliente)
    # if not resultado:
    #     raise excecoes.ObjetoNaoEncontrado

    # response = CarrinhoResponse(resultado)
    # response.produtos_nao_processados = produtos_nao_processados

    return resultado
    # return response
    



async def altera_item_carrinho(produto_carrinho: CarrinhoItemSchema):
    resultado = await carrinhos.altera_item_carrinho(produto_carrinho)
    return resultado

async def atualiza_carrinho(email_cliente: str):
    resultado = await carrinhos.atualiza_carrinho(email_cliente)
    return resultado

async def busca_carrinho_cliente(email_cliente: str):
    dados_carrinho = await carrinhos.busca_carrinho_cliente(email_cliente)
    return dados_carrinho

async def busca_pedido_por_id(id_pedido: str):
    resultado = await carrinhos.busca_pedido_por_id(id_pedido)
    return resultado

async def exclui_carrinho(email_cliente: str):
    resultado = await carrinhos.exclui_carrinho(email_cliente)
    return resultado

async def busca_produto_carrinho(produtos_carrinho: list[CarrinhoItemSchema], produto_procurado :CarrinhoItemSchema):

    for produto in produtos_carrinho:

        if produto.codigo == produto_procurado.codigo and \
            produto.cor == produto_procurado.cor and \
            produto.numeracao == produto_procurado.numeracao:

            return {
                "quantidade": int(produto.quantidade),
                "preco_unitario": float(produto.preco_unitario)
            }
    return

async def exclui_item_carrinho(dados_produto: ExclusaoProdutoRequest, email_cliente: str):

    dados_carrinho = await busca_carrinho_cliente(email_cliente)
    if not dados_carrinho:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado carrinho para o cliente")

    if not dados_carrinho.itens:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado no carrinho")
        
    dados_produto_carrinho = await busca_produto_carrinho(dados_carrinho.itens, dados_produto)

    if not dados_produto_carrinho:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado no carrinho")
        
    if len(dados_carrinho.itens) == 1:
        resultado = await exclui_carrinho(email_cliente)
        if resultado:
            return
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível excluir o produto do carrinho")
    
    valor_total = float(dados_carrinho.valor_total) \
        - float(dados_produto_carrinho.get("preco_unitario", 0)) \
        * float(dados_produto_carrinho.get("quantidade", 0))
    
    quantidade_total = float(dados_carrinho.quantidade_total) \
        - float(dados_produto_carrinho.get("quantidade", 0))

    atualiza_dados = AtualizaCarrinhoExclusaoItem(
        valor_total = round(valor_total, 2),
        quantidade_total = quantidade_total,
        data_atualizacao = data_atual_formatada(),
        email_cliente = email_cliente
    )

    resultado = await carrinhos.exclui_item_carrinho(dados_produto, email_cliente)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível excluir o produto do carrinho")

    resultado = await carrinhos.atualiza_carrinho(atualiza_dados)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível atualizar corretamente os totais do carrinho")

async def fecha_carrinho(email_cliente: str):
    dados_carrinho = await busca_carrinho_cliente(email_cliente)
    
    if not dados_carrinho:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi encontrado carrinho para o client informado")

    pedido = PedidoSchema(**dados_carrinho.dict())

    pedido.data_atualizacao = data_atual_formatada()
    pedido.data_criacao_pedido = data_atual_formatada()
    pedido.status = "Aguardando Aprovação"

    if not pedido.itens:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="O carrinho está vazio")
    
    # baixa_estoque = await produtos.baixa_estoque_pedido(dados_carrinho)
    # if not baixa_estoque:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível realizar a baixa do estoque dos produtos do carrinho")

    id_pedido = await carrinhos.insere_pedido(pedido)
    if not id_pedido:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Não foi possível gerar o pedido a partir do carrinho")

    dados_pedido = await busca_pedido_por_id(id_pedido)
    if not dados_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi possível gerar o pedido a partir do carrinho")

    await carrinhos.exclui_carrinho(email_cliente)

    return dados_pedido



async def busca_pedidos_por_cliente(email_cliente: str):
    resultado = await carrinhos.busca_pedidos_por_cliente(email_cliente)
    if resultado:
        return resultado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foram encontrados pedidos para o cliente")
    





async def busca_carrinhos_por_produto(codigo_produto: str):
    resultado = await carrinhos.busca_carrinhos_por_produto(codigo_produto)
    return resultado

async def busca_produtos_populares():
    resultado = await carrinhos.busca_produtos_populares()
    return resultado

async def busca_carrinhos_abandonados():
    resultado = await carrinhos.busca_carrinhos_abandonados()
    return resultado
