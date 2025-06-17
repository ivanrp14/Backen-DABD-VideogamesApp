from datetime import datetime
from sqlalchemy.orm import Session
from app.models.opinio import Opinio
from app.models.elementvenda import ElementVenda
from app.models.venda import Venda

def has_purchased_game(db: Session, usuarisobrenom: str, elementvendaid: int):
    return db.query(Venda).filter(
        Venda.usuarisobrenom == usuarisobrenom  ,
        
        Venda.elementvendaid == elementvendaid
    ).first() is not None
def create_opinio(db: Session, opinio):
    db_opinio = Opinio(
        textopinio=opinio.textopinio,
        puntuacio=opinio.puntuacio,
        usuarisobrenom=opinio.usuarisobrenom,
        elementvendaid=opinio.elementvendaid,
        datapublicacio=datetime.now().date() 
    )
    db.add(db_opinio)
    db.commit()
    db.refresh(db_opinio)
    return db_opinio

def get_opinions_by_element(db: Session, elementvenda_id: int):
    opinions = (
        db.query(Opinio)
        .join(Opinio.elementvenda)
        .filter(ElementVenda.id == elementvenda_id)
        .all()
    )
    return opinions

def delete_opinio(db: Session, opinio_id: int):
    opinio = db.query(Opinio).filter(Opinio.id == opinio_id).first()
    if opinio:
        db.delete(opinio)
        db.commit()
        return opinio
    return None
def get_opinions_by_user(db: Session, usuarisobrenom: str):
    opinions = db.query(Opinio).filter(Opinio.usuarisobrenom == usuarisobrenom).all()
    return opinions