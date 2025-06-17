from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.etiqueta import Etiqueta, EtiquetaCom
from app.models.elementvenda import Videojoc
from app.models.usuari import Usuari

router = APIRouter(
    prefix="/etiquetes",
    tags=["Etiquetes"]
)
 

@router.post("/", response_model=dict)
def afegir_etiqueta(videojocid: int, etiquetanom: str, usuarisobrenom: str, db: Session = Depends(get_db)):
    # Comprovar si el videojoc existeix
    videojoc = db.query(Videojoc).filter(Videojoc.elementvendaid == videojocid).first()
    if not videojoc:
        raise HTTPException(status_code=404, detail="El videojoc no existeix")

    # Comprovar si l'usuari existeix
    usuari = db.query(Usuari).filter(Usuari.sobrenom == usuarisobrenom).first()
    if not usuari:
        raise HTTPException(status_code=404, detail="L'usuari no existeix")

    # Comprovar si l’etiqueta existeix, si no, crear-la automàticament
    etiqueta = db.query(Etiqueta).filter(Etiqueta.nom == etiquetanom).first()
    if not etiqueta:
        etiqueta = Etiqueta(nom=etiquetanom, descripcio="")
        db.add(etiqueta)
        db.commit()

    # Comprovar quantes etiquetes ha posat aquest usuari per aquest videojoc
    count = db.query(EtiquetaCom).filter(
        EtiquetaCom.videojocid == videojocid,
        EtiquetaCom.usuarisobrenom == usuarisobrenom
    ).count()

    if count >= 5:
        raise HTTPException(status_code=400, detail="Has assolit el màxim de 5 etiquetes per aquest videojoc")

    # Comprovar si la combinació ja existeix
    existing = db.query(EtiquetaCom).filter(
        EtiquetaCom.videojocid == videojocid,
        EtiquetaCom.etiquetanom == etiquetanom,
        EtiquetaCom.usuarisobrenom == usuarisobrenom
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ja has posat aquesta etiqueta a aquest videojoc")

    # Crear la nova etiquetaCom
    nova_etiqueta_com = EtiquetaCom(
        videojocid=videojocid,
        etiquetanom=etiquetanom,
        usuarisobrenom=usuarisobrenom
    )

    db.add(nova_etiqueta_com)
    db.commit()

    return {"missatge": "Etiqueta afegida correctament"}


@router.get("/{videojocid}", response_model=list[str])
def obtenir_etiquetes(videojocid: int, db: Session = Depends(get_db)):
    # Comprovar si el videojoc existeix
    videojoc = db.query(Videojoc).filter(Videojoc.elementvendaid == videojocid).first()
    if not videojoc:
        raise HTTPException(status_code=404, detail="El videojoc no existeix")

    # Obtenir les etiquetes associades al videojoc
    etiquetes = db.query(EtiquetaCom.etiquetanom).filter(EtiquetaCom.videojocid == videojocid).all()

    if not etiquetes:
        raise HTTPException(status_code=404, detail="No hi ha etiquetes per aquest videojoc")

    return [etiqueta.etiquetanom for etiqueta in etiquetes]