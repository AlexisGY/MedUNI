from fastapi import APIRouter, HTTPException, status
from app.schemas.especialidades import Especialidad
from typing import List
from app.services.especialidades_service import listar_especialidades

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])


@router.get("/", response_model=List[Especialidad])
def get_especialidades():
    return listar_especialidades()
