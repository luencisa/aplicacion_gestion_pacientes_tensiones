import tkinter as tk
from tkinter import ttk
from views.pacientes_view import PacientesView
from views.tensiones_view import TensionesView
from views.paciente_detail_view import PacienteDetailView
from estilos import TemaApp, BotonPrincipal

class MainWindow:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection
        self.root.title("App de Salud - Pacientes y Tensiones")
        self.root.geometry("800x500") # Tamaño más compacto para la ventana principal
        
        # Estilos Generales
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
            
        bg_color = TemaApp.COLOR_PRIMARIO
        btn_color = "#5E90FD"
        fg_color = TemaApp.COLOR_TEXTO_BLANCO

        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", font=TemaApp.FUENTE_NORMAL, padding=TemaApp.PADDING_GENERAL, background=btn_color, foreground=fg_color, relief="raised", borderwidth=3)
        style.map("TButton", background=[("active", "#8CB6FF")]) # Color más claro al pasar el ratón
        
        style.configure("Treeview", background=TemaApp.COLOR_FONDO_SECUNDARIO, foreground=TemaApp.COLOR_TEXTO_PRINCIPAL, fieldbackground=TemaApp.COLOR_FONDO_SECUNDARIO)
        style.configure("Treeview.Heading", background=btn_color, foreground=TemaApp.COLOR_TEXTO_BLANCO, font=TemaApp.FUENTE_NORMAL)
        
        self.main_menu_frame = None
        self.current_view_frame = None
        
        self.show_main_menu()

    def show_main_menu(self):
        # Limpiamos la vista actual si volvemos atrás
        if self.current_view_frame:
            self.current_view_frame.destroy()
            self.current_view_frame = None
            
        # ==========================================
        # Creación de Frames y Widgets
        # ==========================================
        
        self.main_menu_frame = ttk.Frame(self.root, padding="20 20 20 20")
        
        lbl_welcome = ttk.Label(self.main_menu_frame, text="¡Bienvenid@!", font=("Arial", 24, "bold"))
        lbl_title = ttk.Label(self.main_menu_frame, text="Menú Principal", font=("Arial", 18))
        
        button_frame = ttk.Frame(self.main_menu_frame)
        
        btn_pacientes = BotonPrincipal(button_frame, text="Pacientes", command=self.open_pacientes, width=30)
        btn_tensiones = BotonPrincipal(button_frame, text="Tensiones", command=self.open_tensiones, width=30)

        # ==========================================
        # Geometría
        # ==========================================
        
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)
        
        lbl_welcome.pack(pady=(40, 10))
        lbl_title.pack(pady=(0, 40))

        button_frame.pack(pady=20)
        
        btn_pacientes.pack(pady=10)
        btn_tensiones.pack(pady=10)

    def open_pacientes(self):
        if self.main_menu_frame:
            self.main_menu_frame.destroy()
            self.main_menu_frame = None
        if self.current_view_frame:
            self.current_view_frame.destroy()
            
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        # Pasamos el callback on_back para poder regresar
        PacientesView(self.current_view_frame, on_back=self.show_main_menu, on_open_detail=self.open_paciente_detail, db_connection=self.db_connection)

    def open_paciente_detail(self, paciente_values):
        if self.current_view_frame:
            self.current_view_frame.destroy()
            
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        PacienteDetailView(self.current_view_frame, paciente_values, on_back=self.open_pacientes, db_connection=self.db_connection)

    def open_tensiones(self):
        self.main_menu_frame.destroy()
        self.main_menu_frame = None
        
        self.current_view_frame = ttk.Frame(self.root)
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
        TensionesView(self.current_view_frame, on_back=self.show_main_menu, db_connection=self.db_connection)
