from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

class Joueur(Base):
    __tablename__ = 'JOUEUR'
    idJoueur = Column(Integer, primary_key=True, autoincrement=True)
    pseudo = Column(String(25), unique=True, nullable=False)
    mdp = Column(String(255), nullable=False)

    stats = relationship("Statistiques", back_populates="joueur", uselist=False)
    coups_joues = relationship("Coup", back_populates="auteur")

class Partie(Base):
    __tablename__ = 'PARTIE'
    idPartie = Column(Integer, primary_key=True, autoincrement=True)
    idJoueur1 = Column(Integer, ForeignKey('JOUEUR.idJoueur'))
    idJoueur2 = Column(Integer, ForeignKey('JOUEUR.idJoueur'))
    resultat = Column(String(50))

    historique_coups = relationship("Coup", back_populates="partie")

class Coup(Base):
    __tablename__ = 'COUP'
    idCoup = Column(Integer, primary_key=True, autoincrement=True)
    idPartie = Column(Integer, ForeignKey('PARTIE.idPartie'))
    idJoueur = Column(Integer, ForeignKey('JOUEUR.idJoueur'))
    notation = Column(String(10))
    numeroCoup = Column(Integer)
    dateHeure = Column(DateTime, default=datetime.datetime.utcnow)

    partie = relationship("Partie", back_populates="historique_coups")
    auteur = relationship("Joueur", back_populates="coups_joues")

class Statistiques(Base):
    __tablename__ = 'STATISTIQUES'
    idStat = Column(Integer, primary_key=True, autoincrement=True)
    joueurId = Column(Integer, ForeignKey('JOUEUR.idJoueur'))
    nbPartiesJouees = Column(Integer, default=0)
    nbVictoires = Column(Integer, default=0)
    nbDefaites = Column(Integer, default=0)
    nbNulles = Column(Integer, default=0)
    joueur = relationship("Joueur", back_populates="stats")

engine = create_engine('sqlite:///echecs.db')
SessionLocal = sessionmaker(bind=engine)