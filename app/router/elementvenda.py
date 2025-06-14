from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.elementvenda import ElementVenda


router = APIRouter(prefix="/elements", tags=["elements"])


@router.get("/products-by-date")
def get_products_by_date(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size

    products = (
        db.query(ElementVenda)
        .filter(ElementVenda.tipus.in_(["videojoc", "dlc"]))
        .order_by(ElementVenda.datallancament.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    response = []
    for product in products:
        response.append({
            "id": product.id,
            "nom": product.nom,
            "descripcio": product.descripcio,
            "preu": product.preu,
            "datallancament": product.datallancament,
            "qualificacioedat": product.qualificacioedat,
            "desenvolupador": product.desenvolupador,
            "tipus": product.tipus
        })

    return {
        "page": page,
        "page_size": page_size,
        "products": response
    }
@router.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    element = db.query(ElementVenda).filter_by(id=product_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Producte no trobat")

    db.delete(element)
    db.commit()

    return {"message": f"Producte {element.tipus} eliminat correctament"}
