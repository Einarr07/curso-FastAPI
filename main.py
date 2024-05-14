# Importar FastAPI
from fastapi import FastAPI
from routes import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Nota: Para ejecutar el servidor, use el comando: python -m uvicorn main:app --reload

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

# Forma para exponer recursos estaticos: /static/images/mouredev_curso_python.jpg
app.mount("/static", StaticFiles(directory="static"), name="static")

# Definir un endpoint para la raíz de la aplicación
@app.get("/")
async def root():
    """
    Devuelve un mensaje de bienvenida.
    """
    return "Hola FastAPI"

# Definir un endpoint para devolver la URL del curso
@app.get("/url")
async def url():
    """
    Devuelve la URL del curso de Python de mouredev.
    """
    return {"url_curso": "https://mouredev.com/python"}

# Nota: La documentación de la API se puede ver en:
# - Swagger: http://127.0.0.1:8000/docs
# - Redocly: http://127.0.0.1:8000/redoc