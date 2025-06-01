from sqlalchemy.orm import Session
from app import models, schemas

# 📌 CRUD USUARIS

def obtenir_usuari(db: Session, sobrenom: str):
    return db.query(models.Usuari).filter(models.Usuari.sobrenom == sobrenom).first()

def crear_usuari(db: Session, usuari: schemas.UsuariCreate):
    db_usuari = models.Usuari(**usuari.dict())
    db.add(db_usuari)
    db.commit()
    db.refresh(db_usuari)
    return db_usuari

def obtenir_usuaris(db: Session):
    return db.query(models.Usuari).all()


# 📌 CRUD TIPUS SUBSCRIPCIO

def obtenir_tipus_subscripcio(db: Session, id: int):
    return db.query(models.TipusSubscripcio).filter(models.TipusSubscripcio.id == id).first()

def obtenir_tots_tipus_subscripcio(db: Session):
    return db.query(models.TipusSubscripcio).all()


# 📌 CRUD SUBSCRIPCIONS

def crear_subscripcio(db: Session, subscripcio: schemas.SubscripcioCreate):
    db_subscripcio = models.Subscripcio(**subscripcio.dict())
    db.add(db_subscripcio)
    db.commit()
    db.refresh(db_subscripcio)
    return db_subscripcio


# 📌 CRUD ELEMENT VENDA

def obtenir_element_venda(db: Session, id: int):
    return db.query(models.ElementVenda).filter(models.ElementVenda.id == id).first()

def obtenir_tots_elements_venda(db: Session):
    return db.query(models.ElementVenda).all()

def crear_element_venda(db: Session, element: schemas.ElementVendaCreate):
    db_element = models.ElementVenda(**element.dict())
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element


# 📌 CRUD VIDEOJOC

def obtenir_videojoc(db: Session, id: int):
    return db.query(models.Videojoc).filter(models.Videojoc.elementVendaId == id).first()

def crear_videojoc(db: Session, videojoc: schemas.VideojocCreate):
    db_videojoc = models.Videojoc(**videojoc.dict())
    db.add(db_videojoc)
    db.commit()
    db.refresh(db_videojoc)
    return db_videojoc


# 📌 CRUD DLC

def obtenir_dlc(db: Session, id: int):
    return db.query(models.Dlc).filter(models.Dlc.elementVendaId == id).first()

def crear_dlc(db: Session, dlc: schemas.DlcCreate):
    db_dlc = models.Dlc(**dlc.dict())
    db.add(db_dlc)
    db.commit()
    db.refresh(db_dlc)
    return db_dlc


# 📌 CRUD VENDA

def crear_venda(db: Session, venda: schemas.VendaCreate):
    db_venda = models.Venda(**venda.dict())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


# 📌 CRUD ETIQUETA

def obtenir_etiquestes(db: Session):
    return db.query(models.Etiqueta).all()

def crear_etiqueta(db: Session, etiqueta: schemas.EtiquetaCreate):
    db_etiqueta = models.Etiqueta(**etiqueta.dict())
    db.add(db_etiqueta)
    db.commit()
    db.refresh(db_etiqueta)
    return db_etiqueta


# 📌 CRUD OPINIO

def crear_opinio(db: Session, opinio: schemas.OpinioCreate):
    db_opinio = models.Opinio(**opinio.dict())
    db.add(db_opinio)
    db.commit()
    db.refresh(db_opinio)
    return db_opinio


# 📌 CRUD ACCÉS

def crear_acces(db: Session, acces: schemas.AccesCreate):
    db_acces = models.Acces(**acces.dict())
    db.add(db_acces)
    db.commit()
    db.refresh(db_acces)
    return db_acces
