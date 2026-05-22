import uuid
import logging
from repositorios.base_repositorio import BaseRepositorio
from dependencias.database import ConexionBaseDatos

logger = logging.getLogger("AppSalud.PacienteRepositorio")

class PacienteRepositorio(BaseRepositorio):
    def __init__(self, conexion_db: ConexionBaseDatos):
        self.db = conexion_db.obtener_db()
        self.collection = self.db["pacientes"] if self.db is not None else None

    def obtener_todos(self):
        if self.collection is None:
            logger.warning("Base de datos no disponible.")
            return []
        try:
            return list(self.collection.find({}))
        except Exception as e:
            logger.error(f"Error al obtener todos los pacientes: {e}")
            return []

    def obtener_por_id(self, paciente_id):
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({"_id": paciente_id})
        except Exception as e:
            logger.error(f"Error al obtener paciente por ID {paciente_id}: {e}")
            return None

    def crear(self, paciente_data):
        if self.collection is None:
            return None
        try:
            if "_id" not in paciente_data or not paciente_data["_id"]:
                paciente_data["_id"] = str(uuid.uuid4())
            self.collection.insert_one(paciente_data)
            return paciente_data["_id"]
        except Exception as e:
            logger.error(f"Error al crear paciente: {e}")
            return None

    def actualizar(self, paciente_id, paciente_data):
        if self.collection is None:
            return False
        try:
            if "_id" in paciente_data:
                del paciente_data["_id"]
            result = self.collection.update_one({"_id": paciente_id}, {"$set": paciente_data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar paciente {paciente_id}: {e}")
            return False

    def eliminar(self, paciente_id):
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_one({"_id": paciente_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar paciente {paciente_id}: {e}")
            return False
