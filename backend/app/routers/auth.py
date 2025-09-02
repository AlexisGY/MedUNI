from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserLogin, AuthenticatedUser
from app.services.user_service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model = AuthenticatedUser)
def login(data: UserLogin):
    user_data = login_user(data.username, data.password)
    
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