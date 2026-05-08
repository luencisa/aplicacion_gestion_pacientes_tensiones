from pydantic import BaseModel, Field
from esquemas.tension_valores import TensionValores

class TensionInput(BaseModel):
    id_paciente: str = Field(..., pattern=r"^[0-9a-fA-F]{24}$", description="ID del paciente (formato ObjectId de MongoDB)")
    valores: TensionValores
    estado: str = Field(..., description="Estado de la medición")
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de la medición en formato YYYY-MM-DD")
    valoracion: str = Field(..., description="Valoración de la tensión")
    valor_en_rango: bool = Field(..., description="Si el valor está en rango o no")
