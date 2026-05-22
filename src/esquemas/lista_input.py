from pydantic import BaseModel, Field
from typing import Literal

class ListaInput(BaseModel):
    id_paciente: str = Field(..., description="ID del paciente al que se prestará el servicio")
    fecha_hora: str = Field(
        ..., 
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", 
        description="Día y hora prevista para la prestación del servicio en formato YYYY-MM-DD HH:MM"
    )
    servicio: Literal["consulta", "enfermeria"] = Field(
        ..., 
        description="Servicio que será prestado: consulta (médico) o enfermería (enfermero)"
    )
    estado: Literal["pendiente", "atendido", "anulado"] = Field(
        "pendiente", 
        description="Estado del servicio en la lista"
    )
