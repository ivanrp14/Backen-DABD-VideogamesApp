from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Venda(Base):
    __tablename__ = "venda"
    __table_args__ = {'schema': 'practica'}

    data = Column(Date, primary_key=True, nullable=False)
    preu = Column(Float, nullable=False)
    usuarisobrenom = Column(String, ForeignKey("usuari.sobrenom"), primary_key=True, nullable=False)
    elementvendaid = Column(Integer, ForeignKey("elementvenda.id"), primary_key=True, nullable=False)

    # Relaciones
    usuari = relationship("Usuari", back_populates="vendes")
    elementvenda = relationship("ElementVenda", back_populates="vendes")
