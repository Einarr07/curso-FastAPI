# Importar la clase MongoClient del módulo pymongo para interactuar con MongoDB
from pymongo import MongoClient
# Importar la variable MONGO_DB_URL del archivo de configuración (config.py)
from db.config import MONGO_DB_URL

# Configuración para base de datos local (comentada porque se está usando una base de datos remota)
# db_client = MongoClient().local

# Conectar a la base de datos remota usando la URL de conexión obtenida de las variables de entorno
client = MongoClient(MONGO_DB_URL).test

# Asignar la base de datos a la variable db
db = client
