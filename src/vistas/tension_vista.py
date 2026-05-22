import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pydantic import ValidationError

from estilos import TemaApp, TituloPrincipal, BotonVista
from vistas.componentes.tabla_base import TablaBase
from vistas.componentes.dialogo_base import DialogoBase
from controladores.tension_controlador import TensionControlador
from controladores.paciente_controlador import PacienteControlador
from esquemas.tension_input import TensionInput
from esquemas.tension_update_input import TensionUpdateInput
from esquemas.tension_valores import TensionValores

class TensionVista:
    def __init__(self, parent_frame, al_volver, controlador_tension: TensionControlador = None, controlador_paciente: PacienteControlador = None):
        self.parent_frame = parent_frame
        self.al_volver = al_volver
        self.controlador_tension = controlador_tension
        self.controlador_paciente = controlador_paciente

        # Título principal de la vista
        lbl_titulo = TituloPrincipal(self.parent_frame, text="Gestión de Tensiones")
        lbl_titulo.pack(pady=TemaApp.PADDING_Y_FRAME)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Contenedor para la botonera
        frame_controles = ttk.Frame(self.parent_frame, padding="10")
        frame_controles.pack(fill=tk.X)

        # Botones de la vista
        btn_volver = BotonVista(frame_controles, text="⬅ Volver Atrás", command=self.al_volver)
        btn_agregar = BotonVista(frame_controles, text="Añadir Tensión", command=self.agregar_tension)
        btn_editar = BotonVista(frame_controles, text="Editar Tensión", command=self.editar_tension)
        btn_eliminar = BotonVista(frame_controles, text="Eliminar Tensión", command=self.eliminar_tension)
        btn_refrescar = BotonVista(frame_controles, text="Refrescar", command=self.cargar_datos)

        btn_volver.pack(side=tk.LEFT, padx=5)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        btn_editar.pack(side=tk.LEFT, padx=5)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_refrescar.pack(side=tk.RIGHT, padx=5)

        # Tabla Reutilizable
        columnas = ("id", "id_paciente", "sistolica", "diastolica", "estado", "fecha", "valoracion", "en_rango")
        cabeceras = {
            "id": "ID",
            "id_paciente": "Paciente",
            "sistolica": "Sistólica",
            "diastolica": "Diastólica",
            "estado": "Estado",
            "fecha": "Fecha",
            "valoracion": "Valoración",
            "en_rango": "En Rango"
        }
        columnas_visibles = ("id_paciente", "sistolica", "diastolica", "estado", "fecha", "valoracion", "en_rango")
        anchos = {
            "id": 0,
            "id_paciente": 150,
            "sistolica": 80,
            "diastolica": 80,
            "estado": 100,
            "fecha": 150,
            "valoracion": 150,
            "en_rango": 80
        }

        self.tabla = TablaBase(
            self.parent_frame,
            columnas=columnas,
            cabeceras=cabeceras,
            columnas_visibles=columnas_visibles,
            anchos=anchos
        )
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_datos(self):
        self.tabla.vaciar()

        # Mapeamos los ID de los pacientes a sus nombres
        pacientes = self.controlador_paciente.obtener_pacientes()
        paciente_map = {p["_id"]: f"{p.get('nombre', '')} {p.get('apellido', '')}" for p in pacientes}

        tensiones = self.controlador_tension.obtener_tensiones()
        for t in tensiones:
            valores = t.get("valores", {})
            fecha = t.get("fecha", "")

            # Formatear la fecha
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

            id_pac = t.get("id_paciente", "")
            nombre_paciente = paciente_map.get(id_pac, id_pac)

            self.tabla.insertar_fila(valores=(
                t.get("_id", ""),
                nombre_paciente,
                valores.get("sistolica", ""),
                valores.get("diastolica", ""),
                t.get("estado", ""),
                fecha,
                t.get("valoracion", ""),
                "Sí" if t.get("valor_en_rango", False) else "No"
            ))

    def agregar_tension(self):
        FormularioTension(
            self.parent_frame,
            self.controlador_tension,
            self.controlador_paciente,
            al_guardar=self.cargar_datos
        )

    def editar_tension(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Atención", "Selecciona una tensión para editar.")
            return
        FormularioTension(
            self.parent_frame,
            self.controlador_tension,
            self.controlador_paciente,
            al_guardar=self.cargar_datos,
            valores=valores
        )

    def eliminar_tension(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Atención", "Selecciona una tensión para eliminar.")
            return

        tension_id = valores[0]
        nombre_paciente = valores[1]
        fecha_toma = valores[5]

        pregunta = f"¿Eliminar la toma de tensión de {nombre_paciente} realizada el {fecha_toma}?"
        if messagebox.askyesno("Confirmar", pregunta):
            if self.controlador_tension.eliminar_tension(tension_id):
                messagebox.showinfo("Éxito", "Tensión eliminada correctamente.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tensión.")


class FormularioTension(DialogoBase):
    def __init__(self, parent, controlador_tension: TensionControlador, controlador_paciente: PacienteControlador, al_guardar, valores=None):
        self.controlador_tension = controlador_tension
        self.controlador_paciente = controlador_paciente
        self.al_guardar = al_guardar
        self.valores = valores

        titulo = "Alta de Tensión" if valores is None else "Editar Tensión"
        super().__init__(parent, title=titulo, geometry="420x700")

        self.pacientes = self.controlador_paciente.obtener_pacientes()
        self.opciones_pacientes = []
        self.mapa_opcion_id = {}

        for p in self.pacientes:
            fecha_nac = p.get("fechaNacimiento", "")
            if hasattr(fecha_nac, "strftime"):
                fecha_nac = fecha_nac.strftime("%Y-%m-%d")
            elif isinstance(fecha_nac, dict) and "$date" in fecha_nac:
                fecha_nac = str(fecha_nac["$date"]).split("T")[0]
            elif isinstance(fecha_nac, str) and "T" in fecha_nac:
                fecha_nac = fecha_nac.split("T")[0]
            else:
                fecha_nac = str(fecha_nac)

            opcion = f"{p.get('nombre', '')} {p.get('apellido', '')} (Nac.: {fecha_nac})"
            self.opciones_pacientes.append(opcion)
            self.mapa_opcion_id[opcion] = p["_id"]

        self.crear_campos()
        if self.valores:
            self.rellenar_campos()
        self.focus_force()

    def crear_campos(self):
        container = ttk.Frame(self, padding="15")
        container.pack(fill=tk.BOTH, expand=True)

        FNT = TemaApp.FUENTE_NORMAL_GRANDE

        ttk.Label(container, text="Paciente:", font=FNT).pack(pady=(10, 0))
        self.cb_paciente = ttk.Combobox(container, values=self.opciones_pacientes, state="readonly", font=FNT)
        self.cb_paciente.pack(fill=tk.X, padx=15)

        ttk.Label(container, text="Sistólica (mmHg):", font=FNT).pack(pady=(8, 0))
        self.entry_sist = tk.Entry(container, font=FNT)
        self.entry_sist.pack(fill=tk.X, padx=15)

        ttk.Label(container, text="Diastólica (mmHg):", font=FNT).pack(pady=(8, 0))
        self.entry_dias = tk.Entry(container, font=FNT)
        self.entry_dias.pack(fill=tk.X, padx=15)

        ttk.Label(container, text="Método:", font=FNT).pack(pady=(8, 0))
        self.cb_metodo = ttk.Combobox(container, values=["Auscultación", "Oscilometría", "Palpación"], state="readonly", font=FNT)
        self.cb_metodo.pack(fill=tk.X, padx=15)
        self.cb_metodo.current(1)

        ttk.Label(container, text="Sitio del cuerpo:", font=FNT).pack(pady=(8, 0))
        self.cb_sitio = ttk.Combobox(container, values=["Brazo Derecho", "Brazo Izquierdo", "Muslo"], state="readonly", font=FNT)
        self.cb_sitio.pack(fill=tk.X, padx=15)
        self.cb_sitio.current(1)

        ttk.Label(container, text="Tamaño del brazalete:", font=FNT).pack(pady=(8, 0))
        self.cb_brazalete = ttk.Combobox(container, values=["Neonatal", "Infantil", "Estándar", "Muslo", "Grandes"], state="readonly", font=FNT)
        self.cb_brazalete.pack(fill=tk.X, padx=15)
        self.cb_brazalete.current(2)

        ttk.Label(container, text="Dispositivo:", font=FNT).pack(pady=(8, 0))
        self.entry_dispositivo = tk.Entry(container, font=FNT)
        self.entry_dispositivo.insert(0, "Esfigmomanómetro Digital")
        self.entry_dispositivo.pack(fill=tk.X, padx=15)

        ttk.Label(container, text="Estado (FHIR):", font=FNT).pack(pady=(8, 0))
        self.cb_estado = ttk.Combobox(container, values=[
            "registered", "preliminary", "final",
            "amended", "corrected", "cancelled",
            "entered-in-error", "unknown"
        ], state="readonly", font=FNT)
        self.cb_estado.pack(fill=tk.X, padx=15)
        self.cb_estado.set("final")

        ttk.Label(container, text="Fecha (YYYY-MM-DD):", font=FNT).pack(pady=(8, 0))
        self.entry_fecha = tk.Entry(container, font=FNT)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.pack(fill=tk.X, padx=15)

        ttk.Label(container, text="Valoración:", font=FNT).pack(pady=(8, 0))
        self.entry_valoracion = tk.Entry(container, font=FNT)
        self.entry_valoracion.insert(0, "Toma en reposo")
        self.entry_valoracion.pack(fill=tk.X, padx=15)

        self.var_rango = tk.BooleanVar(value=True)
        self.chk = tk.Checkbutton(
            container, text="Valor en rango óptimo",
            variable=self.var_rango,
            bg=TemaApp.COLOR_PRIMARIO, fg=TemaApp.COLOR_TEXTO_BLANCO,
            selectcolor=TemaApp.COLOR_PRIMARIO,
            activebackground=TemaApp.COLOR_PRIMARIO, activeforeground=TemaApp.COLOR_TEXTO_BLANCO,
            font=FNT
        )
        self.chk.pack(pady=(10, 0))

        # Eventos para cálculo automático
        self.entry_sist.bind("<KeyRelease>", self.auto_verificar_rango)
        self.entry_dias.bind("<KeyRelease>", self.auto_verificar_rango)

        BotonVista(container, text="💾 Guardar", command=self.guardar).pack(pady=15)

    def auto_verificar_rango(self, event=None):
        try:
            sist = int(self.entry_sist.get())
            dias = int(self.entry_dias.get())
            en_rango = self.controlador_tension.verificar_rango(sist, dias)
            self.var_rango.set(en_rango)
        except ValueError:
            pass

    def rellenar_campos(self):
        self.entry_sist.delete(0, tk.END)
        self.entry_sist.insert(0, self.valores[2])

        self.entry_dias.delete(0, tk.END)
        self.entry_dias.insert(0, self.valores[3])

        self.cb_estado.set(self.valores[4])

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, self.valores[5])

        self.entry_valoracion.delete(0, tk.END)
        self.entry_valoracion.insert(0, self.valores[6])

        self.var_rango.set(self.valores[7] == "Sí")

        tension_id = self.valores[0]
        tension_doc = self.controlador_tension.obtener_tension(tension_id)
        if tension_doc:
            pac_id = tension_doc.get("id_paciente", "")
            pac_doc = self.controlador_paciente.obtener_paciente(pac_id)
            if pac_doc:
                fecha_nac = pac_doc.get("fechaNacimiento", "")
                if hasattr(fecha_nac, "strftime"):
                    fecha_nac = fecha_nac.strftime("%Y-%m-%d")
                elif isinstance(fecha_nac, dict) and "$date" in fecha_nac:
                    fecha_nac = str(fecha_nac["$date"]).split("T")[0]
                elif isinstance(fecha_nac, str) and "T" in fecha_nac:
                    fecha_nac = fecha_nac.split("T")[0]
                else:
                    fecha_nac = str(fecha_nac)

                opcion_esperada = f"{pac_doc.get('nombre', '')} {pac_doc.get('apellido', '')} (Nac.: {fecha_nac})"
                self.cb_paciente.set(opcion_esperada)

            valores = tension_doc.get("valores", {})
            self.cb_metodo.set(valores.get("metodo", ""))
            self.cb_sitio.set(valores.get("sitio_cuerpo", ""))
            self.cb_brazalete.set(valores.get("tamaño_brazalete", ""))
            self.entry_dispositivo.delete(0, tk.END)
            self.entry_dispositivo.insert(0, valores.get("dispositivo", ""))

        self.cb_paciente.config(state="disabled")

    def guardar(self):
        opcion_seleccionada = self.cb_paciente.get()
        id_paciente = self.mapa_opcion_id.get(opcion_seleccionada, "")

        sistolica = self.entry_sist.get().strip()
        diastolica = self.entry_dias.get().strip()
        metodo = self.cb_metodo.get()
        sitio = self.cb_sitio.get()
        brazalete = self.cb_brazalete.get()
        dispositivo = self.entry_dispositivo.get().strip()
        estado = self.cb_estado.get()
        fecha = self.entry_fecha.get().strip()
        valoracion = self.entry_valoracion.get().strip()
        en_rango = self.var_rango.get()

        if not id_paciente:
            messagebox.showerror("Error", "Debes seleccionar un paciente válido de la lista.")
            return

        if fecha:
            try:
                dt = datetime.strptime(fecha, "%Y-%m-%d")
                if dt.date() > datetime.now().date():
                    messagebox.showerror("Error", "La fecha no puede ser en el futuro.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Usa YYYY-MM-DD.")
                return

        try:
            sist_val = int(sistolica)
            dias_val = int(diastolica)
        except ValueError:
            messagebox.showerror("Error", "Sistólica y diastólica deben ser números enteros.")
            return

        try:
            tv = TensionValores(
                sistolica=sist_val,
                diastolica=dias_val,
                metodo=metodo,
                sitio_cuerpo=sitio,
                tamaño_brazalete=brazalete,
                dispositivo=dispositivo
            )
            if self.valores:
                tension_id = self.valores[0]
                tension_in = TensionUpdateInput(
                    valores=tv, estado=estado, fecha=fecha,
                    valoracion=valoracion, valor_en_rango=en_rango
                )
                self.controlador_tension.actualizar_tension(tension_id, tension_in)
                messagebox.showinfo("Éxito", "Tensión modificada con éxito.")
            else:
                tension_in = TensionInput(
                    id_paciente=id_paciente, valores=tv, estado=estado,
                    fecha=fecha, valoracion=valoracion, valor_en_rango=en_rango
                )
                self.controlador_tension.agregar_tension(tension_in)
                messagebox.showinfo("Éxito", "Tensión registrada con éxito.")
        except ValidationError as e:
            err_msg = e.errors()[0]["msg"]
            messagebox.showerror("Error de Validación", f"Datos inválidos: {err_msg}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")
            return

        self.al_guardar()
        self.destroy()
