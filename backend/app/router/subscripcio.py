from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import subscripcio as crud_tipus
from app.models.acces import Acces
from app.models.elementvenda import ElementVenda
from app.models.subscripcio import Subscripcio, TipusSubscripcio
from app.models.usuari import Usuari
from app.schemas.elementvenda import ElementVendaBase
from app.schemas.subscripcio import SubscripcioCreate, SubscripcioResponse, TipusSubscripcioCreate, TipusSubscripcioResponse
from app.database import get_db
from typing import List
from app.crud import subscripcio as crud_subs
routerTipusSubs = APIRouter(prefix="/tipus_subscripcions", tags=["Tipus Subscripcions"])
router = APIRouter(prefix="/subscripcions", tags=["Subscripcions"])

@routerTipusSubs.post("/", response_model=TipusSubscripcioResponse)
def create_tipus_subscripcio(tipus_subscripcio: TipusSubscripcioCreate, db: Session = Depends(get_db)):
    db_tipus = crud_tipus.get_tipus_subscripcio(db, tipus_subscripcio.nom)
    if db_tipus:
        raise HTTPException(status_code=400, detail="Tipus de subscripció ja existeix")
    return crud_tipus.create_tipus_subscripcio(db, tipus_subscripcio)

@routerTipusSubs.get("/", response_model=List[TipusSubscripcioResponse])
def list_tipus_subscripcions( db: Session = Depends(get_db)):
    return crud_tipus.get_tipus_subscripcions(db)

@routerTipusSubs.get("/{tipussubscripcionom}/elementsvenda", response_model=List[ElementVendaBase])
def obtenir_elements_per_subscripcio(tipussubscripcionom: str, db: Session = Depends(get_db)):

    elementvenda_ids = (
        db.query(Acces.elementvendaid)
        .filter(Acces.tipussubscripcionom == tipussubscripcionom)
        .subquery()
    )

    elements = (
        db.query(ElementVenda)
        .filter(ElementVenda.id.in_(elementvenda_ids))
        .all()
    )
    return elements


# Crear subscripció
@router.post("/", response_model=SubscripcioResponse)
def crear_subscripcio(subscripcio: SubscripcioCreate, db: Session = Depends(get_db)):
    # Comprovar que l'usuari existeix
    usuari = db.query(Usuari).filter(Usuari.sobrenom == subscripcio.usuarisobrenom).first()
    if not usuari:
        raise HTTPException(status_code=404, detail="L'usuari no existeix")

    # Comprovar que el tipus de subscripció existeix
    tipus = db.query(TipusSubscripcio).filter(TipusSubscripcio.nom == subscripcio.tipussubscripcionom).first()
    if not tipus:
        raise HTTPException(status_code=404, detail="El tipus de subscripció no existeix")

   

    # Assignar dates automàticament
    data_inici = date.today()
    data_fi = data_inici + timedelta(days=30)

    nova_subscripcio = Subscripcio(
        usuarisobrenom=subscripcio.usuarisobrenom,
        datainici=data_inici,
        datafi=data_fi,
        tipussubscripcionom=subscripcio.tipussubscripcionom,
        activa=True
    )

    db.add(nova_subscripcio)
    db.commit()
    db.refresh(nova_subscripcio)

    return nova_subscripcio

# Obtenir subscripcions d’un usuari
@router.get("/usuari/{sobrenom}", response_model=list[SubscripcioResponse])
def obtenir_subscripcions_usuari(sobrenom: str, db: Session = Depends(get_db)):
    subscripcions = db.query(Subscripcio).filter(Subscripcio.usuarisobrenom == sobrenom).all()
    return subscripcions


# Eliminar subscripció
@router.delete("/{id}")
def eliminar_subscripcio(id: int, db: Session = Depends(get_db)):
    subscripcio = db.query(Subscripcio).filter(Subscripcio.id == id).first()
    if not subscripcio:
        raise HTTPException(status_code=404, detail="Subscripció no trobada")
    db.delete(subscripcio)
    db.commit()
    return {"missatge": "Subscripció eliminada correctament"}



@router.put("/{id}/cancelar")
def cancelar_subscripcio(id: int, db: Session = Depends(get_db)):
    subscripcio = db.query(Subscripcio).filter(Subscripcio.id == id).first()

    if not subscripcio:
        raise HTTPException(status_code=404, detail="Subscripció no trobada")

    if not subscripcio.activa:
        raise HTTPException(status_code=400, detail="La subscripció ja està cancel·lada")

    subscripcio.activa = False
    db.commit()

    return {"missatge": "Subscripció cancel·lada correctament"}

from datetime import date

@router.get("/{id}/comprovar")
def comprovar_subscripcio(id: int, db: Session = Depends(get_db)):
    subscripcio = db.query(Subscripcio).filter(Subscripcio.id == id).first()

    if not subscripcio:
        raise HTTPException(status_code=404, detail="Subscripció no trobada")

    avui = date.today()
    estat_correcte = subscripcio.activa and avui <= subscripcio.datafi

    if estat_correcte:
        return {"missatge": "La subscripció està activa i correcta."}

    # Si la subscripció està malament a la base de dades, la corregim
    if subscripcio.activa and avui > subscripcio.datafi:
        subscripcio.activa = False
        db.commit()
        return {"missatge": "La subscripció estava incorrectament activa i s'ha corregit a inactiva."}

    if not subscripcio.activa and avui <= subscripcio.datafi:
        subscripcio.activa = True
        db.commit()
        return {"missatge": "La subscripció estava incorrectament inactiva i s'ha corregit a activa."}

    return {"missatge": "La subscripció està inactiva i correcta."}
