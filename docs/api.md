# API - MedUNI

Base URL: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

---

## Salud del servicio
- GET `/` → estado y versión de la base de datos

---

## Autenticación
- POST `/auth/login`
	- body: `{ username: string, password: string }`
		- username = código_estudiante
		- password = código_dirce
	- 200: `{ message, user, token }`
	- 401: `Credenciales inválidas`

- GET `/auth/me?username=...`
	- 200: `{ id, nombres, apellidos, correo, codEstudiante }`
	- 401: `Credenciales inválidas`

---

## Especialidades
- GET `/especialidades/`
	- 200: Lista de especialidades

---

## Médicos
- GET `/medicos/especialidad/{especialidadId}`
	- 200: Lista de médicos por especialidad

---

## Disponibilidad de días
- GET `/disponibilidad/{especialidadId}`
	- 200: Días disponibles para la especialidad

---

## Horarios
- GET `/horarios/{medicoId}/{fecha}`
	- params:
		- medicoId: number
		- fecha: string (YYYY-MM-DD)
	- 200: Lista de horarios disponibles

---

## Citas
- POST `/citas/reservar`
	- body: `{ estudianteId, medicoId, especialidadId, fecha (YYYY-MM-DD), hora (HH:MM), estado }`
	- 200: Objeto con los mismos campos confirmados
	- 401: Error al reservar

- GET `/citas/citas_reservadas/{estudianteId}`
	- 200: Lista de citas del estudiante
	- 404: No hay citas confirmadas

- DELETE `/citas/cancelar_cita/{citaId}`
	- 200: Objeto con resultado de cancelación
	- 404/400: Error al cancelar

