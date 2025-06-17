from fastapi import FastAPI
from app.router import usuari, elementvenda, videojoc, dlc, venda, subscripcio,acces, opinio, etiqueta
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
print("Iniciando app...")


app = FastAPI()

origins= [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(usuari.router)
app.include_router(elementvenda.router)

app.include_router(videojoc.router)
app.include_router(dlc.router)
app.include_router(venda.router)
app.include_router(subscripcio.router)
app.include_router(subscripcio.routerTipusSubs)
app.include_router(acces.router)
app.include_router(opinio.router)
app.include_router(etiqueta.router)