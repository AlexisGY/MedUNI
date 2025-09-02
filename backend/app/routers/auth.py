from fastapi import APIRouter, HTTPException
from app.schemas.user import UserLogin
from app.services.user_service import login_user
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
