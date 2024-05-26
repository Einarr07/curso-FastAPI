# Importaciones necesarias para el funcionamiento del enrutador y la base de datos
from fastapi import APIRouter, HTTPException, status
from db.models.user import User  # Modelo de usuario
from db.schemas.user import user_schema, users_schemas  # Esquemas para serialización/deserialización de usuarios
from db.client import db  # Cliente de la base de datos
from bson import ObjectId  # Para trabajar con ObjectId de MongoDB

# Definición del enrutador
router = APIRouter(
    prefix="/userdb",  # Prefijo para todas las rutas definidas en este enrutador
    tags=["usersdb"],  # Etiquetas para la documentación de las rutas
    responses={status.HTTP_404_NOT_FOUND: {"Message": "No encontrado"}}  # Respuestas predeterminadas para ciertos códigos de estado
)

# Lista temporal de usuarios (en este caso, parece que no se utiliza realmente)
users_list = []

# Función para buscar un usuario en la base de datos por un campo específico y una clave
def search_user(field: str, key):
    try:
        # Buscar un usuario en la base de datos
        user = db.users.find_one({field: key})
        # Si se encuentra, retornar el usuario como instancia del modelo User
        return User(**user_schema(user))
    except:
        # En caso de error o si no se encuentra el usuario, retornar un mensaje de error
        return {"Error: No se ha encontrado el usuario"}

# Definir una ruta GET para obtener una lista de todos los usuarios
@router.get("/", response_model=list[User])
async def users():
    # Retornar una lista de todos los usuarios, transformados según el esquema definido
    return users_schemas(db.users.find())

# Definir una ruta GET para obtener un usuario por su ID
@router.get("/{id}")
async def user(id: str):
    # Buscar y retornar el usuario cuyo ID coincide con el proporcionado
    return search_user("_id", ObjectId(id))

# Definir otra ruta GET para obtener un usuario por su ID, posiblemente duplicada de la anterior
@router.get("/user-query-db/")
async def user(id: str):
    # Buscar y retornar el usuario cuyo ID coincide con el proporcionado
    return search_user("_id", ObjectId(id))

# Definir una ruta POST para crear un nuevo usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # Verificar si el usuario con el correo proporcionado ya existe
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    # Convertir el usuario a un diccionario y eliminar el campo ID
    user_dict = dict(user)
    del user_dict["id"]

    # Insertar el nuevo usuario en la base de datos y obtener su ID
    id = db.users.insert_one(user_dict).inserted_id

    # Buscar y retornar el usuario recién creado
    new_user = user_schema(db.users.find_one({"_id": id}))

    return User(**new_user)

# Definir una ruta PUT para actualizar un usuario existente
@router.put("/", response_model=User)
async def update_user(user: User):
    # Convertir el usuario a un diccionario y eliminar el campo ID
    user_dict = dict(user)
    user_id = user_dict.pop("id")
    
    try:
        # Buscar y reemplazar el usuario en la base de datos
        updated_user = db.users.find_one_and_replace(
            {"_id": ObjectId(user_id)},
            user_dict,
            return_document=True
        )
        # Si no se encuentra el usuario, lanzar una excepción
        if not updated_user:
            raise HTTPException(status_code=404, detail="No se ha encontrado el usuario para actualizar")
    except Exception as e:
        # Manejar cualquier error que ocurra durante la actualización
        raise HTTPException(status_code=400, detail=f"Error al actualizar el usuario: {e}")

    # Retornar el usuario actualizado
    return User(**user_schema(updated_user))

# Definir una ruta DELETE para eliminar un usuario por su ID
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    # Buscar y eliminar el usuario cuyo ID coincide con el proporcionado
    found = db.users.find_one_and_delete({"_id": ObjectId(id)})
    
    # Si no se encuentra el usuario, retornar un mensaje de error
    if not found:
        raise HTTPException(status_code=404, detail="No se ha eliminado el usuario")
