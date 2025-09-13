from fastapi import APIRouter, HTTPException, status
from app.schemas.Especialidades import Especialidad
from typing import List
from app.services.EspecialidadesService import listarEspecialidades

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])


@router.get("/", response_model=List[Especialidad])
def getEspecialidades():
    return listarEspecialidades()
