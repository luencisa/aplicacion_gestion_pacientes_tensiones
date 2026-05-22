import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from estilos import TemaApp, BotonVista, EstilosAnalisis
from controladores.tension_controlador import TensionControlador

def _crear_tarjeta(parent, texto_etiqueta, clave, mapa_etiquetas):
    """Crea una tarjeta individual con etiqueta y valor destacado."""
    card = tk.Frame(parent, bg=EstilosAnalisis.COLOR_CARD_BG, bd=0, relief=tk.FLAT)

    lbl = tk.Label(
        card,
        text=texto_etiqueta,
        bg=EstilosAnalisis.COLOR_CARD_BG,
        fg=EstilosAnalisis.COLOR_CARD_LABEL,
        font=EstilosAnalisis.FUENTE_CARD_LABEL,
        anchor=tk.W
    )
    lbl.pack(anchor=tk.W, padx=10, pady=(8, 0))

    val = tk.Label(
        card,
        text="--",
        bg=EstilosAnalisis.COLOR_CARD_BG,
        fg=EstilosAnalisis.COLOR_CARD_VALOR,
        font=EstilosAnalisis.FUENTE_CARD_VALOR,
        anchor=tk.W
    )
    val.pack(anchor=tk.W, padx=10, pady=(0, 10))

    mapa_etiquetas[clave] = val
    return card

class TensionAnalisisVista:
    def __init__(self, parent_frame, valores_paciente, al_volver, controlador: TensionControlador = None):
        self.parent_frame = parent_frame
        self.valores_paciente = valores_paciente
        self.al_volver = al_volver
        self.controlador = controlador
        self.stats_labels = {}
        self.last_labels = {}

        try:
            self.crear_widgets()
            self.cargar_datos()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error Crítico", f"Error inicializando vista de análisis: {str(e)}")

    def crear_widgets(self):
        BG = TemaApp.COLOR_PRIMARIO

        # Canvas con Scrollbar
        canvas = tk.Canvas(self.parent_frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg=BG)
        inner_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(e):
            canvas.itemconfig(inner_window, width=e.width)

        inner.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Cabecera
        frame_header = tk.Frame(inner, bg=BG)
        frame_header.pack(fill=tk.X, padx=15, pady=(15, 5))

        btn_back = BotonVista(frame_header, text="⬅ Volver", command=self.al_volver)
        btn_back.pack(side=tk.LEFT)

        nombre = f"{self.valores_paciente[1]} {self.valores_paciente[2]}"
        lbl_title = tk.Label(
            frame_header,
            text=f"📊  Análisis · {nombre}",
            bg=BG,
            fg=TemaApp.COLOR_TEXTO_BLANCO,
            font=EstilosAnalisis.FUENTE_PANEL_TITULO
        )
        lbl_title.pack(side=tk.LEFT, padx=20)

        # Separador estético
        sep = tk.Frame(inner, bg=EstilosAnalisis.COLOR_SEPARADOR, height=2)
        sep.pack(fill=tk.X, padx=15, pady=5)

        # Filtro de Horizonte Temporal
        frame_filter = tk.Frame(inner, bg=BG)
        frame_filter.pack(fill=tk.X, padx=15, pady=(5, 10))

        lbl_filter = tk.Label(
            frame_filter,
            text="Horizonte temporal (últimas N tomas):",
            bg=BG,
            fg=TemaApp.COLOR_TEXTO_BLANCO,
            font=EstilosAnalisis.FUENTE_FILTRO_LABEL
        )
        lbl_filter.pack(side=tk.LEFT, padx=(5, 5))

        self.entry_n = tk.Entry(
            frame_filter,
            width=8,
            font=EstilosAnalisis.FUENTE_FILTRO_INPUT,
            justify=tk.CENTER
        )
        self.entry_n.pack(side=tk.LEFT, padx=5)
        self.entry_n.insert(0, "")

        btn_filter = BotonVista(
            frame_filter,
            text="🔄 Calcular",
            command=self.aplicar_filtro
        )
        btn_filter.pack(side=tk.LEFT, padx=5)

        # Sección 1: Estadísticas Generales (Tarjetas)
        self._section_header(inner, "📈  Estadísticas Generales")

        frame_grid = tk.Frame(inner, bg=BG)
        frame_grid.pack(fill=tk.X, padx=15, pady=(0, 10))

        stats_config = [
            ("total",    "Total de Mediciones"),
            ("sist_prom","Sistólica Promedio"),
            ("dias_prom","Diastólica Promedio"),
            ("rango_pct","% en Rango"),
            ("sist_min", "Sistólica Mínima"),
            ("sist_max", "Sistólica Máxima"),
            ("dias_min", "Diastólica Mínima"),
            ("dias_max", "Diastólica Máxima"),
        ]

        for c in range(4):
            frame_grid.columnconfigure(c, weight=1, uniform="col")

        for i, (key, label) in enumerate(stats_config):
            row = i // 4
            col = i % 4
            card = _crear_tarjeta(frame_grid, label, key, self.stats_labels)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        # Sección 2: Última Medición Registrada
        self._section_header(inner, "🕐  Última Medición")

        frame_last = tk.Frame(inner, bg=EstilosAnalisis.COLOR_LAST_BG, bd=0)
        frame_last.pack(fill=tk.X, padx=15, pady=(0, 15))

        last_config = [
            ("fecha", "📅  Fecha"),
            ("sist",  "❤️  Sistólica"),
            ("dias",  "💙  Diastólica"),
            ("valor", "📝  Valoración"),
            ("rango", "✅  En Rango"),
        ]

        for c in range(len(last_config)):
            frame_last.columnconfigure(c, weight=1, uniform="last")

        for i, (key, label) in enumerate(last_config):
            cell = tk.Frame(frame_last, bg=EstilosAnalisis.COLOR_LAST_BG)
            cell.grid(row=0, column=i, sticky="nsew", padx=8, pady=12)

            tk.Label(
                cell, text=label,
                bg=EstilosAnalisis.COLOR_LAST_BG,
                fg=EstilosAnalisis.COLOR_CARD_LABEL,
                font=EstilosAnalisis.FUENTE_CARD_LABEL
            ).pack(anchor=tk.CENTER)

            val_lbl = tk.Label(
                cell, text="--",
                bg=EstilosAnalisis.COLOR_LAST_BG,
                fg=EstilosAnalisis.COLOR_CARD_VALOR,
                font=EstilosAnalisis.FUENTE_ULTIMA_VALOR,
                wraplength=120
            )
            val_lbl.pack(anchor=tk.CENTER, pady=(4, 0))
            self.last_labels[key] = val_lbl

    def _section_header(self, parent, text):
        bar = tk.Frame(parent, bg=EstilosAnalisis.COLOR_HEADER_BG)
        bar.pack(fill=tk.X, padx=15, pady=(10, 5))
        tk.Label(
            bar, text=text,
            bg=EstilosAnalisis.COLOR_HEADER_BG,
            fg=TemaApp.COLOR_TEXTO_BLANCO,
            font=EstilosAnalisis.FUENTE_SECCION_TITULO,
            pady=6, padx=10
        ).pack(anchor=tk.W)

    def cargar_datos(self, ultimas_n=None):
        try:
            paciente_id = self.valores_paciente[0]
            
            # Comprobar el total real de mediciones primero sin límite
            analisis_total = self.controlador.obtener_analisis_completo(paciente_id, ultimas_n=None)
            if not analisis_total:
                messagebox.showerror("Error", "No se pudo obtener el análisis.")
                return

            total_real = analisis_total.estadisticas.total_mediciones

            if ultimas_n is not None:
                if total_real == 0:
                    messagebox.showerror("Error de Cálculo", "No se puede calcular: el paciente no tiene ninguna toma de tensión registrada.")
                    return
                elif total_real < ultimas_n:
                    messagebox.showerror(
                        "Error de Cálculo",
                        f"No se puede calcular: el paciente tiene solo {total_real} tomas registradas, "
                        f"que es menor que el horizonte temporal solicitado de las últimas {ultimas_n} tomas."
                    )
                    return

            analisis = self.controlador.obtener_analisis_completo(paciente_id, ultimas_n=ultimas_n)
            if not analisis or analisis.estadisticas.total_mediciones == 0:
                for lbl in self.stats_labels.values():
                    lbl.config(text="--")
                for lbl in self.last_labels.values():
                    lbl.config(text="Sin datos")
                messagebox.showinfo(
                    "Sin datos",
                    "Este paciente no tiene tensiones registradas aún."
                )
                return

            stats = analisis.estadisticas
            self.stats_labels["total"].config(text=str(stats.total_mediciones))
            self.stats_labels["sist_prom"].config(text=f"{stats.sistolica_promedio}")
            self.stats_labels["dias_prom"].config(text=f"{stats.diastolica_promedio}")
            self.stats_labels["sist_min"].config(text=str(stats.sistolica_min))
            self.stats_labels["sist_max"].config(text=str(stats.sistolica_max))
            self.stats_labels["dias_min"].config(text=str(stats.diastolica_min))
            self.stats_labels["dias_max"].config(text=str(stats.diastolica_max))

            pct = stats.en_rango_porcentaje
            color_pct = EstilosAnalisis.COLOR_ACCENT_GREEN if pct >= 70 else (EstilosAnalisis.COLOR_ACCENT_ORANGE if pct >= 40 else EstilosAnalisis.COLOR_ACCENT_RED)
            self.stats_labels["rango_pct"].config(text=f"{pct}%", fg=color_pct)

            if analisis.ultima_medicion:
                ultima = analisis.ultima_medicion
                self.last_labels["fecha"].config(text=ultima.fecha)
                self.last_labels["sist"].config(
                    text=f"{ultima.sistolica} mmHg",
                    fg=EstilosAnalisis.COLOR_ACCENT_RED if ultima.sistolica >= 140 else EstilosAnalisis.COLOR_ACCENT_GREEN
                )
                self.last_labels["dias"].config(
                    text=f"{ultima.diastolica} mmHg",
                    fg=EstilosAnalisis.COLOR_ACCENT_RED if ultima.diastolica >= 90 else EstilosAnalisis.COLOR_ACCENT_GREEN
                )
                self.last_labels["valor"].config(text=ultima.valoracion)
                en_r = ultima.en_rango
                self.last_labels["rango"].config(
                    text="✅ Sí" if en_r else "❌ No",
                    fg=EstilosAnalisis.COLOR_ACCENT_GREEN if en_r else EstilosAnalisis.COLOR_ACCENT_RED
                )
            else:
                for lbl in self.last_labels.values():
                    lbl.config(text="Sin datos")

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al cargar análisis: {str(e)}")

    def aplicar_filtro(self):
        val = self.entry_n.get().strip()
        if not val:
            self.cargar_datos(ultimas_n=None)
            return

        try:
            n = int(val)
            if n <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Por favor introduzca un número entero positivo para las últimas N tomas o déjelo en blanco.")
            return

        self.cargar_datos(ultimas_n=n)
