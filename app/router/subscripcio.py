from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import subscripcio as crud_tipus
from app.models.acces import Acces
from app.models.elementvenda import ElementVenda
from app.models.subscripcio import Subscripcio
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

r = APIRouter()

# Crear subscripció
@router.post("/subscripcions/", response_model=SubscripcioResponse)
def crear_subscripcio(subscripcio: SubscripcioCreate, db: Session = Depends(get_db)):
    nova_subscripcio = Subscripcio(**subscripcio.dict())
    db.add(nova_subscripcio)
    db.commit()
    db.refresh(nova_subscripcio)
    return nova_subscripcio

# Obtenir subscripcions d’un usuari
@router.get("/subscripcions/usuari/{sobrenom}", response_model=list[SubscripcioResponse])
def obtenir_subscripcions_usuari(sobrenom: str, db: Session = Depends(get_db)):
    subscripcions = db.query(Subscripcio).filter(Subscripcio.usuariSobrenom == sobrenom).all()
    return subscripcions

# Eliminar subscripció
@router.delete("/subscripcions/{id}")
def eliminar_subscripcio(id: int, db: Session = Depends(get_db)):
    subscripcio = db.query(Subscripcio).filter(Subscripcio.id == id).first()
    if not subscripcio:
        raise HTTPException(status_code=404, detail="Subscripció no trobada")
    db.delete(subscripcio)
    db.commit()
    return {"missatge": "Subscripció eliminada correctament"}

# Obtenir jocs accessibles per una subscripció
@router.get("/subscripcions/{id}/jocs")
def obtenir_jocs_subscripcio(id: int, db: Session = Depends(get_db)):
    subscripcio = db.query(Subscripcio).filter(Subscripcio.id == id).first()
    if not subscripcio:
        raise HTTPException(status_code=404, detail="Subscripció no trobada")
    
    jocs = (
        db.query(ElementVenda)
        .join(Acces, Acces.elementVendaId == ElementVenda.id)
        .filter(Acces.tipusSubscripcioNom == subscripcio.tipusSubscripcioNom)
        .all()
    )
    return jocs