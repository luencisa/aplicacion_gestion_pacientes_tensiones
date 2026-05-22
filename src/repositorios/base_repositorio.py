from abc import ABC, abstractmethod

class BaseRepositorio(ABC):
    @abstractmethod
    def obtener_todos(self):
        """Recupera todos los registros de la colección."""
        pass

    @abstractmethod
    def obtener_por_id(self, entidad_id):
        """Recupera un único registro por su ID único."""
        pass

    @abstractmethod
    def crear(self, datos):
        """Inserta un nuevo registro en la colección."""
        pass

    @abstractmethod
    def actualizar(self, entidad_id, datos):
        """Actualiza un registro existente."""
        pass

    @abstractmethod
    def eliminar(self, entidad_id):
        """Elimina un registro de la colección."""
        pass
