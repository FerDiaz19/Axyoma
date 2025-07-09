-- BASE DE DATOS ACTUALIZADA: AXYOMA
-- Versión mejorada basada en la estructura original + sistema de evaluaciones implementado

CREATE DATABASE IF NOT EXISTS AxyomaDB;
USE AxyomaDB;

-- ============================================================================
-- SISTEMA DE USUARIOS Y AUTENTICACIÓN
-- ============================================================================

-- Tabla de usuarios - Basada en Django Auth User + Perfil personalizado
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    correo VARCHAR(255) NOT NULL UNIQUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    nivel_usuario ENUM('superadmin', 'admin-empresa', 'admin-planta') NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    admin_empresa INT,
    
    -- Referencia al usuario Django
    user_id INT UNIQUE,
    
    FOREIGN KEY(admin_empresa) REFERENCES usuarios(id),
    INDEX idx_nivel_usuario (nivel_usuario),
    INDEX idx_correo (correo)
);

-- Datos de ejemplo para usuarios
INSERT INTO usuarios (nombre, apellido_paterno, correo, nivel_usuario, admin_empresa) VALUES
    ('Ed', 'Rubio', 'ed-rubio@axyoma.com', 'superadmin', NULL),
    ('Juan', 'Perez', 'juan.perez@codewave.com', 'admin-empresa', NULL),
    ('Maria', 'Gomez', 'maria.gomez@codewave.com', 'admin-planta', 2),
    ('Carlos', 'Ruiz', 'carlos.ruiz@codewave.com', 'admin-planta', 2);

-- ============================================================================
-- SISTEMA DE EMPRESAS Y ORGANIZACIONES
-- ============================================================================

CREATE TABLE IF NOT EXISTS empresas (
    empresa_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(65) NOT NULL UNIQUE,
    rfc VARCHAR(16) NOT NULL UNIQUE,
    direccion TEXT,
    logotipo VARCHAR(128),
    email_contacto VARCHAR(128),
    telefono_contacto VARCHAR(15),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    administrador INT NOT NULL UNIQUE,
    
    FOREIGN KEY(administrador) REFERENCES usuarios(id),
    INDEX idx_nombre (nombre),
    INDEX idx_rfc (rfc)
);

-- Datos de ejemplo para empresas
INSERT INTO empresas (nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, administrador) VALUES 
    ('CodeWave Technologies', 'CWTECH920314ABC', 'Av. Tecnológico 123, Col. Innovación, Tijuana, BC', 
     'https://example.com/codewave-logo.png', 'contacto@codewave.com', '6641234567', 2);

CREATE TABLE IF NOT EXISTS plantas (
    planta_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    empresa INT NOT NULL,
    
    FOREIGN KEY (empresa) REFERENCES empresas(empresa_id),
    INDEX idx_empresa (empresa)
);

-- Datos de ejemplo para plantas
INSERT INTO plantas (nombre, direccion, empresa) VALUES
    ('Oficina Central Tijuana', 'Av. Revolución 1234, Zona Centro, Tijuana, BC', 1),
    ('Sucursal Monterrey', 'Blvd. Díaz Ordaz 5678, San Pedro, Monterrey, NL', 1);

CREATE TABLE IF NOT EXISTS departamentos (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    planta INT NOT NULL,
    
    FOREIGN KEY (planta) REFERENCES plantas(planta_id),
    INDEX idx_planta (planta)
);

-- Datos de ejemplo para departamentos
INSERT INTO departamentos (nombre, descripcion, planta) VALUES
    ('Desarrollo de Software', 'Departamento encargado del desarrollo de aplicaciones web y móviles', 1),
    ('Recursos Humanos', 'Departamento de gestión de personal y desarrollo organizacional', 1),
    ('Contabilidad', 'Departamento de contabilidad y finanzas corporativas', 1);

CREATE TABLE IF NOT EXISTS puestos (
    puesto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    departamento INT NOT NULL,
    
    FOREIGN KEY (departamento) REFERENCES departamentos(departamento_id),
    INDEX idx_departamento (departamento)
);

-- Datos de ejemplo para puestos
INSERT INTO puestos (nombre, descripcion, departamento) VALUES
    ('Desarrollador Full Stack', 'Desarrollador con experiencia en frontend y backend', 1),
    ('Líder de Proyecto', 'Responsable de la gestión y coordinación de proyectos de desarrollo', 1),
    ('Especialista en RRHH', 'Encargado de reclutamiento y gestión del personal', 2);

CREATE TABLE IF NOT EXISTS empleados (
    empleado_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    fecha_ingreso DATE NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    puesto INT NOT NULL,
    
    FOREIGN KEY (puesto) REFERENCES puestos(puesto_id),
    INDEX idx_puesto (puesto),
    INDEX idx_email (email)
);

-- Datos de ejemplo para empleados
INSERT INTO empleados (nombre, apellido_paterno, apellido_materno, email, telefono, fecha_ingreso, puesto) VALUES
    ('Ana', 'García', 'López', 'ana.garcia@codewave.com', '6647654321', '2023-01-15', 1),
    ('Pedro', 'Martínez', 'Rodríguez', 'pedro.martinez@codewave.com', '6647654322', '2023-02-01', 2),
    ('Laura', 'Hernández', 'Sánchez', 'laura.hernandez@codewave.com', '6647654323', '2023-03-01', 3);

-- ============================================================================
-- SISTEMA DE SUSCRIPCIONES Y PAGOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS planes (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    duracion INT NOT NULL COMMENT 'Duración en días',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    
    INDEX idx_nombre (nombre),
    INDEX idx_precio (precio)
);

-- Datos de ejemplo para planes
INSERT INTO planes (nombre, descripcion, precio, duracion) VALUES
    ('Plan Básico', 'Plan básico con funcionalidades esenciales', 299.00, 30),
    ('Plan Premium', 'Plan premium con funcionalidades avanzadas', 599.00, 30),
    ('Plan Enterprise', 'Plan empresarial con soporte completo', 999.00, 30);

CREATE TABLE IF NOT EXISTS suscripciones (
    suscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    empresa INT NOT NULL,
    plan INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('activa', 'vencida', 'cancelada') DEFAULT 'activa',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (empresa) REFERENCES empresas(empresa_id),
    FOREIGN KEY (plan) REFERENCES planes(plan_id),
    INDEX idx_empresa (empresa),
    INDEX idx_estado (estado),
    INDEX idx_fecha_fin (fecha_fin)
);

-- Datos de ejemplo para suscripciones
INSERT INTO suscripciones (empresa, plan, fecha_inicio, fecha_fin, estado) VALUES
    (1, 2, '2024-01-01', '2024-01-31', 'activa');

CREATE TABLE IF NOT EXISTS pagos (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    suscripcion INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(50),
    estado_pago ENUM('pendiente', 'completado', 'fallido') DEFAULT 'pendiente',
    referencia_pago VARCHAR(100),
    usuario INT NOT NULL,
    
    FOREIGN KEY (suscripcion) REFERENCES suscripciones(suscripcion_id),
    FOREIGN KEY (usuario) REFERENCES usuarios(id),
    INDEX idx_suscripcion (suscripcion),
    INDEX idx_estado_pago (estado_pago),
    INDEX idx_fecha_pago (fecha_pago)
);

-- Datos de ejemplo para pagos
INSERT INTO pagos (suscripcion, monto, metodo_pago, estado_pago, referencia_pago, usuario) VALUES
    (1, 599.00, 'tarjeta_credito', 'completado', 'TXN_202401010001', 2);

-- ============================================================================
-- SISTEMA DE EVALUACIONES - ESTRUCTURA COMPLETA
-- ============================================================================

-- Tipos de evaluación disponibles
CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    tipo_evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    
    INDEX idx_nombre (nombre)
);

-- Datos de ejemplo para tipos de evaluación
INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES
    ('Normativa', 'Evaluaciones basadas en normativas oficiales (NOM-035, etc.)'),
    ('Interna', 'Evaluaciones creadas para fines de evaluación internos de la empresa'),
    ('360 Grados', 'Evaluaciones donde se recibe feedback de múltiples fuentes');

-- Evaluaciones principales
CREATE TABLE IF NOT EXISTS evaluaciones (
    evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    instrucciones TEXT,
    tiempo_limite INT COMMENT 'Tiempo límite en minutos',
    status BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Relaciones
    tipo_evaluacion INT NOT NULL,
    empresa INT NULL COMMENT 'NULL para evaluaciones normativas',
    creado_por INT NOT NULL,
    
    FOREIGN KEY(tipo_evaluacion) REFERENCES tipos_evaluacion(tipo_evaluacion_id),
    FOREIGN KEY(empresa) REFERENCES empresas(empresa_id),
    FOREIGN KEY(creado_por) REFERENCES usuarios(id),
    
    INDEX idx_tipo_evaluacion (tipo_evaluacion),
    INDEX idx_empresa (empresa),
    INDEX idx_status (status)
);

-- Datos de ejemplo para evaluaciones
INSERT INTO evaluaciones (nombre, descripcion, instrucciones, tiempo_limite, tipo_evaluacion, empresa, creado_por) VALUES
    ('Evaluación NOM-035 Inicial', 
     'Evaluación de factores de riesgo psicosocial según NOM-035', 
     'Responda todas las preguntas de forma honesta. Esta evaluación es confidencial.',
     60, 1, NULL, 1),
    ('Evaluación de Desempeño Q1', 
     'Evaluación trimestral de desempeño para empleados', 
     'Evalúe su desempeño y el de su equipo durante el primer trimestre.',
     45, 2, 1, 2);

-- Secciones de evaluación (para organizar preguntas)
CREATE TABLE IF NOT EXISTS secciones_eval (
    seccion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    numero_orden INT NOT NULL,
    evaluacion INT NOT NULL,
    
    FOREIGN KEY (evaluacion) REFERENCES evaluaciones(evaluacion_id),
    INDEX idx_evaluacion (evaluacion),
    INDEX idx_orden (numero_orden)
);

-- Datos de ejemplo para secciones
INSERT INTO secciones_eval (evaluacion, nombre, descripcion, numero_orden) VALUES
    (1, 'Identificación Laboral', 'Datos del puesto y horario de trabajo', 1),
    (1, 'Factores de Riesgo Psicosocial', 'Preguntas sobre el ambiente de trabajo', 2),
    (1, 'Entorno Organizacional', 'Percepción del clima y cultura organizacional', 3),
    (2, 'Habilidades Técnicas', 'Evaluación de conocimientos y competencias técnicas', 1),
    (2, 'Colaboración y Comunicación', 'Evaluación de habilidades interpersonales', 2);

-- Conjuntos de opciones para respuestas
CREATE TABLE IF NOT EXISTS conjuntos_opciones (
    conjunto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    predefinido BOOLEAN DEFAULT FALSE,
    
    INDEX idx_nombre (nombre),
    INDEX idx_predefinido (predefinido)
);

-- Datos de ejemplo para conjuntos de opciones
INSERT INTO conjuntos_opciones (nombre, descripcion, predefinido) VALUES
    ('Likert 5-Puntos (Acuerdo)', 'Escala estándar de 5 puntos para preguntas de acuerdo/desacuerdo', TRUE),
    ('Sí/No', 'Opciones de respuesta binaria', TRUE),
    ('Nivel de Satisfacción', 'Escala de 1 a 10 para medir satisfacción', FALSE),
    ('Frecuencia', 'Opciones de frecuencia: Nunca, Raramente, A veces, Frecuentemente, Siempre', TRUE);

-- Opciones específicas dentro de cada conjunto
CREATE TABLE IF NOT EXISTS opciones_conjunto (
    opcion_conjunto_id INT AUTO_INCREMENT PRIMARY KEY,
    texto_opcion VARCHAR(256) NOT NULL,
    valor_booleano BOOLEAN NULL,
    valor_numerico INT NULL,
    puntuaje_escala INT NULL,
    numero_orden INT NOT NULL,
    conjunto_opciones INT NOT NULL,
    
    FOREIGN KEY(conjunto_opciones) REFERENCES conjuntos_opciones(conjunto_id),
    INDEX idx_conjunto (conjunto_opciones),
    INDEX idx_orden (numero_orden)
);

-- Datos de ejemplo para opciones de conjuntos
-- Conjunto Likert 5-Puntos
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    (1, 'Totalmente en desacuerdo', 1, 1, 1),
    (1, 'En desacuerdo', 2, 2, 2),
    (1, 'Ni de acuerdo ni en desacuerdo', 3, 3, 3),
    (1, 'De acuerdo', 4, 4, 4),
    (1, 'Totalmente de acuerdo', 5, 5, 5);

-- Conjunto Sí/No
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_booleano, numero_orden) VALUES
    (2, 'Sí', TRUE, 1),
    (2, 'No', FALSE, 2);

-- Conjunto Nivel de Satisfacción
INSERT INTO opciones_conjunto (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    (3, '1 - Muy Insatisfecho', 1, 1, 1),
    (3, '2 - Insatisfecho', 2, 2, 2),
    (3, '3 - Poco Satisfecho', 3, 3, 3),
    (3, '4 - Neutral', 4, 4, 4),
    (3, '5 - Satisfecho', 5, 5, 5),
    (3, '6 - Muy Satisfecho', 6, 6, 6);

-- Preguntas generales del sistema
CREATE TABLE IF NOT EXISTS preguntas (
    pregunta_id INT AUTO_INCREMENT PRIMARY KEY,
    texto_pregunta TEXT NOT NULL,
    tipo_pregunta ENUM('Abierta', 'Múltiple', 'Escala', 'Bool') NOT NULL,
    es_obligatoria BOOLEAN DEFAULT TRUE,
    pregunta_padre INT NULL,
    activador_padre VARCHAR(255) NULL,
    
    FOREIGN KEY(pregunta_padre) REFERENCES preguntas(pregunta_id),
    INDEX idx_tipo_pregunta (tipo_pregunta)
);

-- Datos de ejemplo para preguntas
INSERT INTO preguntas (texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ('¿Trabaja usted en horario nocturno?', 'Bool', TRUE, NULL, NULL),
    ('¿Experimenta estrés debido a la carga de trabajo?', 'Escala', TRUE, NULL, NULL),
    ('¿Qué tipo de apoyo necesita para manejar el estrés?', 'Abierta', FALSE, 2, '4,5'),
    ('¿Considera que su entorno de trabajo es seguro?', 'Bool', TRUE, NULL, NULL),
    ('¿Cómo calificaría la comunicación con su supervisor?', 'Escala', TRUE, NULL, NULL);

-- Relación entre secciones y preguntas
CREATE TABLE IF NOT EXISTS seccion_preguntas (
    seccion INT NOT NULL,
    pregunta INT NOT NULL,
    conjunto_opciones INT NULL,
    
    PRIMARY KEY (seccion, pregunta),
    FOREIGN KEY (seccion) REFERENCES secciones_eval(seccion_id),
    FOREIGN KEY (pregunta) REFERENCES preguntas(pregunta_id),
    FOREIGN KEY (conjunto_opciones) REFERENCES conjuntos_opciones(conjunto_id)
);

-- Datos de ejemplo para relación sección-preguntas
INSERT INTO seccion_preguntas (seccion, pregunta, conjunto_opciones) VALUES
    (1, 1, 2), -- Pregunta horario nocturno con opciones Sí/No
    (2, 2, 1), -- Pregunta estrés con escala Likert
    (2, 3, NULL), -- Pregunta abierta sobre apoyo
    (3, 4, 2), -- Pregunta entorno seguro con opciones Sí/No
    (3, 5, 1); -- Pregunta comunicación con escala Likert

-- Asignaciones de evaluaciones a empleados
CREATE TABLE IF NOT EXISTS asignaciones (
    asignacion_id INT AUTO_INCREMENT PRIMARY KEY,
    token_acceso VARCHAR(255) UNIQUE NOT NULL,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATETIME NULL,
    status ENUM('Pendiente', 'Completada', 'Vencida') DEFAULT 'Pendiente',
    empleado INT NOT NULL,
    evaluacion INT NOT NULL,
    evaluado INT NULL COMMENT 'Para evaluaciones 360 grados',
    
    FOREIGN KEY(empleado) REFERENCES empleados(empleado_id),
    FOREIGN KEY(evaluacion) REFERENCES evaluaciones(evaluacion_id),
    FOREIGN KEY(evaluado) REFERENCES empleados(empleado_id),
    
    INDEX idx_empleado (empleado),
    INDEX idx_evaluacion (evaluacion),
    INDEX idx_status (status),
    INDEX idx_token (token_acceso)
);

-- Datos de ejemplo para asignaciones
INSERT INTO asignaciones (evaluacion, empleado, token_acceso, status) VALUES
    (1, 1, 'TOK_NOM035_EMP001_2024', 'Pendiente'),
    (2, 2, 'TOK_DESEMP_EMP002_2024', 'Pendiente'),
    (1, 3, 'TOK_NOM035_EMP003_2024', 'Completada');

-- Respuestas de empleados a evaluaciones
CREATE TABLE IF NOT EXISTS respuestas (
    respuesta_id INT AUTO_INCREMENT PRIMARY KEY,
    respuesta_abierta TEXT NULL,
    fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Relaciones
    pregunta INT NOT NULL,
    respuesta INT NULL COMMENT 'Referencia a opción seleccionada',
    empleado INT NOT NULL,
    evaluacion INT NOT NULL COMMENT 'Referencia a asignación',
    
    FOREIGN KEY(pregunta) REFERENCES preguntas(pregunta_id),
    FOREIGN KEY(respuesta) REFERENCES opciones_conjunto(opcion_conjunto_id),
    FOREIGN KEY(empleado) REFERENCES empleados(empleado_id),
    FOREIGN KEY(evaluacion) REFERENCES asignaciones(asignacion_id),
    
    -- Restricción: solo una respuesta por pregunta por evaluación
    UNIQUE(evaluacion, pregunta),
    
    INDEX idx_empleado (empleado),
    INDEX idx_evaluacion (evaluacion),
    INDEX idx_pregunta (pregunta)
);

-- Datos de ejemplo para respuestas
INSERT INTO respuestas (pregunta, respuesta, empleado, evaluacion, respuesta_abierta) VALUES
    (1, 2, 3, 3, NULL), -- Empleado 3 respondió "No" a horario nocturno
    (2, 3, 3, 3, NULL), -- Empleado 3 respondió "Neutral" a estrés
    (4, 1, 3, 3, NULL), -- Empleado 3 respondió "Sí" a entorno seguro
    (5, 4, 3, 3, NULL); -- Empleado 3 respondió "De acuerdo" a comunicación

-- Resultados finales de evaluaciones
CREATE TABLE IF NOT EXISTS resultados_eval (
    resultado_id INT AUTO_INCREMENT PRIMARY KEY,
    puntaje DECIMAL(10, 2) NULL,
    observaciones TEXT,
    recomendaciones TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    asignacion INT NOT NULL UNIQUE,
    
    FOREIGN KEY(asignacion) REFERENCES asignaciones(asignacion_id),
    INDEX idx_asignacion (asignacion),
    INDEX idx_puntaje (puntaje)
);

-- Datos de ejemplo para resultados
INSERT INTO resultados_eval (asignacion, puntaje, observaciones) VALUES
    (3, 75.50, 'Evaluación completada satisfactoriamente. Nivel de riesgo psicosocial bajo.');

-- ============================================================================
-- TABLAS DE COMPATIBILIDAD CON DJANGO
-- ============================================================================

-- Tabla simplificada para compatibilidad con frontend actual
CREATE TABLE IF NOT EXISTS preguntas_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id INT NOT NULL,
    orden INT NOT NULL,
    texto TEXT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    es_requerida BOOLEAN DEFAULT TRUE,
    opciones JSON,
    escala_min INT NULL,
    escala_max INT NULL,
    
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(evaluacion_id),
    INDEX idx_evaluacion (evaluacion_id),
    INDEX idx_orden (orden)
);

-- Tabla para aplicaciones simplificadas
CREATE TABLE IF NOT EXISTS aplicaciones_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evaluacion_id INT NOT NULL,
    empleado_id INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente',
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio DATETIME NULL,
    fecha_completado DATETIME NULL,
    token_acceso VARCHAR(100) UNIQUE NULL,
    evaluado_id INT NULL,
    
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(evaluacion_id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(empleado_id),
    FOREIGN KEY (evaluado_id) REFERENCES empleados(empleado_id),
    
    INDEX idx_evaluacion (evaluacion_id),
    INDEX idx_empleado (empleado_id),
    INDEX idx_estado (estado)
);

-- ============================================================================
-- VISTAS PARA REPORTES Y CONSULTAS COMPLEJAS
-- ============================================================================

-- Vista para estadísticas de evaluaciones
CREATE VIEW IF NOT EXISTS vista_estadisticas_evaluaciones AS
SELECT 
    e.evaluacion_id,
    e.nombre as evaluacion_nombre,
    te.nombre as tipo_evaluacion,
    emp.nombre as empresa_nombre,
    COUNT(a.asignacion_id) as total_asignaciones,
    COUNT(CASE WHEN a.status = 'Completada' THEN 1 END) as completadas,
    COUNT(CASE WHEN a.status = 'Pendiente' THEN 1 END) as pendientes,
    COUNT(CASE WHEN a.status = 'Vencida' THEN 1 END) as vencidas,
    AVG(r.puntaje) as puntaje_promedio
FROM evaluaciones e
LEFT JOIN tipos_evaluacion te ON e.tipo_evaluacion = te.tipo_evaluacion_id
LEFT JOIN empresas emp ON e.empresa = emp.empresa_id
LEFT JOIN asignaciones a ON e.evaluacion_id = a.evaluacion
LEFT JOIN resultados_eval r ON a.asignacion_id = r.asignacion
GROUP BY e.evaluacion_id, e.nombre, te.nombre, emp.nombre;

-- Vista para estado de suscripciones
CREATE VIEW IF NOT EXISTS vista_estado_suscripciones AS
SELECT 
    e.empresa_id,
    e.nombre as empresa_nombre,
    s.suscripcion_id,
    p.nombre as plan_nombre,
    s.fecha_inicio,
    s.fecha_fin,
    s.estado,
    CASE 
        WHEN s.fecha_fin >= CURDATE() AND s.estado = 'activa' THEN 'Activa'
        WHEN s.fecha_fin < CURDATE() THEN 'Vencida'
        ELSE 'Inactiva'
    END as estado_real,
    DATEDIFF(s.fecha_fin, CURDATE()) as dias_restantes
FROM empresas e
LEFT JOIN suscripciones s ON e.empresa_id = s.empresa
LEFT JOIN planes p ON s.plan = p.plan_id
ORDER BY e.empresa_id, s.fecha_inicio DESC;

-- ============================================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================================================

-- Índices para mejorar rendimiento en consultas frecuentes
CREATE INDEX idx_evaluaciones_tipo_status ON evaluaciones(tipo_evaluacion, status);
CREATE INDEX idx_asignaciones_empleado_status ON asignaciones(empleado, status);
CREATE INDEX idx_respuestas_evaluacion_empleado ON respuestas(evaluacion, empleado);
CREATE INDEX idx_suscripciones_empresa_estado ON suscripciones(empresa, estado);
CREATE INDEX idx_pagos_estado_fecha ON pagos(estado_pago, fecha_pago);

-- ============================================================================
-- PROCEDIMIENTOS ALMACENADOS ÚTILES
-- ============================================================================

DELIMITER //

-- Procedimiento para obtener estadísticas de una empresa
CREATE PROCEDURE IF NOT EXISTS sp_estadisticas_empresa(IN empresa_id INT)
BEGIN
    SELECT 
        COUNT(DISTINCT p.planta_id) as total_plantas,
        COUNT(DISTINCT d.departamento_id) as total_departamentos,
        COUNT(DISTINCT pu.puesto_id) as total_puestos,
        COUNT(DISTINCT em.empleado_id) as total_empleados,
        COUNT(DISTINCT ev.evaluacion_id) as evaluaciones_internas,
        COUNT(DISTINCT a.asignacion_id) as evaluaciones_asignadas,
        COUNT(CASE WHEN a.status = 'Completada' THEN 1 END) as evaluaciones_completadas
    FROM empresas e
    LEFT JOIN plantas p ON e.empresa_id = p.empresa
    LEFT JOIN departamentos d ON p.planta_id = d.planta
    LEFT JOIN puestos pu ON d.departamento_id = pu.departamento
    LEFT JOIN empleados em ON pu.puesto_id = em.puesto
    LEFT JOIN evaluaciones ev ON e.empresa_id = ev.empresa
    LEFT JOIN asignaciones a ON ev.evaluacion_id = a.evaluacion
    WHERE e.empresa_id = empresa_id;
END//

DELIMITER ;

-- ============================================================================
-- TRIGGERS PARA MANTENIMIENTO DE DATOS
-- ============================================================================

DELIMITER //

-- Trigger para actualizar fecha_actualizacion en evaluaciones
CREATE TRIGGER IF NOT EXISTS tr_evaluaciones_update_timestamp
    BEFORE UPDATE ON evaluaciones
    FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
END//

-- Trigger para validar fechas de suscripción
CREATE TRIGGER IF NOT EXISTS tr_suscripciones_validate_dates
    BEFORE INSERT ON suscripciones
    FOR EACH ROW
BEGIN
    IF NEW.fecha_fin <= NEW.fecha_inicio THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La fecha fin debe ser posterior a la fecha inicio';
    END IF;
END//

DELIMITER ;

-- ============================================================================
-- COMENTARIOS FINALES
-- ============================================================================

/*
Esta estructura de base de datos integra:

1. SISTEMA ORIGINAL:
   - Usuarios, empresas, plantas, departamentos, puestos, empleados
   - Suscripciones y pagos

2. SISTEMA DE EVALUACIONES MEJORADO:
   - Evaluaciones normativas e internas
   - Preguntas con diferentes tipos de respuesta
   - Secciones para organizar preguntas
   - Conjuntos de opciones reutilizables
   - Asignaciones y respuestas
   - Resultados y estadísticas

3. OPTIMIZACIONES:
   - Índices para mejorar rendimiento
   - Vistas para consultas complejas
   - Procedimientos almacenados
   - Triggers para mantenimiento

4. COMPATIBILIDAD:
   - Mantiene compatibilidad con el frontend React actual
   - Estructura Django-friendly
   - Tablas simplificadas para transición gradual

Para usar esta estructura:
1. Ejecutar este script en MySQL
2. Configurar Django para usar las tablas existentes
3. Crear migraciones para nuevos modelos
4. Actualizar serializers y views según sea necesario
*/
