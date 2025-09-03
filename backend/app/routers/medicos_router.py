from fastapi import APIRouter, HTTPException, status
from app.schemas.medico import Medico
from typing import List
from app.services.medicos_service import listar_medicos

router = APIRouter(prefix="/medicos", tags=["Medicos"])


@router.get("/especialidad/{id_especialidad}",  response_model=List[Medico])
def getMedicos(id_especialidad: int):
    return listar_medicos(id_especialidad)