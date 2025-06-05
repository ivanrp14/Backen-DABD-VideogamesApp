from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.schemas.elementvenda import ElementVendaCreate, ElementVendaUpdate
from app.crud.elementvenda import get_element, create_element, update_element, delete_element
from app.models import elementvenda as models

router = APIRouter(prefix="/elements", tags=["elements"])

# GET by id
@router.get("/{element_id}")
def read_element(element_id: int, db: Session = Depends(get_db)):
    element = db.query(models.ElementVenda).options(
        joinedload(models.ElementVenda.videojoc),
        joinedload(models.ElementVenda.dlc)
    ).filter(models.ElementVenda.id == element_id).first()

    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    result = {
        "id": element.id,
        "nom": element.nom,
        "descripcio": element.descripcio,
        "preu": element.preu,
        "datallançament": element.datallançament,
        "qualificacioedat": element.qualificacioedat,
        "desenvolupador": element.desenvolupador,
        "tipus": element.tipus
    }

    if element.tipus == "videojoc" and element.videojoc:
        result.update({
            "genere": element.videojoc.genere,
            "multijugador": element.videojoc.multijugador,
            "tempsestimat": element.videojoc.tempsestimat
        })

    elif element.tipus == "dlc" and element.dlc:
        result.update({
            "tipusdlc": element.dlc.tipusdlc,
            "esgratuït": element.dlc.esgratuït,
            "videojocbaseid": element.dlc.videojocbaseid
        })

    return result


# POST
@router.post("/")
def create_new_element(element: ElementVendaCreate, db: Session = Depends(get_db)):
    try:
        new_element = create_element(db, element)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = {
        "id": new_element.id,
        "nom": new_element.nom,
        "descripcio": new_element.descripcio,
        "preu": new_element.preu,
        "datallançament": new_element.datallançament,
        "qualificacioedat": new_element.qualificacioedat,
        "desenvolupador": new_element.desenvolupador,
        "tipus": new_element.tipus
    }

    if new_element.tipus == "videojoc" and new_element.videojoc:
        result.update({
            "genere": new_element.videojoc.genere,
            "multijugador": new_element.videojoc.multijugador,
            "tempsestimat": new_element.videojoc.tempsestimat
        })

    elif new_element.tipus == "dlc" and new_element.dlc:
        result.update({
            "tipusdlc": new_element.dlc.tipusdlc,
            "esgratuït": new_element.dlc.esgratuït,
            "videojocbaseid": new_element.dlc.videojocbaseid
        })

    return result


# PUT
@router.put("/{element_id}")
def update_existing_element(element_id: int, element_data: ElementVendaUpdate, db: Session = Depends(get_db)):
    element = update_element(db, element_id, element_data)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    result = {
        "id": element.id,
        "nom": element.nom,
        "descripcio": element.descripcio,
        "preu": element.preu,
        "datallançament": element.datallançament,
        "qualificacioedat": element.qualificacioedat,
        "desenvolupador": element.desenvolupador,
        "tipus": element.tipus
    }

    if element.tipus == "videojoc" and element.videojoc:
        result.update({
            "genere": element.videojoc.genere,
            "multijugador": element.videojoc.multijugador,
            "tempsestimat": element.videojoc.tempsestimat
        })

    elif element.tipus == "dlc" and element.dlc:
        result.update({
            "tipusdlc": element.dlc.tipusdlc,
            "esgratuït": element.dlc.esgratuït,
            "videojocbaseid": element.dlc.videojocbaseid
        })

    return result


# DELETE
@router.delete("/{element_id}", status_code=204)
def delete_existing_element(element_id: int, db: Session = Depends(get_db)):
    success = delete_element(db, element_id)
    if not success:
        raise HTTPException(status_code=404, detail="Element not found")
    return None
