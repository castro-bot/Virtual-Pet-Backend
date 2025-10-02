from fastapi import FastAPI
from Routers import mascota, user  # Asegúrate de que esta importación coincida con la estructura
from Config.database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(user.router)
app.include_router(mascota.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is running!"}