from pydantic import BaseModel
from datetime import time 

class Horario(BaseModel):
    hora_inicio: time
    hora_fin: time 
    disponibilidad: bool