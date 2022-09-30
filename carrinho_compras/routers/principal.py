from fastapi import APIRouter

rota_principal = APIRouter(
    prefix=""
)

@rota_principal.get("/")
def principal():
    return {"status": "200"}