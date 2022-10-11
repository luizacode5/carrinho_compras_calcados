from fastapi import HTTPException, status
import json


async def ajusta_paginacao(numero_pagina: int, qtde_por_pagina: int):
    registros_pular = 0
    if numero_pagina > 1:
        registros_pular = (numero_pagina - 1) * qtde_por_pagina
    
    if qtde_por_pagina > 50:
        qtde_por_pagina = 50

    return registros_pular, qtde_por_pagina

async def gera_filtro_produto(codigo_produto: str, cor_produto: str, numeracao_produto: str):
    filtro = []
    if codigo_produto != None:
        filtro.append(f'"codigo": {{"$regex": "{codigo_produto}", "$options": "i"}}')
    if cor_produto != None:
        filtro.append(f'"cor": {{"$regex": "{cor_produto}", "$options": "i"}}')
    if numeracao_produto != None:
        filtro.append(f'"numeracao": {{"$regex": "{numeracao_produto}", "$options": "i"}}')
    
    string_filtro = ""
    for item_filtro in filtro:
        if item_filtro != None:
            if string_filtro == "":
                string_filtro = str(item_filtro)
            else:
                string_filtro += ", " + str(item_filtro)
    
    if string_filtro == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="É obrigatório informar pelo menos um dos filtros de produto: codigo, cor ou numeração")

    string_filtro = '{'+ f"{string_filtro}" + '}'
    filtro_produto = json.loads(string_filtro)
    
    return filtro_produto