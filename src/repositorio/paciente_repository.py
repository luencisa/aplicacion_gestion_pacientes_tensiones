import uuid

class PacienteRepository:
    def __init__(self, db_connection):
        self.db = db_connection.get_db()
        self.collection = self.db["pacientes"] if self.db is not None else None

    def get_all(self):
        if self.collection is None: return []
        return list(self.collection.find({}))

    def get_by_id(self, paciente_id):
        if self.collection is None: return None
        return self.collection.find_one({"_id": paciente_id})

    def create(self, paciente_data):
        if self.collection is None: return None
        if "_id" not in paciente_data or not paciente_data["_id"]:
            paciente_data["_id"] = str(uuid.uuid4())
        self.collection.insert_one(paciente_data)
        return paciente_data["_id"]

    def update(self, paciente_id, paciente_data):
        if self.collection is None: return False
        # Para prevenir intentar actualizar el _id inmutable
        if "_id" in paciente_data:
            del paciente_data["_id"]
        result = self.collection.update_one({"_id": paciente_id}, {"$set": paciente_data})
        return result.modified_count > 0

    def delete(self, paciente_id):
        if self.collection is None: return False
        result = self.collection.delete_one({"_id": paciente_id})
        return result.deleted_count > 0
