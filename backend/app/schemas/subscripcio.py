# app/schemas/tipus_subscripcio.py
from datetime import date
from pydantic import BaseModel
from typing import Optional


class TipusSubscripcioBase(BaseModel):
    nom: str
    descripcio: Optional[str] = None
    preumensual: float

class TipusSubscripcioCreate(TipusSubscripcioBase):
    pass

class TipusSubscripcioResponse(TipusSubscripcioBase):
    class Config:
        orm_mode = True

class SubscripcioBase(BaseModel):
    usuarisobrenom: str
    
    tipussubscripcionom: str
    

class SubscripcioCreate(SubscripcioBase):
    pass

class SubscripcioResponse(SubscripcioBase):
    id: int

    class Config:
        orm_mode = True