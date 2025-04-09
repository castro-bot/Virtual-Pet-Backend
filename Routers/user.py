from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.mascotas import Mascota
from Schemas.mascotas import MascotaResponse
from Schemas.users import LoginRequest, UserCreate, UserResponse
from Model.users import User
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"]  # Esto agrupa los endpoints bajo la categoría "users" en Swagger
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Contexto para manejar hashing de contraseñas

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está registrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Hashear la contraseña
    hashed_password = pwd_context.hash(user.psw)

    # Crear un nuevo usuario
    new_user = User(name=user.name, email=user.email, psw=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@router.post("/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    # Buscar al usuario por email
    user = db.query(User).filter(User.email == login.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )

    # Verificar la contraseña
    if not pwd_context.verify(login.psw, user.psw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )

    mascotas = db.query(Mascota).filter(Mascota.user_id == user.id).all()
    mascotas_data = [
    {
        "id": mascota.id,
        "nombre": mascota.nombre,
        "tipo_animal": mascota.tipo_animal,
        "hambre": mascota.hambre,
        "felicidad": mascota.felicidad,
        "imagen": mascota.imagen
    }
    for mascota in mascotas
]


    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "mascota": mascotas_data
    }

@router.get("/{user_id}/mascota", response_model=Optional[MascotaResponse])
def get_user_mascota(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user.mascota

@router.get("/mascotas")
def get_users_with_pets(db: Session = Depends(get_db)):
    users = db.query(User).all()

    response = []
    for user in users:
        mascotas = db.query(Mascota).filter(Mascota.user_id == user.id).all()
        user_data = {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "mascotas": [
                {
                    "id": mascota.id,
                    "nombre": mascota.nombre,
                    "tipo_animal": mascota.tipo_animal,
                    "hambre": mascota.hambre,
                    "felicidad": mascota.felicidad,
                    "imagen": mascota.imagen
                }
                for mascota in mascotas
            ]
        }
        response.append(user_data)

    return response
