from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base  # asumiendo que Base está aquí

class Usuari(Base):
    __tablename__ = "usuari"
    __table_args__ = {'schema': 'practica'}

    sobrenom = Column(String, primary_key=True)
    nom = Column(String, nullable=False)
    contrasenya = Column(String, nullable=False)
    correuelectronic = Column(String, nullable=False, unique=True)
    datanaixement = Column(Date, nullable=False)

 
