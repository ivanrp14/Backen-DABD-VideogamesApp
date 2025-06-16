from sqlalchemy.orm import Session
from app.models.subscripcio import Subscripcio, TipusSubscripcio
from app.schemas.subscripcio import SubscripcioCreate, TipusSubscripcioCreate

def get_tipus_subscripcio(db: Session, nom: str):
    return db.query(TipusSubscripcio).filter(TipusSubscripcio.nom == nom).first()

def get_tipus_subscripcions(db: Session):
    return db.query(TipusSubscripcio).all()

def create_tipus_subscripcio(db: Session, tipussubscripcio: TipusSubscripcioCreate):
    db_tipus_subscripcio = TipusSubscripcio(**tipussubscripcio.dict())
    db.add(db_tipus_subscripcio)
    db.commit()
    db.refresh(db_tipus_subscripcio)
    return db_tipus_subscripcio


def get_subscripcio(db: Session, subscripcio_id: int):
    return db.query(Subscripcio).filter(Subscripcio.id == subscripcio_id).first()

def get_subscripcions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Subscripcio).offset(skip).limit(limit).all()

def create_subscripcio(db: Session, subscripcio: SubscripcioCreate):
    db_subscripcio = Subscripcio(**subscripcio.dict())
    db.add(db_subscripcio)
    db.commit()
    db.refresh(db_subscripcio)
    return db_subscripcio