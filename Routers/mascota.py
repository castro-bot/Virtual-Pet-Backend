from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Config.database import get_db
from Model.mascotas import Mascota
from Model.users import User
from Schemas.mascotas import MascotaCreate, MascotaResponse, MascotaUpdate

router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)

@router.post("/{user_id}", response_model=MascotaResponse)
def create_mascota(user_id: int, mascota: MascotaCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no existe o el ID es incorrecto"
        )

    # Verificar si ya existe una mascota con el mismo nombre para este usuario
    existing_mascota = db.query(Mascota).filter(
        Mascota.user_id == user_id, Mascota.nombre == mascota.nombre
    ).first()

    if existing_mascota:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario ya tiene una mascota llamada '{mascota.nombre}'. Usa otro nombre."
        )

    # Crear la nueva mascota
    db_mascota = Mascota(
        nombre=mascota.nombre,
        hambre=mascota.hambre,
        felicidad=mascota.felicidad,
        tipo_animal=mascota.tipo_animal,
        imagen=mascota.imagen,
        user_id=user_id
    )

    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/{user_id}", response_model=list[MascotaResponse])
def get_mascota(user_id: int, db: Session = Depends(get_db)):
    mascotas = db.query(Mascota).filter(Mascota.user_id == user_id).all()
    if not mascotas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron mascotas para este usuario"
        )
    return mascotas


@router.put("/{user_id}/{mascota_id}", response_model=MascotaResponse)
def update_mascota(user_id: int, mascota_id: int, mascota_update: MascotaUpdate, db: Session = Depends(get_db)):
    # Buscar la mascota exacta del usuario
    mascota = db.query(Mascota).filter(Mascota.user_id == user_id, Mascota.id == mascota_id).first()

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada para este usuario"
        )

    # Actualizar solo los campos que se envían en la solicitud
    for field, value in mascota_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(mascota, field, value)

    try:
        db.commit()
        db.refresh(mascota)
        return mascota
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la mascota: {str(e)}"
        )


@router.delete("/{mascota_id}", status_code=status.HTTP_200_OK)
def delete_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )

    db.delete(mascota)
    db.commit()

    return {"message": f"La mascota '{mascota.nombre}' ha sido eliminada correctamente."}
