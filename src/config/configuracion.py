import os
import logging

class Configuracion:
    MONGODB_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "mi_app"
    LOG_LEVEL = "INFO"

    @classmethod
    def cargar_de_env(cls):
        # Buscar .env en el directorio raíz (un nivel arriba de config)
        ruta_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(ruta_env):
            try:
                with open(ruta_env, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if linea and not linea.startswith("#") and "=" in linea:
                            clave, valor = linea.split("=", 1)
                            os.environ[clave.strip()] = valor.strip()
            except Exception as e:
                print(f"Error leyendo el archivo .env: {e}")

        cls.MONGODB_URI = os.getenv("MONGODB_URI", cls.MONGODB_URI)
        cls.DATABASE_NAME = os.getenv("DATABASE_NAME", cls.DATABASE_NAME)
        cls.LOG_LEVEL = os.getenv("LOG_LEVEL", cls.LOG_LEVEL)

        # Configurar el sistema de logging
        nivel = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=nivel,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        logger = logging.getLogger("AppSalud")
        logger.info("Configuración cargada correctamente.")

# Cargar automáticamente al importar
Configuracion.cargar_de_env()
