from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class AuthenticatedUser(BaseModel):
    id: int | None = None
    nombres: str
    apellidos: str
    correo: str
    cod_estudiante: str
