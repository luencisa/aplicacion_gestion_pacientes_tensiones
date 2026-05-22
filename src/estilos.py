import tkinter as tk
from tkinter import ttk

# ==============================================================================
# SECCIÓN 1: CONFIGURACIÓN BASE DEL TEMA GENERAL
# ==============================================================================

class TemaApp:
    # Colores de la paleta general
    COLOR_FONDO_PRINCIPAL = "#f0f0f0"
    COLOR_FONDO_SECUNDARIO = "#ffffff"
    COLOR_PRIMARIO = "#0343CE"
    COLOR_BOTON = "#5E90FD"
    COLOR_BOTON_HOVER = "#8CB6FF"
    COLOR_TEXTO_BLANCO = "#ffffff"
    COLOR_TEXTO_PRINCIPAL = "#333333"
    COLOR_MUTED = "gray"

    # Fuentes estándar y variaciones
    FUENTE_GRANDE = ("Arial", 18, "bold")
    FUENTE_TITULO = ("Arial", 16, "bold")
    FUENTE_SUBTITULO = ("Arial", 12, "bold")
    FUENTE_NORMAL_NEGRITA = ("Arial", 12, "bold")
    FUENTE_NORMAL_GRANDE = ("Arial", 12)
    FUENTE_NORMAL = ("Arial", 10)
    FUENTE_PEQUENA = ("Arial", 8)

    # Espaciados y Márgenes
    ESPACIADO_PEQUENO = 5
    ESPACIADO_MEDIO = 10
    ESPACIADO_GRANDE = 20

    # Márgenes y Paddings derivados
    PADDING_GENERAL = ESPACIADO_MEDIO
    PADDING_X_BOTONES = ESPACIADO_PEQUENO
    PADDING_Y_FRAME = ESPACIADO_MEDIO
    MARGIN_X_ENTRIES = ESPACIADO_MEDIO
    MARGIN_Y_LABELS = ESPACIADO_PEQUENO


# ==============================================================================
# SECCIÓN 2: ESTILOS PARA LA VENTANA PRINCIPAL Y ACCESO
# ==============================================================================

class EstilosVentanaPrincipal:
    # Colores
    COLOR_BOTON_PRINCIPAL = "#5E90FD"
    COLOR_BOTON_PRINCIPAL_ACTIVO = "#8CB6FF"
    
    # Fuentes específicas de acceso y menús
    FUENTE_BIENVENIDA = ("Arial", 22, "bold")
    FUENTE_SUBTITULO_BIENVENIDA = ("Arial", 16)
    FUENTE_MENU_TITULO = ("Arial", 22, "bold")
    FUENTE_MENU_SUBTITULO = ("Arial", 16)


# ==============================================================================
# SECCIÓN 3: ESTILOS PARA DIÁLOGOS MODALES Y FORMULARIOS
# ==============================================================================

class EstilosDialogo:
    # Fuentes y estilos específicos para los elementos internos de los diálogos
    FUENTE_DETALLE_PACIENTE = ("Arial", 12, "bold")
    FUENTE_TITULO_PACIENTE = ("Arial", 14, "bold")
    
    # Nombres de estilos de ttk
    ESTILO_MARCO = "Dialog.TFrame"
    ESTILO_ETIQUETA = "Dialog.TLabel"
    ESTILO_MARCO_ETIQUETA = "Dialog.TLabelframe"
    ESTILO_MARCO_ETIQUETA_TITULO = "Dialog.TLabelframe.Label"
    
    @classmethod
    def aplicar_estilos_ttk(cls, style: ttk.Style):
        """Aplica los estilos uniformes de los diálogos en ttk.Style."""
        style.configure(cls.ESTILO_MARCO, background=TemaApp.COLOR_FONDO_SECUNDARIO)
        style.configure(cls.ESTILO_ETIQUETA, background=TemaApp.COLOR_FONDO_SECUNDARIO, foreground=TemaApp.COLOR_TEXTO_PRINCIPAL)
        style.configure(cls.ESTILO_MARCO_ETIQUETA, background=TemaApp.COLOR_FONDO_SECUNDARIO)
        style.configure(cls.ESTILO_MARCO_ETIQUETA_TITULO, background=TemaApp.COLOR_FONDO_SECUNDARIO, foreground=TemaApp.COLOR_PRIMARIO, font=TemaApp.FUENTE_SUBTITULO)


# ==============================================================================
# SECCIÓN 4: ESTILOS PARA LA VISTA DE ANÁLISIS DE TENSIÓN
# ==============================================================================

class EstilosAnalisis:
    # Colores de fondo de tarjetas y cabeceras
    COLOR_CARD_BG = "#1A56E8"
    COLOR_CARD_VALOR = "#FFFFFF"
    COLOR_CARD_LABEL = "#BDD4FF"
    COLOR_HEADER_BG = "#0F3BAA"
    COLOR_LAST_BG = "#0F3BAA"
    COLOR_SEPARADOR = "#2E5FDF"

    # Colores de acento para la valoración en rango
    COLOR_ACCENT_GREEN = "#22C55E"
    COLOR_ACCENT_ORANGE = "#F97316"
    COLOR_ACCENT_RED = "#EF4444"

    # Fuentes específicas del Dashboard
    FUENTE_CARD_LABEL = ("Arial", 9, "bold")
    FUENTE_CARD_VALOR = ("Arial", 18, "bold")
    FUENTE_SECCION_TITULO = ("Arial", 12, "bold")
    FUENTE_ULTIMA_VALOR = ("Arial", 14, "bold")
    FUENTE_PANEL_TITULO = ("Arial", 16, "bold")
    FUENTE_FILTRO_LABEL = ("Arial", 10, "bold")
    FUENTE_FILTRO_INPUT = ("Arial", 10)


# ==============================================================================
# SECCIÓN 5: COMPONENTES GRÁFICOS REUTILIZABLES (WIDGETS DE UI)
# ==============================================================================

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
