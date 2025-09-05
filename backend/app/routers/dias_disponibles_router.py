from fastapi import APIRouter, HTTPException, status
from app.schemas.dias_disponibles import DiasDisponibles
from typing import List
from app.services.dias_disponibles_service import listar_dias_semana

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad"])


@router.get("/{especialidad_id}", response_model=List[DiasDisponibles])
def get_especialidades(especialidad_id: int):
    return listar_dias_semana(especialidad_id, 1)
