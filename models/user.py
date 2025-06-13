from sqlalchemy import Column, Integer, String
from models.base import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    documento = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)