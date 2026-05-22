from pydantic import BaseModel, Field
from typing import Optional

class EstadisticasTension(BaseModel):
    """Estadísticas de tensiones de un paciente"""
    id_paciente: str = Field(..., description="ID del paciente")
    nombre_paciente: Optional[str] = Field(None, description="Nombre completo del paciente")
    total_mediciones: int = Field(..., description="Total de mediciones registradas")
    sistolica_promedio: float = Field(..., description="Promedio de tensión sistólica")
    diastolica_promedio: float = Field(..., description="Promedio de tensión diastólica")
    sistolica_min: int = Field(..., description="Mínimo sistólico registrado")
    sistolica_max: int = Field(..., description="Máximo sistólico registrado")
    diastolica_min: int = Field(..., description="Mínimo diastólico registrado")
    diastolica_max: int = Field(..., description="Máximo diastólico registrado")
    en_rango_porcentaje: float = Field(..., description="Porcentaje de mediciones en rango")

class UltimaTension(BaseModel):
    """Información de la última toma de tensión"""
    fecha: str = Field(..., description="Fecha de la medición")
    sistolica: int = Field(..., description="Tensión sistólica")
    diastolica: int = Field(..., description="Tensión diastólica")
    valoracion: str = Field(..., description="Valoración de la medición")
    en_rango: bool = Field(..., description="Si está en rango")

class AnalisisTension(BaseModel):
    """Análisis completo de tensiones de un paciente"""
    estadisticas: EstadisticasTension
    ultima_medicion: Optional[UltimaTension] = None
