import tkinter as tk
from tkinter import ttk
from estilos import TemaApp, TituloPrincipal, TituloSecundario, BotonVista
from vistas.componentes.tabla_base import TablaBase
from controladores.paciente_controlador import PacienteControlador

class PacienteDetalleVista:
    def __init__(self, parent_frame, valores_paciente, al_volver, al_abrir_analisis=None, controlador: PacienteControlador = None):
        self.parent_frame = parent_frame
        self.valores_paciente = valores_paciente
        self.al_volver = al_volver
        self.al_abrir_analisis = al_abrir_analisis
        self.controlador = controlador

        # El controlador inyectado para las tensiones se puede obtener a través del servicio o pasando el tension_controlador
        # Para que sea limpio, podemos usar el paciente_servicio que ya tiene acceso a las tensiones a través de obtener_paciente_con_tensiones.
        # ¡Sí! En paciente_servicio tenemos obtener_paciente_con_tensiones(paciente_id).
        # Vamos a comprobar si el controlador tiene un método obtener_paciente_con_tensiones o si podemos acceder a su servicio.
        # En paciente_controlador, tenemos:
        # self.servicio = paciente_servicio.
        # Así que podemos llamar directamente a:
        # self.controlador.servicio.obtener_paciente_con_tensiones(paciente_id)
        # Esto es muy limpio ya que usa el servicio de composición de negocio!
        
        title = f"Ficha Clínica: {self.valores_paciente[1]} {self.valores_paciente[2]}"
        lbl_title = TituloPrincipal(self.parent_frame, text=title)
        lbl_title.pack(pady=TemaApp.PADDING_Y_FRAME)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        # Botonera de control
        frame_superior = ttk.Frame(self.parent_frame, padding="10")
        frame_superior.pack(fill=tk.X)

        btn_volver = BotonVista(frame_superior, text="⬅ Volver a Pacientes", command=self.al_volver)
        btn_volver.pack(side=tk.LEFT, padx=5)

        btn_analisis = BotonVista(frame_superior, text="📊 Análisis", command=self.abrir_analisis)
        btn_analisis.pack(side=tk.LEFT, padx=5)

        # Información general del paciente
        frame_info = ttk.Frame(self.parent_frame, padding="20")
        frame_info.pack(fill=tk.X, padx=10, pady=10)

        lbl_genero_tit = TituloSecundario(frame_info, text="Género:")
        lbl_genero_val = ttk.Label(frame_info, text=self.valores_paciente[3], font=TemaApp.FUENTE_NORMAL_GRANDE)

        lbl_nac_tit = TituloSecundario(frame_info, text="Nacimiento:")
        lbl_nac_val = ttk.Label(frame_info, text=self.valores_paciente[4], font=TemaApp.FUENTE_NORMAL_GRANDE)

        lbl_id_tit = TituloSecundario(frame_info, text="ID Paciente:")
        lbl_id_val = ttk.Label(frame_info, text=self.valores_paciente[0], font=TemaApp.FUENTE_NORMAL_GRANDE)

        lbl_genero_tit.grid(row=0, column=0, sticky=tk.W, pady=2)
        lbl_genero_val.grid(row=0, column=1, sticky=tk.W, pady=2, padx=10)
        lbl_nac_tit.grid(row=1, column=0, sticky=tk.W, pady=2)
        lbl_nac_val.grid(row=1, column=1, sticky=tk.W, pady=2, padx=10)
        lbl_id_tit.grid(row=2, column=0, sticky=tk.W, pady=2)
        lbl_id_val.grid(row=2, column=1, sticky=tk.W, pady=2, padx=10)

        # Historial de tensiones
        lbl_tensiones_tit = TituloPrincipal(self.parent_frame, text="Historial de Tensiones Asociadas")
        lbl_tensiones_tit.pack(pady=TemaApp.PADDING_Y_FRAME)

        columnas = ("fecha", "sistolica", "diastolica", "valoracion", "en_rango")
        cabeceras = {
            "fecha": "Fecha",
            "sistolica": "Sistólica",
            "diastolica": "Diastólica",
            "valoracion": "Valoración",
            "en_rango": "En Rango"
        }
        self.tabla = TablaBase(
            self.parent_frame,
            columnas=columnas,
            cabeceras=cabeceras,
            columnas_visibles=columnas,
            anchos={"fecha": 150, "sistolica": 100, "diastolica": 100, "valoracion": 250, "en_rango": 100}
        )
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_datos(self):
        self.tabla.vaciar()
        paciente_id = self.valores_paciente[0]
        
        # Recuperar información en cascada a través de la operación de composición del servicio
        paciente_completo = self.controlador.servicio.obtener_paciente_con_tensiones(paciente_id)
        if not paciente_completo:
            return

        tensiones = paciente_completo.get("tensiones_asociadas", [])
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

            self.tabla.insertar_fila(valores=(
                fecha,
                valores.get("sistolica", ""),
                valores.get("diastolica", ""),
                t.get("valoracion", ""),
                "Sí" if t.get("valor_en_rango", False) else "No"
            ))

    def abrir_analisis(self):
        if self.al_abrir_analisis:
            self.al_abrir_analisis(self.valores_paciente)
