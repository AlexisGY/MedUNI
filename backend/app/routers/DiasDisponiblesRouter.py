from fastapi import APIRouter, HTTPException, status
from app.schemas.DiasDisponibles import DiasDisponibles
from typing import List
from app.services.DiasDisponiblesService import listarDiasSemana

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad"])


@router.get("/{especialidadId}", response_model=List[DiasDisponibles])
def getDiasDisponibles(especialidadId: int):
    return listarDiasSemana(especialidadId, 2)
