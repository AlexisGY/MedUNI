from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import Auth
from app.db import getConnection
from app.routers import CitasRouter, DiasDisponiblesRouter, EspecialidadesRouter, HorariosRouter, MedicosRouter

# routers 


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], # DOMINIO DEL FRONTEND
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
# routers 
app.include_router(Auth.router)
app.include_router(CitasRouter.router)
app.include_router(EspecialidadesRouter.router)
app.include_router(MedicosRouter.router)
app.include_router(DiasDisponiblesRouter.router)
app.include_router(HorariosRouter.router)
# Verificando la conexión a la base de datos al iniciar la app
@app.get("/")
def root():
    conn = getConnection()
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


