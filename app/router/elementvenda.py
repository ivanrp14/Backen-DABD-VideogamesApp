from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.acces import Acces
from app.models.elementvenda import ElementVenda
from app.models.subscripcio import Subscripcio
from app.models.venda import Venda


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/by-date")
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
@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    element = db.query(ElementVenda).filter_by(id=product_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Producte no trobat")

    db.delete(element)
    db.commit()

    return {"message": f"Producte {element.tipus} eliminat correctament"}

@router.get("/user/{usuarisobrenom}/accessos")
def get_products_user_access(
    usuarisobrenom: str,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1)
):
    offset = (page - 1) * page_size

    # 👉 1. Comprovar si l’usuari té subscripció activa
    subscripcio = db.query(Subscripcio).filter(
        Subscripcio.usuarisobrenom == usuarisobrenom,
        Subscripcio.activa == True
    ).first()

    accessos_subscripcio_ids = []

    if subscripcio:
        # 👉 2. Agafar tots els elementvendaid que dona accés aquest tipus de subscripció
        accessos_subscripcio_ids = db.query(Acces.elementvendaid).filter(
            Acces.tipussubscripcionom == subscripcio.tipussubscripcionom
        ).all()

        # 👉 Convertir de llista de tuples a llista plana d'IDs
        accessos_subscripcio_ids = [id[0] for id in accessos_subscripcio_ids]

    # 👉 3. Agafar IDs de productes comprats directament per l'usuari
    compres_ids = db.query(Venda.elementvendaid).filter(
        Venda.usuarisobrenom == usuarisobrenom
    ).all()
    compres_ids = [id[0] for id in compres_ids]

    # 👉 4. Unir tots els IDs (compres + accessos subscripció) sense duplicats
    total_ids = list(set(compres_ids + accessos_subscripcio_ids))

    if not total_ids:
        return {
            "page": page,
            "page_size": page_size,
            "products": []
        }

    # 👉 5. Consultar els productes corresponents
    products = (
        db.query(ElementVenda)
        .filter(ElementVenda.id.in_(total_ids))
        .filter(ElementVenda.tipus.in_(["videojoc", "dlc"]))
        .order_by(ElementVenda.datallancament.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # 👉 6. Format resposta
    response = [{
        "id": p.id,
        "nom": p.nom,
        "descripcio": p.descripcio,
        "preu": p.preu,
        "datallancament": p.datallancament,
        "qualificacioedat": p.qualificacioedat,
        "desenvolupador": p.desenvolupador,
        "tipus": p.tipus,
    } for p in products]

    return {
        "page": page,
        "page_size": page_size,
        "products": response
    }