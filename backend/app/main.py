from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.db import get_connection

# routers 


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], # DOMINIO DEL FRONTEND
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
# routers 
app.include_router(auth.router)

# Verificando la conexión a la base de datos al iniciar la app
@app.get("/")
def root():
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
        conn.close()
        return {"status": "ok", "db_version": version[0]}
    else:
        return {"status": "error", "message": "No se pudo conectar a la base de datos"}

@app.post("/auth/login")
async def login(data: dict):
    email = data.get("email"); password = data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Faltan credenciales")
    # demo: acepta cualquier cosa no vacía
    return {"token": "demo-token", "user": {"email": email, "nombre": "Estudiante UNI"}}

@app.get("/especialidades")
async def especialidades():
    return ["Odontología","Medicina General","Psicología"]

@app.get("/horarios")
async def horarios(especialidad: str, fecha: str):
    base = ["08:00","08:30","09:00","09:30","10:00","10:30"]
    return [{"hora": h, "ocupado": (especialidad=="Odontología" and i%2==0)} for i,h in enumerate(base)]

# uvicorn main:app --reload     -- Correr backend 
# npm run dev                   -- Correr frontend 


