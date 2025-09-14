from app.db import getConnection

def listarMedicos(especialidadId: int):
    conn = getConnection()
    cursor = conn.cursor()
    query = """
        SELECT id, nombres, apellidos, especialidad_id
        FROM medicos
        WHERE especialidad_id = %s
    """
    cursor.execute(query, (especialidadId,))
    medicos = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": m[0],
            "nombre": m[1],
            "apellido": m[2],
            "especialidadId": m[3]

        }
        for m in medicos
    ]