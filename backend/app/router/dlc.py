# routers/dlc.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.elementvenda as crud
import app.schemas.elementvenda as schemas
from fastapi import HTTPException
from app.models.elementvenda import ElementVenda, DLC, Videojoc
from app.schemas.elementvenda import DLCCreate, DLCUpdate

router = APIRouter(
    prefix="/dlc",
    tags=["DLC"]
)

@router.get("/{elementvenda_id}", response_model=schemas.DLC)
def read_dlc(elementvenda_id: int, db: Session = Depends(get_db)):
    return crud.get_dlc(db, elementvenda_id)


@router.post("/dlcs")
def create_dlc(dlc: DLCCreate, db: Session = Depends(get_db)):
    videojoc_base = db.query(Videojoc).filter_by(elementvendaid=dlc.videojocbaseid).first()
    if not videojoc_base:
        raise HTTPException(status_code=404, detail="Videojoc base no trobat")

    element = ElementVenda(
        nom=dlc.nom,
        descripcio=dlc.descripcio,
        preu=dlc.preu,
        datallancament=dlc.datallancament,
        qualificacioedat=dlc.qualificacioedat,
        desenvolupador=dlc.desenvolupador,
        tipus="dlc"
    )
    db.add(element)
    db.commit()
    db.refresh(element)

    new_dlc = DLC(
        elementvendaid=element.id,
        tipusdlc=dlc.tipusdlc,
        esgratuit=dlc.esgratuit,
        videojocbaseid=dlc.videojocbaseid
    )
    db.add(new_dlc)
    db.commit()

    return {"message": "DLC creat", "id": element.id}

@router.put("/dlcs/{dlc_id}")
def update_dlc(dlc_id: int, dlc_update: DLCUpdate, db: Session = Depends(get_db)):
    element = db.query(ElementVenda).filter_by(id=dlc_id, tipus="dlc").first()
    if not element:
        raise HTTPException(status_code=404, detail="DLC no trobat")

    dlc = db.query(DLC).filter_by(elementvendaid=dlc_id).first()

    # Actualitzar ElementVenda
    element.nom = dlc_update.nom
    element.descripcio = dlc_update.descripcio
    element.preu = dlc_update.preu
    element.datallancament = dlc_update.datallancament
    element.qualificacioedat = dlc_update.qualificacioedat
    element.desenvolupador = dlc_update.desenvolupador

    # Actualitzar DLC
    dlc.tipusdlc = dlc_update.tipusdlc
    dlc.esgratuit = dlc_update.esgratuit
    dlc.videojocbaseid = dlc_update.videojocbaseid

    db.commit()

    return {"message": "DLC actualitzat"}



@router.get("/{videojoc_id}/dlcs", response_model=List[schemas.DLC])
def read_dlcs_of_videojoc(videojoc_id: int, db: Session = Depends(get_db)):
    dlcs = crud.get_dlcs_by_videojoc(db, videojoc_id)
    return dlcs