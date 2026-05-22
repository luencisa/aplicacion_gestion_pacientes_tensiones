import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pydantic import ValidationError

from estilos import TemaApp, TituloPrincipal, BotonVista, EstilosDialogo
from vistas.componentes.tabla_base import TablaBase
from vistas.componentes.dialogo_base import DialogoBase
from controladores.lista_controlador import ListaControlador
from controladores.tension_controlador import TensionControlador
from esquemas.tension_input import TensionInput
from esquemas.tension_valores import TensionValores

class EnfermeroVista:
    def __init__(self, parent_frame, al_salir, controlador_lista: ListaControlador = None, controlador_tension: TensionControlador = None):
        self.parent_frame = parent_frame
        self.al_salir = al_salir
        self.controlador_lista = controlador_lista
        self.controlador_tension = controlador_tension

        # Título
        lbl_titulo = TituloPrincipal(self.parent_frame, text="Portal de Enfermería - Tomas Pendientes")
        lbl_titulo.pack(pady=TemaApp.PADDING_Y_FRAME)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Controles
        frame_controles = ttk.Frame(self.parent_frame, padding="10")
        frame_controles.pack(fill=tk.X)

        btn_salir = BotonVista(frame_controles, text="🚪 Cambiar Rol", command=self.al_salir)
        btn_atender = BotonVista(frame_controles, text="💉 Realizar Toma de Tensión", command=self.realizar_toma)
        btn_anular = BotonVista(frame_controles, text="❌ Anular Toma de Tensión", command=self.anular_toma)
        btn_refrescar = BotonVista(frame_controles, text="🔄 Refrescar", command=self.cargar_datos)

        btn_salir.pack(side=tk.LEFT, padx=5)
        btn_atender.pack(side=tk.LEFT, padx=5)
        btn_anular.pack(side=tk.LEFT, padx=5)
        btn_refrescar.pack(side=tk.RIGHT, padx=5)

        # Tabla de tomas pendientes
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
        tomas_pendientes = self.controlador_lista.obtener_lista_por_servicio("enfermeria", estado="pendiente")
        for item in tomas_pendientes:
            self.tabla.insertar_fila(valores=(
                item.get("_id", ""),
                item.get("id_paciente", ""),
                item.get("nombre_paciente", ""),
                item.get("fecha_hora", ""),
                item.get("estado", "").upper()
            ))

    def realizar_toma(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una toma de tensión de la lista.")
            return

        item_id = valores[0]
        id_paciente = valores[1]
        nombre_paciente = valores[2]

        RealizarTomaDialogo(
            self.parent_frame,
            item_id,
            id_paciente,
            nombre_paciente,
            self.controlador_lista,
            self.controlador_tension,
            al_guardar=self.cargar_datos
        )

    def anular_toma(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione una toma de tensión de la lista.")
            return

        item_id = valores[0]
        paciente = valores[2]

        confirm = messagebox.askyesno(
            "Anular Toma de Tensión",
            f"¿Desea anular la toma de tensión para '{paciente}'?"
        )
        if confirm:
            if self.controlador_lista.actualizar_estado(item_id, "anulado"):
                messagebox.showinfo("Éxito", f"Toma de tensión para '{paciente}' anulada.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo anular la toma de tensión.")


class RealizarTomaDialogo(DialogoBase):
    def __init__(self, parent, item_id, id_paciente, nombre_paciente, controlador_lista: ListaControlador, controlador_tension: TensionControlador, al_guardar):
        self.item_id = item_id
        self.id_paciente = id_paciente
        self.nombre_paciente = nombre_paciente
        self.controlador_lista = controlador_lista
        self.controlador_tension = controlador_tension
        self.al_guardar = al_guardar

        super().__init__(parent, title=f"Registrar Toma de Tensión - {self.nombre_paciente}", geometry="450x700")
        self.resizable(True, True)

        # Configurar estilos locales
        style = ttk.Style()
        EstilosDialogo.aplicar_estilos_ttk(style)

        self.crear_campos()
        self.focus_force()

    def crear_campos(self):
        container = ttk.Frame(self, padding="15", style="Dialog.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        # Paciente (Lectura)
        lbl_paciente_tit = ttk.Label(container, text="Paciente:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel")
        lbl_paciente_tit.pack(anchor=tk.W, pady=(5, 2))
        lbl_paciente_val = ttk.Label(container, text=self.nombre_paciente, font=EstilosDialogo.FUENTE_DETALLE_PACIENTE, foreground=TemaApp.COLOR_PRIMARIO, style="Dialog.TLabel")
        lbl_paciente_val.pack(anchor=tk.W, pady=(0, 10))

        # Sistólica
        ttk.Label(container, text="Tensión Sistólica (mmHg):", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.entry_sist = ttk.Entry(container)
        self.entry_sist.pack(fill=tk.X, pady=(0, 10))

        # Diastólica
        ttk.Label(container, text="Tensión Diastólica (mmHg):", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.entry_dias = ttk.Entry(container)
        self.entry_dias.pack(fill=tk.X, pady=(0, 10))

        # Método
        ttk.Label(container, text="Método de Medición:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.combo_metodo = ttk.Combobox(container, values=["Auscultación", "Oscilometría", "Palpación"], state="readonly")
        self.combo_metodo.pack(fill=tk.X, pady=(0, 10))
        self.combo_metodo.current(1)

        # Sitio del cuerpo
        ttk.Label(container, text="Sitio de Medición:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.combo_sitio = ttk.Combobox(container, values=["Brazo Derecho", "Brazo Izquierdo", "Muslo"], state="readonly")
        self.combo_sitio.pack(fill=tk.X, pady=(0, 10))
        self.combo_sitio.current(1)

        # Brazalete
        ttk.Label(container, text="Tamaño del Brazalete:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.combo_brazalete = ttk.Combobox(container, values=["Neonatal", "Infantil", "Estándar", "Muslo", "Grandes"], state="readonly")
        self.combo_brazalete.pack(fill=tk.X, pady=(0, 10))
        self.combo_brazalete.current(2)

        # Dispositivo
        ttk.Label(container, text="Dispositivo Empleado:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.entry_dispositivo = ttk.Entry(container)
        self.entry_dispositivo.insert(0, "Esfigmomanómetro Digital")
        self.entry_dispositivo.pack(fill=tk.X, pady=(0, 10))

        # Fecha
        ttk.Label(container, text="Fecha de Medición (YYYY-MM-DD):", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.entry_fecha = ttk.Entry(container)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.pack(fill=tk.X, pady=(0, 10))

        # Valoración
        ttk.Label(container, text="Valoración / Observaciones:", font=TemaApp.FUENTE_NORMAL_NEGRITA, style="Dialog.TLabel").pack(anchor=tk.W, pady=(5, 2))
        self.entry_valoracion = ttk.Entry(container)
        self.entry_valoracion.insert(0, "Toma en reposo")
        self.entry_valoracion.pack(fill=tk.X, pady=(0, 10))

        # Rango óptimo
        self.var_rango = tk.BooleanVar(value=True)
        self.chk_rango = tk.Checkbutton(
            container, text="Valor en rango óptimo",
            variable=self.var_rango,
            bg=TemaApp.COLOR_FONDO_SECUNDARIO,
            font=TemaApp.FUENTE_NORMAL
        )
        self.chk_rango.pack(pady=5)

        # Binds para cálculo automático usando la regla de negocio del controlador
        self.entry_sist.bind("<KeyRelease>", self.auto_verificar_rango)
        self.entry_dias.bind("<KeyRelease>", self.auto_verificar_rango)

        # Botonera
        frame_botones = ttk.Frame(container, style="Dialog.TFrame")
        frame_botones.pack(pady=15)

        btn_guardar = BotonVista(frame_botones, text="Guardar Registro", command=self.guardar)
        btn_cancelar = BotonVista(frame_botones, text="Cancelar", command=self.destroy)

        btn_guardar.pack(side=tk.LEFT, padx=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

    def auto_verificar_rango(self, event=None):
        try:
            sist = int(self.entry_sist.get())
            dias = int(self.entry_dias.get())
            # Delegar la validación al controlador
            en_rango = self.controlador_tension.verificar_rango(sist, dias)
            self.var_rango.set(en_rango)
        except ValueError:
            pass

    def guardar(self):
        sistolica = self.entry_sist.get().strip()
        diastolica = self.entry_dias.get().strip()
        metodo = self.combo_metodo.get()
        sitio = self.combo_sitio.get()
        brazalete = self.combo_brazalete.get()
        dispositivo = self.entry_dispositivo.get().strip()
        fecha = self.entry_fecha.get().strip()
        valoracion = self.entry_valoracion.get().strip()
        en_rango = self.var_rango.get()

        if not sistolica or not diastolica:
            messagebox.showerror("Error de entrada", "Debe completar los valores de sistólica y diastólica.")
            return

        try:
            sist_val = int(sistolica)
            dias_val = int(diastolica)
        except ValueError:
            messagebox.showerror("Error de entrada", "La presión sistólica y diastólica deben ser valores numéricos enteros.")
            return

        try:
            dt = datetime.strptime(fecha, "%Y-%m-%d")
            if dt.date() > datetime.now().date():
                messagebox.showerror("Error", "La fecha de la medición no puede ser en el futuro.")
                return
        except ValueError:
            messagebox.showerror("Error de formato", "La fecha de la medición debe estar en formato YYYY-MM-DD.")
            return

        try:
            valores_t = TensionValores(
                sistolica=sist_val,
                diastolica=dias_val,
                metodo=metodo,
                sitio_cuerpo=sitio,
                tamaño_brazalete=brazalete,
                dispositivo=dispositivo
            )
            tension_in = TensionInput(
                id_paciente=self.id_paciente,
                valores=valores_t,
                estado="final",
                fecha=fecha,
                valoracion=valoracion,
                valor_en_rango=en_rango
            )
        except ValidationError as e:
            err_msg = e.errors()[0]["msg"]
            messagebox.showerror("Error de Validación", f"Datos incorrectos: {err_msg}")
            return

        # 1. Registrar la tensión
        result_tension = self.controlador_tension.agregar_tension(tension_in)
        if result_tension:
            # 2. Completar la cita
            if self.controlador_lista.actualizar_estado(self.item_id, "atendido"):
                messagebox.showinfo("Éxito", f"Se ha registrado la toma de tensión de '{self.nombre_paciente}' y completado el servicio.")
                self.al_guardar()
                self.destroy()
            else:
                messagebox.showerror("Error", "Tensión registrada, pero no se pudo actualizar el estado de la cita en lista de espera.")
        else:
            messagebox.showerror("Error", "No se pudo registrar la toma de tensión.")
