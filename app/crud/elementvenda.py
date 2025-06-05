# crud/elementvenda.py

from sqlalchemy.orm import Session
from app.models import elementvenda as models
from app.schemas.elementvenda import ElementVendaCreate, ElementVendaUpdate

def get_element(db: Session, element_id: int):
    return db.query(models.ElementVenda).filter(models.ElementVenda.id == element_id).first()

def create_element(db: Session, element: ElementVendaCreate):
    new_element = models.ElementVenda(
        nom=element.nom,
        descripcio=element.descripcio,
        preu=element.preu,
        datallancament=element.datallancament,
        qualificacioedat=element.qualificacioedat,
        desenvolupador=element.desenvolupador,
    )
    db.add(new_element)
    db.flush()  # Para obtener el id del new_element

    if element.tipus == 'videojoc':
        videojoc = models.Videojoc(
            elementvendaid=new_element.id,
            genere=element.genere,
            multijugador=element.multijugador,
            tempsestimat=element.tempsestimat
        )
        db.add(videojoc)

    elif element.tipus == 'dlc':
        dlc = models.DLC(
            elementvendaid=new_element.id,
            tipusdlc=element.tipusdlc,
            esgratuït=element.esgratuït,
            videojocbaseid=element.videojocbaseid
        )
        db.add(dlc)
    else:
        raise ValueError("Tipus must be 'videojoc' or 'dlc'")

    db.commit()
    db.refresh(new_element)
    return new_element

def update_element(db: Session, element_id: int, element_data: ElementVendaUpdate):
    element = db.query(models.ElementVenda).filter(models.ElementVenda.id == element_id).first()
    if not element:
        return None
    for field, value in element_data.dict(exclude_unset=True).items():
        setattr(element, field, value)
    db.commit()
    db.refresh(element)
    return element

def delete_element(db: Session, element_id: int):
    element = db.query(models.ElementVenda).filter(models.ElementVenda.id == element_id).first()
    if not element:
        return False
    db.delete(element)
    db.commit()
    return True
