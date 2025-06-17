from datetime import datetime
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# Suposo que tens configurada la base de dades i sessió:
from app.database import get_db  # funció que retorna la sessió DB
from app.models.elementvenda import DLC, ElementVenda
from datetime import datetime

from app.models.venda import Venda
from app.schemas.venda import VendaCreate, VendaRead


router = APIRouter(
    prefix="/vendes",
    tags=["Vendes"]
)




@router.post("/", response_model=VendaRead)
def crear_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    # Comprovar si la venda ja existeix
    existing = db.query(Venda).filter(
        Venda.usuarisobrenom == venda.usuarisobrenom,
        Venda.elementvendaid == venda.elementvendaid
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="La venda ja existeix")

    # Obtenir l'element de venda
    element = db.query(ElementVenda).filter(ElementVenda.id == venda.elementvendaid).first()
    if not element:
        raise HTTPException(status_code=404, detail="L'element de venda no existeix")

    # Si l'element és un DLC, comprovar que l'usuari tingui el videojoc base
    if element.tipus.lower() == "dlc":
        dlc = db.query(DLC).filter(DLC.elementvendaid == venda.elementvendaid).first()
        if not dlc:
            raise HTTPException(status_code=404, detail="El DLC no existeix")

        # Comprovar si l'usuari té el videojoc base comprat
        videojoc_comprat = db.query(Venda).filter(
            Venda.usuarisobrenom == venda.usuarisobrenom,
            Venda.elementvendaid == dlc.videojocbaseid
        ).first()

        if not videojoc_comprat and not dlc.esgratuit:
            raise HTTPException(
                status_code=400,
                detail="Per comprar aquest DLC, has de tenir el videojoc base comprat"
            )

    # Crear la nova venda
    nova_venda = Venda(
        data=datetime.now().date(),
        preu=element.preu,
        usuarisobrenom=venda.usuarisobrenom,
        elementvendaid=venda.elementvendaid
    )

    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return nova_venda

@router.get("/", response_model=List[VendaRead])
def llistar_vendes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vendes = db.query(Venda).offset(skip).limit(limit).all()
    return vendes


@router.get("/{usuarisobrenom}/{elementvendaid}/{data}", response_model=VendaRead)
def obtenir_venda(usuarisobrenom: str, elementvendaid: int, data: str, db: Session = Depends(get_db)):
    venda = db.query(Venda).filter(
        Venda.usuarisobrenom == usuarisobrenom,
        Venda.elementvendaid == elementvendaid,
        Venda.data == data
    ).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda no trobada")
    return venda
@router.get("/usuari/{usuarisobrenom}", response_model=List[VendaRead])
def obtenir_vendes_per_usuari(
    usuarisobrenom: str, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    vendes = db.query(Venda).filter(
        Venda.usuarisobrenom == usuarisobrenom
    ).offset(skip).limit(limit).all()

    if not vendes:
        raise HTTPException(status_code=404, detail="No s'han trobat vendes per a aquest usuari")

    return vendes
