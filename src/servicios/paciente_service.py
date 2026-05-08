from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository

class PacienteService:
    """
    Servicio que contiene operaciones de composición que involucran 
    tanto a la colección de pacientes como a la de tensiones.
    """
    def __init__(self, db_connection):
        self.paciente_dao = PacienteRepository(db_connection)
        self.tension_dao = TensionRepository(db_connection)

    def get_paciente_con_tensiones(self, paciente_id):
        """
        Operación de composición: Recupera la información de un paciente 
        y adjunta todas sus tensiones registradas.
        """
        paciente = self.paciente_dao.get_by_id(paciente_id)
        if paciente:
            tensiones = self.tension_dao.get_all(paciente_id)
            paciente['tensiones_asociadas'] = tensiones
            
            # Operaciones de agregación simple sobre las tensiones (opcional)
            paciente['total_tensiones'] = len(tensiones)
            
            if tensiones:
                sistolicas = [t['valores']['sistolica'] for t in tensiones if 'valores' in t and 'sistolica' in t['valores']]
                diastolicas = [t['valores']['diastolica'] for t in tensiones if 'valores' in t and 'diastolica' in t['valores']]
                
                if sistolicas:
                    paciente['promedio_sistolica'] = round(sum(sistolicas) / len(sistolicas), 2)
                if diastolicas:
                    paciente['promedio_diastolica'] = round(sum(diastolicas) / len(diastolicas), 2)
        
        return paciente

    def delete_paciente_en_cascada(self, paciente_id):
        # 1. Eliminar todas las tensiones pertenecientes a este paciente
        self.tension_dao.delete_by_paciente(paciente_id)
        
        # 2. Eliminar el paciente
        return self.paciente_dao.delete(paciente_id)
