import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pydantic import ValidationError

from estilos import TemaApp, TituloPrincipal, BotonVista, EstilosDialogo
from vistas.componentes.tabla_base import TablaBase
from vistas.componentes.dialogo_base import DialogoBase
from controladores.lista_controlador import ListaControlador
from controladores.paciente_controlador import PacienteControlador
from controladores.tension_controlador import TensionControlador
from esquemas.lista_input import ListaInput

class MedicoVista:
    def __init__(self, parent_frame, al_salir, controlador_lista: ListaControlador = None, controlador_paciente: PacienteControlador = None, controlador_tension: TensionControlador = None):
        self.parent_frame = parent_frame
        self.al_salir = al_salir
        self.controlador_lista = controlador_lista
        self.controlador_paciente = controlador_paciente
        self.controlador_tension = controlador_tension

        # Título
        lbl_titulo = TituloPrincipal(self.parent_frame, text="Portal Médico - Consultas Pendientes")
        lbl_titulo.pack(pady=TemaApp.PADDING_Y_FRAME)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Controles
        frame_controles = ttk.Frame(self.parent_frame, padding="10")
        frame_controles.pack(fill=tk.X)

        btn_salir = BotonVista(frame_controles, text="🚪 Cambiar Rol", command=self.al_salir)
        btn_atender = BotonVista(frame_controles, text="🩺 Pasar Consulta", command=self.pasar_consulta)
        btn_anular = BotonVista(frame_controles, text="❌ Anular Consulta", command=self.anular_consulta)
        btn_refrescar = BotonVista(frame_controles, text="🔄 Refrescar", command=self.cargar_datos)

        btn_salir.pack(side=tk.LEFT, padx=5)
        btn_atender.pack(side=tk.LEFT, padx=5)
        btn_anular.pack(side=tk.LEFT, padx=5)
        btn_refrescar.pack(side=tk.RIGHT, padx=5)

        # Tabla de consultas pendientes
        columnas = ("id", "id_paciente", "paciente_nombre", "fecha_hora", "estado")
        cabeceras = {
            "id": "ID",
            "id_paciente": "ID Paciente",
            "paciente_nombre": "Paciente",
            "fecha_hora": "Fecha y Hora Programada",
            "estado": "Estado"
        }
        columnas_visibles = ("paciente_nombre", "fecha_hora", "estado")

        self.tabla = TablaBase(
            self.parent_frame,
            columnas=columnas,
            cabeceras=cabeceras,
            columnas_visibles=columnas_visibles,
            anchos={"paciente_nombre": 300, "fecha_hora": 200, "estado": 150}
        )
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_datos(self):
        self.tabla.vaciar()
        consultas_pendientes = self.controlador_lista.obtener_lista_por_servicio("consulta", estado="pendiente")
        for item in consultas_pendientes:
            self.tabla.insertar_fila(valores=(
                item.get("_id", ""),
                item.get("id_paciente", ""),
                item.get("nombre_paciente", ""),
                item.get("fecha_hora", ""),
                item.get("estado", "").upper()
            ))

    def pasar_consulta(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una consulta de la lista.")
            return

        item_id = valores[0]
        id_paciente = valores[1]
        nombre_paciente = valores[2]

        ConsultaMedicaDialogo(
            self.parent_frame,
            item_id,
            id_paciente,
            nombre_paciente,
            self.controlador_lista,
            self.controlador_tension,
            al_guardar=self.cargar_datos
        )

    def anular_consulta(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una consulta de la lista.")
            return

        item_id = valores[0]
        paciente = valores[2]

        confirm = messagebox.askyesno(
            "Anular Consulta",
            f"¿Desea anular la consulta para '{paciente}' (por incomparecencia u otro motivo)?"
        )
        if confirm:
            if self.controlador_lista.actualizar_estado(item_id, "anulado"):
                messagebox.showinfo("Éxito", f"Consulta de '{paciente}' anulada.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo anular la consulta.")


class ConsultaMedicaDialogo(DialogoBase):
    def __init__(self, parent, item_id, id_paciente, nombre_paciente, controlador_lista: ListaControlador, controlador_tension: TensionControlador, al_guardar):
        self.item_id = item_id
        self.id_paciente = id_paciente
        self.nombre_paciente = nombre_paciente
        self.controlador_lista = controlador_lista
        self.controlador_tension = controlador_tension
        self.al_guardar = al_guardar

        super().__init__(parent, title=f"Consulta Médica - {self.nombre_paciente}", geometry="900x520")
        self.resizable(True, True)

        # Configurar estilos locales
        style = ttk.Style()
        EstilosDialogo.aplicar_estilos_ttk(style)

        self.crear_widgets()
        self.cargar_historico()

    def crear_widgets(self):
        container = ttk.Frame(self, padding="15", style="Dialog.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        # Cabecera
        header_frame = ttk.Frame(container, style="Dialog.TFrame")
        header_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))

        lbl_info = ttk.Label(
            header_frame,
            text=f"Paciente: {self.nombre_paciente}",
            font=EstilosDialogo.FUENTE_TITULO_PACIENTE,
            foreground=TemaApp.COLOR_PRIMARIO,
            style="Dialog.TLabel"
        )
        lbl_info.pack(side=tk.LEFT)

        # Pie de página (Finalizar / Anular / Cerrar)
        footer_frame = ttk.Frame(container, style="Dialog.TFrame")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        btn_finalizar = BotonVista(footer_frame, text="🩺 Finalizar Consulta (Atendida)", command=self.finalizar_consulta)
        btn_anular = BotonVista(footer_frame, text="❌ Anular Consulta", command=self.anular_consulta)
        btn_cerrar = BotonVista(footer_frame, text="Cerrar sin cambios", command=self.destroy)

        btn_finalizar.pack(side=tk.LEFT, padx=5)
        btn_anular.pack(side=tk.LEFT, padx=5)
        btn_cerrar.pack(side=tk.RIGHT, padx=5)

        # Cuerpo central
        body_frame = ttk.Frame(container, style="Dialog.TFrame")
        body_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Columna Derecha: Pautar Seguimiento
        right_frame = ttk.LabelFrame(body_frame, text="Pautar Seguimiento / Solicitar Toma de Tensión", padding="12", style="Dialog.TLabelframe")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        lbl_tipo = ttk.Label(right_frame, text="Tipo de Solicitud:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel")
        lbl_tipo.pack(anchor=tk.W, pady=(2, 2))

        self.var_tipo = tk.StringVar(value="Toma Única")
        self.combo_tipo = ttk.Combobox(right_frame, textvariable=self.var_tipo, values=["Toma Única", "Petición Recurrente"], state="readonly")
        self.combo_tipo.pack(fill=tk.X, pady=(0, 8))
        self.combo_tipo.current(0)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.al_cambiar_tipo)

        self.frame_inputs = ttk.Frame(right_frame, style="Dialog.TFrame")
        self.frame_inputs.pack(fill=tk.BOTH, expand=True)

        # Fecha y Hora Inicial
        self.lbl_inicio = ttk.Label(self.frame_inputs, text="Fecha y Hora Prevista:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel")
        self.lbl_inicio.pack(anchor=tk.W, pady=(2, 2))

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entry_inicio = ttk.Entry(self.frame_inputs)
        self.entry_inicio.insert(0, current_time)
        self.entry_inicio.pack(fill=tk.X, pady=(0, 8))

        # Recurrencia
        self.recurrence_frame = ttk.Frame(self.frame_inputs, style="Dialog.TFrame")
        self.recurrence_frame.pack(fill=tk.X, pady=(5, 5))
        self.recurrence_frame.columnconfigure(0, weight=1)
        self.recurrence_frame.columnconfigure(1, weight=1)

        self.lbl_patron = ttk.Label(self.recurrence_frame, text="Frecuencia:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel")
        self.lbl_patron.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.lbl_repeticiones = ttk.Label(self.recurrence_frame, text="Repeticiones:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel")
        self.lbl_repeticiones.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))

        self.combo_patron = ttk.Combobox(self.recurrence_frame, values=["Diaria", "Semanal"], state="disabled")
        self.combo_patron.grid(row=1, column=0, sticky=tk.EW, padx=(0, 5), pady=(2, 5))
        self.combo_patron.current(0)

        self.entry_repeticiones = ttk.Entry(self.recurrence_frame, state="disabled")
        self.entry_repeticiones.insert(0, "3")
        self.entry_repeticiones.grid(row=1, column=1, sticky=tk.EW, padx=(5, 0), pady=(2, 5))

        self.btn_agendar = BotonVista(right_frame, text="📅 Solicitar Toma(s)", command=self.solicitar_tomas)
        self.btn_agendar.pack(fill=tk.X, pady=(5, 0))

        # Columna Izquierda: Histórico de Tensiones
        left_frame = ttk.LabelFrame(body_frame, text="Histórico de Tensiones", padding="10", style="Dialog.TLabelframe")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        columnas = ("fecha", "sistolica", "diastolica", "estado", "valoracion", "en_rango")
        cabeceras = {
            "fecha": "Fecha",
            "sistolica": "Sist.",
            "diastolica": "Diast.",
            "estado": "Estado",
            "valoracion": "Valoración",
            "en_rango": "En Rango"
        }

        self.tabla_hist = TablaBase(
            left_frame,
            columnas=columnas,
            cabeceras=cabeceras,
            columnas_visibles=columnas,
            anchos={"fecha": 90, "sistolica": 50, "diastolica": 50, "estado": 70, "valoracion": 120, "en_rango": 70}
        )
        self.tabla_hist.pack(fill=tk.BOTH, expand=True)

    def al_cambiar_tipo(self, event=None):
        tipo = self.combo_tipo.get()
        if tipo == "Petición Recurrente":
            self.lbl_inicio.config(text="Fecha y Hora de Inicio:")
            self.combo_patron.config(state="readonly")
            self.entry_repeticiones.config(state="normal")
        else:
            self.lbl_inicio.config(text="Fecha y Hora Prevista:")
            self.combo_patron.config(state="disabled")
            self.entry_repeticiones.config(state="disabled")

    def cargar_historico(self):
        self.tabla_hist.vaciar()
        tensiones = self.controlador_tension.obtener_tensiones(self.id_paciente)

        def parse_date(t):
            fecha_str = t.get("fecha", "")
            if hasattr(fecha_str, "strftime"):
                return fecha_str
            try:
                return datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                return datetime.min

        tensiones.sort(key=parse_date, reverse=True)

        for t in tensiones:
            valores = t.get("valores", {})
            fecha = t.get("fecha", "")
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%Y-%m-%d")
            elif isinstance(fecha, str) and "T" in fecha:
                fecha = fecha.split("T")[0]

            self.tabla_hist.insertar_fila(valores=(
                fecha,
                valores.get("sistolica", "-"),
                valores.get("diastolica", "-"),
                t.get("estado", ""),
                t.get("valoracion", ""),
                "Sí" if t.get("valor_en_rango") else "No"
            ))

    def solicitar_tomas(self):
        tipo = self.combo_tipo.get()
        fecha_inicial = self.entry_inicio.get().strip()

        # Validaciones de fecha inicial en la lógica de negocio
        fechas_generadas = []

        if tipo == "Toma Única":
            try:
                datetime.strptime(fecha_inicial, "%Y-%m-%d %H:%M")
                fechas_generadas.append(fecha_inicial)
            except ValueError:
                messagebox.showerror("Error de formato", "La fecha inicial debe estar en formato YYYY-MM-DD HH:MM")
                return
        else:
            patron = self.combo_patron.get()
            repeticiones_str = self.entry_repeticiones.get().strip()

            try:
                repeticiones = int(repeticiones_str)
            except ValueError:
                messagebox.showerror("Error de entrada", "El número de repeticiones debe ser un entero mayor o igual a 1.")
                return

            try:
                # Usar la lógica de negocio delegada al controlador
                fechas_generadas = self.controlador_lista.generar_fechas_recurrencia(fecha_inicial, patron, repeticiones)
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
                return

        exitos = 0
        errores = []

        for f_str in fechas_generadas:
            try:
                lista_in = ListaInput(
                    id_paciente=self.id_paciente,
                    fecha_hora=f_str,
                    servicio="enfermeria",
                    estado="pendiente"
                )
                result = self.controlador_lista.agregar_lista(lista_in)
                if result:
                    exitos += 1
                else:
                    errores.append(f_str)
            except Exception as e:
                errores.append(f"{f_str} (Error: {e})")

        if exitos > 0:
            msg = f"Se han programado con éxito {exitos} toma(s) de tensión para el paciente."
            if errores:
                msg += f"\n\nHubo errores al programar las siguientes fechas:\n" + "\n".join(errores)
            messagebox.showinfo("Éxito", msg)
        else:
            messagebox.showerror("Error", "No se pudo registrar ninguna de las tomas solicitadas.")

    def finalizar_consulta(self):
        if self.controlador_lista.actualizar_estado(self.item_id, "atendido"):
            messagebox.showinfo("Éxito", "La consulta ha sido marcada como ATENDIDA.")
            self.al_guardar()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo finalizar la consulta.")

    def anular_consulta(self):
        confirm = messagebox.askyesno(
            "Anular Consulta",
            f"¿Está seguro de que desea anular la consulta de '{self.nombre_paciente}'?"
        )
        if confirm:
            if self.controlador_lista.actualizar_estado(self.item_id, "anulado"):
                messagebox.showinfo("Éxito", "La consulta ha sido ANULADA.")
                self.al_guardar()
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo anular la consulta.")
