from app.db import getConnection  # tu conexión psycopg

def listarEspecialidades():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, estado FROM especialidades WHERE estado = TRUE")
    especialidades = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": esp[0], "nombre": esp[1], "estado": esp[2]} for esp in especialidades]