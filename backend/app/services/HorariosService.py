from app.db import getConnection  # tu conexión psycopg
from datetime import date, timedelta


def genHorarios(dia: date, medicoId: int):
    """
    Genera los horarios disponibles para un médico en un día específico.
    - dia: fecha específica
    - medico_id: id del médico
    """
    conn = getConnection()
    cursor = conn.cursor()
    # Definir el rango de horas (por ejemplo, de 08:00 a 17:00)
    query ="""
            SELECT de.hora_inicio, de.hora_fin
        FROM disponibilidad_especialidad de
        INNER JOIN medicos me
            ON me.especialidad_id = de.especialidad_id
        WHERE EXTRACT(ISODOW FROM %s::date) = de.dia_semana 
        AND me.id = %s"""
    cursor.execute(query, (dia, medicoId))
    horas_limte = cursor.fetchall()
    hora_inicio = horas_limte[0][0]
    hora_final = horas_limte[0][1]
    cursor.close()
    #Por ahora se manejará una duración de cita de 30 minutos.


    conn = getConnection()
    cursor = conn.cursor()
    query = """
                WITH horarios AS (
            SELECT 
                generate_series(
                    ('2025-09-05 ' || %s)::timestamp, 
                    ('2025-09-05 ' || %s)::timestamp - interval '30 minutes', 
                    interval '30 minutes'
                ) AS hora_inicio
        )
        SELECT 
            hora_inicio::time AS hora_inicio, 
            (hora_inicio + interval '30 minutes')::time AS hora_final,
            CASE 
                WHEN c.id IS NOT NULL THEN FALSE  -- Si existe una cita, disponibilidad es false
                ELSE TRUE  -- Si no existe una cita, disponibilidad es true
            END AS disponibilidad
        FROM horarios h
        LEFT JOIN citas c
            ON c.medico_id = %s  -- El id del médico que estamos verificando
            AND c.fecha = %s  -- La fecha que estamos verificando
            AND c.hora = hora_inicio::time  -- Verificamos si ya existe una cita a esa hora
        ORDER BY hora_inicio;
    """
    cursor.execute(query, (hora_inicio, hora_final, medicoId, dia))
    horarios = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"horaInicio": horario[0], "horaFin": horario[1],"disponibilidad": horario[2]} for horario in horarios]  
