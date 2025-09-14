from app.schemas.Citas import CitaCrear
from fastapi import HTTPException
from app.db import getConnection  # tu conexión psycopg

def reservarCita(cita: CitaCrear):
        conn = getConnection()
        cur = conn.cursor()
    #---------VALIDACIONES---------------------
        validarEstudiante(cita.estudianteId, cur)
        validarEspecialidad(cita.especialidadId, cur)
        validarMedico(cita.medicoId, cur)
        validarFechaHora(cita.fecha, cita.hora, cita.medicoId, cur)
        validarEstado(cita.estado)
        #------------------------------------------
        cur.execute(
            "INSERT INTO citas (estudiante_id, medico_id, fecha, hora, estado, especialidad_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (cita.estudianteId, cita.medicoId, cita.fecha, cita.hora, cita.estado, cita.especialidadId)
        )
        conn.commit()
        conn.close()
        return cita

def getCitasReservadas(estudianteId: int):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.id, c.estudiante_id, m.nombres, e.nombre, c.fecha, c.hora, c.estado
        FROM citas c
        JOIN medicos m ON c.medico_id = m.id
        JOIN especialidades e ON m.especialidad_id = e.id
        WHERE c.estudiante_id = %s AND c.estado = 'pendiente'
        ORDER BY c.fecha DESC, c.hora DESC
        """,
        (estudianteId,)
    )
    citas = cur.fetchall()
    conn.close()
    return [
        {
            "citaId": c[0],
            "estudianteId": c[1],
            "medicoNombre": c[2],
            "especialidadNombre": c[3],
            "fecha": c[4],
            "hora": c[5],
            "estado": c[6]
        }
        for c in citas
    ]

def cancelarCita(citaId:int):
    conn = getConnection()
    cur = conn.cursor()
    # Validar si la cita existe
    cur.execute("SELECT id FROM citas WHERE id = %s", (citaId,))
    cita = cur.fetchone()
    
    if cita is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    # Proceder con la eliminación de la cita
    cur.execute("DELETE FROM citas WHERE id = %s", (citaId,))
    conn.commit()
    conn.close()
    
    return {"message": "Cita eliminada exitosamente"}

# Validaciones
def validarEstudiante(estudianteId: int, cur):
    cur.execute("SELECT id FROM estudiantes WHERE id = %s", (estudianteId,))
    if cur.fetchone() is None:
        raise ValueError(f"Estudiante con ID {estudianteId} no existe.")

def validarEspecialidad(especialidadId: int, cur):
    cur.execute("SELECT id FROM especialidades WHERE id = %s", (especialidadId,))  
    if cur.fetchone() is None:
        raise ValueError(f"Especialidad con ID {especialidadId} no existe.")

def validarMedico(medicoId: int, cur):
    cur.execute("SELECT id FROM medicos WHERE id = %s", (medicoId,))
    if cur.fetchone() is None:
        raise ValueError(f"Médico con ID {medicoId} no existe.")

def validarFechaHora(fecha, hora, medicoId, cur):
    cur.execute("SELECT id FROM citas WHERE fecha = %s AND hora = %s AND medico_id =%s", (fecha, hora, medicoId))
    if cur.fetchone() is not None:
        raise ValueError(f"Ya existe una cita programada para {fecha} a las {hora} para el medico seleccionado.")
    
def validarEstado(estado: str):
    estados_validos = ["pendiente", "confirmada", "cancelada"]
    if estado not in estados_validos:
        raise ValueError(f"Estado '{estado}' no es válido. Estados permitidos: {', '.join(estados_validos)}.")