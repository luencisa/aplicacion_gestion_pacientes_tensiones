import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata
from datetime import datetime
from pydantic import ValidationError

from estilos import TemaApp, TituloPrincipal, BotonVista
from vistas.componentes.tabla_base import TablaBase
from vistas.componentes.dialogo_base import DialogoBase
from controladores.paciente_controlador import PacienteControlador
from esquemas.paciente_input import PacienteInput

class PacienteVista:
    def __init__(self, parent_frame, al_volver, al_abrir_detalle=None, controlador: PacienteControlador = None):
        self.parent_frame = parent_frame
        self.al_volver = al_volver
        self.al_abrir_detalle = al_abrir_detalle
        self.controlador = controlador

        # Crear widgets
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Título
        lbl_titulo = TituloPrincipal(self.parent_frame, text="Gestión de Pacientes")
        lbl_titulo.pack(pady=TemaApp.PADDING_Y_FRAME)

        # Botonera superior
        frame_controles = ttk.Frame(self.parent_frame, padding="10")
        frame_controles.pack(fill=tk.X)

        btn_volver = BotonVista(frame_controles, text="⬅ Volver Atrás", command=self.al_volver)
        btn_detalle = BotonVista(frame_controles, text="🗂 Ver Ficha", command=self.abrir_detalle)
        btn_alta = BotonVista(frame_controles, text="➕ Alta", command=self.alta_paciente)
        btn_modificar = BotonVista(frame_controles, text="✏️ Modificar", command=self.modificar_paciente)
        btn_baja = BotonVista(frame_controles, text="🗑 Baja", command=self.baja_paciente)
        btn_refrescar = BotonVista(frame_controles, text="🔄 Refrescar", command=self.cargar_datos)

        btn_volver.pack(side=tk.LEFT, padx=4)
        btn_detalle.pack(side=tk.LEFT, padx=4)
        btn_alta.pack(side=tk.LEFT, padx=4)
        btn_modificar.pack(side=tk.LEFT, padx=4)
        btn_baja.pack(side=tk.LEFT, padx=4)
        btn_refrescar.pack(side=tk.RIGHT, padx=4)

        # Buscador
        frame_busqueda = ttk.Frame(self.parent_frame, padding="5")
        frame_busqueda.pack(fill=tk.X, pady=(5, 10))

        lbl_buscar = ttk.Label(frame_busqueda, text="Buscar paciente:")
        lbl_buscar.pack(side=tk.LEFT, padx=5)

        self.entry_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.entry_busqueda.bind("<Return>", lambda e: self.ejecutar_busqueda())
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)

        btn_buscar = BotonVista(frame_busqueda, text="Buscar", command=self.ejecutar_busqueda)
        btn_buscar.pack(side=tk.LEFT, padx=5)

        btn_limpiar = BotonVista(frame_busqueda, text="Limpiar", command=self.limpiar_busqueda)
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Tabla Reutilizable
        columnas = ("id", "nombre", "apellido", "genero", "fecha_nacimiento")
        cabeceras = {
            "id": "ID",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "genero": "Género",
            "fecha_nacimiento": "Fecha de Nacimiento"
        }
        columnas_visibles = ("nombre", "apellido", "genero", "fecha_nacimiento")
        anchos = {
            "id": 0,
            "nombre": 150,
            "apellido": 180,
            "genero": 100,
            "fecha_nacimiento": 150
        }

        self.tabla = TablaBase(
            self.parent_frame,
            columnas=columnas,
            cabeceras=cabeceras,
            columnas_visibles=columnas_visibles,
            anchos=anchos
        )
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def ejecutar_busqueda(self):
        query = self.entry_busqueda.get()
        self.cargar_datos(busqueda=query)

    def limpiar_busqueda(self):
        self.entry_busqueda.delete(0, tk.END)
        self.cargar_datos()

    def cargar_datos(self, busqueda=""):
        self.tabla.vaciar()
        pacientes = self.controlador.obtener_pacientes()

        def quitar_acentos(texto):
            return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

        clean_query = quitar_acentos(busqueda.lower()).strip()
        query_words = clean_query.split()

        for p in pacientes:
            nombre = p.get("nombre", "")
            apellido = p.get("apellido", "")

            if query_words:
                full_name = quitar_acentos(f"{nombre} {apellido}".lower())
                if not all(word in full_name for word in query_words):
                    continue

            fecha_nac = p.get("fechaNacimiento", "")
            if hasattr(fecha_nac, "strftime"):
                fecha_nac = fecha_nac.strftime("%Y-%m-%d")
            elif isinstance(fecha_nac, dict) and "$date" in fecha_nac:
                fecha_nac = str(fecha_nac["$date"]).split("T")[0]
            elif isinstance(fecha_nac, str) and "T" in fecha_nac:
                fecha_nac = fecha_nac.split("T")[0]
            elif isinstance(fecha_nac, str) and " " in fecha_nac:
                fecha_nac = fecha_nac.split(" ")[0]
            else:
                fecha_nac = str(fecha_nac)

            self.tabla.insertar_fila(valores=(
                p.get("_id", ""),
                p.get("nombre", ""),
                p.get("apellido", ""),
                p.get("género", ""),
                fecha_nac
            ))

    def alta_paciente(self):
        self.abrir_formulario()

    def modificar_paciente(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Atención", "Seleccione un paciente para modificar.")
            return
        self.abrir_formulario(valores)

    def baja_paciente(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Atención", "Seleccione un paciente para dar de baja.")
            return

        paciente_id = valores[0]
        nombre_completo = f"{valores[1]} {valores[2]}"

        pregunta = f"¿Dar de baja al paciente {nombre_completo}? Se eliminarán también todas sus tomas de tensión asociadas."
        if messagebox.askyesno("Confirmar", pregunta):
            try:
                if self.controlador.eliminar_paciente(paciente_id):
                    messagebox.showinfo("Éxito", "Paciente y sus tomas de tensión eliminados correctamente.")
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "No se pudo dar de baja al paciente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar paciente: {e}")

    def abrir_detalle(self):
        if not self.al_abrir_detalle:
            return
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Atención", "Seleccione un paciente para ver su ficha.")
            return
        self.al_abrir_detalle(valores)

    def abrir_formulario(self, valores=None):
        titulo = "Alta de Paciente" if valores is None else "Modificar Paciente"
        form = DialogoBase(self.parent_frame, title=titulo, geometry="380x450")

        lbl_nombre = ttk.Label(form, text="Nombre:")
        entry_nombre = tk.Entry(form)

        lbl_apellido = ttk.Label(form, text="Apellido:")
        entry_apellido = tk.Entry(form)

        lbl_genero = ttk.Label(form, text="Género (FHIR):")
        entry_genero = ttk.Combobox(form, values=["male", "female", "other", "unknown"], state="readonly")

        lbl_fecha = ttk.Label(form, text="Fecha de Nacimiento:")
        lbl_fecha_ayuda = ttk.Label(form, text="(Formato: YYYY-MM-DD)", font=TemaApp.FUENTE_PEQUENA)
        entry_fecha = tk.Entry(form)

        # Empaquetado
        lbl_nombre.pack(pady=(15, 2))
        entry_nombre.pack(fill=tk.X, padx=20)

        lbl_apellido.pack(pady=(10, 2))
        entry_apellido.pack(fill=tk.X, padx=20)

        lbl_genero.pack(pady=(10, 2))
        entry_genero.pack(fill=tk.X, padx=20)

        lbl_fecha.pack(pady=(10, 2))
        lbl_fecha_ayuda.pack()
        entry_fecha.pack(fill=tk.X, padx=20)

        # Pre-rellenar en caso de modificación
        if valores:
            entry_nombre.insert(0, valores[1])
            entry_apellido.insert(0, valores[2])
            entry_genero.set(valores[3])
            entry_fecha.insert(0, valores[4])
            paciente_id = valores[0]

        def guardar():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            genero = entry_genero.get()
            fecha = entry_fecha.get().strip()

            if fecha:
                try:
                    dt = datetime.strptime(fecha, "%Y-%m-%d")
                    if dt.date() > datetime.now().date():
                        messagebox.showerror("Error de Validación", "La fecha de nacimiento no puede ser en el futuro.")
                        return
                except ValueError:
                    messagebox.showerror("Error de Validación", "La fecha debe estar en formato YYYY-MM-DD.")
                    return

            try:
                paciente_in = PacienteInput(
                    nombre=nombre,
                    apellido=apellido,
                    género=genero,
                    fechaNacimiento=fecha
                )
            except ValidationError as e:
                err_msg = e.errors()[0]['msg']
                messagebox.showerror("Error de Validación", f"Datos incorrectos: {err_msg}")
                return

            try:
                if valores:
                    self.controlador.actualizar_paciente(paciente_id, paciente_in)
                    messagebox.showinfo("Éxito", "Paciente modificado con éxito.")
                else:
                    self.controlador.agregar_paciente(paciente_in)
                    messagebox.showinfo("Éxito", "Paciente registrado con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el paciente: {e}")
                return

            form.destroy()
            self.cargar_datos()

        BotonVista(form, text="💾 Guardar", command=guardar).pack(pady=25)
