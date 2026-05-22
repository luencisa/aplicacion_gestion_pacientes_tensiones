import logging
from esquemas.paciente_input import PacienteInput
from servicios.paciente_servicio import PacienteServicio

logger = logging.getLogger("AppSalud.PacienteControlador")

class PacienteControlador:
    def __init__(self, paciente_servicio: PacienteServicio):
        self.servicio = paciente_servicio

    def obtener_pacientes(self):
        try:
            return self.servicio.obtener_todos()
        except Exception as e:
            logger.error(f"Error al obtener pacientes: {e}")
            return []

    def obtener_paciente(self, paciente_id):
        try:
            return self.servicio.obtener_por_id(paciente_id)
        except Exception as e:
            logger.error(f"Error al obtener paciente {paciente_id}: {e}")
            return None

    def agregar_paciente(self, paciente_in: PacienteInput):
        try:
            return self.servicio.crear(paciente_in.model_dump())
        except Exception as e:
            logger.error(f"Error al agregar paciente: {e}")
            raise e

    def actualizar_paciente(self, paciente_id, paciente_in: PacienteInput):
        try:
            return self.servicio.actualizar(paciente_id, paciente_in.model_dump())
        except Exception as e:
            logger.error(f"Error al actualizar paciente {paciente_id}: {e}")
            raise e

    def eliminar_paciente(self, paciente_id):
        try:
            return self.servicio.eliminar_paciente_en_cascada(paciente_id)
        except Exception as e:
            logger.error(f"Error al eliminar paciente {paciente_id}: {e}")
            raise e
