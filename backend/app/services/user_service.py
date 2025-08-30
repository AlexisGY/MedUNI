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