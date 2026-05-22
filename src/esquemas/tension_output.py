from pydantic import BaseModel, Field
from typing import Optional
from esquemas.tension_valores import TensionValores

class TensionOutput(BaseModel):
    id: str = Field(..., alias="_id", description="ID de la medición")
    id_paciente: str = Field(..., description="ID del paciente")
    nombre_paciente: Optional[str] = Field(None, description="Nombre completo del paciente")
    valores: TensionValores = Field(..., description="Valores de tensión")
    estado: str = Field(..., description="Estado de la medición")
    fecha: str = Field(..., description="Fecha de la medición")
    valoracion: str = Field(..., description="Valoración de la tensión")
    valor_en_rango: bool = Field(..., description="Si el valor está en rango")

    class Config:
        populate_by_name = True
