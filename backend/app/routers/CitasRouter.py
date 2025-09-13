from fastapi import APIRouter, HTTPException, status
from app.schemas.Citas import CitaCreada, CitaCrear
from app.services.CitasService import reservarCita, getCitasReservadas
from typing import List

router = APIRouter(prefix="/citas", tags=["Citas"])

#INTEGRAR 
@router.post("/reservar", response_model = CitaCrear)
def reservar(data: CitaCrear):
    citaReservada = reservarCita(data)
    
    if citaReservada:
        return {
            "estudianteId": data.estudianteId,
            "medicoId": data.medicoId,
            "especialidadId": data.especialidadId,
            "fecha": data.fecha,
            "hora": data.hora.strftime("%H:%M"),
            "estado": data.estado
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="❌ Credenciales inválidas"
    )


@router.get("/citas_reservadas/{estudianteId}", response_model=List[CitaCreada])
def mostrarCitas(estudianteId: int):
    data = getCitasReservadas(estudianteId)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="❌ No hay citas confirmadas"
        )

    return data