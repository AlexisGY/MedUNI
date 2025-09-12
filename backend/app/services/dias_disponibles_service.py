from app.db import get_connection
from datetime import date, timedelta

def listar_dias_semana(especialidad_id, semanas=2):
    """
    Retorna los días de la semana (o semanas siguientes) con su estado disponible/no disponible.
    - especialidad_id: id de la especialidad
    - semanas: número de semanas a generar (default 1 = semana actual)
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Calcular rango de fechas
    hoy = date.today()
    inicio_semana = hoy # lunes de esta semana
    fin_semana = inicio_semana + timedelta(days=7*semanas - 1)

    query = """
            WITH rango AS (
            SELECT generate_series(%s::date, %s::date, '1 day')::date AS fecha
        )
        SELECT  r.fecha,
               CASE WHEN MAX(CASE
			                   WHEN de.id IS NOT NULL
			                        AND r.fecha BETWEEN de.fecha_inicio AND de.fecha_fin
			                        AND EXTRACT(ISODOW FROM r.fecha)::int = de.dia_semana
			                        AND de.disponibilidad = true
			                   THEN 1
			                   ELSE 0
               		END) = 1
				THEN true
		        ELSE false
		END AS disponible
        FROM rango r
        LEFT JOIN disponibilidad_especialidad de
               ON de.especialidad_id = %s
		GROUP BY r.fecha
        ORDER BY r.fecha
    """
    cursor.execute(query, (inicio_semana, fin_semana, especialidad_id))
    dias = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"fecha": dia[0], "disponible": dia[1]} for dia in dias]