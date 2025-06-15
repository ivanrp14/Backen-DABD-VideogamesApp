from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta, datetime
from app.database import get_db
from app.config import SECRET_KEY, ALGORITHM
import app.schemas.usuari as schemas, app.models.usuari as models, app.crud.usuari as crud

router = APIRouter(
    prefix="/auth",
    tags=["Autentication"]
)
bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=schemas.Usuari)
def register(usuari: schemas.UsuariCreate, db: Session = Depends(get_db)):
    existent = crud.get_usuari_by_sobrenom(db, usuari.sobrenom)
    if existent:
        raise HTTPException(status_code=400, detail="Sobrenom ja existeix")
    return crud.create_usuari(db, usuari)

@router.post("/login")
def login(form_data: schemas.UsuariLogin, db: Session = Depends(get_db)):
    usuari = crud.get_usuari_by_sobrenom(db, form_data.sobrenom)
    if not usuari:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuari no trobat")
    if form_data.contrasenya != usuari.contrasenya:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contrasenya incorrecta")

    access_token = create_access_token(data={"sub": usuari.sobrenom})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invàlid o expirat",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sobrenom: str = payload.get("sub")
        if sobrenom is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuari = crud.get_usuari_by_sobrenom(db, sobrenom)
    if usuari is None:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return usuari

@router.get("/get-user", response_model=schemas.Usuari)
def perfil(current_user: models.Usuari = Depends(get_current_user)):
    return current_user
