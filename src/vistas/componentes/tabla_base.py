import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger("AppSalud.TablaBase")

class TablaBase(ttk.Frame):
    """
    Componente de tabla reusable que encapsula un ttk.Treeview con un Scrollbar vertical
    y gestiona la ordenación inteligente por columnas y el filtrado visual.
    """
    def __init__(self, parent, columnas, cabeceras, columnas_visibles=None, anchos=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnas = columnas
        self.cabeceras = cabeceras
        self.columnas_visibles = columnas_visibles if columnas_visibles is not None else columnas
        self.anchos = anchos if anchos is not None else {}

        # Configuración de pesos para expandirse
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear Treeview
        self.tree = ttk.Treeview(self, columns=self.columnas, show="headings")
        self.tree["displaycolumns"] = self.columnas_visibles

        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Ubicación en grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Inicializar columnas y cabeceras
        for col in self.columnas:
            titulo = self.cabeceras.get(col, col.capitalize())
            self.tree.heading(col, text=titulo, command=lambda c=col: self._ordenar_columna(c, False))
            
            ancho = self.anchos.get(col, 150)
            self.tree.column(col, width=ancho, anchor=tk.W if col != "id" else tk.CENTER)

        # Ocultar la primera columna oculta por defecto en el widget (id)
        self.tree.column("#0", width=0, stretch=tk.NO)

    def _ordenar_columna(self, col, reverso):
        """Ordena el contenido de la columna de manera ascendente o descendente (numérica o alfabética)."""
        hijos = self.tree.get_children('')
        if not hijos:
            return

        valores = []
        for h in hijos:
            val = self.tree.set(h, col)
            # Intentar conversión para ordenación natural
            try:
                val_comp = int(val)
            except ValueError:
                try:
                    val_comp = float(val)
                except ValueError:
                    val_comp = str(val).lower()
            valores.append((val_comp, h))

        valores.sort(key=lambda t: t[0], reverse=reverso)

        for index, (_, h) in enumerate(valores):
            self.tree.move(h, '', index)

        self.tree.heading(col, command=lambda: self._ordenar_columna(col, not reverso))

    def vaciar(self):
        """Elimina todos los elementos de la tabla."""
        for fila in self.tree.get_children():
            self.tree.delete(fila)

    def insertar_fila(self, valores, tags=()):
        """Inserta una nueva fila de valores al final."""
        return self.tree.insert("", tk.END, values=valores, tags=tags)

    def enfocar(self):
        """Obtiene el ID del elemento enfocado actual."""
        return self.tree.focus()

    def obtener_valores(self, item_id):
        """Obtiene la tupla de valores del item_id."""
        return self.tree.item(item_id, "values")

    def obtener_seleccionado(self):
        """Obtiene los valores de la fila seleccionada actual o None."""
        sel = self.tree.focus()
        if not sel:
            return None
        return self.tree.item(sel, "values")

    def bind(self, event, handler):
        """Vincula un evento al Treeview interno."""
        self.tree.bind(event, handler)
