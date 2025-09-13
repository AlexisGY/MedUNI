from fastapi import APIRouter, HTTPException, status
from app.schemas.Horarios import Horario
from datetime import time, date
from typing import List
from app.services.HorariosService import genHorarios

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/{medicoId}/{fecha}",  response_model=List[Horario])
def getHorarios(fecha: date, medicoId:int):
    horarios = genHorarios(fecha, medicoId)
    return horarios