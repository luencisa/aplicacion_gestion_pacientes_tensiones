from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import date

class PacienteOutput(BaseModel):
    id: str = Field(..., alias="_id", description="ID del paciente")
    nombre: str = Field(..., description="Nombre del paciente")
    apellido: str = Field(..., description="Apellido del paciente")
    género: Literal["Masculino", "Femenino"] = Field(..., description="Género del paciente")
    fechaNacimiento: date = Field(..., description="Fecha de nacimiento del paciente")

    class Config:
        populate_by_name = True
