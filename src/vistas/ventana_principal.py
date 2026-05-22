import tkinter as tk
from tkinter import ttk

from vistas.paciente_vista import PacienteVista
from vistas.tension_vista import TensionVista
from vistas.paciente_detalle_vista import PacienteDetalleVista
from vistas.tension_analisis_vista import TensionAnalisisVista
from vistas.lista_espera_vista import ListaEsperaVista
from vistas.medico_vista import MedicoVista
from vistas.enfermero_vista import EnfermeroVista
from estilos import TemaApp, BotonPrincipal, EstilosVentanaPrincipal

class VentanaPrincipal:
    def __init__(self, root, contenedor):
        self.root = root
        self.contenedor = contenedor
        self.root.title("App de Salud - Pacientes y Tensiones")
        self.root.geometry("800x500")

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        bg_color = TemaApp.COLOR_PRIMARIO
        btn_color = EstilosVentanaPrincipal.COLOR_BOTON_PRINCIPAL
        fg_color = TemaApp.COLOR_TEXTO_BLANCO

        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", font=TemaApp.FUENTE_NORMAL, padding=TemaApp.PADDING_GENERAL, background=btn_color, foreground=fg_color, relief="raised", borderwidth=3)
        style.map("TButton", background=[("active", EstilosVentanaPrincipal.COLOR_BOTON_PRINCIPAL_ACTIVO)])

        style.configure("Treeview", background=TemaApp.COLOR_FONDO_SECUNDARIO, foreground=TemaApp.COLOR_TEXTO_PRINCIPAL, fieldbackground=TemaApp.COLOR_FONDO_SECUNDARIO)
        style.configure("Treeview.Heading", background=btn_color, foreground=TemaApp.COLOR_TEXTO_BLANCO, font=TemaApp.FUENTE_NORMAL)

        self.role_frame = None
        self.main_menu_frame = None
        self.current_view_frame = None

        self.show_role_selector()

    def show_role_selector(self):
        self.root.geometry("800x500")
        if self.current_view_frame:
            self.current_view_frame.destroy()
            self.current_view_frame = None
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None
        if self.role_frame:
            self.role_frame.destroy()
            self.role_frame = None

        self.role_frame = ttk.Frame(self.root, padding="20 20 20 20")

        lbl_welcome = ttk.Label(self.role_frame, text="¡Bienvenid@!", font=EstilosVentanaPrincipal.FUENTE_BIENVENIDA)
        lbl_select = ttk.Label(self.role_frame, text="Seleccione su rol de acceso:", font=EstilosVentanaPrincipal.FUENTE_SUBTITULO_BIENVENIDA)

        button_frame = ttk.Frame(self.role_frame)

        btn_admin = BotonPrincipal(button_frame, text="Administrador", command=self.select_admin, width=30)
        btn_medico = BotonPrincipal(button_frame, text="Médico", command=self.select_medico, width=30)
        btn_enfermero = BotonPrincipal(button_frame, text="Enfermero", command=self.select_enfermero, width=30)

        self.role_frame.pack(fill=tk.BOTH, expand=True)

        lbl_welcome.pack(pady=(40, 10))
        lbl_select.pack(pady=(0, 40))

        button_frame.pack(pady=10)

        btn_admin.pack(pady=10)
        btn_medico.pack(pady=10)
        btn_enfermero.pack(pady=10)

    def select_admin(self):
        self.show_main_menu()

    def select_medico(self):
        if self.role_frame:
            self.role_frame.destroy()
            self.role_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.root.geometry("1000x600")
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        MedicoVista(
            self.current_view_frame,
            al_salir=self.show_role_selector,
            controlador_lista=self.contenedor.lista_controlador,
            controlador_paciente=self.contenedor.paciente_controlador,
            controlador_tension=self.contenedor.tension_controlador
        )

    def select_enfermero(self):
        if self.role_frame:
            self.role_frame.destroy()
            self.role_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.root.geometry("1000x600")
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        EnfermeroVista(
            self.current_view_frame,
            al_salir=self.show_role_selector,
            controlador_lista=self.contenedor.lista_controlador,
            controlador_tension=self.contenedor.tension_controlador
        )

    def show_main_menu(self):
        self.root.geometry("800x550")
        if self.role_frame:
            self.role_frame.destroy()
            self.role_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()
            self.current_view_frame = None
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None

        self.main_menu_frame = ttk.Frame(self.root, padding="20 20 20 20")

        lbl_welcome = ttk.Label(self.main_menu_frame, text="¡Bienvenid@, Administrador!", font=EstilosVentanaPrincipal.FUENTE_MENU_TITULO)
        lbl_title = ttk.Label(self.main_menu_frame, text="Menú de Administración", font=EstilosVentanaPrincipal.FUENTE_MENU_SUBTITULO)

        button_frame = ttk.Frame(self.main_menu_frame)

        btn_pacientes = BotonPrincipal(button_frame, text="Pacientes", command=self.open_pacientes, width=30)
        btn_tensiones = BotonPrincipal(button_frame, text="Tensiones", command=self.open_tensiones, width=30)
        btn_lista = BotonPrincipal(button_frame, text="Lista de Espera", command=self.open_lista, width=30)
        btn_logout = BotonPrincipal(button_frame, text="🚪 Cambiar Rol", command=self.show_role_selector, width=30)

        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        lbl_welcome.pack(pady=(30, 10))
        lbl_title.pack(pady=(0, 25))

        button_frame.pack(pady=10)

        btn_pacientes.pack(pady=8)
        btn_tensiones.pack(pady=8)
        btn_lista.pack(pady=8)
        btn_logout.pack(pady=8)

    def open_pacientes(self):
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.root.geometry("1100x650")
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        PacienteVista(
            self.current_view_frame,
            al_volver=self.show_main_menu,
            al_abrir_detalle=self.open_paciente_detail,
            controlador=self.contenedor.paciente_controlador
        )

    def open_paciente_detail(self, paciente_valores):
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        PacienteDetalleVista(
            self.current_view_frame,
            valores_paciente=paciente_valores,
            al_volver=self.open_pacientes,
            al_abrir_analisis=self.open_tension_analisis,
            controlador=self.contenedor.paciente_controlador
        )

    def open_tension_analisis(self, paciente_valores):
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        al_back = lambda: self.open_paciente_detail(paciente_valores)
        TensionAnalisisVista(
            self.current_view_frame,
            valores_paciente=paciente_valores,
            al_volver=al_back,
            controlador=self.contenedor.tension_controlador
        )

    def open_tensiones(self):
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.root.geometry("1100x650")
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        TensionVista(
            self.current_view_frame,
            al_volver=self.show_main_menu,
            controlador_tension=self.contenedor.tension_controlador,
            controlador_paciente=self.contenedor.paciente_controlador
        )

    def open_lista(self):
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()

        self.root.geometry("1100x650")
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        ListaEsperaVista(
            self.current_view_frame,
            al_volver=self.show_main_menu,
            controlador_lista=self.contenedor.lista_controlador,
            controlador_paciente=self.contenedor.paciente_controlador
        )
