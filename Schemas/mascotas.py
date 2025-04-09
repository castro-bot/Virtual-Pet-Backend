from pydantic import BaseModel

class MascotaBase(BaseModel):
    nombre: str = "Sin Nombre"
    hambre: int = 50
    felicidad: int = 50
    tipo_animal: str
    imagen: str = ""

class MascotaCreate(MascotaBase):
    user_id: int

class MascotaUpdate(MascotaBase):
    nombre: str | None = None
    hambre: int | None = None
    felicidad: int | None = None
    tipo_animal: str | None = None
    imagen: str | None = None

class MascotaResponse(MascotaBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True