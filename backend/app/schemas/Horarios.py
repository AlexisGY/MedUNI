from pydantic import BaseModel
from datetime import time 

class Horario(BaseModel):
    horaInicio: time
    horaFin: time 
    disponibilidad: bool