import logging
from datetime import datetime, timedelta
from repositorios.lista_repositorio import ListaRepositorio
from repositorios.paciente_repositorio import PacienteRepositorio

logger = logging.getLogger("AppSalud.ListaServicio")

class ListaServicio:
    def __init__(self, lista_repo: ListaRepositorio, paciente_repo: PacienteRepositorio):
        self.lista_repo = lista_repo
        self.paciente_repo = paciente_repo

    def obtener_lista_completa(self):
        """Devuelve toda la lista de espera con datos de pacientes asociados."""
        lista_espera = self.lista_repo.obtener_todos()
        pacientes = self.paciente_repo.obtener_todos()
        paciente_map = {p["_id"]: f"{p.get('nombre', '')} {p.get('apellido', '')}" for p in pacientes}

        for item in lista_espera:
            id_pac = item.get("id_paciente", "")
            item["nombre_paciente"] = paciente_map.get(id_pac, "Paciente no encontrado")
        
        lista_espera.sort(key=lambda x: x.get("fecha_hora", ""))
        return lista_espera

    def obtener_lista_por_servicio(self, servicio, estado=None):
        """Devuelve la lista filtrada por tipo de servicio (consulta/enfermeria) y opcionalmente por estado."""
        if estado:
            lista_espera = self.lista_repo.obtener_por_estado_y_servicio(estado, servicio)
        else:
            todos = self.lista_repo.obtener_todos()
            lista_espera = [t for t in todos if t.get("servicio") == servicio]

        pacientes = self.paciente_repo.obtener_todos()
        paciente_map = {p["_id"]: f"{p.get('nombre', '')} {p.get('apellido', '')}" for p in pacientes}

        for item in lista_espera:
            id_pac = item.get("id_paciente", "")
            item["nombre_paciente"] = paciente_map.get(id_pac, "Paciente no encontrado")
            
        lista_espera.sort(key=lambda x: x.get("fecha_hora", ""))
        return lista_espera

    def generar_fechas_recurrencia(self, fecha_inicio_str: str, patron: str, repeticiones: int):
        """
        Regla de negocio: Calcula y devuelve una lista de fechas (strings) en base al patrón
        y número de repeticiones indicados.
        """
        try:
            dt_inicio = datetime.strptime(fecha_inicio_str.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            logger.error(f"Formato de fecha inválido recibido: {fecha_inicio_str}")
            raise ValueError("La fecha inicial debe estar en formato YYYY-MM-DD HH:MM")

        if repeticiones < 1:
            logger.error(f"Número de repeticiones inválido: {repeticiones}")
            raise ValueError("El número de repeticiones debe ser un entero mayor o igual a 1.")

        fechas_generadas = []
        delta = timedelta(days=1) if patron == "Diaria" else timedelta(weeks=1)
        for i in range(repeticiones):
            dt_actual = dt_inicio + i * delta
            fechas_generadas.append(dt_actual.strftime("%Y-%m-%d %H:%M"))
            
        return fechas_generadas

    def crear(self, datos_lista):
        """Crea un nuevo registro en la lista de espera."""
        return self.lista_repo.crear(datos_lista)

    def actualizar_estado(self, lista_id, nuevo_estado):
        """Actualiza el estado de un registro de la lista de espera."""
        return self.lista_repo.actualizar_estado(lista_id, nuevo_estado)

    def eliminar(self, lista_id):
        """Elimina un registro de la lista de espera."""
        return self.lista_repo.eliminar(lista_id)
