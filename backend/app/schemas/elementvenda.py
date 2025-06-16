from pydantic import BaseModel
from typing import Optional
from datetime import date
class ElementVendaBase(BaseModel):
    id: int
    nom: str
    descripcio: Optional[str] = None
    preu: float
    datallancament: date
    qualificacioedat: Optional[int]
    desenvolupador: str

    class Config:
        orm_mode = True

class Videojoc(ElementVendaBase):
    genere: str
    multijugador: bool
    tempsestimat: Optional[int]

class DLC(ElementVendaBase):
    tipusdlc: str
    esgratuit: bool
    videojocbaseid: int


class VideojocCreate(BaseModel):
    nom: str
    descripcio: Optional[str] = None
    preu: float
    datallancament: date
    qualificacioedat: Optional[int]
    desenvolupador: str
    genere: str
    multijugador: bool
    tempsestimat: Optional[int]

    class Config:
        orm_mode = True

class DLCCreate(BaseModel):
    nom: str
    descripcio: Optional[str] = None
    preu: float
    datallancament: date
    qualificacioedat: Optional[int]
    desenvolupador: str
    tipusdlc: str
    esgratuit: bool
    videojocbaseid: int

    class Config:
        orm_mode = True
class DLCUpdate(BaseModel):
    nom: Optional[str] = None
    descripcio: Optional[str] = None
    preu: Optional[float] = None
    datallancament: Optional[date] = None
    qualificacioedat: Optional[int] = None
    desenvolupador: Optional[str] = None
    tipusdlc: Optional[str] = None
    esgratuit: Optional[bool] = None
    videojocbaseid: Optional[int] = None

    class Config:
        orm_mode = True
class VideojocUpdate(BaseModel):
    nom: Optional[str] = None
    descripcio: Optional[str] = None
    preu: Optional[float] = None
    datallancament: Optional[date] = None
    qualificacioedat: Optional[int] = None
    desenvolupador: Optional[str] = None
    genere: Optional[str] = None
    multijugador: Optional[bool] = None
    tempsestimat: Optional[int] = None

    class Config:
        orm_mode = True
