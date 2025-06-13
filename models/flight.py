from sqlalchemy import Column, Integer, String, Date, Boolean
from models.base import Base

class Flight(Base):
    __tablename__ = "vuelos"
    id = Column(Integer, primary_key=True, index=True)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    disponible = Column(Boolean, default=True)
    asientos = Column(Integer, default=0)