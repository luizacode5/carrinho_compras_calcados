from fastapi import APIRouter

rota_principal = APIRouter(prefix="", tags=["Página inicial"])


@rota_principal.get(
    "/",
    summary="Rota principal da API",
    description="Esta rota pode ser utilizada para verificar a disponibilidade da API.",
)
def principal():
    return {"status": "200"}
