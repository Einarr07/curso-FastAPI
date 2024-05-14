# Importaciones
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schemas
from db.client import db_client

router = APIRouter(
    prefix="/userdb",
    tags=["usersdb"],
    responses={status.HTTP_404_NOT_FOUND: {"Message": "No encontrado"}}
)


users_list = []



@router.get("/")
async def users():
    return users_list

@router.get("/{id}")
async def users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}

@router.get("/user-query-db/")
async def users(id: int):
    """
    Recupera un usuario por ID utilizando parámetros de consulta.
    :param id: int
    :return: Objeto de usuario o mensaje de error
    """
    return search_user(id)

# Definir una función auxiliar para buscar un usuario por ID
def search_user(id: int):
    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error: No se ha encontrado el usuario"}


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schemas(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)

# Definir un endpoint para actualizar un usuario
@router.put("/")
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