from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, citas_router, especialidades_router, medicos_router, dias_disponibles_router, horarios_router
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
app.include_router(citas_router.router)
app.include_router(especialidades_router.router)
app.include_router(medicos_router.router)
app.include_router(dias_disponibles_router.router)
app.include_router(horarios_router.router)
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


# uvicorn app.main:app --reload     -- Correr backend 
# npm run dev                   -- Correr frontend 


