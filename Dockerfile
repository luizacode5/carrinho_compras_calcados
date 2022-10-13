FROM python:3.10.7-bullseye
WORKDIR /code
COPY ./requerimentos.txt /code/requerimentos.txt
RUN pip install --no-cache-dir --upgrade -r /code/requerimentos.txt
COPY ./carrinho_compras /code/carrinho_compras
CMD ["uvicorn", "carrinho_compras.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]