import logging
from dependencias.database import ConexionBaseDatos
from repositorios.paciente_repositorio import PacienteRepositorio
from repositorios.tension_repositorio import TensionRepositorio
from repositorios.lista_repositorio import ListaRepositorio
from servicios.paciente_servicio import PacienteServicio
from servicios.tension_servicio import TensionServicio
from servicios.analisis_tension_servicio import AnalisisTensionServicio
from servicios.lista_servicio import ListaServicio
from controladores.paciente_controlador import PacienteControlador
from controladores.tension_controlador import TensionControlador
from controladores.lista_controlador import ListaControlador

logger = logging.getLogger("AppSalud.Contenedor")

class Contenedor:
    def __init__(self):
        logger.info("Inicializando el contenedor de dependencias central...")
        
        # 1. Conexión de Base de Datos
        self.conexion_db = ConexionBaseDatos()
        
        # 2. Repositorios (Infraestructura)
        self.paciente_repositorio = PacienteRepositorio(self.conexion_db)
        self.tension_repositorio = TensionRepositorio(self.conexion_db)
        self.lista_repositorio = ListaRepositorio(self.conexion_db)
        
        # 3. Servicios (Lógica de Negocio/Aplicación)
        self.paciente_servicio = PacienteServicio(self.paciente_repositorio, self.tension_repositorio)
        self.tension_servicio = TensionServicio(self.tension_repositorio)
        self.analisis_tension_servicio = AnalisisTensionServicio(self.tension_repositorio, self.paciente_repositorio)
        self.lista_servicio = ListaServicio(self.lista_repositorio, self.paciente_repositorio)
        
        # 4. Controladores (Adaptadores de Interfaz)
        self.paciente_controlador = PacienteControlador(self.paciente_servicio)
        self.tension_controlador = TensionControlador(self.tension_servicio, self.analisis_tension_servicio)
        self.lista_controlador = ListaControlador(self.lista_servicio)
        
        logger.info("Contenedor de dependencias inicializado exitosamente.")
