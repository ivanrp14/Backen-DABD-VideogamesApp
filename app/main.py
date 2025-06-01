from fastapi import FastAPI
from app.api.endpoints import usuari  # asegúrate que este archivo existe y no da error al importar
from app.database import engine, Base

print("Iniciando app...")

app = FastAPI()


app.include_router(usuari.router, prefix="/api/auth", tags=["usuari"])

