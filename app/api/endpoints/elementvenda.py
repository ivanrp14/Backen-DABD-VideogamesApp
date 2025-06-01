from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ElementVenda)
def crear_element(element: schemas.ElementVendaCreate, db: Session = Depends(get_db)):
    existent = db.query(models.ElementVenda).filter(models.ElementVenda.nom == element.nom).first()
    if existent:
        raise HTTPException(status_code=400, detail="ElementVenda ja existeix")
    db_element = models.ElementVenda(**element.model_dump())
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element

@router.get("/{id}", response_model=schemas.ElementVenda)
def llegir_element(id: int, db: Session = Depends(get_db)):
    element = db.query(models.ElementVenda).filter(models.ElementVenda.id == id).first()
    if not element:
        raise HTTPException(status_code=404, detail="ElementVenda no trobat")
    return element
