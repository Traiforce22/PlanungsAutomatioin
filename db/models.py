# db/models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Mitarbeiter(Base):
    __tablename__ = "mitarbeiter"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    name = Column(String, nullable=False)
    farbe = Column(String)  # Optional: Hex color code

    urlaube = relationship("Urlaub", back_populates="mitarbeiter")


class Urlaub(Base):
    __tablename__ = "urlaub"

    id = Column(Integer, primary_key=True, index=True)
    mitarbeiter_id = Column(Integer, ForeignKey("mitarbeiter.id"))
    von = Column(Date)
    bis = Column(Date)
    status = Column(String)

    mitarbeiter = relationship("Mitarbeiter", back_populates="urlaube")
