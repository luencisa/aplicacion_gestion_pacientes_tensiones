import uuid
import logging
from repositorios.base_repositorio import BaseRepositorio
from dependencias.database import ConexionBaseDatos

logger = logging.getLogger("AppSalud.ListaRepositorio")

class ListaRepositorio(BaseRepositorio):
    def __init__(self, conexion_db: ConexionBaseDatos):
        self.db = conexion_db.obtener_db()
        self.collection = self.db["lista"] if self.db is not None else None

    def obtener_todos(self):
        if self.collection is None:
            logger.warning("Base de datos no disponible.")
            return []
        try:
            return list(self.collection.find({}))
        except Exception as e:
            logger.error(f"Error al obtener lista de espera: {e}")
            return []

    def obtener_por_id(self, lista_id):
        if self.collection is None:
            return None
        try:
            return self.collection.find_one({"_id": lista_id})
        except Exception as e:
            logger.error(f"Error al obtener elemento de lista por ID {lista_id}: {e}")
            return None

    def obtener_por_estado_y_servicio(self, estado, servicio):
        if self.collection is None:
            return []
        try:
            return list(self.collection.find({"estado": estado, "servicio": servicio}))
        except Exception as e:
            logger.error(f"Error al obtener lista por estado={estado} y servicio={servicio}: {e}")
            return []

    def crear(self, lista_data):
        if self.collection is None:
            return None
        try:
            if "_id" not in lista_data or not lista_data["_id"]:
                lista_data["_id"] = str(uuid.uuid4())
            self.collection.insert_one(lista_data)
            return lista_data["_id"]
        except Exception as e:
            logger.error(f"Error al registrar elemento en lista de espera: {e}")
            return None

    def actualizar(self, lista_id, lista_data):
        if self.collection is None:
            return False
        try:
            if "_id" in lista_data:
                del lista_data["_id"]
            result = self.collection.update_one({"_id": lista_id}, {"$set": lista_data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar elemento de lista {lista_id}: {e}")
            return False

    def actualizar_estado(self, lista_id, nuevo_estado):
        if self.collection is None:
            return False
        try:
            result = self.collection.update_one({"_id": lista_id}, {"$set": {"estado": nuevo_estado}})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar estado en lista {lista_id}: {e}")
            return False

    def eliminar(self, lista_id):
        if self.collection is None:
            return False
        try:
            result = self.collection.delete_one({"_id": lista_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar elemento de lista {lista_id}: {e}")
            return False
