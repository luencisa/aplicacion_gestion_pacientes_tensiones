import tkinter as tk
from tkinter import ttk
from controllers.tension_controller import TensionController
from estilos import TemaApp, TituloPrincipal, TituloSecundario, BotonVista

class PacienteDetailView:
    def __init__(self, parent_frame, paciente_values, on_back, db_connection=None):
        self.parent_frame = parent_frame
        self.paciente_values = paciente_values
        self.on_back = on_back
        self.db_connection = db_connection
        self.tension_controller = TensionController(self.db_connection)
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # 1. Creación de Frames
        frame_top = ttk.Frame(self.parent_frame, padding="10")
        frame_info = ttk.Frame(self.parent_frame, padding="20")

        # 2. Creación de widgets (Frame superior)
        btn_back = BotonVista(frame_top, text="⬅ Volver a Pacientes", command=self.on_back)

        # 3. Creación de widgets (Panel de Información)
        title = f"Ficha Clínica: {self.paciente_values[1]} {self.paciente_values[2]}"
        lbl_title = ttk.Label(frame_info, text=title, font=TemaApp.FUENTE_GRANDE)
        
        lbl_genero_tit = TituloSecundario(frame_info, text="Género:")
        lbl_genero_val = ttk.Label(frame_info, text=self.paciente_values[3], font=TemaApp.FUENTE_NORMAL_GRANDE)
        
        lbl_nac_tit = TituloSecundario(frame_info, text="Nacimiento:")
        lbl_nac_val = ttk.Label(frame_info, text=self.paciente_values[4], font=TemaApp.FUENTE_NORMAL_GRANDE)

        # 4. Creación de widgets (Tabla Tensiones)
        lbl_tensiones_tit = TituloPrincipal(self.parent_frame, text="Historial de Tensiones Asociadas")
        
        columns = ("fecha", "sistolica", "diastolica", "valoracion", "en_rango")
        self.tree = ttk.Treeview(self.parent_frame, columns=columns, show="headings")
        
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("sistolica", text="Sistólica")
        self.tree.heading("diastolica", text="Diastólica")
        self.tree.heading("valoracion", text="Valoración")
        self.tree.heading("en_rango", text="En Rango")
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("fecha", width=150, stretch=tk.YES)
        self.tree.column("sistolica", width=100, stretch=tk.YES)
        self.tree.column("diastolica", width=100, stretch=tk.YES)
        self.tree.column("valoracion", width=250, stretch=tk.YES)
        self.tree.column("en_rango", width=100, stretch=tk.YES)

        # ==========================================
        # Geometría
        # ==========================================

        # Geometría de Frames
        frame_top.pack(fill=tk.X)
        frame_info.pack(fill=tk.X, padx=10, pady=10)

        # Geometría Frame superior
        btn_back.pack(side=tk.LEFT, padx=5)

        # Geometría Panel de Información
        lbl_title.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        lbl_genero_tit.grid(row=1, column=0, sticky=tk.W, pady=2)
        lbl_genero_val.grid(row=1, column=1, sticky=tk.W, pady=2, padx=10)
        lbl_nac_tit.grid(row=2, column=0, sticky=tk.W, pady=2)
        lbl_nac_val.grid(row=2, column=1, sticky=tk.W, pady=2, padx=10)

        # Geometría Tabla Tensiones
        lbl_tensiones_tit.pack(pady=TemaApp.PADDING_Y_FRAME)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        paciente_id = self.paciente_values[0]
        # Nuestro backend ya permite esto porque le programamos el filtro en el DAO
        tensiones = self.tension_controller.get_tensiones(paciente_id)
        
        for t in tensiones:
            valores = t.get("valores", {})
            fecha = t.get("fecha", "")
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%Y-%m-%d")
            elif isinstance(fecha, dict) and "$date" in fecha:
                fecha = str(fecha["$date"]).split("T")[0]
            elif isinstance(fecha, str) and "T" in fecha:
                fecha = fecha.split("T")[0]
            elif isinstance(fecha, str) and " " in fecha:
                fecha = fecha.split(" ")[0]
            else:
                fecha = str(fecha)
                
            self.tree.insert("", tk.END, values=(
                fecha,
                valores.get("sistolica", ""),
                valores.get("diastolica", ""),
                t.get("valoracion", ""),
                "Sí" if t.get("valor_en_rango", False) else "No"
            ))
