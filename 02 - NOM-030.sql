
-- INSERCIÓN DE DATILLOS DE LAS EVALUACIONES -------------------------------- --

-- ! NOTA: Estos inserciones fueron diseñadas para funcionar tras haber insertado los datos de la NOM-035.

-- -------------------------------------------------------------------------- --

-- * 01: Ya habiendo registrado los tipos de evaluación.
    -- ? 1: Normativa
    -- ? 2: Interna

    -- ! Tomando en cuenta que estas dos inserciones fueron hechas anteriormente:
    -- ( 'Normativa', 'Evaluación estandarizada que cumple con normativas o estándares oficiales.' ), -- ! ID: 1
    -- ( 'Interna', 'Evaluación exclusiva de una empresa para su aplicación en el contexto interno de esta misma.' ); -- ! ID: 2


-- * 02: Creamos las evaluaciones base.
    -- ? nombre: Sería, claramente, el nombre de la evaluación.
    -- ? descripcion: Sería la descripción de la evaluación.
    -- ? instrucciones: Sería, claramente, el nombre del tipo de evaluación.
    -- ? tiempo_limite: Sería la descripción del tipo de evaluación.
    -- ? umbral_aprobacion: Sería, claramente, el nombre del tipo de evaluación.
    -- ? status: Sería la descripción del tipo de evaluación.
    -- ? tipo_evaluacion: Sería, claramente, el nombre del tipo de evaluación.
    -- ? creado_por: Sería la descripción del tipo de evaluación.
INSERT INTO EVALUACIONES(nombre, descripcion, instrucciones, tiempo_limite, umbral_aprobacion, status, tipo_evaluacion, empresa, creado_por) VALUES
    (
        'Cumplimiento de la NOM-030 STPS 2009',
        'Evaluación destinada a la identificación y gestión de riesgos de seguridad y salud en un centro de trabajo',

        'Para responder de forma efectiva, por favor:
            Busca un lugar tranquilo y cómodo: Sin interrupciones para concentrarte.
            Lee con atención cada pregunta: Tómate tu tiempo para entender bien antes de responder.
        Tu honestidad y participación son muy importantes para mejorar nuestro entorno de trabajo.',

        NULL, -- Esta evaluación no posee un tiempo límite para contestarla.
        80, -- El empleado debe contestar bien el 80% de las preguntas para ser considerado como aprobatorio.
        TRUE, -- Se registra la evaluación con un estado activo.
        1, -- Teniendo en cuenta que el tipo de evaluación normativo tiene este ID.
        NULL, -- Al ser una evaluación normativa no pertenece a una empresa específica.
        NULL -- Igualmente no se guarda un usuario creador.
    ); -- ! ID: 2


-- * 03: Insertamos cada una de las secciones de la evaluación.
    -- ? nombre: Sería, claramente, el nombre de la sección.
    -- ? descripcion: Sería la descripción de la sección.
    -- ? numero_orden: Este es el número de orden que tiene esta sección en la evaluación.
    -- ? es_evaluable: Determina si el las preguntas de esta sección se toman en cuenta para una evaluación.
    -- ? evaluacion: Esta es la evaluación a la que pertenece la sección.
INSERT INTO SECCIONES_EVAL(nombre, descripcion, numero_orden, es_evaluable, evaluacion) VALUES
    (
        'Servicios preventivos de seguridad y salud',
        'Preguntas relacionadas con las funciones y actividades de los servicios preventivos de seguridad y salud en el trabajo.',
        1, -- Primer sección de la evaluación.
        TRUE, -- Las respuestas son evaluables.
        2 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-030.
    ), -- ! ID: 15
    (
        'Diagnóstico y programa de seguridad y salud',
        'Preguntas sobre el diagnóstico y el programa de seguridad y salud en el trabajo.',
        2, -- Segunda sección de la evaluación.
        TRUE, -- Las respuestas son evaluables.
        2 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-030.
    ), -- ! ID: 16
    (
        'Medidas de prevención y atención de emergencias',
        'Preguntas sobre botiquines, atención médica, y acciones para emergencias.',
        3, -- Tercer sección de la evaluación.
        TRUE, -- Las respuestas son evaluables.
        2 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-030.
    ), -- ! ID: 17
    (
        'Capacitación y promoción de la salud',
        'Preguntas relacionadas con la capacitación de mandos superiores y la promoción de la salud.',
        4, -- Cuarta sección de la evaluación.
        TRUE, -- Las respuestas son evaluables.
        2 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-030.
    ), -- ! ID: 18
    (
        'Reportes, investigación y adecuaciones',
        'Preguntas sobre el seguimiento de reportes, investigación de riesgos y adecuaciones al programa.',
        5, -- Quinta sección de la evaluación.
        TRUE, -- Las respuestas son evaluables.
        2 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-030.
    ); -- ! ID: 19


-- * 04: Comenzamos a registrar cada una de las preguntas.
    -- ? texto_pregunta: Texto de la pregunta en sí.
    -- ? tipo_pregunta: Tipo de respuesta que se espera de esta pregunta.
    -- ? es_obligatoria: Define si la respuesta debe ser o no contestada.
    -- ? pregunta_padre: Determina la pregunta de la cual depende esta para ser mostrada.
    -- ? activador_padre: Este es el valor esperado de la pregunta padre para ser mostrada.
INSERT INTO PREGUNTAS(texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ( '¿Qué debe demostrar el patrón referente al personal de la empresa que forma parte de los servicios preventivos de seguridad y salud en el trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 75
    ( 'El patrón cumple cuando presenta mediante una entrevista que asume funciones y actividades de seguridad y ______',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 76
    ( 'Todos los medios de difusión se deberán utilizar para proporcionar:',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 77
    ( '¿Quién elabora la relación de acciones preventivas y correctivas de seguridad y salud en el trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 78
    ( 'El patrón cumple cuando un diagnóstico ______ o por ______ de las condiciones de seguridad y salud en el centro de trabajo',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 79
    ( '¿Cuál es el fin de orientar al patrón y a los trabajadores de las funciones y actividades a desarrollar por los servicios preventivos y salud en el trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 80
    ( '¿Cuáles son las características que el botiquín debe cumplir?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 81
    ( 'El programa de seguridad y salud en el trabajo, deberá tener las fechas de inicio y término programadas para instrumentar las acciones preventivas o correctivas y para la atención de emergencias',
        'Bool', TRUE, NULL, NULL ), -- ! ID: 82
    ( 'El patrón cumple cuando presenta reportes. ¿Qué debe contener dicho reporte?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 83
    ( '¿En qué situaciones se brindará atención de consulta médica?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 84
    ( '¿Cómo se realiza la capacitación para mandos superiores?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 85
    ( 'Las acciones y programas de promoción para la salud de los trabajadores y prevención de adicciones es información que debe contener el ______ con base al diagnostico elaborado en el centro de trabajo',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 86
    ( '¿Qué acciones deberá contener el programa de seguridad y salud?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 87
    ( 'Cuando las unidades de verificación evalúan el cumplimiento de esta norma, ¿Qué documento se debe emitir?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 88
    ( '¿Cuál es principal objetivo de la emisión de las recomendaciones para instrumentar as acciones para la atención a emergencias en los centros de trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 89
    ( '¿Qué debe hacer el responsable de seguridad y salud en el trabajo cuando se detecte un riesgo grave e inminente?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 90
    ( '¿Qué debe realizar el responsable de seguridad y salud en el trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 91
    ( '¿Qué incluye la capacitación en salud en el centro de trabajo?',
        'Múltiple', TRUE, NULL, NULL ), -- ! ID: 92
    ( 'En las acciones recomendadas se deben considerar aspectos como la planeación y dirección; la capacitación e información a los trabajadores y las medidas de prevención. Se deben exceptuar las medidas de protección y las políticas temporales',
        'Bool', TRUE, NULL, NULL ), -- ! ID: 93
    ( 'Cuando el programa de seguridad y salud en el trabajo o de la relación de acciones preventivas y correctivas no cumple con el objeto de su aplicación, ¿Qué se debe hacer?',
        'Múltiple', TRUE, NULL, NULL ); -- ! ID: 94


-- * 05: Proseguimos a insertar los conjuntos de respuestas.
    -- ? nombre: Nombre del conjunto de respuestas.
    -- ? descripcion: Descripción del conjunto de respuestas.
    -- ? predefinido: Define si este conjunto puede ser globalmente utilizado en todas las evaluaciones.

    -- ! Tomando en cuenta que estas dos inserciones fueron hechas anteriormente:
    -- ( 'Escala (Siempre/Nunca)', 'Opciones de respuesta para una escala de "Siempre" a "Nunca".', TRUE), -- ! ID: 1
    -- ( 'Booleano (Sí/No)', 'Opciones de respuesta para preguntas booleanas.', TRUE); -- ! ID: 2
INSERT INTO CONJUNTO_RESPUESTAS(nombre, descripcion, predefinido) VALUES
    ( 'Opciones P01: NOM-030', NULL, FALSE ), -- ! ID: 3
    ( 'Opciones P02: NOM-030', NULL, FALSE ), -- ! ID: 4
    ( 'Opciones P03: NOM-030', NULL, FALSE ), -- ! ID: 5
    ( 'Opciones P04: NOM-030', NULL, FALSE ), -- ! ID: 6
    ( 'Opciones P05: NOM-030', NULL, FALSE ), -- ! ID: 7
    ( 'Opciones P06: NOM-030', NULL, FALSE ), -- ! ID: 8
    ( 'Opciones P07: NOM-030', NULL, FALSE ), -- ! ID: 9
    ( 'Opciones P09: NOM-030', NULL, FALSE ), -- ! ID: 10
    ( 'Opciones P10: NOM-030', NULL, FALSE ), -- ! ID: 11
    ( 'Opciones P11: NOM-030', NULL, FALSE ), -- ! ID: 12
    ( 'Opciones P12: NOM-030', NULL, FALSE ), -- ! ID: 13
    ( 'Opciones P13: NOM-030', NULL, FALSE ), -- ! ID: 14
    ( 'Opciones P14: NOM-030', NULL, FALSE ), -- ! ID: 15
    ( 'Opciones P15: NOM-030', NULL, FALSE ), -- ! ID: 16
    ( 'Opciones P16: NOM-030', NULL, FALSE ), -- ! ID: 17
    ( 'Opciones P17: NOM-030', NULL, FALSE ), -- ! ID: 18
    ( 'Opciones P18: NOM-030', NULL, FALSE ), -- ! ID: 19
    ( 'Opciones P20: NOM-030', NULL, FALSE ); -- ! ID: 20


-- * 06: Después ingresamos cada una de las posibles respuestas de estos conjuntos.
    -- ? nombre: Nombre del conjunto de respuestas.
    -- ? descripcion: Descripción del conjunto de respuestas.
    -- ? predefinido: Define si este conjunto puede ser globalmente utilizado en todas las evaluaciones.

    -- ! Tomando en cuenta que estas siete inserciones fueron hechas anteriormente:
    -- ( 'Siempre', NULL, NULL, NULL, 1, 1), -- ! ID: 1
    -- ( 'Casi siempre', NULL, NULL, NULL, 2, 1), -- ! ID: 2
    -- ( 'Algunas veces', NULL, NULL, NULL, 3, 1), -- ! ID: 3
    -- ( 'Casi nunca', NULL, NULL, NULL, 4, 1), -- ! ID: 4
    -- ( 'Nunca', NULL, NULL, NULL, 5, 1), -- ! ID: 5

    -- ('Sí', TRUE, NULL, NULL, 1, 2), -- ! ID: 6
    -- ('No', FALSE, NULL, NULL, 2, 2); -- ! ID: 7
INSERT INTO POSIBLES_RESPUESTAS(texto_opcion, valor_booleano, valor_int, valor_decimal, numero_orden, conjunto_respuestas) VALUES
    ( 'Que es capacitado en las funciones y actividades', NULL, NULL, NULL, 1, 3 ), -- ! ID: 8
    ( 'Que no se han presentado accidentes recientes', NULL, NULL, NULL, 2, 3 ), -- ! ID: 9
    ( 'Que tienen conocimiento acerca de las funciones y actividades a realizar', NULL, NULL, NULL, 3, 3 ), -- ! ID: 10
    ( 'Que es actualizado constantemente dentro del centro de trabajo', NULL, NULL, NULL, 4, 3), -- ! ID: 11

    ( 'Preventivas - Salud', NULL, NULL, NULL, 1, 4), -- ! ID: 12
    ( 'Seguras - Prevención', NULL, NULL, NULL, 2, 4), -- ! ID: 13
    ( 'Funcionales - Salud', NULL, NULL, NULL, 3, 4), -- ! ID: 14
    ( 'Esenciales - Prevención', NULL, NULL, NULL, 4, 4), -- ! ID: 15

    ( '1, 4, 5', NULL, NULL, NULL, 1, 5), -- ! ID: 16
    ( '2, 3, 5', NULL, NULL, NULL, 2, 5), -- ! ID: 17
    ( '2, 3, 4', NULL, NULL, NULL, 3, 5), -- ! ID: 18
    ( '1, 2, 3', NULL, NULL, NULL, 4, 5), -- ! ID: 19

    ( 'Los centros de trabajo que no cuenten con un diagnóstico sobre los riesgos en el trabajo', NULL, NULL, NULL, 1, 6), -- ! ID: 20
    ( 'Los centros de trabajo que cuenten con menos de cien trabajadores', NULL, NULL, NULL, 2, 6), -- ! ID: 21
    ( 'Los centros de trabajo que cuenten con más de cien trabajadores', NULL, NULL, NULL, 3, 6), -- ! ID: 22
    ( 'Los centros de trabajo que cuenten con un diagnóstico de seguridad dirigido a los trabajadores', NULL, NULL, NULL, 4, 6), -- ! ID: 23

    ( 'Inicial - Secciones de trabajo', NULL, NULL, NULL, 1, 7), -- ! ID: 24
    ( 'Integral - Áreas de trabajo', NULL, NULL, NULL, 2, 7), -- ! ID: 25
    ( 'General - Departamento', NULL, NULL, NULL, 3, 7), -- ! ID: 26
    ( 'Físico - Observación', NULL, NULL, NULL, 4, 7), -- ! ID: 27

    ( 'Cumplir con la obligación de brindar capacitación', NULL, NULL, NULL, 1, 8), -- ! ID: 28
    ( 'Prever que los trabajadores desarrollen sus actividades en condiciones seguras', NULL, NULL, NULL, 2, 8), -- ! ID: 29
    ( 'Prever que los trabajadores no tengan accidentes y esto produzca costos adicionales', NULL, NULL, NULL, 3, 8), -- ! ID: 30
    ( 'Fortalecer una cultura de reacción ante accidentes', NULL, NULL, NULL, 4, 8), -- ! ID: 31

    ( 'Ser de fácil transporte, visible y de fácil acceso, que contenga material suficiente, identificable con una cruz rija, de peso no excesivo', NULL, NULL, NULL, 1, 9), -- ! ID: 32
    ( 'Ser de fácil transporte, visible y de fácil acceso, identificable con una cruz roja, de peso no excesivo, sin candados o dispositivos que dificulten el acceso a su contenido', NULL, NULL, NULL, 2, 9), -- ! ID: 33
    ( 'Ser de fácil transporte, colocado en un lugar den donde todos tengan acceso a él, identificable con una cruz roja, de material resistente y sin candados o dispositivos que dificulten el acceso a su contenido', NULL, NULL, NULL, 3, 9), -- ! ID: 34
    ( 'Ser de fácil transporte y de fácil acceso, en una ubicación fácil para los trabajadores, con contenido suficiente para todos, sin candados que dificulten el acceso a su contenido', NULL, NULL, NULL, 4, 9), -- ! ID: 35

    ( 'Propuestas y seguimiento del uso del equipo de protección personal de acuerdo a las indicaciones del proveedor', NULL, NULL, NULL, 1, 10), -- ! ID: 36
    ( 'Seguimiento de avances en la instauración del programa de seguridad y salud en nel trabajo', NULL, NULL, NULL, 2, 10), -- ! ID: 37
    ( 'Lista diaria por cada trabajador del seguimiento de las indicaciones del programa de seguridad y salud en el centro de trabajo', NULL, NULL, NULL, 3, 10), -- ! ID: 38
    ( 'Historial de riesgos de trabajo presentados en el centro de trabajo', NULL, NULL, NULL, 4, 10), -- ! ID: 39

    ( 'Por enfermedad general y por enfermedad de trabajo', NULL, NULL, NULL, 1, 11), -- ! ID: 40
    ( 'Por enfermedad de trabajo y por una situación de emergencia en el trabajo', NULL, NULL, NULL, 2, 11), -- ! ID: 41
    ( 'Por enfermedad general y por accidente de trabajo', NULL, NULL, NULL, 3, 11), -- ! ID: 42
    ( 'Por enfermedad general y por lesiones graves de trabajo', NULL, NULL, NULL, 4, 11), -- ! ID: 43

    ( 'Brindándoles asesoramiento sobre las dudas que tengan respecto a la seguridad y salud en el trabajo', NULL, NULL, NULL, 1, 12), -- ! ID: 44
    ( 'Mediante el asesoramiento sobre los temas que los especialistas en seguridad y salud deben conocer', NULL, NULL, NULL, 2, 12), -- ! ID: 45
    ( 'A través del asesoramiento para enseñarles como realizar un programa y normas internas de salud en el trabajo', NULL, NULL, NULL, 3, 12), -- ! ID: 46
    ( 'Mediante el asesoramiento para el establecimiento de políticas y normas internas de salud en el trabajo', NULL, NULL, NULL, 4, 12), -- ! ID: 47

    ( 'Programa de seguridad y salud', NULL, NULL, NULL, 1, 13), -- ! ID: 48
    ( 'Plan de seguridad y salud', NULL, NULL, NULL, 2, 13), -- ! ID: 49
    ( 'Diagnostico de seguridad y salud', NULL, NULL, NULL, 3, 13), -- ! ID: 50
    ( 'Dictamen de seguridad y salud', NULL, NULL, NULL, 4, 13), -- ! ID: 51

    ( 'Las acciones para peligros circundantes al centro de trabajo que lo puedan afectar', NULL, NULL, NULL, 1, 14), -- ! ID: 52
    ( 'Las acciones para el seguimiento de los avances en la instrumentación del programa', NULL, NULL, NULL, 2, 14), -- ! ID: 53
    ( 'Las acciones para las adecuaciones que se requieren tanto al diagnostico como al programa o la relación', NULL, NULL, NULL, 3, 14), -- ! ID: 54
    ( 'Las acciones para la atención de emergencias y contingencias sanitarias', NULL, NULL, NULL, 4, 14), -- ! ID: 55

    ( 'Acta', NULL, NULL, NULL, 1, 15), -- ! ID: 56
    ( 'Dictamen', NULL, NULL, NULL, 2, 15), -- ! ID: 57
    ( 'Recibo', NULL, NULL, NULL, 3, 15), -- ! ID: 58
    ( 'Reglamento', NULL, NULL, NULL, 4, 15), -- ! ID: 59

    ( 'Orientar al patrón y a los trabajadores sobre los servicios preventivos de seguridad y salud en el trabajo', NULL, NULL, NULL, 1, 16), -- ! ID: 60
    ( 'Evitar que los centros de trabajo obtengan una multa por parte de la secretaría del trabajo y previsión social', NULL, NULL, NULL, 2, 16), -- ! ID: 61
    ( 'Facilitar a los empleados la identificación e instrumentación de las normas de promoción, prevención y control', NULL, NULL, NULL, 3, 16), -- ! ID: 62
    ( 'Establecer un programa para todo el personal sobre temas de prevención de enfermedades', NULL, NULL, NULL, 4, 16), -- ! ID: 63

    ( 'Consultar con los trabajadores el plan de acción a seguir', NULL, NULL, NULL, 1, 17), -- ! ID: 64
    ( 'Consultar los procedimientos adecuados para actuar', NULL, NULL, NULL, 2, 17), -- ! ID: 65
    ( 'Esperar a que la autoridad laboral expida las recomendaciones necesarias', NULL, NULL, NULL, 3, 17), -- ! ID: 66
    ( 'Establecer los mecanismos de respuesta inmediata', NULL, NULL, NULL, 4, 17), -- ! ID: 67

    ( 'Un recorrido en el centro de trabajo para detectar los posibles riesgos, y con base a ellos realizar las acciones preventivas pertinentes', NULL, NULL, NULL, 1, 18), -- ! ID: 68
    ( 'Un procedimiento específico sobre las medidas de seguridad que debe llevar a cabo los trabajadores dentro del centro de trabajo', NULL, NULL, NULL, 2, 18), -- ! ID: 69
    ( 'Un diagnostico sobre los riesgos a los que esta expuestos los trabajadores en el centro de trabajo', NULL, NULL, NULL, 3, 18), -- ! ID: 70
    ( 'Un programa de seguridad y salud en el trabajo o la relación de acciones preventivas y correctivas de seguridad y salud en el trabajo', NULL, NULL, NULL, 4, 18), -- ! ID: 71

    ( 'El seguimiento a la salud de los trabajadores y revisiones médicas anualmente', NULL, NULL, NULL, 1, 19), -- ! ID: 72
    ( 'El seguimiento a la salud de los trabajadores mediante exámenes médicos', NULL, NULL, NULL, 2, 19), -- ! ID: 73
    ( 'Evacuaciones teóricas y prácticas sobre primeros auxilios', NULL, NULL, NULL, 3, 19), -- ! ID: 74
    ( 'Talleres sobre como resguardar la salud y el seguimiento del aprendizaje', NULL, NULL, NULL, 4, 19), -- ! ID: 75

    ( 'Realizar las adecuaciones requeridas tanto al diagnostico como al programa o a la relación', NULL, NULL, NULL, 1, 20), -- ! ID: 76
    ( 'Indagar en los factores que influyen y tratar de eliminarlos', NULL, NULL, NULL, 2, 20), -- ! ID: 77
    ( 'Consultar con el patrón y con los trabajadores las modificaciones que serían pertinentes', NULL, NULL, NULL, 3, 20), -- ! ID: 78
    ( 'Eliminar el programa instaurado y realizar uno nuevo', NULL, NULL, NULL, 4, 20); -- ! ID: 79


-- * 07: Iniciamos por insertar los tipos de evaluación.
    -- ? seccion: Sección de una evaluación en la cual estará la pregunta.
    -- ? pregunta: Preguntilla a asignar a una sección.
    -- ? conjunto_respuestas: Conjunto de posibles respuestas de la pregunta dada.
    -- ? respuesta_correcta: Respuesta correcta a la pregunta.
    -- ? numero_orden: Orden de las preguntas dentro de la sección.
INSERT INTO SECCION_PREGUNTAS (seccion, pregunta, conjunto_respuestas, respuesta_correcta, numero_orden) VALUES
    ( 15, 75, 3, 8, 1 ),
    ( 15, 76, 4, 12, 2 ),
    ( 15, 77, 5, 17, 3 ),
    ( 15, 80, 8, 29, 4 ),
    ( 15, 90, 17, 67, 5 ),
    ( 15, 91, 18, 71, 6 ),

    ( 16, 78, 6, 21, 1 ),
    ( 16, 79, 7, 25, 2 ),
    ( 16, 82, 2, 6, 3 ),
    ( 16, 86, 13, 48, 4 ),
    ( 16, 87, 14, 55, 5 ),

    ( 17, 81, 9, 33, 1 ),
    ( 17, 84, 11, 40, 2 ),
    ( 17, 89, 16, 62, 3 ),

    ( 18, 85, 12, 47, 1 ),
    ( 18, 92, 19, 73, 2 ),
    ( 18, 93, 2, 7, 3 ),

    ( 19, 83, 10, 37, 1 ),
    ( 19, 88, 15, 57, 2 ),
    ( 19, 94, 20, 76 );

-- -------------------------------------------------------------------------- --
