from pydantic import BaseModel
from datetime import date
from typing import Optional

class OpinioBase(BaseModel):
    textopinio: str
    puntuacio: int
    usuarisobrenom: str
    elementvendaid: int

    class Config:
        orm_mode = True 
class OpinioCreate(OpinioBase):
    
    class Config:
        orm_mode = True
class Opinio(OpinioBase):
    id: int
    datapublicacio: date

    class Config:
        orm_mode = True
from pydantic import BaseModel
from datetime import date

class OpinioResponse(BaseModel):
    textopinio: str
    puntuacio: int
    datapublicacio: date
    usuarisobrenom: str
    videojocid: int

    class Config:
        orm_mode = True  # Importante para que Pydantic pueda leer de SQLAlchemy
