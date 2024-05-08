# Importar FastAPI y Pydantic's BaseModel
from fastapi import FastAPI
from pydantic import BaseModel

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Nota: Para ejecutar el servidor, use el comando: python -m uvicorn users:app --reload

# Definir una entidad de usuario utilizando Pydantic's BaseModel
class User(BaseModel):
    """
    Representa un usuario con los siguientes atributos:
    - id: int
    - nombre: str
    - apellido: str
    - edad: int
    - correo electrónico: str
    """
    id: int
    nombre: str
    apellido: str
    edad: int
    correo_electronico: str

# Inicializar una lista de usuarios
user_list = [
    # Usuario 1
    User(id=1, nombre="Joaquin", apellido="Palomo", edad=23, correo_electronico="joaqui.palomo@gmail.com"),
    # Usuario 2
    User(id=2, nombre="Nestor", apellido="Galarza", edad=23, correo_electronico="nestor.galarza@gmail.com"),
    # Usuario 3
    User(id=3, nombre="Pedro", apellido="Gualli", edad=23, correo_electronico="pedro.gualli@gmail.com")
]

# Definir un endpoint para devolver una lista de usuarios en formato JSON
@app.get("/users_json")
async def users_json():
    """
    Devuelve una lista de usuarios en formato JSON.
    """
    return [
        {"nombre": "Juan", "apellido": "Casallas", "edad": 32, "correo_electronico": "juan.casallas@gmail.com"},
        {"nombre": "Hernesto", "apellido": "Ramirez", "edad": 20, "correo_electronico": "hernesto.ramirez@gmail.com"},
        {"nombre": "Ricardo", "apellido": "Perez", "edad": 21, "correo_electronico": "ricardo.perez@gmail.com"}
    ]

# Definir un endpoint para devolver la lista de usuarios
@app.get("/users")
async def users():
    """
    Devuelve la lista de usuarios.
    """
    return user_list

# Definir un endpoint para recuperar un usuario por ID utilizando parámetros de ruta
@app.get("/user/{id}")
async def users(id: int):
    """
    Recupera un usuario por ID.
    :param id: int
    :return: Objeto de usuario o mensaje de error
    """
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}

# Definir un endpoint para recuperar un usuario por ID utilizando parámetros de consultas
@app.get("/user-query/")
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
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}
    
@app.post("/user/")
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        return{"Error": "El usuario ya existe"}
    else:
        user_list.append(user)

@app.put("/user/")
async def update_user(user: User):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True

    if not found:
        return {"Error": "No se ha actualizado el usuario"}
    else:
        return user

@app.delete("/user/{id}")
async def delete_user(id: int):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True
        
    if not found:
        return {"Error": "No se ha eliminado el usuario"}    
