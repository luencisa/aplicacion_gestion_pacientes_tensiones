import logging
from typing import Optional
from esquemas.analisis_tension import EstadisticasTension, UltimaTension, AnalisisTension
from repositorios.tension_repositorio import TensionRepositorio
from repositorios.paciente_repositorio import PacienteRepositorio

logger = logging.getLogger("AppSalud.AnalisisTensionServicio")


def _obtener_fecha_string(toma):
    fecha = toma.get("fecha", "")
    if hasattr(fecha, "strftime"):
        return fecha.strftime("%Y-%m-%d %H:%M")
    if isinstance(fecha, dict) and "$date" in fecha:
        return str(fecha["$date"])
    if isinstance(fecha, str):
        return fecha
    return str(fecha)


class AnalisisTensionServicio:
    """Servicio para análisis estadísticos de tensiones"""

    def __init__(self, tension_repo: TensionRepositorio, paciente_repo: PacienteRepositorio = None):
        self.tension_repo = tension_repo
        self.paciente_repo = paciente_repo

    def calcular_estadisticas(self, id_paciente: str, ultimas_n: Optional[int] = None) -> EstadisticasTension:
        """Calcula estadísticas de tensiones de un paciente"""
        nombre_paciente = None
        try:
            if self.paciente_repo:
                pac = self.paciente_repo.obtener_por_id(id_paciente)
                if pac:
                    nombre_paciente = f"{pac.get('nombre', '')} {pac.get('apellido', '')}".strip()

            tensiones = self.tension_repo.obtener_todos(id_paciente)

            if not tensiones:
                return EstadisticasTension(
                    id_paciente=id_paciente,
                    nombre_paciente=nombre_paciente,
                    total_mediciones=0,
                    sistolica_promedio=0,
                    diastolica_promedio=0,
                    sistolica_min=0,
                    sistolica_max=0,
                    diastolica_min=0,
                    diastolica_max=0,
                    en_rango_porcentaje=0
                )

            # Garantizar la ordenación cronológica por fecha
            tensiones = sorted(tensiones, key=_obtener_fecha_string)

            if ultimas_n:
                tensiones = tensiones[-ultimas_n:]

            sistolicas = [t["valores"]["sistolica"] for t in tensiones if "valores" in t and "sistolica" in t["valores"]]
            diastolicas = [t["valores"]["diastolica"] for t in tensiones if "valores" in t and "diastolica" in t["valores"]]

            if not sistolicas or not diastolicas:
                return EstadisticasTension(
                    id_paciente=id_paciente,
                    nombre_paciente=nombre_paciente,
                    total_mediciones=len(tensiones),
                    sistolica_promedio=0,
                    diastolica_promedio=0,
                    sistolica_min=0,
                    sistolica_max=0,
                    diastolica_min=0,
                    diastolica_max=0,
                    en_rango_porcentaje=0
                )

            en_rango_count = sum(1 for t in tensiones if t.get("valor_en_rango", False))

            return EstadisticasTension(
                id_paciente=id_paciente,
                nombre_paciente=nombre_paciente,
                total_mediciones=len(tensiones),
                sistolica_promedio=round(sum(sistolicas) / len(sistolicas), 2),
                diastolica_promedio=round(sum(diastolicas) / len(diastolicas), 2),
                sistolica_min=min(sistolicas),
                sistolica_max=max(sistolicas),
                diastolica_min=min(diastolicas),
                diastolica_max=max(diastolicas),
                en_rango_porcentaje=round((en_rango_count / len(tensiones)) * 100, 2) if tensiones else 0
            )
        except Exception as e:
            logger.error(f"Error calculando estadísticas para paciente {id_paciente}: {e}")
            return EstadisticasTension(
                id_paciente=id_paciente,
                nombre_paciente=nombre_paciente,
                total_mediciones=0,
                sistolica_promedio=0,
                diastolica_promedio=0,
                sistolica_min=0,
                sistolica_max=0,
                diastolica_min=0,
                diastolica_max=0,
                en_rango_porcentaje=0
            )

    def obtener_ultima_medicion(self, id_paciente: str) -> Optional[UltimaTension]:
        """Obtiene la última toma de tensión de un paciente"""
        try:
            tensiones = self.tension_repo.obtener_todos(id_paciente)

            if not tensiones:
                return None

            # Garantizar la ordenación cronológica por fecha
            tensiones = sorted(tensiones, key=_obtener_fecha_string)
            ultima = tensiones[-1]
            fecha = ultima.get("fecha", "")
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%Y-%m-%d")
            elif isinstance(fecha, dict) and "$date" in fecha:
                fecha = str(fecha["$date"]).split("T")[0]
            elif isinstance(fecha, str) and "T" in fecha:
                fecha = fecha.split("T")[0]

            return UltimaTension(
                fecha=fecha,
                sistolica=ultima["valores"]["sistolica"],
                diastolica=ultima["valores"]["diastolica"],
                valoracion=ultima.get("valoracion", ""),
                en_rango=ultima.get("valor_en_rango", False)
            )
        except Exception as e:
            logger.error(f"Error obteniendo última medición para paciente {id_paciente}: {e}")
            return None

    def obtener_analisis_completo(self, id_paciente: str, ultimas_n: Optional[int] = None) -> AnalisisTension:
        """Obtiene análisis completo de tensiones de un paciente"""
        estadisticas = self.calcular_estadisticas(id_paciente, ultimas_n)
        ultima = self.obtener_ultima_medicion(id_paciente)

        return AnalisisTension(
            estadisticas=estadisticas,
            ultima_medicion=ultima
        )
