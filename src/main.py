import sys
import os

# Agregamos la ruta actua (src) al path para que funcionen las importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from views.main_window import MainWindow
from dependencias.database import DatabaseConnection

def main():
    root = tk.Tk()
    db_connection = DatabaseConnection()
    app = MainWindow(root, db_connection)
    root.mainloop()

if __name__ == "__main__":
    main()
