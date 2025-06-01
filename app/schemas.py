from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class UsuariBase(BaseModel):
    nom: str
    sobrenom: str
    correuelectronic: str
    datanaixement: date

class UsuariCreate(UsuariBase):
    contrasenya: str

class Usuari(UsuariBase):
    class Config:
        orm_mode = True

class UsuariLogin(BaseModel):
    sobrenom: str
    contrasenya: str

# --- TipusSubscripcio ---
class TipusSubscripcioBase(BaseModel):
    nom: str
    descripcio: Optional[str]
    preuMensual: float

    model_config = ConfigDict(from_attributes=True)

class TipusSubscripcioCreate(TipusSubscripcioBase):
    pass

class TipusSubscripcio(TipusSubscripcioBase):
    id: int


# --- Subscripcio ---
class SubscripcioBase(BaseModel):
    dataInici: date
    dataFi: date
    usuari: str
    tipusSubscripcioId: int

    model_config = ConfigDict(from_attributes=True)

class SubscripcioCreate(SubscripcioBase):
    pass

class Subscripcio(SubscripcioBase):
    id: int


# --- ElementVenda ---
class ElementVendaBase(BaseModel):
    nom: str
    descripcio: Optional[str]
    preu: float
    dataLlançament: date
    qualificacioEdat: int
    desenvolupador: str

    model_config = ConfigDict(from_attributes=True)

class ElementVendaCreate(ElementVendaBase):
    pass

class ElementVenda(ElementVendaBase):
    id: int


# --- Videojoc ---
class VideojocBase(BaseModel):
    genere: str
    multijugador: bool
    tempsEstimat: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class VideojocCreate(VideojocBase):
    elementVendaId: int

class Videojoc(VideojocBase):
    elementVendaId: int


# --- Dlc ---
class DlcBase(BaseModel):
    tipusDlc: str
    esGratuït: bool
    videojocBaseId: int

    model_config = ConfigDict(from_attributes=True)

class DlcCreate(DlcBase):
    elementVendaId: int

class Dlc(DlcBase):
    elementVendaId: int


# --- Venda ---
class VendaBase(BaseModel):
    data: date
    preu: float
    usuariSobrenom: str
    elementVendaId: int

    model_config = ConfigDict(from_attributes=True)

class VendaCreate(VendaBase):
    pass

class Venda(VendaBase):
    pass


# --- Etiqueta ---
class EtiquetaBase(BaseModel):
    nom: str
    descripcio: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class EtiquetaCreate(EtiquetaBase):
    pass

class Etiqueta(EtiquetaBase):
    id: int


# --- EtiquetaCom ---
class EtiquetaComBase(BaseModel):
    elementVendaId: int
    etiquetaId: int
    usuari: str

    model_config = ConfigDict(from_attributes=True)

class EtiquetaComCreate(EtiquetaComBase):
    pass

class EtiquetaCom(EtiquetaComBase):
    pass


# --- Opinio ---
class OpinioBase(BaseModel):
    textOpinio: Optional[str]
    puntuacio: Optional[int]
    dataPublicacio: date

    model_config = ConfigDict(from_attributes=True)

class OpinioCreate(OpinioBase):
    usuari: str
    elementVendaId: int

class Opinio(OpinioBase):
    usuari: str
    elementVendaId: int


# --- Acces ---
class AccesBase(BaseModel):
    subscripcioId: int
    elementVendaId: int

    model_config = ConfigDict(from_attributes=True)

class AccesCreate(AccesBase):
    pass

class Acces(AccesBase):
    pass
