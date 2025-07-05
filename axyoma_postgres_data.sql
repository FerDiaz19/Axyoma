-- ========================================
-- SCRIPT SQL PARA POSTGRESQL - AXYOMA
-- ========================================
-- Ejecuta estos comandos en tu base de datos PostgreSQL 'axyoma'

-- 1. CREAR TABLA USUARIOS (adaptada para Django User model)
-- ========================================

CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- 2. CREAR TABLA PERFIL DE USUARIOS
-- ========================================

CREATE TABLE IF NOT EXISTS users_perfilusuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    nivel_usuario VARCHAR(20) NOT NULL CHECK (nivel_usuario IN ('superadmin', 'admin-empresa', 'admin-planta')),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    admin_empresa_id INTEGER,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_empresa_id) REFERENCES users_perfilusuario(id)
);

-- 3. CREAR TABLA EMPRESAS
-- ========================================

CREATE TABLE IF NOT EXISTS users_empresa (
    empresa_id SERIAL PRIMARY KEY,
    nombre VARCHAR(65) NOT NULL UNIQUE,
    rfc VARCHAR(16) NOT NULL UNIQUE,
    direccion TEXT,
    logotipo VARCHAR(128),
    email_contacto VARCHAR(128),
    telefono_contacto VARCHAR(15),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    administrador_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (administrador_id) REFERENCES users_perfilusuario(id)
);

-- 4. CREAR TABLA PLANTAS
-- ========================================

CREATE TABLE IF NOT EXISTS users_planta (
    planta_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    direccion TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES users_empresa(empresa_id)
);

-- 5. CREAR TABLA DEPARTAMENTOS
-- ========================================

CREATE TABLE IF NOT EXISTS users_departamento (
    departamento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    descripcion TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    planta_id INTEGER NOT NULL,
    FOREIGN KEY (planta_id) REFERENCES users_planta(planta_id)
);

-- 6. CREAR TABLA PUESTOS
-- ========================================

CREATE TABLE IF NOT EXISTS users_puesto (
    puesto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    departamento_id INTEGER NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES users_departamento(departamento_id)
);

-- 7. CREAR TABLA EMPLEADOS
-- ========================================

CREATE TABLE IF NOT EXISTS users_empleado (
    empleado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    genero VARCHAR(10) NOT NULL CHECK (genero IN ('Masculino', 'Femenino')),
    antiguedad INTEGER,
    status BOOLEAN DEFAULT TRUE,
    puesto_id INTEGER NOT NULL,
    departamento_id INTEGER NOT NULL,
    planta_id INTEGER NOT NULL,
    FOREIGN KEY (puesto_id) REFERENCES users_puesto(puesto_id),
    FOREIGN KEY (departamento_id) REFERENCES users_departamento(departamento_id),
    FOREIGN KEY (planta_id) REFERENCES users_planta(planta_id)
);

-- ========================================
-- INSERTAR DATOS DE PRUEBA
-- ========================================

-- 1. INSERTAR USUARIOS AUTH_USER
-- ========================================

INSERT INTO auth_user (username, email, password, first_name, last_name, is_staff, is_superuser, is_active, date_joined) VALUES
('ed-rubio@axyoma.com', 'ed-rubio@axyoma.com', 'pbkdf2_sha256$600000$' || encode(gen_random_bytes(12), 'base64') || '$1234', 'Ed', 'Rubio', TRUE, TRUE, TRUE, NOW()),
('juan.perez@codewave.com', 'juan.perez@codewave.com', 'pbkdf2_sha256$600000$' || encode(gen_random_bytes(12), 'base64') || '$1234', 'Juan', 'Perez', FALSE, FALSE, TRUE, NOW()),
('maria.gomez@codewave.com', 'maria.gomez@codewave.com', 'pbkdf2_sha256$600000$' || encode(gen_random_bytes(12), 'base64') || '$1234', 'Maria', 'Gomez', FALSE, FALSE, TRUE, NOW()),
('carlos.ruiz@codewave.com', 'carlos.ruiz@codewave.com', 'pbkdf2_sha256$600000$' || encode(gen_random_bytes(12), 'base64') || '$1234', 'Carlos', 'Ruiz', FALSE, FALSE, TRUE, NOW());

-- 2. INSERTAR PERFILES DE USUARIO
-- ========================================

INSERT INTO users_perfilusuario (nombre, apellido_paterno, apellido_materno, nivel_usuario, user_id, admin_empresa_id) VALUES
('Ed', 'Rubio', NULL, 'superadmin', 1, NULL),
('Juan', 'Perez', NULL, 'admin-empresa', 2, NULL),
('Maria', 'Gomez', NULL, 'admin-planta', 3, 2),
('Carlos', 'Ruiz', NULL, 'admin-planta', 4, 2);

-- 3. INSERTAR EMPRESA
-- ========================================

INSERT INTO users_empresa (nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, administrador_id) VALUES
('Soluciones Industriales MX', 'SIMX920314ABC', 'Av. Revolución 123, Col. Centro, CDMX', 'https://i.pinimg.com/736x/24/7e/85/247e85b4cdcc74b50326fb36128dbce4.jpg', 'contacto@solucionesmx.com', '5551234567', 2);

-- 4. INSERTAR PLANTAS
-- ========================================

INSERT INTO users_planta (nombre, direccion, empresa_id) VALUES
('Oficina Central Tijuana', 'Av. Principal 456, Tijuana, BC', 1),
('Oficina Monterrey', 'Blvd. Constitución 789, Monterrey, NL', 1);

-- 5. INSERTAR DEPARTAMENTOS
-- ========================================

INSERT INTO users_departamento (nombre, descripcion, planta_id) VALUES
('Recursos Humanos', 'Gestión de personal y bienestar laboral', 1),
('Desarrollo de Software', 'Creación y mantenimiento de aplicaciones', 1),
('Operaciones', 'Gestión de operaciones y producción', 1),
('Calidad', 'Control de calidad y aseguramiento', 2),
('Mantenimiento', 'Mantenimiento de equipos e instalaciones', 2);

-- 6. INSERTAR PUESTOS
-- ========================================

INSERT INTO users_puesto (nombre, descripcion, departamento_id) VALUES
('Gerente de RRHH', 'Líder del equipo de Recursos Humanos', 1),
('Desarrollador Senior', 'Programador experimentado', 2),
('Desarrollador Junior', 'Programador en formación', 2),
('Supervisor de Operaciones', 'Supervisión de procesos operativos', 3),
('Especialista en Calidad', 'Análisis y control de calidad', 4),
('Técnico de Mantenimiento', 'Mantenimiento preventivo y correctivo', 5);

-- 7. INSERTAR EMPLEADOS
-- ========================================

INSERT INTO users_empleado (nombre, apellido_paterno, apellido_materno, genero, antiguedad, puesto_id, departamento_id, planta_id) VALUES
('Laura', 'Fernández', 'Torres', 'Femenino', 5, 1, 1, 1),
('José', 'Martínez', 'López', 'Masculino', 2, 2, 2, 1),
('Ana', 'García', 'Ruiz', 'Femenino', 3, 3, 2, 1),
('Carlos', 'López', 'Hernández', 'Masculino', 4, 4, 3, 1),
('María', 'Rodríguez', 'Sánchez', 'Femenino', 1, 5, 4, 2),
('Pedro', 'González', 'Morales', 'Masculino', 6, 6, 5, 2);

-- ========================================
-- VERIFICAR DATOS INSERTADOS
-- ========================================

-- Verificar usuarios
SELECT u.username, u.email, p.nombre, p.apellido_paterno, p.nivel_usuario 
FROM auth_user u 
JOIN users_perfilusuario p ON u.id = p.user_id;

-- Verificar empresas
SELECT e.nombre, e.rfc, p.nombre as administrador, p.apellido_paterno
FROM users_empresa e 
JOIN users_perfilusuario p ON e.administrador_id = p.id;

-- Verificar plantas
SELECT pl.nombre as planta, e.nombre as empresa
FROM users_planta pl 
JOIN users_empresa e ON pl.empresa_id = e.empresa_id;

-- Verificar empleados
SELECT 
    emp.nombre, 
    emp.apellido_paterno, 
    p.nombre as puesto,
    d.nombre as departamento,
    pl.nombre as planta
FROM users_empleado emp
JOIN users_puesto p ON emp.puesto_id = p.puesto_id
JOIN users_departamento d ON emp.departamento_id = d.departamento_id
JOIN users_planta pl ON emp.planta_id = pl.planta_id;

-- ========================================
-- COMANDOS ADICIONALES PARA DJANGO
-- ========================================

-- Estas son las migraciones que Django necesita, ejecuta estos comandos en el terminal después:
-- python manage.py makemigrations
-- python manage.py migrate

COMMIT;
