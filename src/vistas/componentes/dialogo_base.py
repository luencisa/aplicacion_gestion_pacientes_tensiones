import tkinter as tk
from tkinter import ttk
from estilos import TemaApp

class DialogoBase(tk.Toplevel):
    """
    Clase base reutilizable para diálogos (ventanas emergentes modales).
    Desactiva temporalmente la ventana principal para evitar interacciones accidentales
    y resuelve problemas de enfoque en controles (como comboboxes) en Windows.
    """
    def __init__(self, parent, title="Diálogo", geometry="350x450"):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry(geometry)
        self.configure(bg=TemaApp.COLOR_PRIMARIO)
        
        # Guardar referencia al top-level principal y deshabilitarlo
        self.parent_win = parent.winfo_toplevel()
        self.parent_win.attributes("-disabled", True)
        
        self.bind("<Destroy>", self._al_destruir)
        self.focus_force()

    def _al_destruir(self, event):
        # Aseguramos que solo reaccionamos a la destrucción de este diálogo y no de sus hijos
        if event.widget == self and self.parent_win.winfo_exists():
            self.parent_win.attributes("-disabled", False)
            self.parent_win.focus_force()
