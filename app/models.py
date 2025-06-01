from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base



class Usuari(Base):
    __tablename__ = "usuari"  # <- minúscula
    __table_args__ = {'schema': 'practica'}

    nom = Column(String, nullable=False)
    sobrenom = Column(String, primary_key=True, index=True)
    contrasenya = Column(String, nullable=False)
    correuelectronic = Column(String, unique=True, nullable=False)
    datanaixement = Column(Date, nullable=False)

    subscripcions = relationship("Subscripcio", back_populates="usuari_rel")
    vendes = relationship("Venda", back_populates="usuari_rel")
    opinions = relationship("Opinio", back_populates="usuari_rel")


class TipusSubscripcio(Base):
    __tablename__ = "tipussubscripcio"
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    descripcio = Column(String)
    preuMensual = Column(Float, nullable=False)

    subscripcions = relationship("Subscripcio", back_populates="tipus_rel")


class Subscripcio(Base):
    __tablename__ = "subscripcio"
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True)
    dataInici = Column(Date, nullable=False)
    dataFi = Column(Date, nullable=False)
    usuari = Column(String, ForeignKey("practica.usuari.sobrenom"), nullable=False)
    tipusSubscripcioId = Column(Integer, ForeignKey("practica.tipussubscripcio.id"), nullable=False)

    usuari_rel = relationship("Usuari", back_populates="subscripcions")
    tipus_rel = relationship("TipusSubscripcio", back_populates="subscripcions")
    accesos = relationship("Acces", back_populates="subscripcio_rel")


class ElementVenda(Base):
    __tablename__ = "elementvenda"
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    descripcio = Column(String)
    preu = Column(Float, nullable=False)
    dataLlançament = Column(Date, nullable=False)
    qualificacioEdat = Column(Integer, CheckConstraint("qualificacioEdat IN (3,7,12,16,18)"), nullable=False)
    desenvolupador = Column(String, nullable=False)

    videojoc = relationship("Videojoc", uselist=False, back_populates="element_venda_rel")
    dlc = relationship("Dlc", uselist=False, back_populates="element_venda_rel")
    vendes = relationship("Venda", back_populates="element_venda_rel")
    opinions = relationship("Opinio", back_populates="element_venda_rel")
    etiquetes_com = relationship("EtiquetaCom", back_populates="element_venda_rel")
    accesos = relationship("Acces", back_populates="element_venda_rel")


class Videojoc(Base):
    __tablename__ = "videojoc"
    __table_args__ = {'schema': 'practica'}

    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), primary_key=True)
    genere = Column(String, nullable=False)
    multijugador = Column(Boolean, nullable=False)
    tempsEstimat = Column(Integer)

    element_venda_rel = relationship("ElementVenda", back_populates="videojoc")
    dlcs = relationship("Dlc", back_populates="videojoc_base_rel")


class Dlc(Base):
    __tablename__ = "dlc"
    __table_args__ = {'schema': 'practica'}

    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), primary_key=True)
    tipusDlc = Column(String, nullable=False)
    esGratuït = Column(Boolean, nullable=False)
    videojocBaseId = Column(Integer, ForeignKey("practica.videojoc.elementVendaId"), nullable=False)

    element_venda_rel = relationship("ElementVenda", back_populates="dlc")
    videojoc_base_rel = relationship("Videojoc", back_populates="dlcs")


class Venda(Base):
    __tablename__ = "venda"
    __table_args__ = (
        PrimaryKeyConstraint("usuariSobrenom", "elementVendaId", "data", name="pk_venda"),
        {'schema': 'practica'}
    )

    data = Column(Date, nullable=False)
    preu = Column(Float, nullable=False)
    usuariSobrenom = Column(String, ForeignKey("practica.usuari.sobrenom"), nullable=False)
    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id"), nullable=False)

    usuari_rel = relationship("Usuari", back_populates="vendes")
    element_venda_rel = relationship("ElementVenda", back_populates="vendes")


class Etiqueta(Base):
    __tablename__ = "etiqueta"
    __table_args__ = {'schema': 'practica'}

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    descripcio = Column(String)

    etiquetes_com = relationship("EtiquetaCom", back_populates="etiqueta_rel")


class EtiquetaCom(Base):
    __tablename__ = "etiquetacom"
    __table_args__ = (
        PrimaryKeyConstraint("elementVendaId", "etiquetaId", "usuari", name="pk_etiquetacom"),
        {'schema': 'practica'}
    )

    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), nullable=False)
    etiquetaId = Column(Integer, ForeignKey("practica.etiqueta.id", ondelete="CASCADE"), nullable=False)
    usuari = Column(String, ForeignKey("practica.usuari.sobrenom"), nullable=False)

    element_venda_rel = relationship("ElementVenda", back_populates="etiquetes_com")
    etiqueta_rel = relationship("Etiqueta", back_populates="etiquetes_com")


class Opinio(Base):
    __tablename__ = "opinio"
    __table_args__ = (
        PrimaryKeyConstraint("usuari", "elementVendaId", name="pk_opinio"),
        {'schema': 'practica'}
    )

    usuari = Column(String, ForeignKey("practica.usuari.sobrenom"), nullable=False)
    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), nullable=False)
    textOpinio = Column(String)
    puntuacio = Column(Integer, CheckConstraint("puntuacio BETWEEN 1 AND 5"))
    dataPublicacio = Column(Date, nullable=False)

    usuari_rel = relationship("Usuari", back_populates="opinions")
    element_venda_rel = relationship("ElementVenda", back_populates="opinions")


class Acces(Base):
    __tablename__ = "acces"
    __table_args__ = (
        PrimaryKeyConstraint("subscripcioId", "elementVendaId", name="pk_acces"),
        {'schema': 'practica'}
    )

    subscripcioId = Column(Integer, ForeignKey("practica.subscripcio.id", ondelete="CASCADE"), nullable=False)
    elementVendaId = Column(Integer, ForeignKey("practica.elementvenda.id", ondelete="CASCADE"), nullable=False)

    subscripcio_rel = relationship("Subscripcio", back_populates="accesos")
    element_venda_rel = relationship("ElementVenda", back_populates="accesos")


"""
    CREATE TABLE Usuari (
        nom VARCHAR NOT NULL,
        sobrenom VARCHAR PRIMARY KEY,
        contrasenya VARCHAR NOT NULL,
        correuElectronic VARCHAR UNIQUE NOT NULL,
        dataNaixement DATE NOT NULL
    );
    CREATE TABLE TipusSubscripcio (
        id INT PRIMARY KEY,
        nom VARCHAR NOT NULL,
        descripcio VARCHAR,
        preuMensual FLOAT NOT NULL
    );
    CREATE TABLE Subscripcio (
        id INT PRIMARY KEY,
        dataInici DATE NOT NULL,
        dataFi DATE NOT NULL,
        usuari VARCHAR NOT NULL REFERENCES Usuari(sobrenom),
        tipusSubscripcioId INT NOT NULL REFERENCES TipusSubscripcio(id)
    );
    CREATE TABLE ElementVenda (
        id INT PRIMARY KEY,
        nom VARCHAR NOT NULL,
        descripcio VARCHAR,
        preu FLOAT NOT NULL,
        dataLlançament DATE NOT NULL,
        qualificacioEdat INT CHECK (qualificacioEdat IN (3,7,12,16,18)),
        desenvolupador VARCHAR NOT NULL
    );
    CREATE TABLE Videojoc (
        elementVendaId INT PRIMARY KEY REFERENCES ElementVenda(id) ON DELETE CASCADE,
        genere VARCHAR NOT NULL,
        multijugador BOOLEAN NOT NULL,
        tempsEstimat INT
    );
    CREATE TABLE Dlc (
        elementVendaId INT PRIMARY KEY REFERENCES ElementVenda(id) ON DELETE CASCADE,
        tipusDlc VARCHAR NOT NULL,
        esGratuït BOOLEAN NOT NULL,
        videojocBaseId INT NOT NULL REFERENCES Videojoc(elementVendaId)
    );
    CREATE TABLE Venda (
        data DATE NOT NULL,
        preu FLOAT NOT NULL,
        usuariSobrenom VARCHAR NOT NULL REFERENCES Usuari(sobrenom),
        elementVendaId INT NOT NULL REFERENCES ElementVenda(id),
        PRIMARY KEY (usuariSobrenom, elementVendaId, data)
    );
    CREATE TABLE Etiqueta (
        id INT PRIMARY KEY,
        nom VARCHAR NOT NULL,
        descripcio VARCHAR
    );
    CREATE TABLE EtiquetaCom (
        elementVendaId INT NOT NULL REFERENCES ElementVenda(id) ON DELETE CASCADE,
        etiquetaId INT NOT NULL REFERENCES Etiqueta(id) ON DELETE CASCADE,
        usuari VARCHAR NOT NULL REFERENCES Usuari(sobrenom),
        PRIMARY KEY (elementVendaId, etiquetaId, usuari)
    );
    CREATE TABLE Opinio (
        usuari VARCHAR NOT NULL REFERENCES Usuari(sobrenom),
        elementVendaId INT NOT NULL REFERENCES ElementVenda(id) ON DELETE CASCADE,
        textOpinio VARCHAR,
        puntuacio INT CHECK (puntuacio BETWEEN 1 AND 5),
        dataPublicacio DATE NOT NULL,
        PRIMARY KEY (usuari, elementVendaId)
    );
    CREATE TABLE Acces (
        subscripcioId INT NOT NULL REFERENCES Subscripcio(id) ON DELETE CASCADE,
        elementVendaId INT NOT NULL REFERENCES ElementVenda(id) ON DELETE CASCADE,
        PRIMARY KEY (subscripcioId, elementVendaId)
    );
    """