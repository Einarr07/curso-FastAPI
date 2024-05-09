# Importaciones
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Crear una instancia de la aplicación FastAPI
router = APIRouter(
    tags=["users"],
    responses={404: {"Message": "No encontrado"}}
)

# Nota: Para ejecutar el servidor, use the command: python -m uvicorn users:app --reload

# Definir una entidad de usuario utilizando Pydantic's BaseModel
class User(BaseModel):
    """
    Representa un usuario con los siguientes atributos:
    - id: int
    - first_name: str
    - last_name: str
    - age: int
    - email: str
    """
    id: int
    first_name: str
    last_name: str
    age: int
    email: str

# Inicializar una lista de usuarios
users_list = [
    # Usuario 1
    User(id=1, first_name="Joaquin", last_name="Palomo", age=23, email="joaqui.palomo@gmail.com"),
    # Usuario 2
    User(id=2, first_name="Nestor", last_name="Galarza", age=23, email="nestor.galarza@gmail.com"),
    # Usuario 3
    User(id=3, first_name="Pedro", last_name="Gualli", age=23, email="pedro.gualli@gmail.com")
]

# Definir un endpoint para devolver una lista de usuarios en formato JSON
@router.get("/users_json")
async def users_json():
    """
    Devuelve una lista de usuarios en formato JSON.
    """
    return [
        {"first_name": "Juan", "last_name": "Casallas", "age": 32, "email": "juan.casallas@gmail.com"},
        {"first_name": "Hernesto", "last_name": "Ramirez", "age": 20, "email": "hernesto.ramirez@gmail.com"},
        {"first_name": "Ricardo", "last_name": "Perez", "age": 21, "email": "ricardo.perez@gmail.com"}
    ]

# Definir un endpoint para devolver la lista de usuarios
@router.get("/users")
async def users():
    """
    Devuelve la lista de usuarios.
    """
    return users_list

# Definir un endpoint para recuperar un usuario por ID utilizando parámetros de ruta
@router.get("/user/{id}")
async def users(id: int):
    """
    Recupera un usuario por ID.
    :param id: int
    :return: Objeto de usuario o mensaje de error
    """
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}

# Definir un endpoint para recuperar un usuario por ID utilizando parámetros de consultas
@router.get("/user-query/")
async def users(id: int):
    """
    Recupera un usuario por ID utilizando parámetros de consulta.
    :param id: int
    :return: Objeto de usuario o mensaje de error
    """
    return search_user(id)

# Definir una función auxiliar para buscar un usuario por ID
def search_user(id: int):
    """
    Busca un usuario por ID.
    :param id: int
    :return: Objeto de usuario o mensaje de error
    """
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}

# Definir un endpoint para crear un usuario
@router.post("/user/", response_model=User, status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user

# Definir un endpoint para actualizar un usuario
@router.put("/user/")
async def update_user(user: User):
    """
    Actualizar un usuario en la lista de usuarios.
    """
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    return {"Error": "No se ha actualizado el usuario"}

# Definir un endpoint para eliminar un usuario
@router.delete("/user/{id}")
async def delete_user(id: int):
    """
    Eliminar un usuario de la lista de usuarios.
    """
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"Mensaje": "Usuario eliminado"}
    return {"Error": "No se ha eliminado el usuario"}