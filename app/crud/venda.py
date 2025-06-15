# crud/venda.py
from typing import List
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.venda import Venda
from app.schemas.venda import VendaCreate, VendaUpdate

def get_venda(db: Session, data: date, usuarisobrenom: str, elementvendaid: int) -> Venda:
    venda = db.query(Venda).filter(
        Venda.data == data,
        Venda.usuarisobrenom == usuarisobrenom,
        Venda.elementvendaid == elementvendaid
    ).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda no trobada")
    return venda

def get_vendes(db: Session, skip: int = 0, limit: int = 100) -> List[Venda]:
    return db.query(Venda).offset(skip).limit(limit).all()

def get_vendes_by_user(db: Session, usuarisobrenom: str) -> List[Venda]:
    return db.query(Venda).filter(Venda.usuarisobrenom == usuarisobrenom).all()

def create_venda(db: Session, venda: VendaCreate) -> Venda:
    db_venda = Venda(**venda.dict())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda

def update_venda(db: Session, data: date, usuarisobrenom: str, elementvendaid: int, venda_update: VendaUpdate) -> Venda:
    venda = get_venda(db, data, usuarisobrenom, elementvendaid)
    for var, value in venda_update.dict(exclude_unset=True).items():
        setattr(venda, var, value)
    db.commit()
    db.refresh(venda)
    return venda

def delete_venda(db: Session, data: date, usuarisobrenom: str, elementvendaid: int):
    venda = get_venda(db, data, usuarisobrenom, elementvendaid)
    db.delete(venda)
    db.commit()
