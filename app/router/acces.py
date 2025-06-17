# routers/acces.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.acces import Acces
from app.database import get_db
from app.schemas.acces import AccesCreate, AccesResponse

router = APIRouter(
    prefix="/accessos",
    tags=["Accessos"]
)

# Afegir accés (relacionar subscripció amb un joc)
@router.post("/", response_model=AccesResponse)
def afegir_acces(acces: AccesCreate, db: Session = Depends(get_db)):
    # Comprovar si ja existeix
    existent = db.query(Acces).filter_by(
        tipusSubscripcioNom=acces.tipusSubscripcioNom,
        elementVendaId=acces.elementVendaId
    ).first()
    if existent:
        raise HTTPException(status_code=400, detail="Aquest accés ja existeix")

    nou_acces = Acces(**acces.dict())
    db.add(nou_acces)
    db.commit()
    db.refresh(nou_acces)
    return nou_acces

# Eliminar accés
@router.delete("/{tipusSubscripcioNom}/{elementVendaId}", response_model=dict)
def eliminar_acces(tipusSubscripcioNom: str, elementVendaId: int, db: Session = Depends(get_db)):
    acces = db.query(Acces).filter_by(
        tipusSubscripcioNom=tipusSubscripcioNom,
        elementVendaId=elementVendaId
    ).first()

    if not acces:
        raise HTTPException(status_code=404, detail="Accés no trobat")

    db.delete(acces)
    db.commit()
    return {"missatge": "Accés eliminat correctament"}

# Obtenir jocs associats a un tipus de subscripció
@router.get("/accessos/{tipussubscripcionom}", response_model=list[AccesResponse])
def obtenir_accessos(tipussubscripcionom: str, db: Session = Depends(get_db)):
    accessos = db.query(Acces).filter_by(tipussubscripcionom=tipussubscripcionom).all()
    return accessos
