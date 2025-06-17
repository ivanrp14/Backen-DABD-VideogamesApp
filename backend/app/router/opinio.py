from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.opinio as crud
import app.schemas.opinio as schemas
from app.models.venda import Venda
from app.models.elementvenda import ElementVenda

router = APIRouter(
    prefix="/opinions",
    tags=["opinions"]
)

@router.post("/", response_model=schemas.Opinio)
def create_opinio(opinio: schemas.OpinioCreate, db: Session = Depends(get_db)):
    has_purchased = crud.has_purchased_game(db, opinio.usuarisobrenom, opinio.elementvendaid)
    if not has_purchased:
        raise HTTPException(status_code=403, detail="User has not purchased this game")

    return crud.create_opinio(db=db, opinio=opinio)

@router.get("/element/{elementvenda_id}", response_model=list[schemas.Opinio])
def read_opinions_by_videojoc(elementvenda_id: int, db: Session = Depends(get_db)):
    opinions = crud.get_opinions_by_element(db, elementvenda_id=elementvenda_id)
    if not opinions:
        raise HTTPException(status_code=404, detail="No opinions found for this videojoc")
    return opinions

@router.delete("/{opinio_id}", response_model=schemas.OpinioCreate)
def delete_opinio(opinio_id: int, db: Session = Depends(get_db)):
    opinio = crud.delete_opinio(db, opinio_id=opinio_id)
    if opinio is None:
        raise HTTPException(status_code=404, detail="Opinio not found")
    return opinio


@router.get("/user/{usuarisobrenom}", response_model=list[schemas.Opinio])
def read_opinions_by_user(usuarisobrenom: str, db: Session = Depends(get_db)):
    opinions = crud.get_opinions_by_user(db, usuarisobrenom=usuarisobrenom)
    if not opinions:
        raise HTTPException(status_code=404, detail="No opinions found for this user")
    return opinions