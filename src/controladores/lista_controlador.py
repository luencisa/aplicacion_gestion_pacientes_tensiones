import logging
from esquemas.lista_input import ListaInput
from servicios.lista_servicio import ListaServicio

logger = logging.getLogger("AppSalud.ListaControlador")

class ListaControlador:
    def __init__(self, lista_servicio: ListaServicio):
        self.servicio = lista_servicio

    def obtener_lista_completa(self):
        try:
            return self.servicio.obtener_lista_completa()
        except Exception as e:
            logger.error(f"Error al obtener lista completa: {e}")
            return []

    def obtener_lista_por_servicio(self, servicio, estado=None):
        try:
            return self.servicio.obtener_lista_por_servicio(servicio, estado)
        except Exception as e:
            logger.error(f"Error al obtener lista por servicio {servicio}: {e}")
            return []

    def agregar_lista(self, lista_in: ListaInput):
        try:
            return self.servicio.crear(lista_in.model_dump())
        except Exception as e:
            logger.error(f"Error al agregar a la lista de espera: {e}")
            raise e

    def actualizar_estado(self, lista_id, nuevo_estado):
        try:
            return self.servicio.actualizar_estado(lista_id, nuevo_estado)
        except Exception as e:
            logger.error(f"Error al actualizar estado {lista_id}: {e}")
            return False

    def eliminar_lista(self, lista_id):
        try:
            return self.servicio.eliminar(lista_id)
        except Exception as e:
            logger.error(f"Error al eliminar de lista {lista_id}: {e}")
            return False

    def generar_fechas_recurrencia(self, fecha_inicio_str, patron, repeticiones):
        try:
            return self.servicio.generar_fechas_recurrencia(fecha_inicio_str, patron, repeticiones)
        except Exception as e:
            logger.error(f"Error al generar fechas de recurrencia: {e}")
            raise e

