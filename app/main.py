from fastapi import FastAPI
from app.router import usuari, elementvenda
from app.database import engine, Base

print("Iniciando app...")

app = FastAPI()


app.include_router(usuari.router, prefix="/api/auth", tags=["usuari"])
app.include_router(elementvenda.router, prefix="/api/vendes", tags=["venda"])

