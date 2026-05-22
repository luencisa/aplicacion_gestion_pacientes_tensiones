import uuid
import logging
from repositorios.base_repositorio import BaseRepositorio
from dependencias.database import ConexionBaseDatos

logger = logging.getLogger("AppSalud.TensionRepositorio")

class TensionRepositorio(BaseRepositorio):
    def __init__(self, conexion_db: ConexionBaseDatos):
        self.db = conexion_db.obtener_db()
        self.collection = self.db["tensiones"] if self.db is not None else None

    def obtener_todos(self, paciente_id=None):
        if self.collection is None:
            logger.warning("Base de datos no disponible.")
            return []
        try:
            query = {}
            if paciente_id:
                query["id_paciente"] = paciente_id
            return list(self.collection.find(query).sort("fecha", 1))
        except Exception as e:
            logger.error(f"Error al obtener todas las tensiones: {e}")
            return []

    def obtener_por_id(self, tension_id):
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({"_id": tension_id})
        except Exception as e:
            logger.error(f"Error al obtener toma de tensión por ID {tension_id}: {e}")
            return None

    def crear(self, tension_data):
        if self.collection is None:
            return None
        try:
            if "_id" not in tension_data or not tension_data["_id"]:
                tension_data["_id"] = str(uuid.uuid4())
            self.collection.insert_one(tension_data)
            return tension_data["_id"]
        except Exception as e:
            logger.error(f"Error al registrar toma de tensión: {e}")
            return None

    def actualizar(self, tension_id, tension_data):
        if self.collection is None:
            return False
        try:
            if "_id" in tension_data:
                del tension_data["_id"]
            result = self.collection.update_one({"_id": tension_id}, {"$set": tension_data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar toma de tensión {tension_id}: {e}")
            return False

    def eliminar(self, tension_id):
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_one({"_id": tension_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar toma de tensión {tension_id}: {e}")
            return False

    def eliminar_por_paciente(self, paciente_id):
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_many({"id_paciente": paciente_id})
            return result.acknowledged
        except Exception as e:
            logger.error(f"Error al eliminar tensiones del paciente {paciente_id}: {e}")
            return False
