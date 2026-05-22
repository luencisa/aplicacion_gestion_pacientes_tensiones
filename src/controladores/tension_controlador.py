import logging
from esquemas.tension_input import TensionInput
from servicios.tension_servicio import TensionServicio
from servicios.analisis_tension_servicio import AnalisisTensionServicio

logger = logging.getLogger("AppSalud.TensionControlador")

class TensionControlador:
    def __init__(self, tension_servicio: TensionServicio, analisis_servicio: AnalisisTensionServicio):
        self.servicio = tension_servicio
        self.analisis_servicio = analisis_servicio

    def obtener_tensiones(self, paciente_id=None):
        try:
            return self.servicio.obtener_todas(paciente_id)
        except Exception as e:
            logger.error(f"Error al obtener tensiones: {e}")
            return []

    def obtener_tension(self, tension_id):
        try:
            return self.servicio.obtener_por_id(tension_id)
        except Exception as e:
            logger.error(f"Error al obtener toma de tensión {tension_id}: {e}")
            return None

    def agregar_tension(self, tension_in: TensionInput):
        try:
            return self.servicio.crear_toma(tension_in)
        except Exception as e:
            logger.error(f"Error al registrar toma de tensión: {e}")
            raise e

    def actualizar_tension(self, tension_id, tension_in: TensionInput):
        try:
            return self.servicio.actualizar_toma(tension_id, tension_in)
        except Exception as e:
            logger.error(f"Error al actualizar toma de tensión {tension_id}: {e}")
            raise e

    def eliminar_tension(self, tension_id):
        try:
            return self.servicio.eliminar_toma(tension_id)
        except Exception as e:
            logger.error(f"Error al eliminar toma de tensión {tension_id}: {e}")
            return False

    def obtener_analisis_completo(self, paciente_id, ultimas_n=None):
        try:
            return self.analisis_servicio.obtener_analisis_completo(paciente_id, ultimas_n)
        except Exception as e:
            logger.error(f"Error al obtener análisis completo para paciente {paciente_id}: {e}")
            return None

    def verificar_rango(self, sistolica: int, diastolica: int) -> bool:
        try:
            return self.servicio.verificar_rango(sistolica, diastolica)
        except Exception as e:
            logger.error(f"Error al verificar rango: {e}")
            return False

