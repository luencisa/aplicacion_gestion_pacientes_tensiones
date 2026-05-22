import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pydantic import ValidationError

from estilos import TemaApp, TituloPrincipal, BotonVista
from vistas.componentes.tabla_base import TablaBase
from vistas.componentes.dialogo_base import DialogoBase
from controladores.lista_controlador import ListaControlador
from controladores.paciente_controlador import PacienteControlador
from esquemas.lista_input import ListaInput

class ListaEsperaVista:
    def __init__(self, parent_frame, al_volver, controlador_lista: ListaControlador = None, controlador_paciente: PacienteControlador = None):
        self.parent_frame = parent_frame
        self.al_volver = al_volver
        self.controlador_lista = controlador_lista
        self.controlador_paciente = controlador_paciente

        # Título de la vista
        lbl_titulo = TituloPrincipal(self.parent_frame, text="Gestión de Lista de Espera")
        lbl_titulo.pack(pady=TemaApp.PADDING_Y_FRAME)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Controles superiores
        frame_controles = ttk.Frame(self.parent_frame, padding="10")
        frame_controles.pack(fill=tk.X)

        btn_volver = BotonVista(frame_controles, text="⬅ Volver Atrás", command=self.al_volver)
        btn_agregar = BotonVista(frame_controles, text="➕ Programar Servicio", command=self.agregar_servicio)
        btn_atendido = BotonVista(frame_controles, text="✔ Marcar Atendido", command=self.marcar_atendido)
        btn_anular = BotonVista(frame_controles, text="❌ Anular Servicio", command=self.anular_servicio)
        btn_eliminar = BotonVista(frame_controles, text="🗑 Eliminar", command=self.eliminar_servicio)
        btn_refrescar = BotonVista(frame_controles, text="🔄 Refrescar", command=self.cargar_datos)

        btn_volver.pack(side=tk.LEFT, padx=5)
        btn_agregar.pack(side=tk.LEFT, padx=5)
        btn_atendido.pack(side=tk.LEFT, padx=5)
        btn_anular.pack(side=tk.LEFT, padx=5)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        btn_refrescar.pack(side=tk.RIGHT, padx=5)

        # Tabla Reutilizable
        columnas = ("id", "id_paciente", "paciente_nombre", "fecha_hora", "servicio", "estado")
        cabeceras = {
            "id": "ID",
            "id_paciente": "ID Paciente",
            "paciente_nombre": "Paciente",
            "fecha_hora": "Fecha y Hora prevista",
            "servicio": "Servicio",
            "estado": "Estado"
        }
        columnas_visibles = ("paciente_nombre", "fecha_hora", "servicio", "estado")
        anchos = {
            "id": 0,
            "id_paciente": 0,
            "paciente_nombre": 250,
            "fecha_hora": 180,
            "servicio": 150,
            "estado": 120
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
        lista_completa = self.controlador_lista.obtener_lista_completa()
        for item in lista_completa:
            serv_display = "Consulta Médica" if item.get("servicio") == "consulta" else "Toma de Tensión"
            estado_val = item.get("estado", "pendiente")

            self.tabla.insertar_fila(valores=(
                item.get("_id", ""),
                item.get("id_paciente", ""),
                item.get("nombre_paciente", ""),
                item.get("fecha_hora", ""),
                serv_display,
                estado_val.upper()
            ))

    def marcar_atendido(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un servicio de la lista.")
            return

        item_id = valores[0]
        if self.controlador_lista.actualizar_estado(item_id, "atendido"):
            messagebox.showinfo("Éxito", "El servicio ha sido marcado como ATENDIDO.")
            self.cargar_datos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado del servicio.")

    def anular_servicio(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un servicio de la lista.")
            return

        item_id = valores[0]
        if self.controlador_lista.actualizar_estado(item_id, "anulado"):
            messagebox.showinfo("Éxito", "El servicio ha sido ANULADO.")
            self.cargar_datos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado del servicio.")

    def eliminar_servicio(self):
        valores = self.tabla.obtener_seleccionado()
        if not valores:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un servicio de la lista.")
            return

        item_id = valores[0]
        paciente = valores[2]
        fecha = valores[3]

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar la cita de '{paciente}' programada para el {fecha}?"
        )
        if confirm:
            if self.controlador_lista.eliminar_lista(item_id):
                messagebox.showinfo("Éxito", "El servicio ha sido eliminado de la lista de espera.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el servicio.")

    def agregar_servicio(self):
        FormularioServicio(self.parent_frame, self.controlador_lista, self.controlador_paciente, al_guardar=self.cargar_datos)


class FormularioServicio(DialogoBase):
    def __init__(self, parent, controlador_lista: ListaControlador, controlador_paciente: PacienteControlador, al_guardar):
        self.controlador_lista = controlador_lista
        self.controlador_paciente = controlador_paciente
        self.al_guardar = al_guardar

        super().__init__(parent, title="Programar Servicio", geometry="450x300")

        self.pacientes = self.controlador_paciente.obtener_pacientes()
        self.pacientes_map = {
            f"{p.get('nombre', '')} {p.get('apellido', '')} ({p.get('_id', '')[:8]})": p.get("_id")
            for p in self.pacientes
        }

        self.crear_campos()
        self.focus_force()

    def crear_campos(self):
        container = ttk.Frame(self, padding="20")
        container.pack(fill=tk.BOTH, expand=True)

        # Selección de Paciente
        lbl_paciente = ttk.Label(container, text="Paciente:", font=TemaApp.FUENTE_NORMAL_NEGRITA)
        lbl_paciente.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.combo_paciente = ttk.Combobox(container, values=list(self.pacientes_map.keys()), state="readonly", width=35)
        self.combo_paciente.grid(row=0, column=1, sticky=tk.W, pady=5)
        if self.pacientes_map:
            self.combo_paciente.current(0)

        # Selección de Servicio
        lbl_servicio = ttk.Label(container, text="Servicio:", font=TemaApp.FUENTE_NORMAL_NEGRITA)
        lbl_servicio.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.combo_servicio = ttk.Combobox(container, values=["Consulta Médica", "Toma de Tensión"], state="readonly", width=25)
        self.combo_servicio.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.combo_servicio.current(0)

        # Selección de Fecha y Hora
        lbl_fecha = ttk.Label(container, text="Fecha y Hora:", font=TemaApp.FUENTE_NORMAL_NEGRITA)
        lbl_fecha.grid(row=2, column=0, sticky=tk.W, pady=5)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entry_fecha = ttk.Entry(container, width=25)
        self.entry_fecha.insert(0, current_time)
        self.entry_fecha.grid(row=2, column=1, sticky=tk.W, pady=5)

        lbl_fecha_format = ttk.Label(container, text="Formato: YYYY-MM-DD HH:MM", font=TemaApp.FUENTE_PEQUENA, foreground=TemaApp.COLOR_MUTED)
        lbl_fecha_format.grid(row=3, column=1, sticky=tk.W, pady=(0, 10))

        # Botones de Acción
        frame_botones = ttk.Frame(container)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=15)

        btn_guardar = BotonVista(frame_botones, text="Guardar", command=self.guardar)
        btn_cancelar = BotonVista(frame_botones, text="Cancelar", command=self.destroy)

        btn_guardar.pack(side=tk.LEFT, padx=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

    def guardar(self):
        selected_paciente_label = self.combo_paciente.get()
        if not selected_paciente_label:
            messagebox.showerror("Error", "Debe seleccionar un paciente.")
            return

        id_paciente = self.pacientes_map.get(selected_paciente_label)
        servicio_label = self.combo_servicio.get()
        servicio = "consulta" if servicio_label == "Consulta Médica" else "enfermeria"
        fecha_hora = self.entry_fecha.get().strip()

        try:
            # Validación mediante esquema
            lista_in = ListaInput(
                id_paciente=id_paciente,
                fecha_hora=fecha_hora,
                servicio=servicio,
                estado="pendiente"
            )
        except ValidationError as e:
            err_msg = e.errors()[0]["msg"]
            messagebox.showerror("Error de validación", f"Datos incorrectos:\n{err_msg}")
            return

        try:
            result = self.controlador_lista.agregar_lista(lista_in)
            if result:
                messagebox.showinfo("Éxito", "El servicio ha sido programado exitosamente.")
                self.al_guardar()
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el servicio en la lista de espera.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {e}")
