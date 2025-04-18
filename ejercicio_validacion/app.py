from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr, Field
from typing import List
import uvicorn

app = FastAPI()

# Esquema base sin el campo `id`
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="El nombre debe tener entre 3 y 50 caracteres")
    email: EmailStr = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="El correo electrónico debe ser válido")
    age: int = Field(..., gt=0, description="La edad debe ser mayor a 0")

# Esquema para respuestas y operaciones `GET` (incluye `id`)
class UserResponse(UserBase):
    id: int

    def update_userbase(self, user: UserBase):
        self.name = user.name
        self.email = user.email
        self.age = user.age

fake_db: List[UserResponse] = [
     UserResponse(id=1, name="Alice Smith", email="alice.smith@example.com", age=30),
     UserResponse(id=2, name="Bob Johnson", email="bob.johnson@example.com", age=25),
     UserResponse(id=3, name="Charlie Brown", email="charlie.brown@example.com", age=35),
     UserResponse(id=4, name="Diana Prince", email="diana.prince@example.com", age=28),
     UserResponse(id=5, name="Ethan Hunt", email="ethan.hunt@example.com", age=40),
]

# Variable global para el último ID usado
last_id = max(user.id for user in fake_db)

# Crear un usuario
@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserBase):
     global last_id
     for existing_user in fake_db:
          if existing_user.email == user.email:
                raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
     last_id += 1
     user.id = last_id
     fake_db.append(user)
     return user

# Leer todos los usuarios
@app.get("/users/", response_model=List[UserResponse])
async def read_users():
     return fake_db

# Leer un usuario por ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
     for user in fake_db:
          if user.id == user_id:
                return user
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Actualizar un usuario
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, updated_user: UserBase):
     for index, user in enumerate(fake_db):
          if user.id == user_id:
                #fake_db[index].update_userbase(updated_user)
                #return fake_db[index]
                response = UserResponse(id=user_id, **updated_user.model_dump())
                fake_db[index] = response
                return response
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Eliminar un usuario
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
     for index, user in enumerate(fake_db):
          if user.id == user_id:
                del fake_db[index]
                return
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/userssss/{name}", response_model=UserResponse)
async def get_user(
     name: str = Path(
          ..., 
          pattern="^[a-zA-Z0-9_\\s-]{3,16}$", 
          title="Nombre de usuario",
          description="Debe contener entre 3 y 16 caracteres, y solo puede incluir letras, números, guiones bajos o guiones."
     )
     ):
     """
     Validación del parámetro de ruta `username`:
     - Debe tener entre 3 y 16 caracteres.
     - Solo puede contener letras, números, guiones bajos (_) o guiones (-).
     """
     for user in fake_db:
          if user.name == name:
                return user
     raise HTTPException(status_code=404, detail="Usuario no encontrado")

if __name__ == "__main__":
     uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)