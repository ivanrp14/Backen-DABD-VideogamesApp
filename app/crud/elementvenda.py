# crud/elementvenda.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.elementvenda import ElementVenda, Videojoc, DLC 
from app.schemas.elementvenda import ElementVendaBase

def get_videojoc(db: Session, elementvenda_id: int):
    element = db.query(ElementVenda).filter(ElementVenda.id == elementvenda_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element no trobat")
    if element.tipus != "videojoc":
        raise HTTPException(status_code=400, detail="L'element no és un videojoc")
    
    videojoc = db.query(Videojoc).filter(Videojoc.elementvendaid == elementvenda_id).first()
    return {"id": element.id, "nom": element.nom, "descripcio": element.descripcio, "preu": element.preu,
            "datallancament": element.datallancament, "qualificacioedat": element.qualificacioedat,
            "desenvolupador": element.desenvolupador,
            "genere": videojoc.genere, "multijugador": videojoc.multijugador, "tempsestimat": videojoc.tempsestimat}

def get_dlc(db: Session, elementvenda_id: int):
    element = db.query(ElementVenda).filter(ElementVenda.id == elementvenda_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element no trobat")
    if element.tipus != "dlc":
        raise HTTPException(status_code=400, detail="L'element no és un DLC")
    
    dlc = db.query(DLC).filter(DLC.elementvendaid == elementvenda_id).first()
    return {"id": element.id, "nom": element.nom, "descripcio": element.descripcio, "preu": element.preu,
            "datallancament": element.datallancament, "qualificacioedat": element.qualificacioedat,
            "desenvolupador": element.desenvolupador,
            "tipusdlc": dlc.tipusdlc, "esgratuit": dlc.esgratuit, "videojocbaseid": dlc.videojocbaseid}
def filter_videojocs(db: Session, genere: Optional[str] = None, preu_min: Optional[float] = None, preu_max: Optional[float] = None) -> List[dict]:
    query = db.query(ElementVenda, Videojoc).join(Videojoc, Videojoc.elementvendaid == ElementVenda.id).filter(ElementVenda.tipus == "videojoc")

    if genere:
        query = query.filter(Videojoc.genere == genere)
    if preu_min is not None:
        query = query.filter(ElementVenda.preu >= preu_min)
    if preu_max is not None:
        query = query.filter(ElementVenda.preu <= preu_max)

    results = query.all()

    # Retornem llistat amb la info completa combinada d'ElementVenda i Videojoc
    videojocs = []
    for element, videojoc in results:
        videojocs.append({
            "id": element.id,
            "nom": element.nom,
            "descripcio": element.descripcio,
            "preu": element.preu,
            "datallancament": element.datallancament,
            "qualificacioedat": element.qualificacioedat,
            "desenvolupador": element.desenvolupador,
            "genere": videojoc.genere,
            "multijugador": videojoc.multijugador,
            "tempsestimat": videojoc.tempsestimat
        })
    return videojocs