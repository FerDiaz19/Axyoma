-- BASE DE DATOS ACTUALIZADA: AXYOMA PARA POSTGRESQL
-- Versión adaptada de MySQL a PostgreSQL con datos de prueba

-- ============================================================================
-- SISTEMA DE USUARIOS Y AUTENTICACIÓN
-- ============================================================================

-- Tabla de usuarios - Basada en Django Auth User + Perfil personalizado
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    correo VARCHAR(255) NOT NULL UNIQUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nivel_usuario VARCHAR(20) CHECK (nivel_usuario IN ('superadmin', 'admin-empresa', 'admin-planta')) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    admin_empresa INTEGER,
    
    -- Referencia al usuario Django
    user_id INTEGER UNIQUE,
    
    CONSTRAINT fk_admin_empresa FOREIGN KEY(admin_empresa) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_nivel_usuario ON usuarios (nivel_usuario);
CREATE INDEX IF NOT EXISTS idx_correo ON usuarios (correo);

-- Datos de ejemplo para usuarios
INSERT INTO usuarios (nombre, apellido_paterno, correo, nivel_usuario, admin_empresa) VALUES
    ('Ed', 'Rubio', 'ed-rubio@axyoma.com', 'superadmin', NULL),
    ('Juan', 'Perez', 'juan.perez@codewave.com', 'admin-empresa', NULL),
    ('Maria', 'Gomez', 'maria.gomez@codewave.com', 'admin-planta', 2),
    ('Carlos', 'Ruiz', 'carlos.ruiz@codewave.com', 'admin-planta', 2)
ON CONFLICT (correo) DO NOTHING;

-- ============================================================================
-- SISTEMA DE EMPRESAS Y ORGANIZACIONES
-- ============================================================================

CREATE TABLE IF NOT EXISTS empresas (
    empresa_id SERIAL PRIMARY KEY,
    nombre VARCHAR(65) NOT NULL UNIQUE,
    rfc VARCHAR(16) NOT NULL UNIQUE,
    direccion TEXT,
    logotipo VARCHAR(128),
    email_contacto VARCHAR(128),
    telefono_contacto VARCHAR(15),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    administrador INTEGER NOT NULL UNIQUE,
    
    CONSTRAINT fk_empresas_administrador FOREIGN KEY(administrador) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_nombre_empresa ON empresas (nombre);
CREATE INDEX IF NOT EXISTS idx_rfc ON empresas (rfc);

-- Datos de ejemplo para empresas
INSERT INTO empresas (nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, administrador) VALUES 
    ('CodeWave Technologies', 'CWTECH920314ABC', 'Av. Tecnológico 123, Col. Innovación, Tijuana, BC', 
     'https://example.com/codewave-logo.png', 'contacto@codewave.com', '6641234567', 2)
ON CONFLICT (rfc) DO NOTHING;

CREATE TABLE IF NOT EXISTS plantas (
    planta_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    empresa INTEGER NOT NULL,
    
    CONSTRAINT fk_plantas_empresa FOREIGN KEY (empresa) REFERENCES empresas(empresa_id)
);

CREATE INDEX IF NOT EXISTS idx_empresa_planta ON plantas (empresa);

-- Datos de ejemplo para plantas
INSERT INTO plantas (nombre, direccion, empresa) VALUES
    ('Oficina Central Tijuana', 'Av. Revolución 1234, Zona Centro, Tijuana, BC', 1),
    ('Sucursal Monterrey', 'Blvd. Díaz Ordaz 5678, San Pedro, Monterrey, NL', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS departamentos (
    departamento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    planta INTEGER NOT NULL,
    
    CONSTRAINT fk_departamentos_planta FOREIGN KEY (planta) REFERENCES plantas(planta_id)
);

CREATE INDEX IF NOT EXISTS idx_planta_depto ON departamentos (planta);

-- Datos de ejemplo para departamentos
INSERT INTO departamentos (nombre, descripcion, planta) VALUES
    ('Desarrollo de Software', 'Departamento encargado del desarrollo de aplicaciones web y móviles', 1),
    ('Recursos Humanos', 'Departamento de gestión de personal y desarrollo organizacional', 1),
    ('Contabilidad', 'Departamento de contabilidad y finanzas corporativas', 1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS puestos (
    puesto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    departamento INTEGER NOT NULL,
    
    CONSTRAINT fk_puestos_departamento FOREIGN KEY (departamento) REFERENCES departamentos(departamento_id)
);

CREATE INDEX IF NOT EXISTS idx_departamento_puesto ON puestos (departamento);

-- Datos de ejemplo para puestos
INSERT INTO puestos (nombre, descripcion, departamento) VALUES
    ('Desarrollador Full Stack', 'Desarrollador con experiencia en frontend y backend', 1),
    ('Líder de Proyecto', 'Responsable de la gestión y coordinación de proyectos de desarrollo', 1),
    ('Especialista en RRHH', 'Encargado de reclutamiento y gestión del personal', 2)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS empleados (
    empleado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    fecha_ingreso DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    puesto INTEGER NOT NULL,
    
    CONSTRAINT fk_empleados_puesto FOREIGN KEY (puesto) REFERENCES puestos(puesto_id)
);

CREATE INDEX IF NOT EXISTS idx_puesto_empleado ON empleados (puesto);
CREATE INDEX IF NOT EXISTS idx_email_empleado ON empleados (email);

-- Datos de ejemplo para empleados
INSERT INTO empleados (nombre, apellido_paterno, apellido_materno, email, telefono, fecha_ingreso, puesto) VALUES
    ('Ana', 'García', 'López', 'ana.garcia@codewave.com', '6647654321', '2023-01-15', 1),
    ('Pedro', 'Martínez', 'Rodríguez', 'pedro.martinez@codewave.com', '6647654322', '2023-02-01', 2),
    ('Laura', 'Hernández', 'Sánchez', 'laura.hernandez@codewave.com', '6647654323', '2023-03-01', 3)
ON CONFLICT (email) DO NOTHING;

-- ============================================================================
-- SISTEMA DE SUSCRIPCIONES Y PAGOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS planes (
    plan_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    duracion INTEGER NOT NULL, -- Duración en días
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_nombre_plan ON planes (nombre);
CREATE INDEX IF NOT EXISTS idx_precio_plan ON planes (precio);

-- Datos de ejemplo para planes
INSERT INTO planes (nombre, descripcion, precio, duracion) VALUES
    ('Plan Básico', 'Plan básico con funcionalidades esenciales', 299.00, 30),
    ('Plan Premium', 'Plan premium con funcionalidades avanzadas', 599.00, 30),
    ('Plan Enterprise', 'Plan empresarial con soporte completo', 999.00, 30)
ON CONFLICT (nombre) DO NOTHING;

CREATE TABLE IF NOT EXISTS suscripciones (
    suscripcion_id SERIAL PRIMARY KEY,
    empresa INTEGER NOT NULL,
    plan INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('activa', 'vencida', 'cancelada')) DEFAULT 'activa',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_suscripciones_empresa FOREIGN KEY (empresa) REFERENCES empresas(empresa_id),
    CONSTRAINT fk_suscripciones_plan FOREIGN KEY (plan) REFERENCES planes(plan_id)
);

CREATE INDEX IF NOT EXISTS idx_empresa_suscripcion ON suscripciones (empresa);
CREATE INDEX IF NOT EXISTS idx_estado_suscripcion ON suscripciones (estado);
CREATE INDEX IF NOT EXISTS idx_fecha_fin_suscripcion ON suscripciones (fecha_fin);

-- Datos de ejemplo para suscripciones (3 suscripciones como solicitas)
INSERT INTO suscripciones (empresa, plan, fecha_inicio, fecha_fin, estado) VALUES
    (1, 2, '2024-01-01', '2024-01-31', 'activa'),
    (1, 1, '2023-12-01', '2023-12-31', 'vencida'),
    (1, 3, '2024-02-01', '2024-02-28', 'activa')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS pagos (
    pago_id SERIAL PRIMARY KEY,
    suscripcion INTEGER NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(20) CHECK (estado_pago IN ('pendiente', 'completado', 'fallido')) DEFAULT 'pendiente',
    referencia_pago VARCHAR(100),
    usuario INTEGER NOT NULL,
    
    CONSTRAINT fk_pagos_suscripcion FOREIGN KEY (suscripcion) REFERENCES suscripciones(suscripcion_id),
    CONSTRAINT fk_pagos_usuario FOREIGN KEY (usuario) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_suscripcion_pago ON pagos (suscripcion);
CREATE INDEX IF NOT EXISTS idx_estado_pago ON pagos (estado_pago);
CREATE INDEX IF NOT EXISTS idx_fecha_pago ON pagos (fecha_pago);

-- Datos de ejemplo para pagos (3 pagos correspondientes a las suscripciones)
INSERT INTO pagos (suscripcion, monto, metodo_pago, estado_pago, referencia_pago, usuario) VALUES
    (1, 599.00, 'tarjeta_credito', 'completado', 'TXN_202401010001', 2),
    (2, 299.00, 'transferencia', 'completado', 'TXN_202312010001', 2),
    (3, 999.00, 'tarjeta_credito', 'completado', 'TXN_202402010001', 2)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- SISTEMA DE EVALUACIONES - ESTRUCTURA COMPLETA
-- ============================================================================

-- Tipos de evaluación disponibles
CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    tipo_evaluacion_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE INDEX IF NOT EXISTS idx_nombre_tipo_eval ON tipos_evaluacion (nombre);

-- Datos de ejemplo para tipos de evaluación
INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES
    ('Normativa', 'Evaluaciones basadas en normativas oficiales (NOM-035, etc.)'),
    ('Interna', 'Evaluaciones creadas para fines de evaluación internos de la empresa'),
    ('360 Grados', 'Evaluaciones donde se recibe feedback de múltiples fuentes')
ON CONFLICT (nombre) DO NOTHING;

-- Evaluaciones principales
CREATE TABLE IF NOT EXISTS evaluaciones (
    evaluacion_id SERIAL PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    instrucciones TEXT,
    tiempo_limite INTEGER, -- Tiempo límite en minutos
    status BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    tipo_evaluacion INTEGER NOT NULL,
    empresa INTEGER NULL, -- NULL para evaluaciones normativas
    creado_por INTEGER NOT NULL,
    
    CONSTRAINT fk_evaluaciones_tipo FOREIGN KEY(tipo_evaluacion) REFERENCES tipos_evaluacion(tipo_evaluacion_id),
    CONSTRAINT fk_evaluaciones_empresa FOREIGN KEY(empresa) REFERENCES empresas(empresa_id),
    CONSTRAINT fk_evaluaciones_creado_por FOREIGN KEY(creado_por) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_tipo_evaluacion ON evaluaciones (tipo_evaluacion);
CREATE INDEX IF NOT EXISTS idx_empresa_evaluacion ON evaluaciones (empresa);
CREATE INDEX IF NOT EXISTS idx_status_evaluacion ON evaluaciones (status);

-- Datos de ejemplo para evaluaciones (3 evaluaciones como solicitas)
INSERT INTO evaluaciones (nombre, descripcion, instrucciones, tiempo_limite, tipo_evaluacion, empresa, creado_por) VALUES
    ('Evaluación NOM-035 Inicial', 
     'Evaluación de factores de riesgo psicosocial según NOM-035', 
     'Responda todas las preguntas de forma honesta. Esta evaluación es confidencial.',
     60, 1, NULL, 1),
    ('Evaluación de Desempeño Q1', 
     'Evaluación trimestral de desempeño para empleados', 
     'Evalúe su desempeño y el de su equipo durante el primer trimestre.',
     45, 2, 1, 2),
    ('Evaluación Liderazgo 360', 
     'Evaluación de liderazgo para gerentes con feedback 360 grados',
     'Esta evaluación recopila feedback de supervisores, pares y subordinados.',
     90, 3, 1, 2)
ON CONFLICT DO NOTHING;

-- ============================================================================
-- SISTEMA DE EVALUACIONES - ESTRUCTURA COMPLETA (PARTE 2)
-- ============================================================================

-- Secciones de evaluación (para organizar preguntas)
CREATE TABLE IF NOT EXISTS secciones_eval (
    seccion_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    numero_orden INTEGER NOT NULL,
    evaluacion INTEGER NOT NULL,
    
    CONSTRAINT fk_secciones_evaluacion FOREIGN KEY (evaluacion) REFERENCES evaluaciones(evaluacion_id)
);

CREATE INDEX IF NOT EXISTS idx_evaluacion_seccion ON secciones_eval (evaluacion);
CREATE INDEX IF NOT EXISTS idx_orden_seccion ON secciones_eval (numero_orden);

-- Datos de ejemplo para secciones
INSERT INTO secciones_eval (evaluacion, nombre, descripcion, numero_orden) VALUES
    (1, 'Identificación Laboral', 'Datos del puesto y horario de trabajo', 1),
    (1, 'Factores de Riesgo Psicosocial', 'Preguntas sobre el ambiente de trabajo', 2),
    (1, 'Entorno Organizacional', 'Percepción del clima y cultura organizacional', 3),
    (2, 'Habilidades Técnicas', 'Evaluación de conocimientos y competencias técnicas', 1),
    (2, 'Colaboración y Comunicación', 'Evaluación de habilidades interpersonales', 2),
    (3, 'Liderazgo y Gestión', 'Evaluación de habilidades de liderazgo', 1),
    (3, 'Feedback 360', 'Retroalimentación de múltiples fuentes', 2)
ON CONFLICT DO NOTHING;

-- Conjuntos de opciones para respuestas
CREATE TABLE IF NOT EXISTS conjuntos_opciones (
    conjunto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    predefinido BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_nombre_conjunto ON conjuntos_opciones (nombre);
CREATE INDEX IF NOT EXISTS idx_predefinido_conjunto ON conjuntos_opciones (predefinido);

-- Datos de ejemplo para conjuntos de opciones
INSERT INTO conjuntos_opciones (nombre, descripcion, predefinido) VALUES
    ('Likert 5-Puntos (Acuerdo)', 'Escala estándar de 5 puntos para preguntas de acuerdo/desacuerdo', TRUE),
    ('Sí/No', 'Opciones de respuesta binaria', TRUE),
    ('Nivel de Satisfacción', 'Escala de 1 a 10 para medir satisfacción', FALSE),
    ('Frecuencia', 'Opciones de frecuencia: Nunca, Raramente, A veces, Frecuentemente, Siempre', TRUE),
    ('Opciones de Software', 'Opciones para elegir software favorito', FALSE)
ON CONFLICT (nombre) DO NOTHING;

-- Opciones específicas dentro de cada conjunto
CREATE TABLE IF NOT EXISTS opciones_conjunto (
    opcion_conjunto_id SERIAL PRIMARY KEY,
    texto_opcion VARCHAR(256) NOT NULL,
    valor_booleano BOOLEAN NULL,
    valor_numerico INTEGER NULL,
    puntuaje_escala INTEGER NULL,
    numero_orden INTEGER NOT NULL,
    conjunto_opciones INTEGER NOT NULL,
    
    CONSTRAINT fk_opciones_conjunto FOREIGN KEY(conjunto_opciones) REFERENCES conjuntos_opciones(conjunto_id)
);

CREATE INDEX IF NOT EXISTS idx_conjunto_opciones ON opciones_conjunto (conjunto_opciones);
CREATE INDEX IF NOT EXISTS idx_orden_opciones ON opciones_conjunto (numero_orden);

-- Datos de ejemplo para opciones de conjuntos
-- Conjunto Likert 5-Puntos
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    (1, 'Totalmente en desacuerdo', 1, 1, 1),
    (1, 'En desacuerdo', 2, 2, 2),
    (1, 'Ni de acuerdo ni en desacuerdo', 3, 3, 3),
    (1, 'De acuerdo', 4, 4, 4),
    (1, 'Totalmente de acuerdo', 5, 5, 5)
ON CONFLICT DO NOTHING;

-- Conjunto Sí/No
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_booleano, numero_orden) VALUES
    (2, 'Sí', TRUE, 1),
    (2, 'No', FALSE, 2)
ON CONFLICT DO NOTHING;

-- Conjunto Frecuencia
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    (4, 'Nunca', 1, 1, 1),
    (4, 'Raramente', 2, 2, 2),
    (4, 'A veces', 3, 3, 3),
    (4, 'Frecuentemente', 4, 4, 4),
    (4, 'Siempre', 5, 5, 5)
ON CONFLICT DO NOTHING;

-- Preguntas generales del sistema
CREATE TABLE IF NOT EXISTS preguntas (
    pregunta_id SERIAL PRIMARY KEY,
    texto_pregunta TEXT NOT NULL,
    tipo_pregunta VARCHAR(20) CHECK (tipo_pregunta IN ('Abierta', 'Múltiple', 'Escala', 'Bool')) NOT NULL,
    es_obligatoria BOOLEAN DEFAULT TRUE,
    pregunta_padre INTEGER NULL,
    activador_padre VARCHAR(255) NULL,
    
    CONSTRAINT fk_pregunta_padre FOREIGN KEY(pregunta_padre) REFERENCES preguntas(pregunta_id)
);

CREATE INDEX IF NOT EXISTS idx_tipo_pregunta ON preguntas (tipo_pregunta);

-- Datos de ejemplo para preguntas
INSERT INTO preguntas (texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ('¿Trabaja usted en horario nocturno?', 'Bool', TRUE, NULL, NULL),
    ('¿Experimenta estrés debido a la carga de trabajo?', 'Escala', TRUE, NULL, NULL),
    ('¿Qué tipo de apoyo necesita para manejar el estrés?', 'Abierta', FALSE, 2, '4,5'),
    ('¿Considera que su entorno de trabajo es seguro?', 'Bool', TRUE, NULL, NULL),
    ('¿Cómo calificaría la comunicación con su supervisor?', 'Escala', TRUE, NULL, NULL),
    ('¿Cuál de las siguientes herramientas de software utiliza más frecuentemente?', 'Múltiple', TRUE, NULL, NULL),
    ('¿Con qué frecuencia recibe retroalimentación constructiva?', 'Escala', TRUE, NULL, NULL),
    ('¿Se siente valorado en su trabajo?', 'Escala', TRUE, NULL, NULL)
ON CONFLICT DO NOTHING;

-- Relación entre secciones y preguntas
CREATE TABLE IF NOT EXISTS seccion_preguntas (
    seccion INTEGER NOT NULL,
    pregunta INTEGER NOT NULL,
    conjunto_opciones INTEGER NULL,
    
    PRIMARY KEY (seccion, pregunta),
    CONSTRAINT fk_seccion_preguntas_seccion FOREIGN KEY (seccion) REFERENCES secciones_eval(seccion_id),
    CONSTRAINT fk_seccion_preguntas_pregunta FOREIGN KEY (pregunta) REFERENCES preguntas(pregunta_id),
    CONSTRAINT fk_seccion_preguntas_conjunto FOREIGN KEY (conjunto_opciones) REFERENCES conjuntos_opciones(conjunto_id)
);

-- Datos de ejemplo para relación sección-preguntas
INSERT INTO seccion_preguntas (seccion, pregunta, conjunto_opciones) VALUES
    (1, 1, 2), -- Pregunta horario nocturno con opciones Sí/No
    (2, 2, 1), -- Pregunta estrés con escala Likert
    (2, 3, NULL), -- Pregunta abierta sobre apoyo
    (3, 4, 2), -- Pregunta entorno seguro con opciones Sí/No
    (3, 5, 1), -- Pregunta comunicación con escala Likert
    (4, 6, NULL), -- Pregunta múltiple sobre software
    (5, 7, 4), -- Pregunta frecuencia de feedback
    (6, 8, 1), -- Pregunta valoración en trabajo
    (7, 8, 1)  -- Misma pregunta en sección de feedback 360
ON CONFLICT DO NOTHING;

-- Mostrar resumen de datos creados
SELECT 'RESUMEN DE DATOS CREADOS:' as info;
SELECT 'Usuarios: ' || COUNT(*) FROM usuarios;
SELECT 'Empresas: ' || COUNT(*) FROM empresas;
SELECT 'Plantas: ' || COUNT(*) FROM plantas;
SELECT 'Departamentos: ' || COUNT(*) FROM departamentos;
SELECT 'Puestos: ' || COUNT(*) FROM puestos;
SELECT 'Empleados: ' || COUNT(*) FROM empleados;
SELECT 'Planes: ' || COUNT(*) FROM planes;
SELECT 'Suscripciones: ' || COUNT(*) FROM suscripciones;
SELECT 'Pagos: ' || COUNT(*) FROM pagos;
SELECT 'Tipos de evaluación: ' || COUNT(*) FROM tipos_evaluacion;
SELECT 'Evaluaciones: ' || COUNT(*) FROM evaluaciones;
SELECT 'Secciones de eval: ' || COUNT(*) FROM secciones_eval;
SELECT 'Conjuntos de opciones: ' || COUNT(*) FROM conjuntos_opciones;
SELECT 'Opciones de conjunto: ' || COUNT(*) FROM opciones_conjunto;
SELECT 'Preguntas: ' || COUNT(*) FROM preguntas;
SELECT 'Sección-Preguntas: ' || COUNT(*) FROM seccion_preguntas;
