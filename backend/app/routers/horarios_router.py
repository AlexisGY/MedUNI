from fastapi import APIRouter, HTTPException, status
from app.schemas.horarios import Horario
from datetime import time, date
from typing import List
from app.services.horarios_service import gen_horarios

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/{medico_id}/{fecha}",  response_model=List[Horario])
def getMedicos(fecha: date, medico_id:int):
    return gen_horarios(fecha, medico_id)