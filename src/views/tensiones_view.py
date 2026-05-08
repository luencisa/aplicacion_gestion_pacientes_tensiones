import tkinter as tk
from tkinter import ttk, messagebox
from controllers.tension_controller import TensionController
from controllers.paciente_controller import PacienteController
from estilos import TemaApp, TituloPrincipal, BotonVista

class TensionesView:
    def __init__(self, parent_frame, on_back, db_connection=None):
        self.parent_frame = parent_frame
        self.on_back = on_back
        self.db_connection = db_connection
        self.controller = TensionController(self.db_connection)
        # Se requiere para validaciones de pacientes en altas de tensión
        self.paciente_controller = PacienteController(self.db_connection)
        
        lbl_title = TituloPrincipal(self.parent_frame, text="Gestión de Tensiones")
        lbl_title.pack(pady=TemaApp.PADDING_Y_FRAME)
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # ==========================================
        # Creación de Frames y Widgets
        # ==========================================
        
        frame_controls = ttk.Frame(self.parent_frame, padding="10")
        
        # Botones
        btn_back = BotonVista(frame_controls, text="⬅ Volver Atrás", command=self.on_back)
        btn_add = BotonVista(frame_controls, text="Añadir Tensión", command=self.add_tension)
        btn_edit = BotonVista(frame_controls, text="Editar Tensión", command=self.edit_tension)
        btn_delete = BotonVista(frame_controls, text="Eliminar Tensión", command=self.delete_tension)
        btn_refresh = BotonVista(frame_controls, text="Refrescar", command=self.load_data)
        
        # Treeview
        columns = ("id", "id_paciente", "sistolica", "diastolica", "estado", "fecha", "valoracion", "en_rango")
        self.tree = ttk.Treeview(self.parent_frame, columns=columns, show="headings")
        self.tree["displaycolumns"] = ("id_paciente", "sistolica", "diastolica", "estado", "fecha", "valoracion", "en_rango")
        widths = [150, 150, 80, 80, 100, 150, 150, 80]
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        for i, col in enumerate(columns):
            if col in ("id_paciente", "sistolica", "diastolica", "estado", "valoracion", "en_rango"):
                self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.treeview_sort_column(c, False))
            elif col == "fecha":
                self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.treeview_sort_column(c, True))
            else:
                self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=widths[i], stretch=tk.YES)
            
        # ==========================================
        # Geometría
        # ==========================================
        
        frame_controls.pack(fill=tk.X)
        
        btn_back.pack(side=tk.LEFT, padx=5)
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_edit.pack(side=tk.LEFT, padx=5)
        btn_delete.pack(side=tk.LEFT, padx=5)
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        tensiones = self.controller.get_tensiones()
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
                t.get("_id", ""),
                t.get("id_paciente", ""),
                valores.get("sistolica", ""),
                valores.get("diastolica", ""),
                t.get("estado", ""),
                fecha,
                t.get("valoracion", ""),
                "Sí" if t.get("valor_en_rango", False) else "No"
            ))

    def add_tension(self):
        self.open_form()

    def edit_tension(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona una tensión para editar.")
            return
        values = self.tree.item(selected, "values")
        self.open_form(values)

    def delete_tension(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona una tensión para eliminar.")
            return
        values = self.tree.item(selected, "values")
        tension_id = values[0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar tensión con ID {tension_id}?"):
            if self.controller.delete_tension(tension_id):
                messagebox.showinfo("Éxito", "Tensión eliminada.")
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tensión.")

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        if col in ("sistolica", "diastolica"):
            try:
                l.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
            except ValueError:
                l.sort(key=lambda t: t[0].lower(), reverse=reverse)
        else:
            # Para fechas en formato YYYY-MM-DD y strings normales, la ordenación alfabética funciona perfecto
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)
            
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
            
        # Invertimos la acción para el siguiente clic
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def open_form(self, values=None):
        form = tk.Toplevel(self.parent_frame)
        form.title("Tensión" if values is None else "Editar Tensión")
        form.geometry("400x550")
        form.grab_set()
        form.configure(bg=TemaApp.COLOR_PRIMARIO)

        # ==========================================
        # Creación de Widgets
        # ==========================================
        
        fields = [
            ("ID Paciente:", "id_paciente"),
            ("Sistólica:", "sistolica"),
            ("Diastólica:", "diastolica"),
            ("Estado (ej. final):", "estado"),
            ("Fecha:", "fecha"),
            ("Valoración:", "valoracion"),
        ]
        
        entries = {}
        labels = {}
        for label_text, key in fields:
            lbl = ttk.Label(form, text=label_text)
            entry = tk.Entry(form)
            labels[key] = lbl
            entries[key] = entry
            
        var_rango = tk.BooleanVar()
        chk_rango = tk.Checkbutton(form, text="Valor en rango", variable=var_rango, bg=TemaApp.COLOR_PRIMARIO, fg=TemaApp.COLOR_TEXTO_BLANCO, selectcolor=TemaApp.COLOR_PRIMARIO)
        
        # ==========================================
        # Geometría
        # ==========================================
        
        for key in [f[1] for f in fields]:
            labels[key].pack(pady=2)
            entries[key].pack(fill=tk.X, padx=10)
            
        chk_rango.pack(pady=TemaApp.PADDING_Y_FRAME)
        
        if values:
            entries["id_paciente"].insert(0, values[1])
            entries["id_paciente"].config(state='disabled') # Cambiar paciente de una misma tensión no se suele hacer
            entries["sistolica"].insert(0, values[2])
            entries["diastolica"].insert(0, values[3])
            entries["estado"].insert(0, values[4])
            entries["fecha"].insert(0, values[5])
            entries["valoracion"].insert(0, values[6])
            var_rango.set(values[7] == 'Sí')
            tension_id = values[0]
            
        def save():
            id_paciente = entries["id_paciente"].get()
            sistolica = entries["sistolica"].get()
            diastolica = entries["diastolica"].get()
            estado = entries["estado"].get()
            fecha = entries["fecha"].get()
            valoracion = entries["valoracion"].get()
            en_rango = var_rango.get()
            
            if fecha:
                from datetime import datetime
                try:
                    dt = datetime.strptime(fecha, "%Y-%m-%d")
                    if dt.date() > datetime.now().date():
                        messagebox.showerror("Error", "La fecha no puede ser en el futuro.")
                        return
                except ValueError:
                    pass
            
            if not values: # Es un alta, validamos que el paciente exista
                paciente = self.paciente_controller.get_paciente(id_paciente)
                if not paciente:
                    messagebox.showerror("Error", "El ID de paciente indicado no existe en la base de datos.")
                    return

            from esquemas.tension_input import TensionInput
            from esquemas.tension_update_input import TensionUpdateInput
            from esquemas.tension_valores import TensionValores
            from pydantic import ValidationError
            
            try:
                if values:
                    tension_in = TensionUpdateInput(
                        valores=TensionValores(sistolica=int(sistolica), diastolica=int(diastolica)),
                        estado=estado,
                        fecha=fecha,
                        valoracion=valoracion,
                        valor_en_rango=en_rango
                    )
                else:
                    tension_in = TensionInput(
                        id_paciente=id_paciente,
                        valores=TensionValores(sistolica=int(sistolica), diastolica=int(diastolica)),
                        estado=estado,
                        fecha=fecha,
                        valoracion=valoracion,
                        valor_en_rango=en_rango
                    )
            except ValidationError as e:
                err_msg = e.errors()[0]['msg']
                messagebox.showerror("Error de Validación", f"Datos inválidos: {err_msg}")
                return
            except ValueError:
                messagebox.showerror("Error de Validación", "Los valores de sistólica y diastólica deben ser números enteros.")
                return

            try:
                if values:
                    self.controller.update_tension(tension_id, tension_in)
                    messagebox.showinfo("Éxito", "Tensión modificada.")
                else:
                    self.controller.add_tension(tension_in)
                    messagebox.showinfo("Éxito", "Tensión agregada.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            
            form.destroy()
            self.load_data()
            
        BotonVista(form, text="Guardar", command=save).pack(pady=20)
