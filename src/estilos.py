import tkinter as tk
from tkinter import ttk

class TemaApp:
    # Colores
    COLOR_FONDO_PRINCIPAL = "#f0f0f0"
    COLOR_FONDO_SECUNDARIO = "#ffffff"
    COLOR_PRIMARIO = "#0343CE"
    COLOR_BOTON = "#5E90FD"
    COLOR_BOTON_HOVER = "#8CB6FF"
    COLOR_TEXTO_BLANCO = "#ffffff"
    COLOR_TEXTO_PRINCIPAL = "#333333"

    # Fuentes
    FUENTE_GRANDE = ("Arial", 18, "bold")
    FUENTE_TITULO = ("Arial", 16, "bold")
    FUENTE_SUBTITULO = ("Arial", 12, "bold")
    FUENTE_NORMAL_NEGRITA = ("Arial", 12, "bold")
    FUENTE_NORMAL_GRANDE = ("Arial", 12)
    FUENTE_NORMAL = ("Arial", 10)
    FUENTE_PEQUENA = ("Arial", 8)

    # Tamaños y Espaciados Comunes
    ESPACIADO_PEQUENO = 5
    ESPACIADO_MEDIO = 10
    ESPACIADO_GRANDE = 20

    # Márgenes y Paddings derivados
    PADDING_GENERAL = ESPACIADO_MEDIO
    PADDING_X_BOTONES = ESPACIADO_PEQUENO
    PADDING_Y_FRAME = ESPACIADO_MEDIO
    MARGIN_X_ENTRIES = ESPACIADO_MEDIO
    MARGIN_Y_LABELS = ESPACIADO_PEQUENO

class TituloPrincipal(ttk.Label):
    def __init__(self, parent, text, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = TemaApp.FUENTE_TITULO
        super().__init__(parent, text=text, **kwargs)

class TituloSecundario(ttk.Label):
    def __init__(self, parent, text, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = TemaApp.FUENTE_SUBTITULO
        super().__init__(parent, text=text, **kwargs)

class BotonBase(tk.Button):
    """Clase base de botón con soporte para hover"""
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        # Deshabilitado no cambia el hover
        if self['state'] != 'disabled':
            self['bg'] = TemaApp.COLOR_BOTON_HOVER

    def on_leave(self, e):
        self['bg'] = TemaApp.COLOR_BOTON

class BotonPrincipal(BotonBase):
    """Boton grande para los menús principales"""
    def __init__(self, parent, text, command=None, **kwargs):
        config = {
            "bg": TemaApp.COLOR_BOTON,
            "fg": TemaApp.COLOR_TEXTO_BLANCO,
            "activebackground": TemaApp.COLOR_BOTON_HOVER,
            "activeforeground": TemaApp.COLOR_TEXTO_BLANCO,
            "font": TemaApp.FUENTE_SUBTITULO,
            "relief": tk.RAISED,
            "bd": 3,
            "padx": TemaApp.ESPACIADO_MEDIO,
            "pady": TemaApp.ESPACIADO_PEQUENO,
            "cursor": "hand2"
        }
        config.update(kwargs)
        super().__init__(parent, text, command, **config)

class BotonVista(BotonBase):
    """Botones para los formularios y tablas en las vistas"""
    def __init__(self, parent, text, command=None, **kwargs):
        config = {
            "bg": TemaApp.COLOR_BOTON,
            "fg": TemaApp.COLOR_TEXTO_BLANCO,
            "activebackground": TemaApp.COLOR_BOTON_HOVER,
            "activeforeground": TemaApp.COLOR_TEXTO_BLANCO,
            "font": TemaApp.FUENTE_NORMAL_NEGRITA,
            "relief": tk.RAISED,
            "bd": 2,
            "padx": TemaApp.ESPACIADO_MEDIO,
            "pady": TemaApp.ESPACIADO_PEQUENO,
            "cursor": "hand2"
        }
        config.update(kwargs)
        super().__init__(parent, text, command, **config)
