# Importar FastAPI
from fastapi import FastAPI

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Nota: Para ejecutar el servidor, use el comando: python -m uvicorn main:app --reload

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