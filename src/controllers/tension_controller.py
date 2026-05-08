from repositorio.tension_repository import TensionRepository
from esquemas.tension_input import TensionInput
from esquemas.tension_update_input import TensionUpdateInput
from esquemas.tension_valores import TensionValores
class TensionController:
    def __init__(self, db_connection):
        self.dao = TensionRepository(db_connection)

    def get_tensiones(self, paciente_id=None):
        return self.dao.get_all(paciente_id)

    def get_tension(self, tension_id):
        return self.dao.get_by_id(tension_id)

    def add_tension(self, tension_in: TensionInput):
        return self.dao.create(tension_in.model_dump())

    def update_tension(self, tension_id, tension_in: TensionUpdateInput):
        return self.dao.update(tension_id, tension_in.model_dump())

    def delete_tension(self, tension_id):
        return self.dao.delete(tension_id)
