from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ElementVenda(Base):
    __tablename__ = "elementvenda"
    __table_args__ = {'schema': 'practica'}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String, nullable=False)
    descripcio = Column(String)
    preu = Column(Float, nullable=False)
    datallancament = Column(Date, nullable=False)
    qualificacioedat = Column(Integer)
    desenvolupador = Column(String, nullable=False)
    tipus = Column(String, nullable=False)

    videojoc = relationship("Videojoc", back_populates="elementvenda", uselist=False)
    dlc = relationship("DLC", back_populates="elementvenda")  # <== CORRECCIÓ: llista
    vendes = relationship("Venda", back_populates="elementvenda")

class Videojoc(Base):
    __tablename__ = "videojoc"
    __table_args__ = {'schema': 'practica'}
    elementvendaid = Column(Integer, ForeignKey("practica.elementvenda.id"), primary_key=True)
    genere = Column(String, nullable=False)
    multijugador = Column(Boolean, nullable=False)
    tempsestimat = Column(Integer)

    elementvenda = relationship("ElementVenda", back_populates="videojoc")
    dlcs = relationship("DLC", back_populates="videojoc_base")  # <== RELACIÓ AFEGIDA

class DLC(Base):
    __tablename__ = "dlc"
    __table_args__ = {'schema': 'practica'}
    elementvendaid = Column(Integer, ForeignKey("practica.elementvenda.id"), primary_key=True)
    tipusdlc = Column(String, nullable=False)
    esgratuit = Column(Boolean, nullable=False)
    videojocbaseid = Column(Integer, ForeignKey("practica.videojoc.elementvendaid"), nullable=False)

    elementvenda = relationship("ElementVenda", back_populates="dlc")
    videojoc_base = relationship("Videojoc", back_populates="dlcs")  # <== RELACIÓ CORRECTA
