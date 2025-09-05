from pydantic import BaseModel
from datetime import date

class DiasDisponibles(BaseModel):
    fecha: date
    disponible: bool