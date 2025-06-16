from fastapi import FastAPI
from app.router import usuari, elementvenda, videojoc, dlc, venda, subscripcio,acces
from app.database import engine, Base

print("Iniciando app...")

app = FastAPI()


app.include_router(usuari.router)
app.include_router(elementvenda.router)

app.include_router(videojoc.router)
app.include_router(dlc.router)
app.include_router(venda.router)
app.include_router(subscripcio.router)
app.include_router(subscripcio.routerTipusSubs)
app.include_router(acces.router)