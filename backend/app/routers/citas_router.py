from fastapi import APIRouter, HTTPException, status
from app.schemas.citas import CitaCreate, CitaResponse
from app.services.citas_service import reservar_cita, getCitaReservada

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


#CITA RESERVADA (DEBE MOSTRARSE EN PANTALLA)
@router.get("/cita-confirmada", response_model = CitaResponse)
def mostrar_cita(estudiante_id: int):
    data = getCitaReservada(estudiante_id)
    if data:
        return {
            "cita_id": data[0],
            "estudiante_id": data[1],
            "medico_nombre": data[2],
            "especialidad_nombre" : data[3],
            "fecha": data[4],
            "hora": data[5].strftime("%H:%M"),
            "estado": data[6]
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="❌ No hay citas confirmadas"
    )