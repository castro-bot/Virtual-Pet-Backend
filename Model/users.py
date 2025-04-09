from sqlalchemy import Column, Integer, String
from Config.database import Base
from sqlalchemy.orm import relationship

# Modelo para la tabla 'users'
class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    psw = Column(String, nullable=False) # Almacena la contraseña en formato hash

    mascotas = relationship("Mascota", back_populates="user", uselist=True)