from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class ResponseData(BaseModel, Generic[T]):
    """Respuesta genérica de la aplicación"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de la respuesta")
    data: Optional[T] = Field(None, description="Datos de la respuesta")

class ErrorResponse(BaseModel):
    """Respuesta de error"""
    success: bool = Field(False, description="Siempre False para errores")
    message: str = Field(..., description="Descripción del error")
    error_code: Optional[str] = Field(None, description="Código de error")
