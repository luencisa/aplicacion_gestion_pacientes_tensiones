from pydantic import BaseModel, Field
from esquemas.tension_valores import TensionValores
from esquemas.estado_observacion import EstadoObservacion

class TensionInput(BaseModel):
    id_paciente: str = Field(..., description="ID del paciente")
    valores: TensionValores
    estado: EstadoObservacion = Field(..., description="Estado FHIR Observation.status")
    fecha: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Fecha de la medición en formato YYYY-MM-DD")
    valoracion: str = Field(..., description="Valoración de la tensión")
    valor_en_rango: bool = Field(..., description="Si el valor está en rango o no")
