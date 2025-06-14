# routers/videojoc.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.elementvenda as crud
import app.schemas.elementvenda as schemas
from fastapi import HTTPException
from app.models.elementvenda import ElementVenda, Videojoc
from app.schemas.elementvenda import VideojocCreate, VideojocUpdate

router = APIRouter(
    prefix="/videojoc",
    tags=["Videojoc"]
)

@router.get("/{elementvenda_id}", response_model=schemas.Videojoc)
def read_videojoc(elementvenda_id: int, db: Session = Depends(get_db)):
    return crud.get_videojoc(db, elementvenda_id)



@router.post("/videojocs")
def create_videojoc(videojoc: VideojocCreate, db: Session = Depends(get_db)):
    element = ElementVenda(
        nom=videojoc.nom,
        descripcio=videojoc.descripcio,
        preu=videojoc.preu,
        datallancament=videojoc.datallancament,
        qualificacioedat=videojoc.qualificacioedat,
        desenvolupador=videojoc.desenvolupador,
        tipus="videojoc"
    )
    db.add(element)
    db.commit()
    db.refresh(element)

    new_videojoc = Videojoc(
        elementvendaid=element.id,
        genere=videojoc.genere,
        multijugador=videojoc.multijugador,
        tempsestimat=videojoc.tempsestimat
    )
    db.add(new_videojoc)
    db.commit()

    return {"message": "Videojoc creat", "id": element.id}
@router.put("/videojocs/{videojoc_id}")
def update_videojoc(videojoc_id: int, videojoc_update: VideojocUpdate, db: Session = Depends(get_db)):
    element = db.query(ElementVenda).filter_by(id=videojoc_id, tipus="videojoc").first()
    if not element:
        raise HTTPException(status_code=404, detail="Videojoc no trobat")

    videojoc = db.query(Videojoc).filter_by(elementvendaid=videojoc_id).first()

    # Actualitzar ElementVenda
    element.nom = videojoc_update.nom
    element.descripcio = videojoc_update.descripcio
    element.preu = videojoc_update.preu
    element.datallancament = videojoc_update.datallancament
    element.qualificacioedat = videojoc_update.qualificacioedat
    element.desenvolupador = videojoc_update.desenvolupador

    # Actualitzar Videojoc
    videojoc.genere = videojoc_update.genere
    videojoc.multijugador = videojoc_update.multijugador
    videojoc.tempsestimat = videojoc_update.tempsestimat

    db.commit()

    return {"message": "Videojoc actualitzat"}
