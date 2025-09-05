from pydantic import BaseModel
from datetime import time 

class Horario(BaseModel):
    hora_incio: time
    hora_fin: time 