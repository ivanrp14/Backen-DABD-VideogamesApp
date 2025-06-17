# models/opinio.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Opinio(Base):
    __tablename__ = "opinio"  # minúscules per consistència
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True, index=True)
    textopinio = Column(Text, nullable=False)
    puntuacio = Column(Integer, nullable=False)
    datapublicacio = Column(Date, default=datetime.date.today)

    usuarisobrenom = Column(String, ForeignKey("practica.usuari.sobrenom", onupdate="RESTRICT", ondelete="CASCADE"))
    elementvendaid = Column(Integer, ForeignKey("practica.elementvenda.id", onupdate="RESTRICT", ondelete="CASCADE"))

    usuari = relationship("Usuari", back_populates="opinions")
    elementvenda = relationship("ElementVenda", back_populates="opinions")
