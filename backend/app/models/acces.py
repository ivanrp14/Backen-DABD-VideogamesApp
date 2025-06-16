from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Acces(Base):
    __tablename__ = "acces"
    __table_args__ = {'schema': 'practica'}

    tipusSubscripcioNom = Column(String(50), ForeignKey('practica.tipussubscripcio.nom'), primary_key=True)
    elementvendaid = Column(Integer, ForeignKey('practica.elementvenda.id'), primary_key=True)

    elementvenda = relationship("ElementVenda", back_populates="acces")
    tipussubscripcio = relationship("TipusSubscripcio", back_populates="acces")
