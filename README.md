# MedUNI – Sistema de reservas de citas

## ¿Qué es MedUNI?
MedUNI es una aplicación web para reservar citas médicas en el Centro Médico de la UNI de manera **rápida, remota y sin colas**.  
Con solo unos clics desde tu celular o computadora puedes:
- Ver especialidades disponibles.
- Elegir día y hora.
- Confirmar tu cita en segundos.

 Está pensada para **estudiantes de la UNI** y busca mejorar la organización y reducir la espera en la atención médica.

---

## Probar en 30 segundos
```bash
git clone https://github.com/AlexisGY/MedUNI.git
cd MedUNI
docker compose up --build
```
Abrir *http://localhost:5173* 

- [Frontend](http://localhost:5173)
- [Backend – Swagger](http://localhost:8000/docs)
- [pgAdmin](http://localhost:5050) (correo: admin@admin.com, pass: admin)
 

---

## Arquitectura
- **Backend**: FastAPI (Python 3.11) + Uvicorn  
- **Frontend**: Vue 3 + Vite, Bootstrap 5, Bootstrap Icons  
- **Base de datos**: PostgreSQL 13  
- **Administración DB**: pgAdmin4  

Servicios y puertos por defecto:
- Backend (FastAPI): `http://localhost:8000` (Swagger: `/docs`)
- Frontend (Vite dev): `http://localhost:5173`
- Postgres: `localhost:5432`
- pgAdmin: `http://localhost:5050`

---

## Requisitos
- Windows 10/11 con Docker Desktop + WSL2 (recomendado), o  
- macOS con Docker Desktop, o Linux con Docker Engine + Docker Compose  
- Memoria libre: ~2 GB para contenedores (Postgres + pgAdmin + frontend + backend)  
- Puertos libres: 5173, 8000, 5432, 5050  
- Opcional: Node 20 y Python 3.11 para desarrollo local 

---

## Inicio rápido con Docker
1) Levantar todo
```bash
docker compose up --build
```
2) Acceso rápido
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
- pgAdmin: [http://localhost:5050](http://localhost:5050)  
  (usuario: admin@admin.com / contraseña: admin)

3) Base de datos inicial
- Usuario: `user`  
- Contraseña: `password`  
- Base: `your_database`  
- Volumen persistente: `./data/db`  
- Si existe `./database-backup/dump.sql`, se restaurará al inicializar un volumen vacío.

4) Conexión en pgAdmin
- Host: `db`
- Port: `5432`
- User: `user`
- Password: `password`
- Database: `your_database`

---

## Variables de entorno (Backend)
El backend usa variables para conectar a Postgres (cargadas con `python-dotenv`).

Ejemplo de `backend/.env`:
```env
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database
DB_USER=user
DB_PASSWORD=password
```

---

## Desarrollo local (sin Docker)
### Backend
```bash
cd backend
python -m venv venv
./venv/Scripts/Activate.ps1 # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
### Frontend
```bash
cd frontend
npm ci
npm run dev
```
> Asegúrate de tener un Postgres local o un contenedor en marcha.

---

## Estructura de carpetas
```
backend/
  app/
    main.py
    db.py
    routers/
    schemas/
  Dockerfile
  requirements.txt
frontend/
  src/
    components/
    views/
    stores/
    services/
    utils/
  Dockerfile
  package.json
  vite.config.js

data/db/                 # Volumen de datos de Postgres
database-backup/dump.sql # Dump opcional auto-restaurado
docker-compose.yml
```

---

## Notas para desarrolladores

### Endpoints útiles
- **GET /** → prueba de conexión a la DB (retorna versión)
- **Swagger** → `/docs`

### Problemas comunes
- **Frontend no refresca en Docker**  
  Variables `CHOKIDAR_USEPOLLING` y `WATCHPACK_POLLING` ya están configuradas.  
  Si no ves cambios, reinicia el contenedor `frontend`.  

- **Backend no conecta a la DB**  
  Revisa `.env` en `backend/`. En Docker: `DB_HOST=db`.  

- **pgAdmin vacío**  
  Añade un servidor manualmente en pgAdmin con:  
  - Host: `db`, Puerto: `5432`, Usuario: `user`, Pass: `password`.  

- **Dump no aplicado**  
  `dump.sql` solo se ejecuta al iniciar un volumen vacío.  
  Si ya existe `./data/db`, elimínalo (⚠️ cuidado, perderás datos).  

---

## Licencia
Uso académico y demostrativo.
