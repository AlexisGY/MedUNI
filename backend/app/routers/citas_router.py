from fastapi import APIRouter, HTTPException, status
from app.schemas.citas import CitaCreate, CitaResponse
from app.services.citas_service import reservar_cita, getCitasReservadas
from typing import List

router = APIRouter(prefix="/citas", tags=["Citas"])

#INTEGRAR 
@router.post("/reservar", response_model = CitaCreate)
def reservar(data: CitaCreate):
    cita_reservada = reservar_cita(data)
    
    if cita_reservada:
        return {
            "estudiante_id": data.estudiante_id,
            "medico_id": data.medico_id,
            "especialidad_id": data.especialidad_id,
            "fecha": data.fecha,
            "hora": data.hora.strftime("%H:%M"),
            "estado": data.estado
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="❌ Credenciales inválidas"
    )


@router.get("/citas_reservadas/{estudiante_id}", response_model=List[CitaResponse])
def mostrar_citas(estudiante_id: int):
    data = getCitasReservadas(estudiante_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="❌ No hay citas confirmadas"
        )

    return [
        {
            "cita_id": row[0],
            "estudiante_id": row[1],
            "medico_nombre": row[2],
            "especialidad_nombre": row[3],
            "fecha": row[4],
            "hora": row[5].strftime("%H:%M"),
            "estado": row[6],
        }
        for row in data
    ]