from pydantic import BaseModel
from datetime import datetime, date, time

class CitaCreate(BaseModel):
    estudiante_id: int
    medico_id: int
    especialidad_id: int
    fecha: date
    hora: time
    estado: str # e.g., "pendiente", "confirmada", "cancelada"

class CitaResponse(BaseModel):
    cita_id: int
    estudiante_id: int
    medico_nombre: str
    especialidad_nombre: str
    fecha: date
    hora: time
    estado: str