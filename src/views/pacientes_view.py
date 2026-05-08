import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata
from controllers.paciente_controller import PacienteController
from estilos import TemaApp, TituloPrincipal, BotonVista

class PacientesView:
    def __init__(self, parent_frame, on_back, on_open_detail=None, db_connection=None):
        self.parent_frame = parent_frame
        self.on_back = on_back
        self.on_open_detail = on_open_detail
        self.db_connection = db_connection
        self.controller = PacienteController(self.db_connection)
        
        lbl_title = TituloPrincipal(self.parent_frame, text="Gestión de Pacientes")
        lbl_title.pack(pady=TemaApp.PADDING_Y_FRAME)
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # ==========================================
        # Creación de Frames y Widgets
        # ==========================================
        
        # --- Controles Superiores ---
        frame_controls = ttk.Frame(self.parent_frame, padding="10")
        
        btn_back = BotonVista(frame_controls, text="⬅ Volver Atrás", command=self.on_back)
        btn_detail = BotonVista(frame_controls, text="Ver Ficha", command=self.open_detail)
        btn_add = BotonVista(frame_controls, text="Alta Paciente", command=self.add_paciente)
        btn_edit = BotonVista(frame_controls, text="Modificar Paciente", command=self.edit_paciente)
        btn_delete = BotonVista(frame_controls, text="Baja Paciente", command=self.delete_paciente)
        btn_refresh = BotonVista(frame_controls, text="Refrescar", command=self.load_data)
        
        # --- Buscador ---
        frame_search = ttk.Frame(self.parent_frame, padding="5")
        
        lbl_search = ttk.Label(frame_search, text="Buscar paciente:")
        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.bind("<Return>", lambda e: self.perform_search())
        
        btn_search = BotonVista(frame_search, text="Buscar", command=self.perform_search)
        btn_clear = BotonVista(frame_search, text="Limpiar", command=self.clear_search)
        
        # --- Treeview ---
        columns = ("id", "nombre", "apellido", "genero", "fecha_nacimiento")
        self.tree = ttk.Treeview(self.parent_frame, columns=columns, show="headings")
        self.tree["displaycolumns"] = ("nombre", "apellido", "genero", "fecha_nacimiento")
        
        self.tree.heading("id", text="ID", command=lambda: self.treeview_sort_column("id", False))
        self.tree.heading("nombre", text="Nombre", command=lambda: self.treeview_sort_column("nombre", False))
        self.tree.heading("apellido", text="Apellido", command=lambda: self.treeview_sort_column("apellido", False))
        self.tree.heading("genero", text="Género", command=lambda: self.treeview_sort_column("genero", False))
        self.tree.heading("fecha_nacimiento", text="Fecha de Nacimiento", command=lambda: self.treeview_sort_column("fecha_nacimiento", False))
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=220)
        self.tree.column("nombre", width=120, stretch=tk.YES)
        self.tree.column("apellido", width=150, stretch=tk.YES)
        self.tree.column("genero", width=100, stretch=tk.YES)
        self.tree.column("fecha_nacimiento", width=150, stretch=tk.YES)
        
        # ==========================================
        # Geometría
        # ==========================================
        
        # Controles
        frame_controls.pack(fill=tk.X)
        btn_back.pack(side=tk.LEFT, padx=5)
        btn_detail.pack(side=tk.LEFT, padx=5)
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_edit.pack(side=tk.LEFT, padx=5)
        btn_delete.pack(side=tk.LEFT, padx=5)
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        # Buscador
        frame_search.pack(fill=tk.X, pady=(5, 10))
        lbl_search.pack(side=tk.LEFT, padx=5)
        self.entry_search.pack(side=tk.LEFT, padx=5)
        btn_search.pack(side=tk.LEFT, padx=5)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def perform_search(self):
        query = self.entry_search.get()
        self.load_data(search_query=query)
        
    def clear_search(self):
        self.entry_search.delete(0, tk.END)
        self.load_data()

    def load_data(self, search_query=""):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Cargar todos los pacientes de la base de datos
        pacientes = self.controller.get_pacientes()
        
        # Función auxiliar para quitar acentos
        def quitar_acentos(texto):
            return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
            
        clean_query = quitar_acentos(search_query.lower()).strip()
        query_words = clean_query.split()
        
        for p in pacientes:
            nombre = p.get("nombre", "")
            apellido = p.get("apellido", "")
            
            # Filtro de búsqueda ignorando acentos
            if query_words:
                full_name = quitar_acentos(f"{nombre} {apellido}".lower())
                matches_all = all(word in full_name for word in query_words)
                if not matches_all:
                    continue
            fecha_nac = p.get("fechaNacimiento", "")
            if hasattr(fecha_nac, "strftime"):
                fecha_nac = fecha_nac.strftime("%Y-%m-%d")
            elif isinstance(fecha_nac, dict) and "$date" in fecha_nac:
                fecha_nac = str(fecha_nac["$date"]).split("T")[0]
            elif isinstance(fecha_nac, str) and "T" in fecha_nac:
                fecha_nac = fecha_nac.split("T")[0]
            elif isinstance(fecha_nac, str) and " " in fecha_nac:
                # Caso de str(datetime) pre-parseado
                fecha_nac = fecha_nac.split(" ")[0]
            else:
                fecha_nac = str(fecha_nac)
            self.tree.insert("", tk.END, values=(
                p.get("_id", ""),
                p.get("nombre", ""),
                p.get("apellido", ""),
                p.get("género", "").capitalize(),
                fecha_nac
            ))

    def add_paciente(self):
        self.open_form()

    def edit_paciente(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un paciente para modificar.")
            return
        values = self.tree.item(selected, "values")
        self.open_form(values)

    def delete_paciente(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un paciente para dar de baja.")
            return
        
        values = self.tree.item(selected, "values")
        paciente_id = values[0]
        
        if messagebox.askyesno("Confirmar", f"¿Dar de baja al paciente {values[1]} {values[2]}?"):
            if self.controller.delete_paciente(paciente_id):
                messagebox.showinfo("Éxito", "Paciente borrado.")
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo borrar el paciente.")

    def open_detail(self):
        if not self.on_open_detail:
            return
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un paciente para ver su ficha.")
            return
        values = self.tree.item(selected, "values")
        self.on_open_detail(values)

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        # Intentamos ordenar (las fechas en formato ISO y texto se ordenan bien con string sort habitual)
        l.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        # Invertimos la acción para el siguiente clic
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def open_form(self, values=None):
        form = tk.Toplevel(self.parent_frame)
        form.title("Paciente" if values is None else "Modificar Paciente")
        form.geometry("350x400")
        form.grab_set() # Modal
        
        form.configure(bg=TemaApp.COLOR_PRIMARIO)
        
        # ==========================================
        # Creación de Widgets
        # ==========================================
        
        lbl_nombre = ttk.Label(form, text="Nombre:")
        entry_nombre = tk.Entry(form)
        
        lbl_apellido = ttk.Label(form, text="Apellido:")
        entry_apellido = tk.Entry(form)
        
        lbl_genero = ttk.Label(form, text="Género:")
        entry_genero = ttk.Combobox(form, values=["Masculino", "Femenino"], state="readonly")
        
        lbl_fecha = ttk.Label(form, text="Fecha de Nacimiento:")
        lbl_fecha_ayuda = ttk.Label(form, text="(Ej: 1982-01-15)", font=TemaApp.FUENTE_PEQUENA)
        entry_fecha = tk.Entry(form)
        
        # ==========================================
        # Geometría
        # ==========================================
        
        lbl_nombre.pack(pady=5)
        entry_nombre.pack(fill=tk.X, padx=10)
        
        lbl_apellido.pack(pady=5)
        entry_apellido.pack(fill=tk.X, padx=10)
        
        lbl_genero.pack(pady=5)
        entry_genero.pack(fill=tk.X, padx=10)
        
        lbl_fecha.pack(pady=5)
        lbl_fecha_ayuda.pack()
        entry_fecha.pack(fill=tk.X, padx=10)
        
        if values:
            entry_nombre.insert(0, values[1])
            entry_apellido.insert(0, values[2])
            entry_genero.set(values[3])
            entry_fecha.insert(0, values[4])
            paciente_id = values[0]
            
        def save():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            genero = entry_genero.get()
            fecha = entry_fecha.get()
            
            if fecha:
                from datetime import datetime
                try:
                    dt = datetime.strptime(fecha, "%Y-%m-%d")
                    if dt.date() > datetime.now().date():
                        messagebox.showerror("Error", "La fecha no puede ser en el futuro.")
                        return
                except ValueError:
                    pass
            
            from esquemas.paciente_input import PacienteInput
            from pydantic import ValidationError
            
            try:
                paciente_in = PacienteInput(
                    nombre=nombre,
                    apellido=apellido,
                    género=genero,
                    fechaNacimiento=fecha
                )
            except ValidationError as e:
                # Mostrar el primer error encontrado
                err_msg = e.errors()[0]['msg']
                messagebox.showerror("Error de Validación", f"Datos inválidos: {err_msg}")
                return
            
            try:
                if values:
                    self.controller.update_paciente(paciente_id, paciente_in)
                    messagebox.showinfo("Éxito", "Paciente modificado.")
                else:
                    self.controller.add_paciente(paciente_in)
                    messagebox.showinfo("Éxito", "Paciente agregado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            
            form.destroy()
            self.load_data()
            
        BotonVista(form, text="Guardar", command=save).pack(pady=20)
