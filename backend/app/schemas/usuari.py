from pydantic import BaseModel
from datetime import date

class UsuariBase(BaseModel):
    nom: str
    sobrenom: str
    correuelectronic: str
    datanaixement: date

class UsuariCreate(UsuariBase):
    contrasenya: str

class UsuariLogin(BaseModel):
    sobrenom: str
    contrasenya: str

class Usuari(UsuariBase):
    class Config:
        orm_mode = True
