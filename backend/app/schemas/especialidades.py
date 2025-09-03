from pydantic import BaseModel

class Especialidad(BaseModel):
    id: int
    nombre: str
    estado: bool