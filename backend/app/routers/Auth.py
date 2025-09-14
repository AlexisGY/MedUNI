from fastapi import APIRouter, HTTPException, status
from app.schemas.Usuario import UserLogin, AuthenticatedUser
from app.services.UserService import loginUsuario, getUsuario
import secrets, time

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(data: UserLogin):
    ok = loginUsuario(data.username, data.password)
    if ok:
        # Token muy básico (NO usar en producción) solo para que el frontend detecte sesión.
        fake_token = secrets.token_hex(16) + ":" + str(int(time.time()))
        return {
            "message": "✅ Login exitoso",
            "user": data.username,
            "token": fake_token,
        }
    raise HTTPException(status_code=401, detail="Credenciales inválidas")


#INTEGRAR
@router.get("/me", response_model = AuthenticatedUser)
def me(username: str):
    user_data = getUsuario(username)
    if user_data:
        return {
            "id" : user_data["id"],
            "nombres": user_data["nombres"] , # Return the full user data here
            "apellidos": user_data["apellidos"],
            "correo": user_data["correo"],
            "codEstudiante": user_data["codEstudiante"]
     }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="❌ Credenciales inválidas"
    )