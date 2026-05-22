from pydantic import BaseModel, Field
from typing import Literal

class TensionValores(BaseModel):
    sistolica: int = Field(..., gt=0, description="Tensión sistólica (mmHg)")
    diastolica: int = Field(..., gt=0, description="Tensión diastólica (mmHg)")
    metodo: Literal["Auscultación", "Oscilometría", "Palpación"] = Field(..., description="Método de medición")
    sitio_cuerpo: Literal["Brazo Derecho", "Brazo Izquierdo", "Muslo"] = Field(..., description="Sitio donde se tomó")
    tamaño_brazalete: Literal["Neonatal", "Infantil", "Estándar", "Muslo", "Grandes"] = Field(..., description="Tamaño del brazalete usado")
    dispositivo: str = Field(..., description="Dispositivo empleado para la medición")
