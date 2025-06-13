from sqlalchemy import Column, Integer, String
from models.base import Base

class Pet(Base):
    __tablename__ = "mascotas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    duenio = Column(String, nullable=False)
    tipo_mascota = Column(String, nullable=False)
    raza = Column(String, nullable=False)