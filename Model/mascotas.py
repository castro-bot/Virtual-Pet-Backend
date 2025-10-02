from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, default="Sin Nombre")
    hambre = Column(Integer, default=50)
    felicidad = Column(Integer, default=50)
    tipo_animal = Column(String)
    imagen = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"))  # unique=True was removed

    user = relationship("User", back_populates="mascotas")  # "mascota" was changed to "mascotas"