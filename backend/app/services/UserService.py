from app.db import getConnection  # tu conexión psycopg



def loginUsuario(username: str, password: str):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute("SELECT codigo_dirce FROM estudiantes WHERE codigo_estudiante = %s", (username,))
    row = cur.fetchone()
    conn.close()

    # Si existe y coincide la contraseña
    if row and row[0] == password:
        return True
    return False


def getUsuario(codigo_estudiante: str):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombres, apellidos, correo, codigo_estudiante, codigo_dirce FROM estudiantes WHERE codigo_estudiante = %s", (codigo_estudiante,))
    row = cur.fetchone()
    conn.close()

    if row :
        # If the password matches, return a dictionary with all the user's data.
        return {
            "id": row[0],
            "nombres": row[1],
            "apellidos": row[2],
            "correo": row[3],
            "codEstudiante": row[4]
        }

    # If login fails, return None.
    return None