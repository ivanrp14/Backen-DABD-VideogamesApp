from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from app.config import DATABASE_URL
# Cargar variables de entorno desde .env
load_dotenv()



if not DATABASE_URL:
    raise ValueError("DATABASE_URL no està definida a .env")

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
