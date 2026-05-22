from typing import Literal

# Valores admitidos por FHIR Observation.status
EstadoObservacion = Literal[
    "registered", "preliminary", "final",
    "amended", "corrected", "cancelled",
    "entered-in-error", "unknown"
]
