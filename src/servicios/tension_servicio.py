import logging
from repositorios.tension_repositorio import TensionRepositorio

logger = logging.getLogger("AppSalud.TensionServicio")

class TensionServicio:
    """
    Servicio encargado de la lógica de negocio y validación de las tomas de tensión.
    """
    def __init__(self, tension_repo: TensionRepositorio):
        self.tension_repo = tension_repo

    def obtener_todas(self, paciente_id=None):
        return self.tension_repo.obtener_todos(paciente_id)

    def obtener_por_id(self, tension_id):
        return self.tension_repo.obtener_por_id(tension_id)

    def crear_toma(self, tension_in):
        try:
            # Regla de negocio: Verificar rango óptimo antes de guardar
            sistolica = tension_in.valores.sistolica
            diastolica = tension_in.valores.diastolica
            
            # Forzar validación de consistencia
            tension_in.valor_en_rango = self.verificar_rango(sistolica, diastolica)
            
            return self.tension_repo.crear(tension_in.model_dump())
        except Exception as e:
            logger.error(f"Error al registrar toma en el servicio: {e}")
            raise e

    def actualizar_toma(self, tension_id, tension_in):
        try:
            sistolica = tension_in.valores.sistolica
            diastolica = tension_in.valores.diastolica
            tension_in.valor_en_rango = self.verificar_rango(sistolica, diastolica)
            
            return self.tension_repo.actualizar(tension_id, tension_in.model_dump())
        except Exception as e:
            logger.error(f"Error al actualizar toma en el servicio: {e}")
            raise e

    def eliminar_toma(self, tension_id):
        return self.tension_repo.eliminar(tension_id)

    def eliminar_por_paciente(self, paciente_id):
        return self.tension_repo.eliminar_por_paciente(paciente_id)

    def verificar_rango(self, sistolica: int, diastolica: int) -> bool:
        """
        Regla de negocio: Determina si una medición de tensión sistólica y diastólica
        está en el rango óptimo (< 140 / 90 mmHg).
        """
        # Sistólica < 140 y Diastólica < 90
        return sistolica < 140 and diastolica < 90
