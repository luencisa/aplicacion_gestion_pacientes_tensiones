import sys
import os

# Agregamos la ruta actual (src) al path para que funcionen las importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from config.configuracion import Configuracion
from dependencias.contenedor import Contenedor
from vistas.ventana_principal import VentanaPrincipal

def main():
    # Inicializar configuración del entorno y logging
    Configuracion.cargar_de_env()
    
    # Crear el contenedor de dependencias centralizado (inyección de dependencias)
    contenedor = Contenedor()
    
    # Inicializar la interfaz gráfica de usuario
    root = tk.Tk()
    app = VentanaPrincipal(root, contenedor)
    root.mainloop()

if __name__ == "__main__":
    main()
