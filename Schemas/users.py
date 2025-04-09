from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    psw: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # Permite convertir objetos ORM a modelos Pydantic

class LoginRequest(BaseModel):
    email: str
    psw: str