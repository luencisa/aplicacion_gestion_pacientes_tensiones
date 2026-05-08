import uuid

class TensionRepository:
    def __init__(self, db_connection):
        self.db = db_connection.get_db()
        self.collection = self.db["tensiones"] if self.db is not None else None

    def get_all(self, paciente_id=None):
        if self.collection is None: return []
        query = {}
        if paciente_id:
            query["id_paciente"] = paciente_id
        return list(self.collection.find(query))

    def get_by_id(self, tension_id):
        if self.collection is None: return None
        return self.collection.find_one({"_id": tension_id})

    def create(self, tension_data):
        if self.collection is None: return None
        if "_id" not in tension_data or not tension_data["_id"]:
            tension_data["_id"] = str(uuid.uuid4())
        self.collection.insert_one(tension_data)
        return tension_data["_id"]

    def update(self, tension_id, tension_data):
        if self.collection is None: return False
        if "_id" in tension_data:
            del tension_data["_id"]
        result = self.collection.update_one({"_id": tension_id}, {"$set": tension_data})
        return result.modified_count > 0

    def delete(self, tension_id):
        if self.collection is None: return False
        result = self.collection.delete_one({"_id": tension_id})
        return result.deleted_count > 0

    def delete_by_paciente(self, paciente_id):
        if self.collection is None: return False
        result = self.collection.delete_many({"id_paciente": paciente_id})
        # Returns True if the operation was successful (even if deleted 0)
        return result.acknowledged
