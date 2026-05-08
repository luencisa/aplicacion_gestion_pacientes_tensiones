from pymongo import MongoClient

class DatabaseConnection:
    def __init__(self):
        try:
            # Nos conectamos a localhost en el puerto por defecto de MongoDB
            self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
            # Forzamos una llamada para verificar que hay conexión
            self.client.server_info()
            # Seleccionamos la base de datos mi_app
            self.db = self.client["mi_app"]
            print("Conectado a MongoDB ('mi_app') exitosamente.")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            self.client = None
            self.db = None

    def get_db(self):
        return self.db
