# schemas/elementvenda.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class Videojoc(BaseModel):
    genere: str
    multijugador: bool
    tempsestimat: Optional[int]

    class Config:
        orm_mode = True

class DLC(BaseModel):
    tipusdlc: str
    esgratuït: bool
    videojocbaseid: int

    class Config:
        orm_mode = True

class ElementVendaBase(BaseModel):
    nom: str
    descripcio: Optional[str]
    preu: float
    datallançament: date
    qualificacioedat: Optional[int]
    desenvolupador: str
    tipus: str  # 'videojoc' o 'dlc'

class ElementVendaCreate(ElementVendaBase):
    tipus: str  # 'videojoc' o 'dlc'

    # Para Videojoc
    genere: Optional[str]
    multijugador: Optional[bool]
    tempsestimat: Optional[int]

    # Para DLC
    tipusdlc: Optional[str]
    esgratuït: Optional[bool]
    videojocbaseid: Optional[int]

class ElementVendaUpdate(ElementVendaBase):
    pass  # Igual que base pero opcional si quieres

class ElementVenda(ElementVendaBase):
    id: int
    videojoc: Optional[Videojoc]
    dlc: Optional[DLC]

    class Config:
        orm_mode = True
