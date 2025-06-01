from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import schemas, models
from app.database import SessionLocal
from datetime import timedelta, datetime
from app.config import SECRET_KEY, ALGORITHM


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Registro de usuario
@router.post("/register", response_model=schemas.Usuari)
def register(usuari: schemas.UsuariCreate, db: Session = Depends(get_db)):
    existent = db.query(models.Usuari).filter(models.Usuari.sobrenom == usuari.sobrenom).first()
    if existent:
        raise HTTPException(status_code=400, detail="Sobrenom ja existeix")
    db_usuari = models.Usuari(**usuari.model_dump())
    db.add(db_usuari)
    db.commit()
    db.refresh(db_usuari)
    return db_usuari

# Login
@router.post("/login")
def login(form_data: schemas.UsuariLogin, db: Session = Depends(get_db)):
    usuari = db.query(models.Usuari).filter(models.Usuari.sobrenom == form_data.sobrenom).first()
    if not usuari:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuari no trobat")
    if form_data.contrasenya != usuari.contrasenya:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contrasenya incorrecta")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": usuari.sobrenom}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Función para obtener usuario desde token
def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sobrenom: str = payload.get("sub")
        if sobrenom is None:
            raise HTTPException(status_code=401, detail="Token invàlid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invàlid")

    usuari = db.query(models.Usuari).filter(models.Usuari.sobrenom == sobrenom).first()
    if usuari is None:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

# Endpoint para obtener usuario actual desde token
@router.get("/perfil", response_model=schemas.Usuari)
def perfil(token: str = Header(...), db: Session = Depends(get_db)):
    usuari = get_current_user(token, db)
    return usuari
