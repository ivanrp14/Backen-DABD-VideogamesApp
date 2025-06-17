# app/models/etiqueta.py
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Etiqueta(Base):
    __tablename__ = 'etiqueta'
    __table_args__ = {'schema': 'practica'}

    nom = Column(String(50), primary_key=True)
    descripcio = Column(Text)

    etiquetes_com = relationship('EtiquetaCom', back_populates='etiqueta')

class EtiquetaCom(Base):
    __tablename__ = 'etiquetacom'
    __table_args__ = {'schema': 'practica'}

    videojocid = Column(Integer, ForeignKey('practica.videojoc.elementvendaid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    etiquetanom = Column(String(50), ForeignKey('practica.etiqueta.nom', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    usuarisobrenom = Column(String(50), ForeignKey('practica.usuari.sobrenom', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    etiqueta = relationship('Etiqueta', back_populates='etiquetes_com')
    videojoc = relationship('Videojoc', back_populates='etiquetes_com')
    usuari = relationship('Usuari', back_populates='etiquetes_com')