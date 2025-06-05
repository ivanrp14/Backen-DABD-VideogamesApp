from sqlalchemy.orm import Session
from app.models import usuari as models
from app.schemas import usuari as schemas

def get_usuari_by_sobrenom(db: Session, sobrenom: str):
    return db.query(models.Usuari).filter(models.Usuari.sobrenom == sobrenom).first()

def create_usuari(db: Session, usuari: schemas.UsuariCreate):
    db_usuari = models.Usuari(**usuari.dict())
    db.add(db_usuari)
    db.commit()
    db.refresh(db_usuari)
    return db_usuari
