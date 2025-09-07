from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserLogin, AuthenticatedUser
from app.services.user_service import login_user, get_me
import secrets, time

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(data: UserLogin):
    ok = login_user(data.username, data.password)
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
    user_data = get_me(username)
    if user_data:
        return {
            "id" : user_data["id"],
            "nombres": user_data["nombres"] , # Return the full user data here
            "apellidos": user_data["apellidos"],
            "correo": user_data["correo"],
            "cod_estudiante": user_data["cod_estudiante"]
     }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="❌ Credenciales inválidas"
    )