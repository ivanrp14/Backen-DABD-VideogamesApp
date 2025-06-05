from sqlalchemy import Column, Float, Integer, String, Date, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ElementVenda(Base):
    __tablename__ = "elementvenda"
    __table_args__ = (
        CheckConstraint("qualificacioedat IN (3, 7, 12, 16, 18)", name="qualificacioedat_check"),
        {'schema': 'practica'}
    )

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    descripcio = Column(String)
    preu = Column(Float, nullable=False)
    datallançament = Column(Date, nullable=False)
    qualificacioedat = Column(Integer)
    desenvolupador = Column(String, nullable=False)
    tipus = Column(String, nullable=False)

    dlc = relationship("DLC", back_populates="elementvenda", uselist=False, cascade="all, delete-orphan")
    videojoc = relationship("Videojoc", back_populates="elementvenda", uselist=False, cascade="all, delete-orphan")


class Videojoc(Base):
    __tablename__ = "videojoc"
    __table_args__ = (
        CheckConstraint(
            "genere IN ('Acció', 'Aventura', 'Estratègia', 'Simulació', 'Rol', 'Tir', 'Esports')",
            name="videojoc_genere_check"
        ),
        {'schema': 'practica'}
    )

    elementvendaid = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), primary_key=True)
    genere = Column(String, nullable=False)
    multijugador = Column(Boolean, nullable=False)
    tempsestimat = Column(Integer)

    elementvenda = relationship("ElementVenda", back_populates="videojoc")
    dlcs = relationship("DLC", back_populates="videojocbase", cascade="all, delete-orphan")


class DLC(Base):
    __tablename__ = "dlc"
    __table_args__ = {'schema': 'practica'}

    elementvendaid = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), primary_key=True)
    tipusdlc = Column(String, nullable=False)
    esgratuït = Column(Boolean, nullable=False)
    videojocbaseid = Column(Integer, ForeignKey("practica.videojoc.elementvendaid", ondelete="RESTRICT"), nullable=False)

    elementvenda = relationship("ElementVenda", back_populates="dlc")
    videojocbase = relationship("Videojoc", back_populates="dlcs")
