from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Reservation(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))
    pet_id = Column(Integer, ForeignKey('mascotas.id'))
    flight_id = Column(Integer, ForeignKey('vuelos.id'))
    pagada = Column(Boolean, default=False)

    user = relationship("User")
    pet = relationship("Pet")
    flight = relationship("Flight")