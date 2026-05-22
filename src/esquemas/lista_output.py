from pydantic import BaseModel, Field
from typing import Literal

class ListaOutput(BaseModel):
    id: str = Field(..., alias="_id", description="ID técnico de la entrada en la lista")
    id_paciente: str = Field(..., description="ID del paciente asociado")
    fecha_hora: str = Field(..., description="Día y hora prevista (YYYY-MM-DD HH:MM)")
    servicio: Literal["consulta", "enfermeria"] = Field(..., description="Servicio a prestar")
    estado: Literal["pendiente", "atendido", "anulado"] = Field(..., description="Estado actual de la cita")

    class Config:
        populate_by_name = True
