from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class TipusSubscripcio(Base):
    __tablename__ = "tipussubscripcio"
    __table_args__ = {'schema': 'practica'}

    nom = Column(String, primary_key=True)
    descripcio = Column(Text)
    preumensual = Column(Numeric(10, 2))

    subscripcions = relationship("Subscripcio", back_populates="tipussubscripcio")
    acces = relationship("Acces", back_populates="tipussubscripcio", cascade="all, delete-orphan")




class Subscripcio(Base):
    __tablename__ = "subscripcio"
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuarisobrenom = Column(String, ForeignKey('practica.usuari.sobrenom', onupdate="RESTRICT", ondelete="CASCADE"))
    datainici = Column(Date, nullable=False)
    datafi = Column(Date)
    tipussubscripcionom = Column(String, ForeignKey('practica.tipussubscripcio.nom', onupdate="RESTRICT", ondelete="CASCADE"))
    activa = Column(Boolean, default=True)

    usuari = relationship("Usuari", back_populates="subscripcions")
    tipussubscripcio = relationship("TipusSubscripcio", back_populates="subscripcions")
