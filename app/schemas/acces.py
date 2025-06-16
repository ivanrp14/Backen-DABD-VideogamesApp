# schemas.py

from pydantic import BaseModel

class AccesBase(BaseModel):
    tipussubscripcionom: str
    elementvendaid: int

class AccesCreate(AccesBase):
    pass

class AccesResponse(BaseModel):
    class Config:
        orm_mode = True
