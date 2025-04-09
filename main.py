from fastapi import FastAPI
from Routers import mascota, user  # Asegúrate de que esta importación coincida con la estructura
from Config.database import Base, engine

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar enrutadores
app.include_router(user.router)
app.include_router(mascota.router)

@app.get("/")
def read_root():
    return {"message": "¡FastAPI con PostgreSQL está funcionando!"}