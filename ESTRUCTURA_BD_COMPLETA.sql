-- ===============================================
-- ESTRUCTURA COMPLETA DE LA BASE DE DATOS AXYOMA
-- ===============================================
-- Este es el esquema EXACTO que Django creará

-- 1. TABLA: auth_user (Django User model)
-- ===============================================
-- Django crea esta tabla automáticamente para manejo de usuarios
-- Campos principales: id, username, email, password, first_name, last_name, is_active, date_joined

-- 2. TABLA: usuarios (PerfilUsuario model)
-- ===============================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    correo VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    nivel_usuario VARCHAR(20) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    admin_empresa_id INTEGER,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_empresa_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- 3. TABLA: empresas (Empresa model)
-- ===============================================
CREATE TABLE empresas (
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
    FOREIGN KEY (administrador_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 4. TABLA: plantas (Planta model)
-- ===============================================
CREATE TABLE plantas (
    planta_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    direccion TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(empresa_id) ON DELETE CASCADE
);

-- 5. TABLA: admin_plantas (AdminPlanta model)
-- ===============================================
CREATE TABLE admin_plantas (
    id SERIAL PRIMARY KEY,
    fecha_asignacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    usuario_id INTEGER NOT NULL,
    planta_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (planta_id) REFERENCES plantas(planta_id) ON DELETE CASCADE,
    UNIQUE (usuario_id, planta_id)
);

-- 6. TABLA: departamentos (Departamento model)
-- ===============================================
CREATE TABLE departamentos (
    departamento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status BOOLEAN DEFAULT TRUE,
    planta_id INTEGER NOT NULL,
    FOREIGN KEY (planta_id) REFERENCES plantas(planta_id) ON DELETE CASCADE
);

-- 7. TABLA: puestos (Puesto model)
-- ===============================================
CREATE TABLE puestos (
    puesto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    departamento_id INTEGER NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(departamento_id) ON DELETE CASCADE
);

-- 8. TABLA: empleados (Empleado model)  
-- ===============================================
CREATE TABLE empleados (
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
    FOREIGN KEY (puesto_id) REFERENCES puestos(puesto_id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(departamento_id) ON DELETE CASCADE,
    FOREIGN KEY (planta_id) REFERENCES plantas(planta_id) ON DELETE CASCADE
);

-- ===============================================
-- DATOS QUE SE INSERTARÁN AUTOMÁTICAMENTE
-- ===============================================

-- USUARIOS DJANGO (auth_user):
-- 1. ed-rubio@axyoma.com / 1234
-- 2. juan.perez@codewave.com / 1234  
-- 3. maria.gomez@codewave.com / 1234
-- 4. carlos.ruiz@codewave.com / 1234

-- PERFILES DE USUARIO (usuarios):
-- 1. Ed Rubio - superadmin
-- 2. Juan Perez - admin-empresa  
-- 3. Maria Gomez - admin-planta (admin_empresa_id: 2)
-- 4. Carlos Ruiz - admin-planta (admin_empresa_id: 2)

-- EMPRESA (empresas):
-- 1. Soluciones Industriales MX (administrador_id: 2)

-- PLANTAS (plantas):
-- 1. Oficina Central Tijuana (empresa_id: 1)
-- 2. Oficina Monterrey (empresa_id: 1)

-- ADMIN-PLANTAS (admin_plantas):
-- 1. usuario_id: 3 (Maria), planta_id: 1 (Tijuana)

-- DEPARTAMENTOS (departamentos):
-- 1. Recursos Humanos (planta_id: 1)
-- 2. Desarrollo de Software (planta_id: 1)  
-- 3. Operaciones (planta_id: 1)
-- 4. Calidad (planta_id: 2)
-- 5. Mantenimiento (planta_id: 2)

-- PUESTOS (puestos):
-- 1. Gerente de RRHH (departamento_id: 1)
-- 2. Desarrollador Senior (departamento_id: 2)
-- 3. Desarrollador Junior (departamento_id: 2)  
-- 4. Supervisor de Operaciones (departamento_id: 3)
-- 5. Especialista en Calidad (departamento_id: 4)
-- 6. Técnico de Mantenimiento (departamento_id: 5)

-- EMPLEADOS (empleados):
-- 1. Laura Fernández Torres - Gerente RRHH
-- 2. José Martínez López - Desarrollador Senior
-- 3. Ana García Ruiz - Desarrollador Junior
-- 4. Carlos López Hernández - Supervisor Operaciones  
-- 5. María Rodríguez Sánchez - Especialista Calidad
-- 6. Pedro González Morales - Técnico Mantenimiento

-- ===============================================
-- COMANDOS PARA EJECUTAR:
-- ===============================================
-- 1. setup_reset_completo.bat (resetea todo y configura desde cero)
-- 2. O manualmente:
--    cd Backend
--    python manage.py makemigrations
--    python manage.py migrate  
--    python manage.py insertar_datos
