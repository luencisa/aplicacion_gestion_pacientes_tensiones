from pydantic import BaseModel, Field
from typing import Optional

class BusquedaPaciente(BaseModel):
    """Esquema para búsqueda de pacientes"""
    query: str = Field(..., min_length=1, description="Término de búsqueda")
    buscar_por: Optional[str] = Field("nombre", description="Campo en el que buscar: nombre, apellido, todos")

class FiltroTension(BaseModel):
    """Esquema para filtrado de mediciones de tensión"""
    id_paciente: str = Field(..., description="ID del paciente")
    fecha_inicio: Optional[str] = Field(None, description="Fecha de inicio (YYYY-MM-DD)")
    fecha_fin: Optional[str] = Field(None, description="Fecha de fin (YYYY-MM-DD)")
    estado: Optional[str] = Field(None, description="Estado a filtrar")
