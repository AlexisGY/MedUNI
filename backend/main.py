from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

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
