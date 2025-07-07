
-- BASE DE DATOS: AXYOMA ---------------------------------------------------- --

CREATE DATABASE AxyomaDB;

-- -------------------------------------------------------------------------- --

''' USUARIOS:
    Habrá que hacer cambios al modelo de USERS de DJANGO.
    Investiguen/Experimenten un poco con dicho modelo, pues será necesario.

    - contraseña: Esta se cifraría solita gracias al modelo USERS de DJANGO.

    - admin_empresa: Este campo es usado únicamente cuando el usuario es administrador de una planta.
    -- Es importante pues se necesita saber quien fue el usuario que lo creo (de qué empresa).
'''
CREATE TABLE USUARIOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    correo VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    nivel_usuario ENUM('superadmin', 'admin-empresa', 'admin-planta') NOT NULL,
    status BOOLEAN DEFAULT TRUE,

    admin_empresa INT,
    FOREIGN KEY(admin_empresa) REFERENCES USUARIOS(id)
);

-- EJEMPLOS:
INSERT INTO USUARIOS (nombre, apellido_paterno, correo, contrasena, nivel_usuario, admin_empresa) VALUES
    ( 'Ed', 'Rubio', 'ed-rubio@axyoma.com', '1234', 'superadmin', NULL ),
    ( 'Juan', 'Perez', 'juan.perez@codewave.com', '1234', 'admin-empresa', NULL),
    ( 'Maria', 'Gomez', 'maria.gomez@codewave.com', '1234', 'admin-planta', 2),
    ( 'Carlos', 'Ruiz', 'carlos.ruiz@codewave.com', '1234', 'admin-planta', 2);

SELECT * FROM USUARIOS;

-- -------------------------------------------------------------------------- --

''' EMPRESAS:
    
    - logotipo: Almacenará el logo de cada empresa registrada.
    -- Dicho logo será útil en la generación de certificados (tras completar evaluaciones.).

    - rfc: Si bien dude un poco el mantener este campo...
    -- Será útil para asegurar que la autenticidad de una empresa.

    - administrador: Es la ID del usuario que registró la empresa.
'''
CREATE TABLE EMPRESAS (
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
    FOREIGN KEY(administrador) REFERENCES USUARIOS(id)
);

-- EJEMPLO:
INSERT INTO EMPRESAS (nombre, rfc, direccion, logotipo, email_contacto, telefono_contacto, administrador) VALUES (
    'Soluciones Industriales MX', 'SIMX920314ABC',
    'Av. Revolución 123, Col. Centro, CDMX',
    'https://i.pinimg.com/736x/24/7e/85/247e85b4cdcc74b50326fb36128dbce4.jpg',
    'contacto@solucionesmx.com', '5551234567', 2
);

SELECT * FROM EMPRESAS;

-- -------------------------------------------------------------------------- --

''' PLANTAS:
'''
CREATE TABLE PLANTAS (
    planta_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,

    empresa INT NOT NULL,
    FOREIGN KEY (empresa) REFERENCES EMPRESAS(empresa_id)
);

-- EJEMPLO:
INSERT INTO PLANTAS (nombre, direccion, empresa) VALUES
    ( 'Oficina Central Tijuana', 'Dirección X.', 1 ),
    ( 'Oficina Monterrey', 'Dirección X.', 1 );

SELECT * FROM PLANTAS;

''' ADMINISTRADORES DE PLANTAS:
    Lo normalillo, se asegura de ligar usuarios a plantas.
    La hice de "muchos a muchos" por cosas de escalabilidad (roles futuros).

    Habrá que crear un TRIGGER que asegure que un USUARIO...
    no sea ligado a una planta que no pertenece a su empresa.
'''
CREATE TABLE ADMIN_PLANTAS (
    usuario INT NOT NULL,
    planta INT NOT NULL,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,

    PRIMARY KEY(usuario, planta),
    FOREIGN KEY(usuario) REFERENCES USUARIOS(id),
    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);

-- EJEMPLO:
INSERT INTO ADMIN_PLANTAS (usuario, planta) VALUES ( 3,  1 );

-- -------------------------------------------------------------------------- --

''' PLANES DE SUSCRIPCIÓN:

    - duración: este campo podría ser en días o meses, ustedes deciden cómo guardar los datos.
'''
CREATE TABLE PLANES_SUSCRIPCION (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    descripcion TEXT,
    duracion INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    status BOOLEAN DEFAULT TRUE
);

-- PLANES BASE DEL SISTEMA:
INSERT INTO PLANES_SUSCRIPCION (nombre, descripcion, duracion, precio) VALUES
    ('Plan Básico (1 Mes)', 'Plan mensual con funcionalidades básicas', 30, 299.00),
    ('Plan Profesional (3 Meses)', 'Plan trimestral con descuento y funcionalidades avanzadas', 90, 799.00),
    ('Plan Anual', 'Plan anual con máximo descuento y todas las funcionalidades', 365, 2999.00);

SELECT * FROM PLANES_SUSCRIPCION;

-- -------------------------------------------------------------------------- --

''' SUSCRIPCIONES DE LAS EMPRESAS:

    Habrá que implementar un TRIGGER el cual tome la fecha de pago...
    posteriormente le sume los días/meses (duración) de la suscripción...
    e inserte los datos en esta tabla de manera automática.
'''
CREATE TABLE SUSCRIPCION_EMPRESA (
    suscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado ENUM('Activa', 'Suspendida', 'Cancelada') DEFAULT 'Activa',
    status BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    plan_suscripcion INT NOT NULL,
    empresa INT NOT NULL,

    FOREIGN KEY(plan_suscripcion) REFERENCES PLANES_SUSCRIPCION(plan_id),
    FOREIGN KEY(empresa) REFERENCES EMPRESAS(empresa_id)
);

-- EJEMPLO:
INSERT INTO SUSCRIPCION_EMPRESA (fecha_inicio, fecha_fin, estado, plan_suscripcion, empresa) VALUES  ('2025-06-01', '2025-08-30', 'Activa', 1, 1);
SELECT * FROM SUSCRIPCION_EMPRESA;

-- -------------------------------------------------------------------------- --

''' PAGOS:
    - transaccion_id: Es una ID de pago que se genera en cualquier sistema de pago Online.

    Podría implementarse un TRIGGER para asegurar que el costo total de la suscripción...
    ha sido pagado antes de marcar el status como de la suscripción de la empresa como activo.
'''
CREATE TABLE PAGOS (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    costo DECIMAL(10,2) NOT NULL,
    monto_pago DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    transaccion_id VARCHAR(64),
    estado_pago ENUM('Pendiente', 'Completado', 'Fallido') DEFAULT 'Pendiente',

    suscripcion_empresa INT NOT NULL,
    FOREIGN KEY (suscripcion_empresa) REFERENCES SUSCRIPCION_EMPRESA(suscripcion_id)
);

-- EJEMPLO:
INSERT INTO PAGOS (costo, monto_pago, fecha_pago, transaccion_id, estado_pago, suscripcion_empresa)
VALUES ( 899.99, 899.99, '2025-06-01', 'TXN-ABC123', 'Completado', 1 );

SELECT * FROM PAGOS;

-- -------------------------------------------------------------------------- --

''' DEPARTAMENTOS:
'''
CREATE TABLE DEPARTAMENTOS (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    planta INT NOT NULL,

    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);

-- EJEMPLO:
INSERT INTO DEPARTAMENTOS (nombre, descripcion, planta) VALUES
    ( 'Recursos Humanos', 'Gestión de personal.', 1 ),
    ( 'Desarrollo de Software', 'Creación de aplicaciones.', 1 );

SELECT * FROM DEPARTAMENTOS;

-- -------------------------------------------------------------------------- --

''' PUESTOS:
    En efecto, hace referencia a los roles de los empleados.
'''
CREATE TABLE PUESTOS (
    puesto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    departamento INT NOT NULL,
    
    FOREIGN KEY(departamento) REFERENCES DEPARTAMENTOS(departamento_id)
);

-- EJEMPLO:
INSERT INTO PUESTOS (nombre, descripcion, departamento) VALUES
    ( 'Gerente de RRHH', 'Líder del equipo de Recursos Humanos.', 1 ),
    ( 'Desarrollador Senior', 'Programador experimentado.', 2 );

SELECT * FROM PUESTOS;

-- -------------------------------------------------------------------------- --

''' EMPLEADOS:

    - antiguedad: Sería el número de años que lleva el empleado trabajando.
    -- Aunque también podría cambiarse por un campo tipo DATE, ustedes deciden.

    Podría añadirse un TRIGGER para asegurar que no se le asigne un puesto...
    que no pertenece al departamento en el que está trabajando.
'''
CREATE TABLE EMPLEADOS (
    empleado_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    genero ENUM('Masculino', 'Femenino') NOT NULL,
    antiguedad INT,
    status BOOLEAN DEFAULT TRUE,
    puesto INT NOT NULL,
    departamento INT NOT NULL,
    planta INT NOT NULL,

    FOREIGN KEY(puesto) REFERENCES PUESTOS(puesto_id),
    FOREIGN KEY(departamento) REFERENCES DEPARTAMENTOS(departamento_id),
    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);

-- EJEMPLO:
INSERT INTO EMPLEADOS (nombre, apellido_paterno, genero, antiguedad, puesto, departamento, planta) VALUES
    ( 'Laura', 'Fernández', 'Femenino', 5, 1, 1, 1 ),
    ( 'José', 'Martínez', 'Masculino', 2, 2, 2, 2 );

SELECT * FROM EMPLEADOS;

-- -------------------------------------------------------------------------- --

''' TIPOS DE EVALUACIÓN:
    Almacena los tres tipos de evaluación que manejamos.
'''
CREATE TABLE TIPOS_EVALUACION (
    tipo_evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT
);

-- EJEMPLO:
INSERT INTO TIPOS_EVALUACION (nombre, descripcion) VALUES
    ( 'Normativa', 'Evaluaciones basadas en normativas oficiales' ),
    ( 'Interna', 'Evaluaciones creadas para fines de evaluación internos' ),
    ( '360 Grados', 'Evaluaciones donde se recibe feedback de múltiples fuentes' );

SELECT * FROM TIPOS_EVALUACION;

-- -------------------------------------------------------------------------- --

''' EVALUACIONES:

    - empresa: Se liga a una empresa únicamente cuando no es una evaluación 'Normativa'.
'''
CREATE TABLE EVALUACIONES (
    evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_evaluacion INT NOT NULL,
    empresa INT,
    
    FOREIGN KEY(tipo_evaluacion) REFERENCES TIPOS_EVALUACION(tipo_evaluacion_id),
    FOREIGN KEY(empresa) REFERENCES EMPRESAS(empresa_id)
);

-- EJEMPLO:
INSERT INTO EVALUACIONES (nombre, descripcion, tipo_evaluacion, empresa) VALUES
    ( 'Evaluación NOM-035 Inicial', 'Evaluación de los factores de riesgo psicosocial según NOM-035.', 1, NULL ),
    ( 'Evaluación de Desempeño Q2', 'Evaluación trimestral de desempeño para empleados de desarrollo.', 2, 1 ),
    ( 'Evaluación Liderazgo 360', 'Evaluación de liderazgo para gerentes.', 3, 1 );

SELECT * FROM EVALUACIONES;

-- -------------------------------------------------------------------------- --

''' SECCIONES DE EVALUACIÓN:
    Esta tabla existe debido a que, evaluaciones como la NOM-035, ...
    poseen varias secciones en las cuales dristribuyen sus preguntas.

    - nummero_orden: Especifica el orden en que tendrán las secciones de la evaluación.
'''
CREATE TABLE SECCIONES_EVAL (
    seccion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    numero_orden INT NOT NULL,
    evaluacion INT NOT NULL,

    FOREIGN KEY (evaluacion) REFERENCES EVALUACIONES(evaluacion_id)
);

-- EJEMPLO:
INSERT INTO SECCIONES_EVAL (evaluacion, nombre, descripcion, numero_orden) VALUES
    ( 1, 'Identificación Laboral', 'Datos del puesto y horario.', 1 ),
    ( 1, 'Factores de Riesgo Psicosocial', 'Preguntas sobre el ambiente de trabajo.', 2 ),
    ( 1, 'Entorno Organizacional', 'Percepción del clima y organización.', 3 ),
    ( 2, 'Habilidades Técnicas', 'Evaluación de conocimientos técnicos.', 1 ),
    ( 2, 'Colaboración y Comunicación', 'Evaluación de habilidades blandas.', 2 );

SELECT * FROM SECCIONES_EVAL;

-- -------------------------------------------------------------------------- --

''' PREGUNTAS:

    - tipo_pregunta: Este campo servirá principalmente para el FrontEnd, ...
    -- pues permitirá derminar fácilmente qué estilos aplicar y cómo mostrar las respuestas.

    - pregunta_padre: Un campo curioso, verán, en la NOM-035 hay ciertas preguntas...
    -- las cuales no deben ser contestadas dependiendo del resultado de la anterior 'activador_padre'
    -- EJ. ¿Tienes empleados bajo tu mando?
    -- Teniendo eso en cuenta 'pregunta_padre' y 'activador_padre' serán NULL...
    -- en los casos que no dependan de un resultado anterior.
'''
CREATE TABLE PREGUNTAS (
    pregunta_id INT AUTO_INCREMENT PRIMARY KEY,
    texto_pregunta TEXT NOT NULL,
    tipo_pregunta ENUM('Abierta', 'Múltiple', 'Escala', 'Bool') NOT NULL,
    es_obligatoria BOOLEAN DEFAULT TRUE,
    pregunta_padre INT,
    activador_padre VARCHAR(255),

    FOREIGN KEY(pregunta_padre) REFERENCES PREGUNTAS(pregunta_id)
);

-- EJEMPLO:
INSERT INTO PREGUNTAS (texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ( '¿Trabaja usted en horario nocturno?', 'Bool', TRUE, NULL, NULL ),
    ( '¿Experimenta estrés debido a la carga de trabajo?', 'Escala', TRUE, NULL, NULL ),
    ( '¿Qué tipo de apoyo necesita para manejar el estrés?', 'Abierta', FALSE, 2, '4' ),
    ( '¿Considera que su entorno de trabajo es seguro?', 'Bool', TRUE, NULL, NULL ),
    ( '¿Cuál de las siguientes herramientas de software utiliza más frecuentemente?', 'Multiple', TRUE, NULL, NULL ),
    ( 'Por favor, describa cualquier incidente de seguridad que haya presenciado.', 'Abierta', FALSE, 4, 'FALSE' );

SELECT * FROM PREGUNTAS;

-- -------------------------------------------------------------------------- --

''' CONJUNTO DE OPCIONES:
    Por más tonto que parezca, tardé un poco en encontrar esta solución.

    Anteriormente ligaba una posible RESPUESTA con su PREGUNTA específica, algo que parece bien, ¿no?
    Pues nel, al momento de llevar a cabo evaluaciones con escalas de Likert (como las que maneja la NOM-035).
    Tendría que hacer lo siguiente para cada respuesta:

    INSERT INTO QuestionOptions (preguntaId, textoRespuesta, valorRespuesta, numeroOrden) VALUES
        (1, 'Totalmente en desacuerdo', 1, 1),
        (1, 'En desacuerdo', 2, 2),
        (1, 'Ni de acuerdo ni en desacuerdo', 3, 3),
        (1, 'De acuerdo', 4, 4),
        (1, 'Totalmente de acuerdo', 5, 5);

    Eso tendría que repetirse en cada posible respuesta, creando una inmensa cantidad de registros bien innecesarios.
    Para ello, decidí crear 'Conjuntos de Opciones'.

    - predefinido: Esto sirve principalmente para conjuntos con escalas de Likert u opciones (Sí/No)...
    -- principalmente en el FrontEnd, pues al saber cuales son las que no suelen cambiar...
    -- ahorra trabajo al crear nuevas evaluaciones.
'''
CREATE TABLE CONJUNTOS_OPCIONES (
    conjunto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    predefinido BOOLEAN DEFAULT FALSE
);

-- EJEMPLO:
INSERT INTO CONJUNTOS_OPCIONES (nombre, descripcion, predefinido) VALUES
    ( 'Likert 5-Puntos (Acuerdo)', 'Escala estándar de 5 puntos para preguntas de acuerdo/desacuerdo.', TRUE ),
    ( 'Sí/No', 'Opciones de respuesta Sí o No.', TRUE ),
    ( 'Nivel de Satisfacción', 'Escala de 1 a 10 para medir satisfacción.', FALSE ),
    ( 'Opciones de Software', 'Opciones para elegir un software favorito.', FALSE );

SELECT * FROM CONJUNTOS_OPCIONES;

-- -------------------------------------------------------------------------- --

''' OPCIONES DE RESPUESTA DE UN CONJUNTO:
    Una vez teniendo un conjunto de opciones, falta... añadir las opciones.

    - valor_booleano: Almacena valores booleanos, en caso de que la respuesta sea de ese tipo.
    - valor_numerico: Almacena valores númericos, en caso de que la respuesta sea de ese tipo.
    
    - puntuaje_escala: Este campo es un poco especial, pues la evalución de la NOM-035, ...
    -- es evaluada de manera rara, en ciertas respuestas, el valor que se le da para puntuarlas...
    -- varía entre preguntas. Por ello este campo está aquí

    - numero_orden: Determina el orden de las respuestas en el 'Conjunto de Respuestas'
'''
CREATE TABLE OPCIONES_CONJUNTO (
    opcion_conjunto_id INT AUTO_INCREMENT PRIMARY KEY,
    texto_opcion VARCHAR(256) NOT NULL,
    valor_booleano BOOLEAN,
    valor_numerico INT,
    puntuaje_escala INT,
    numero_orden INT NOT NULL,
    conjunto_opciones INT NOT NULL,
    
    FOREIGN KEY(conjunto_opciones) REFERENCES CONJUNTOS_OPCIONES(conjunto_id)
);

-- EJEMPLO (Conjunto Likert):
INSERT INTO OPCIONES_CONJUNTO (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    ( 1, 'Totalmente en desacuerdo', 1, 1, 1),
    ( 1, 'En desacuerdo', 2, 2, 2),
    ( 1, 'Ni de acuerdo ni en desacuerdo', 3, 3, 3),
    ( 1, 'De acuerdo', 4, 4, 4),
    ( 1, 'Totalmente de acuerdo', 5, 5, 5);

-- EJEMPLO (Conjunto Sí/No):
INSERT INTO OPCIONES_CONJUNTO (conjunto_opciones, texto_opcion, valor_booleano, numero_orden) VALUES
    ( 2, 'Sí', TRUE, 1 ), ( 2, 'No', FALSE, 2 );

-- EJEMPLO (Conjunto Nivel de Satisfacción):
INSERT INTO OPCIONES_CONJUNTO (conjunto_opciones, texto_opcion, valor_numerico, puntuaje_escala, numero_orden) VALUES
    ( 3, '1 - Muy Insatisfecho', 1, 1, 1 ),
    ( 3, '5 - Neutro', 5, 5, 2 ),
    ( 3, '10 - Muy Satisfecho', 10, 10, 3 );

-- EJEMPLO (Conjunto Opciones de Software):
INSERT INTO OPCIONES_CONJUNTO (conjunto_opciones, texto_opcion, numero_orden) VALUES
    ( 4, 'Microsoft Office', 1 ),
    ( 4, 'Google Workspace', 2 ),
    ( 4, 'LibreOffice', 3 );

SELECT * FROM OPCIONES_CONJUNTO;

-- -------------------------------------------------------------------------- --

''' PREGUNTAS DE UNA SECCIÓN:
    Ahora lo resuelto lo importante queda una sola cosa, ...
    ligar las preguntas a las secciones de una evaluación, ...
    además de ligar también sus posibles respuestas, ...
    lo cual significa ligarlas a una evaluación, por supuesto.

    Añiah ñiah ñiah...

    - conjunto_opciones: Pues da las posibles respuestas a la pregunta asociada.
    -- Esta debe ser null en caso de poner preguntillas abiertas.
'''
CREATE TABLE SECCION_PREGUNTAS (
    seccion INT NOT NULL,
    pregunta INT NOT NULL,
    conjunto_opciones INT,

    PRIMARY KEY (seccion, pregunta),
    FOREIGN KEY (seccion) REFERENCES SECCIONES_EVAL(seccion_id),
    FOREIGN KEY (pregunta) REFERENCES PREGUNTAS(pregunta_id),
    FOREIGN KEY (conjunto_opciones) REFERENCES CONJUNTOS_OPCIONES(conjunto_id)
);

-- EJEMPLO (Identificación Laboral):
INSERT INTO SECCION_PREGUNTAS (seccion, pregunta, conjunto_opciones) VALUES
    ( 1, 1, 2 ); -- Pregunta "¿Trabaja usted en horario nocturno?" (Bool) usa Conjunto Sí/No.

-- EJEMPLO (Factores de Riesgo Psicosocial):
INSERT INTO SECCION_PREGUNTAS (seccion, pregunta, conjunto_opciones) VALUES
    ( 2, 2, 1 ), -- Pregunta "¿Experimenta estrés...?" (Escala) usa Conjunto Likert.
    ( 2, 3, NULL ); -- Pregunta "¿Qué tipo de apoyo...?" (Abierta) no usa conjunto.

-- EJEMPLO (Habilidades Técnicas):
INSERT INTO SECCION_PREGUNTAS (seccion, pregunta, conjunto_opciones) VALUES
    ( 4, 5, 4 ), -- Pregunta "¿Cuál de las siguientes herramientas...?" (Multiple) usa Conjunto Opciones de Software.
    ( 4, 4, 2 ), -- Pregunta "¿Considera que su entorno de trabajo es seguro?" (Bool) usa Conjunto Sí/No.
    ( 4, 6, NULL ); -- Pregunta "Describa incidente..." (Abierta) no usa conjunto.

-- -------------------------------------------------------------------------- --

''' ASIGNACIÓN DE EVALUACIONES:
    He aquí donde se generan los UUID (tokens) para responder las evalucaciones.

    - token_acceso: UUID generado para acceder.
    - empleado: Empleado que realizará la evaluación.
    - evaluacion: Evaluación que contestará el empleado.
    - evaluado: Empleado evaluado, únicamente se llenará este campo en las evaluaciones 360.
'''
CREATE TABLE ASIGNACIONES (
    asignacion_id INT AUTO_INCREMENT PRIMARY KEY,
    token_acceso VARCHAR(255) UNIQUE NOT NULL,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATETIME,
    status ENUM('Pendiente', 'Completada', 'Vencida'),
    empleado INT NOT NULL,
    evaluacion INT NOT NULL,
    evaluado INT,

    FOREIGN KEY(empleado) REFERENCES EMPLEADOS(empleado_id),
    FOREIGN KEY(evaluacion) REFERENCES EVALUACIONES(evaluacion_id),
    FOREIGN KEY(evaluado) REFERENCES EMPLEADOS(empleado_id)
);

-- EJEMPLO:
INSERT INTO ASIGNACIONES (evaluacion, empleado, token_acceso, status, evaluado) VALUES
    ( 1, 1, 'TOK_NOM035_EMP001', 'Pendiente', NULL),
    ( 2, 2, 'TOK_DESEMP_EMP002', 'Pendiente', NULL);

SELECT * FROM ASIGNACIONES;

-- -------------------------------------------------------------------------- --

''' RESPUESTAS:
    Respiestas dadas por los empleados en las evaluaciones.

    - respuesta_abierta: En caso de haber sido pregunra de tipo 'abierta', ...
    -- es aquí donde se guarda lo introducido por el usuario.

    - respuesta: Por el contrario, de seleccionar una respuesta de...
    -- un conjunto, aqui se guarda su relación con dicha respuesta.
'''
CREATE TABLE RESPUESTAS (
    respuesta_id INT AUTO_INCREMENT PRIMARY KEY,
    respuesta_abierta TEXT,
    pregunta INT NOT NULL,
    respuesta INT,
    empleado INT NOT NULL,
    evaluacion INT NOT NULL,

    FOREIGN KEY(pregunta) REFERENCES PREGUNTAS(pregunta_id),
    FOREIGN KEY(respuesta) REFERENCES OPCIONES_CONJUNTO(opcion_conjunto_id),
    FOREIGN KEY(empleado) REFERENCES EMPLEADOS(empleado_id),
    FOREIGN KEY(evaluacion) REFERENCES ASIGNACIONES(asignacion_id),

    -- Asegura que solamente se pueda responder una vez.
    UNIQUE(evaluacion, pregunta)
);

-- EJEMPLOs:

-- Pregunta 1: "¿Trabaja usted en horario nocturno?" (Bool - Opciones: Sí/No)
INSERT INTO RESPUESTAS (pregunta, respuesta, empleado, evaluacion, respuesta_abierta) VALUES
    ( 1, 7, 1, 1, NULL );

-- Pregunta 2: "¿Experimenta estrés debido a la carga de trabajo?" (Escala Likert 5-Puntos)
INSERT INTO RESPUESTAS (pregunta, respuesta, empleado, evaluacion, respuesta_abierta) VALUES
    ( 2, 4, 1, 1, NULL );

-- Pregunta 3: "¿Qué tipo de apoyo necesita para manejar el estrés?" (Abierta)
INSERT INTO RESPUESTAS (pregunta, respuesta_abierta, empleado, evaluacion, respuesta) VALUES
    ( 3, 'Necesito más flexibilidad en mis horarios para manejar mejor mi tiempo.', 1, 1, NULL );

-- Pregunta 5: "¿Cuál de las siguientes herramientas de software utiliza más frecuentemente?" (Múltiple - Opciones de Software).
INSERT INTO RESPUESTAS (pregunta, respuesta, empleado, evaluacion, respuesta_abierta) VALUES
    ( 5, 11, 2, 2, NULL );

-- Pregunta 4: "¿Considera que su entorno de trabajo es seguro?" (Bool - Opciones: Sí/No).
INSERT INTO RESPUESTAS (pregunta, respuesta, empleado, evaluacion, respuesta_abierta) VALUES
    ( 4, 6, 2, 2, NULL );

-- -------------------------------------------------------------------------- --

''' RESULTADOS DE LAS EVALUACIONES:
    Esta tabla servirá principalmente para la emisión de certificados.

    - puntaje: Puntaje final/promedio, ...
    -- se usa principalmente en evaluaciones 360.
'''
CREATE TABLE RESULTADOS_EVAL (
    resultado_id INT AUTO_INCREMENT PRIMARY KEY,
    puntaje DECIMAL(10, 2),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    asignacion INT NOT NULL UNIQUE,

    FOREIGN KEY(asignacion) REFERENCES ASIGNACIONES(asignacion_id)
);

-- EJEMPLO:
INSERT INTO RESULTADOS_EVAL (asignacion, puntaje) VALUES ( 1, 85.50 );

SELECT * FROM RESULTADOS_EVAL;

-- -------------------------------------------------------------------------- --

-- Let the sun shine upon this Lord of Cinder...

-- -------------------------------------------------------------------------- --
