from fastapi import APIRouter, HTTPException, status
from app.schemas.Medicos import Medico
from typing import List
from app.services.MedicosService import listarMedicos

router = APIRouter(prefix="/medicos", tags=["Medicos"])


@router.get("/especialidad/{especialidadId}",  response_model=List[Medico])
def getMedicos(especialidadId: int):
    return listarMedicos(especialidadId)