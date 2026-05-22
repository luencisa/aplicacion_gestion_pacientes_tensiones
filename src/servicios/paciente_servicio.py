import logging
from repositorios.paciente_repositorio import PacienteRepositorio
from repositorios.tension_repositorio import TensionRepositorio

logger = logging.getLogger("AppSalud.PacienteServicio")

class PacienteServicio:
    """
    Servicio que contiene operaciones de composición que involucran 
    tanto a la colección de pacientes como a la de tensiones.
    """
    def __init__(self, paciente_repo: PacienteRepositorio, tension_repo: TensionRepositorio):
        self.paciente_repo = paciente_repo
        self.tension_repo = tension_repo

    def obtener_paciente_con_tensiones(self, paciente_id):
        """
        Operación de composición: Recupera la información de un paciente 
        y adjunta todas sus tensiones registradas.
        """
        paciente = self.paciente_repo.obtener_por_id(paciente_id)
        if paciente:
            tensiones = self.tension_repo.obtener_todos(paciente_id)
            paciente['tensiones_asociadas'] = tensiones
            paciente['total_tensiones'] = len(tensiones)
            
            if tensiones:
                sistolicas = [t['valores']['sistolica'] for t in tensiones if 'valores' in t and 'sistolica' in t['valores']]
                diastolicas = [t['valores']['diastolica'] for t in tensiones if 'valores' in t and 'diastolica' in t['valores']]
                
                if sistolicas:
                    paciente['promedio_sistolica'] = round(sum(sistolicas) / len(sistolicas), 2)
                if diastolicas:
                    paciente['promedio_diastolica'] = round(sum(diastolicas) / len(diastolicas), 2)
        
        return paciente

    def eliminar_paciente_en_cascada(self, paciente_id):
        """Elimina un paciente y todas sus tomas de tensión asociadas de manera segura."""
        logger.info(f"Iniciando eliminación en cascada para el paciente {paciente_id}")
        try:
            # 1. Eliminar todas las tensiones pertenecientes a este paciente
            self.tension_repo.eliminar_por_paciente(paciente_id)
            # 2. Eliminar el paciente
            return self.paciente_repo.eliminar(paciente_id)
        except Exception as e:
            logger.error(f"Error en eliminación en cascada para paciente {paciente_id}: {e}")
            raise e

    def obtener_todos(self):
        """Devuelve todos los pacientes del repositorio."""
        return self.paciente_repo.obtener_todos()

    def obtener_por_id(self, paciente_id):
        """Devuelve un paciente por su ID del repositorio."""
        return self.paciente_repo.obtener_por_id(paciente_id)

    def crear(self, datos_paciente):
        """Crea un nuevo paciente en el repositorio."""
        return self.paciente_repo.crear(datos_paciente)

    def actualizar(self, paciente_id, datos_paciente):
        """Actualiza la información de un paciente en el repositorio."""
        return self.paciente_repo.actualizar(paciente_id, datos_paciente)
