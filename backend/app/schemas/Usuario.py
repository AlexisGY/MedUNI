from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class AuthenticatedUser(BaseModel):
    id: int 
    nombres: str
    apellidos: str
    correo: str
    codEstudiante: str
