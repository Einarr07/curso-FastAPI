# Importar la función load_dotenv del módulo dotenv para cargar variables de entorno desde un archivo .env
from dotenv import load_dotenv
import os  # Importar el módulo os para acceder a las variables de entorno

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno MONGO_DB_URL y asignarlo a la variable MONGO_DB_URL
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
