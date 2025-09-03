from app.db import get_connection  # tu conexión psycopg



def login_user(username: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contrasena_dirce FROM estudiantes WHERE codigo_estudiante = %s", (username,))
    row = cur.fetchone()
    conn.close()
    
    # Si existe y coincide la contraseña
    if row and row[0] == password:
        return True
    return False


def get_me(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombres, apellidos, correo, codigo_estudiante, contrasena_dirce FROM estudiantes WHERE codigo_estudiante = %s", (username,))
    row = cur.fetchone()
    conn.close()

    if row :
        # If the password matches, return a dictionary with all the user's data.
        return {
            "id": row[0],
            "nombres": row[1],
            "apellidos": row[2],
            "correo": row[3],
            "cod_estudiante": row[4]
        }
    
    # If login fails, return None.
    return None