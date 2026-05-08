from pydantic import BaseModel, Field

class TensionValores(BaseModel):
    sistolica: int = Field(..., gt=0, description="Tensión sistólica")
    diastolica: int = Field(..., gt=0, description="Tensión diastólica")
