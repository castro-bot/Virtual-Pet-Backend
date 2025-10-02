from sqlalchemy import Column, Integer, String
from Config.database import Base
from sqlalchemy.orm import relationship

# Model for the 'users' table
class User(Base):
    __tablename__ = "users"  # Table name in the database
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    psw = Column(String, nullable=False) # Stores the password in hash format

    mascotas = relationship("Mascota", back_populates="user", uselist=True)