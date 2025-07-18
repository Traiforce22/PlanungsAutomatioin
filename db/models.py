# db/models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import time

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")  # 'user' or 'admin'

class Mitarbeiter(Base):
    __tablename__ = "mitarbeiter"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    name = Column(String, nullable=False)
    nachname = Column(String, nullable=False)
    farbe = Column(String)  # Optional: Hex color code

    urlaube = relationship("Urlaub", back_populates="mitarbeiter")
    woechentlicheschichten = relationship("WoechentlicheSchicht", back_populates="mitarbeiter", cascade="all, delete")

class Urlaub(Base):
    __tablename__ = "urlaub"

    id = Column(Integer, primary_key=True, index=True)
    mitarbeiter_id = Column(Integer, ForeignKey("mitarbeiter.id"))
    von = Column(Date)
    bis = Column(Date)
    status = Column(String) #genehmigt, offen, vergangen

    mitarbeiter = relationship("Mitarbeiter", back_populates="urlaube")
    
class WoechentlicheSchicht(Base):
    __tablename__ = "woechentliche_schicht"

    id = Column(Integer, primary_key=True, index=True)
    wochentag = Column(String, nullable=False)  # e.g. "Montag"
    von = Column(Time, nullable=False)
    bis = Column(Time, nullable=False)
    mitarbeiter_id = Column(Integer, ForeignKey("mitarbeiter.id"), nullable=False)
    mitarbeiter = relationship("Mitarbeiter", back_populates="woechentlicheschichten")
    
class Oeffnungszeiten(Base):
    __tablename__ = "oeffnungszeiten"

    id = Column(Integer, primary_key=True, index=True)
    wochentag = Column(String, nullable=False)  # e.g. Montag
    von = Column(Time, nullable=False)
    bis = Column(Time, nullable=False)

class SonderOeffnungszeiten(Base):
    __tablename__ = "sonder_oeffnungszeiten"

    id = Column(Integer, primary_key=True, index=True)
    datum = Column(Date, nullable=False, unique=True)
    von = Column(Time, nullable=False)
    bis = Column(Time, nullable=False)
    beschreibung = Column(String, nullable=True)  # Optional description for the special opening
