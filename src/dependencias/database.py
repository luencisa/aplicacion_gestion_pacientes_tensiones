import logging
from pymongo import MongoClient
from config.configuracion import Configuracion

logger = logging.getLogger("AppSalud.ConexionBaseDatos")

class ConexionBaseDatos:
    def __init__(self):
        try:
            # Conexión usando valores de configuración externa
            self.client = MongoClient(Configuracion.MONGODB_URI, serverSelectionTimeoutMS=2000)
            self.client.server_info() # Verificar conexión activa
            self.db = self.client[Configuracion.DATABASE_NAME]
            logger.info(f"Conectado a MongoDB ('{Configuracion.DATABASE_NAME}') exitosamente.")
        except Exception as e:
            logger.error(f"Error al conectar con MongoDB: {e}")
            self.client = None
            self.db = None

    def obtener_db(self):
        return self.db
