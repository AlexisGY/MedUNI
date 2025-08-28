from fastapi import APIRouter, HTTPException
from ..schemas.user import UserLogin
from ..services.user_service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: UserLogin):
    success = login_user(data.username, data.password)
    if success:
        return {"message": "✅ Login exitoso", "user": data.username}
    raise HTTPException(status_code=401, detail="❌ Credenciales inválidas")