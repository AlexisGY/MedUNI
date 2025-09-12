--- =======================
-- TABLAS
-- =======================

CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    codigo_estudiante VARCHAR(100) UNIQUE NOT NULL,
    codigo_dirce VARCHAR(100) NOT NULL
);

CREATE TABLE especialidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT true
);

CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    especialidad_id INT NOT NULL REFERENCES especialidades(id)
);

CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    estudiante_id INT NOT NULL REFERENCES estudiantes(id),
    medico_id INT NOT NULL REFERENCES medicos(id),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente', -- pendiente, confirmada, cancelada
    especialidad_id INT NOT NULL REFERENCES especialidades(id)
);

CREATE TABLE disponibilidad_especialidad (
    id SERIAL PRIMARY KEY,
    especialidad_id INT NOT NULL REFERENCES especialidades(id),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    dia_semana INT NOT NULL, -- ejemplo: [1,2,3,4,5] = lunes a viernes
    disponibilidad BOOLEAN NOT NULL DEFAULT TRUE,
    duracion_turno INT NOT NULL DEFAULT 30 --minutos por turno
);

CREATE TABLE horario_medico (
    id SERIAL PRIMARY KEY,               -- corregido: SERIAL para autoincrementar
    medico_id INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    dia_semana INT NOT NULL,             -- 1=Lunes ... 7=Domingo
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- =======================
-- DATOS
-- =======================

INSERT INTO especialidades (nombre) VALUES
('Cirugía General'),
('Cardiología'),
('Ginecología'),
('Urología'),
('Oftalmología'),
('Endocrinología'),
('Psicología'),
('Otorrinolaringología'),
('Odontología'),
('Psiquiatría'),
('Laboratorio Clínico'),
('Neumología'),
('Medicina Interna/Familia/General'),
('Nutrición'),
('Ecografía');

-- Disponibilidad por especialidad (días disponibles)
INSERT INTO disponibilidad_especialidad (especialidad_id, fecha_inicio, fecha_fin, hora_inicio, hora_fin, dia_semana)
VALUES
(1, '2025-09-01', '2025-09-30', '08:00', '12:00', 1),
(1, '2025-09-01', '2025-09-30', '08:00', '12:00', 2),
(1, '2025-09-01', '2025-09-30', '08:00', '12:00', 4);

-- Días no disponibles
INSERT INTO disponibilidad_especialidad (especialidad_id, fecha_inicio, fecha_fin, hora_inicio, hora_fin, dia_semana, disponibilidad)
VALUES
(1, '2025-09-01', '2025-09-30', '08:00', '12:00', 3, FALSE),
(1, '2025-09-01', '2025-09-30', '08:00', '12:00', 5, FALSE);

-- Médicos
INSERT INTO medicos (nombres, apellidos, correo, especialidad_id)
VALUES
('Saldivar', 'Medina', 'saldivar.medina@gmail.com', 1),
('Samuel', 'Gutierrez', 'Samuel.gutierrez@gmail.com', 1);


-- Insertar un estudiante
INSERT INTO estudiantes (nombres, apellidos, correo, codigo_estudiante, codigo_dirce)
VALUES
('Jharo', 'Paucarcaja Ramos', 'jharolym.paucarcaja.r@uni.pe', '20234044I', '111111'),
('Rolly Alejandro', 'Mamani Cutipa', 'rolly.mamani.c@uni.pe', '20240010E', '123456');