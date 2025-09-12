from app.db import get_connection

def listar_medicos(id_especialidad: int):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, nombres, apellidos, especialidad_id
        FROM medicos
        WHERE especialidad_id = %s
    """
    cursor.execute(query, (id_especialidad,))
    medicos = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": m[0],
            "nombres": m[1],
            "apellidos": m[2],
            "especialidad_id": m[3]

        }
        for m in medicos
    ]