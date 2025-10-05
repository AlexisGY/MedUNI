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
(1, '2025-10-01', '2025-10-30', '14:00', '20:00', 2),
(1, '2025-10-01', '2025-10-30', '08:00', '14:00', 4);

-- Días no disponibles
INSERT INTO disponibilidad_especialidad (especialidad_id, fecha_inicio, fecha_fin, hora_inicio, hora_fin, dia_semana)
VALUES
--(1, '2025-10-01', '2025-10-30', '08:00', '12:00', 3, FALSE),
--(1, '2025-10-01', '2025-10-30', '08:00', '12:00', 5, FALSE);
(2, '2025-10-01', '2025-10-30', '10:00', '18:00', 4),  -- Cardiología:
(3, '2025-10-01', '2025-10-30', '08:00', '14:00', 2),  -- Nutrición: Martes, Miércoles, Jueves de 8 a.m. a 2 p.m.
(3, '2025-10-01', '2025-10-30', '08:00', '20:00', 4),
(3, '2025-10-01', '2025-10-30', '08:00', '14:00', 5),
(5, '2025-10-01', '2025-10-30', '08:00', '20:00', 1),
(6, '2025-10-01', '2025-10-30', '08:00', '20:00', 2),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 1),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 2),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 3),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 4),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 5),
(7, '2025-10-01', '2025-10-30', '08:00', '20:00', 6),
(8, '2025-10-01', '2025-10-30', '1500', '20:00', 4),
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 1),  -- Odontología: Lunes a Sábado
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 2),
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 3),
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 4),
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 5),
(9, '2025-10-01', '2025-10-30', '08:00', '20:00', 6),
(10, '2025-10-01', '2025-10-30', '08:00', '20:00', 1),
(10, '2025-10-01', '2025-10-30', '10:00', '16:00', 2),
(10, '2025-10-01', '2025-10-30', '10:00', '16:00', 3),
(10, '2025-10-01', '2025-10-30', '10:00', '16:00', 4),
(10, '2025-10-01', '2025-10-30', '10:00', '16:00', 5),
(10, '2025-10-01', '2025-10-30', '10:00', '16:00', 6),
(12, '2025-10-01', '2025-10-30', '14:00', '20:00', 1),
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 1),
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 2),
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 3),
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 4),
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 5),-- Cardiología: Jueves de 10 a.m. a 4 p.m.
(13, '2025-10-01', '2025-10-30', '08:00', '20:00', 6),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 1),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 2),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 3),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 4),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 6),
(14, '2025-10-01', '2025-10-30', '08:00', '14:00', 1),
(15, '2025-10-01', '2025-10-30', '08:00', '14:00', 1),
(15, '2025-10-01', '2025-10-30', '08:00', '14:00', 2),
(15, '2025-10-01', '2025-10-30', '08:00', '14:00', 3),
(15, '2025-10-01', '2025-10-30', '08:00', '14:00', 4),
(15, '2025-10-01', '2025-10-30', '08:00', '14:00', 5);



-- Médicos
INSERT INTO medicos (nombres, apellidos, correo, especialidad_id)
VALUES
-- Cirugía General
('Saldivar', 'Medina', 'saldivar.medina@gmail.com', 1),
('Samuel', 'Gutierrez', 'Samuel.gutierrez@gmail.com', 1),
-- Cardiología
('Ana', 'López', 'ana.lopez@correo.com', 2),
('Ricardo', 'Ramírez', 'ricardo.ramirez@correo.com', 2),

-- Ginecología
('María', 'Hernández', 'maria.hernandez@correo.com', 3),
('Sofía', 'Torres', 'sofia.torres@correo.com', 3),

-- Urología
('Luis', 'Martínez', 'luis.martinez@correo.com', 4),
('Pedro', 'García', 'pedro.garcia@correo.com', 4),

-- Oftalmología
('Laura', 'Sánchez', 'laura.sanchez@correo.com', 5),
('Javier', 'Rodríguez', 'javier.rodriguez@correo.com', 5),

-- Endocrinología
('Ricardo', 'Jiménez', 'ricardo.jimenez@correo.com', 6),
('Elena', 'Pérez', 'elena.perez@correo.com', 6),

-- Psicología
('Beatriz', 'Flores', 'beatriz.flores@correo.com', 7),
('Claudia', 'Gutiérrez', 'claudia.gutierrez@correo.com', 7),

-- Otorrinolaringología
('José', 'Díaz', 'jose.diaz@correo.com', 8),
('Victor', 'Morales', 'victor.morales@correo.com', 8),

-- Odontología
('Andrea', 'Martínez', 'andrea.martinez@correo.com', 9),
('Manuel', 'Luna', 'manuel.luna@correo.com', 9),

-- Psiquiatría
('Lucía', 'Vargas', 'lucia.vargas@correo.com', 10),
('Francisco', 'Serrano', 'francisco.serrano@correo.com', 10),

-- Laboratorio Clínico
('Alejandro', 'Castro', 'alejandro.castro@correo.com', 11),
('Marta', 'Salazar', 'marta.salazar@correo.com', 11),

-- Neumología
('Carlos', 'Jiménez', 'carlos.jimenez@correo.com', 12),
('Paula', 'Ríos', 'paula.rios@correo.com', 12),

-- Medicina Interna/Familia/General
('José', 'González', 'jose.gonzalez@correo.com', 13),
('Isabel', 'López', 'isabel.lopez@correo.com', 13),

-- Nutrición
('Valeria', 'García', 'valeria.garcia@correo.com', 14),
('Raúl', 'Mendoza', 'raul.mendoza@correo.com', 14),

-- Ecografía
('Gabriela', 'Figueroa', 'gabriela.figueroa@correo.com', 15),
('Juan', 'Sánchez', 'juan.sanchez@correo.com', 15);










-- Insertar un estudiante
INSERT INTO estudiantes (nombres, apellidos, correo, codigo_estudiante, codigo_dirce)
VALUES ('Jharo', 'Paucarcaja Ramos', 'jharolym.paucarcaja.r@uni.pe', '20234044I', '111111'),
('Alexis', 'Garay', 'alexis.g@uni.pe', '20244017D', '111111'),
('Rolly', 'Mamani', 'rolly.m@uni.pe', '20240010E', '111111');
