from repositorio.paciente_repository import PacienteRepository
from esquemas.paciente_input import PacienteInput

class PacienteController:
    def __init__(self, db_connection):
        self.dao = PacienteRepository(db_connection)

    def get_pacientes(self):
        return self.dao.get_all()

    def get_paciente(self, paciente_id):
        return self.dao.get_by_id(paciente_id)

    def add_paciente(self, paciente_in: PacienteInput):
        return self.dao.create(paciente_in.model_dump())

    def update_paciente(self, paciente_id, paciente_in: PacienteInput):
        return self.dao.update(paciente_id, paciente_in.model_dump())

    def delete_paciente(self, paciente_id):
        return self.dao.delete(paciente_id)
