from pydantic import BaseModel, Field
from typing import Literal

class PacienteInput(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del paciente")
    apellido: str = Field(..., min_length=1, description="Apellido del paciente")
    género: Literal["Masculino", "Femenino"] = Field(..., description="Género del paciente")
    fechaNacimiento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de nacimiento en formato YYYY-MM-DD")
