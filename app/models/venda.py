# app/models/venda.py
from sqlalchemy import Column, Date, Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuari import Usuari  # important importar abans per carregar la taula

class Venda(Base):
    __tablename__ = 'venda'
    __table_args__ = {'schema': 'practica'}

    data = Column(Date, primary_key=True, nullable=False)
    preu = Column(Float, nullable=False)
    usuarisobrenom = Column(String, ForeignKey('practica.usuari.sobrenom', onupdate="RESTRICT", ondelete="CASCADE"), primary_key=True, nullable=False)
    elementvendaid = Column(Integer, ForeignKey('practica.elementvenda.id', onupdate="RESTRICT", ondelete="CASCADE"), primary_key=True, nullable=False)

    usuari = relationship("Usuari", back_populates="vendes")
    elementvenda = relationship("ElementVenda", back_populates="vendes")
