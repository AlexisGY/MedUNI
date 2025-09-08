from app.schemas.citas import CitaCreate, CitaResponse
from app.db import get_connection  # tu conexión psycopg

def reservar_cita(cita: CitaCreate):
        conn = get_connection()
        cur = conn.cursor()
    #---------VALIDACIONES---------------------
        validarEstudiante(cita.estudiante_id, cur)
        validarEspecialidad(cita.especialidad_id, cur)
        validarMedico(cita.medico_id, cur)
        validarFechaHora(cita.fecha, cita.hora, cita.medico_id, cur)
        validarEstado(cita.estado)
        #------------------------------------------
        cur.execute(
            "INSERT INTO citas (estudiante_id, medico_id, fecha, hora, estado, especialidad_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (cita.estudiante_id, cita.medico_id, cita.fecha, cita.hora, cita.estado, cita.especialidad_id)
        )
        conn.commit()
        conn.close()
        return cita

def getCitasReservadas(estudiante_id: int):
    conn = get_connection()
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
        (estudiante_id,)
    )
    citas = cur.fetchall()
    conn.close()
    return citas

# Validaciones
def validarEstudiante(estudiante_id: int, cur):
    cur.execute("SELECT id FROM estudiantes WHERE id = %s", (estudiante_id,))
    if cur.fetchone() is None:
        raise ValueError(f"Estudiante con ID {estudiante_id} no existe.")

def validarEspecialidad(especialidad_id: int, cur):
    cur.execute("SELECT id FROM especialidades WHERE id = %s", (especialidad_id,))  
    if cur.fetchone() is None:
        raise ValueError(f"Especialidad con ID {especialidad_id} no existe.")

def validarMedico(medico_id: int, cur):
    cur.execute("SELECT id FROM medicos WHERE id = %s", (medico_id,))
    if cur.fetchone() is None:
        raise ValueError(f"Médico con ID {medico_id} no existe.")

def validarFechaHora(fecha, hora, medico_id, cur):
    cur.execute("SELECT id FROM citas WHERE fecha = %s AND hora = %s AND medico_id =%s", (fecha, hora, medico_id))
    if cur.fetchone() is not None:
        raise ValueError(f"Ya existe una cita programada para {fecha} a las {hora} para el medico seleccionado.")
    
def validarEstado(estado: str):
    estados_validos = ["pendiente", "confirmada", "cancelada"]
    if estado not in estados_validos:
        raise ValueError(f"Estado '{estado}' no es válido. Estados permitidos: {', '.join(estados_validos)}.")