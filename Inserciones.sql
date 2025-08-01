
-- -------------------------------------------------------------------------- --

-- ! NOTA: Archivo obsoleto, para los datos usen un el 'Respaldo'.
-- Al insertar datos de esta manera no genera los UUIDs.

-- INSERCIÓN DE DATILLOS DE ESTRUCTURA ORGANIZACIONAL ----------------------- --

-- * 01: Iniciamos por insertar los usuarios.
    -- ? nombre: Nombre(s) del usuario.
    -- ? apellido_paterno: Apellido paterno del usuario.
    -- ? apellido_materno: Apellido materno del usuario.
    -- ? correo: Correo electrónico del usuario.
    -- ? nivel_usuario: Nivel del usuario.
    -- ? status: Estado del usuario.
    -- ? admin_empresa: ID del usuario 'administrador de empresa', usado en usarios nivel 'administrador de planta'.
    -- ? user_id: ID del usuario de DJANGO.
INSERT INTO USUARIOS(nombre, apellido_paterno, apellido_materno, correo, nivel_usuario, status, admin_empresa, user_id) VALUES
    ( 'Ed', 'Rubio', NULL, 'ed-rubio@outlook.com', 'superadmin', true, NULL, 1 ); -- ! ID: 1

-- -------------------------------------------------------------------------- --

-- * 02: Después creamos las empresas clientes.
    -- ? nombre: Nombre de la empresa.
    -- ? rfc: RFC de la empresa.
    -- ? direccion: Dirección física de la empresa.
    -- ? email_contacto: Correo electrónico de la empresa.
    -- ? telefono_contacto: Número de contacto de la empresa.
    -- ? status: Estado de la empresa.
    -- ? administrador: Usuario creador de la empresa 'administrador de empresa'.
INSERT INTO EMPRESAS(nombre, rfc, direccion, email_contacto, telefono_contacto, status, administrador) VALUES
    ( 'CodeWave', 'EASA123456ABC', 'Carretera Libre Tijuana-Tecate Km 10 Fracc. El Refugio, Quintas Campestre, 22253 Redondo, B.C.',
        'contacto@code-wave.com', '+526640000000', true, 1 ); -- ! ID: 1

-- -------------------------------------------------------------------------- --

-- * 03: A continuación, insertamos las plantas de las empresas.
    -- ? nombre: Sería, claramente, el nombre del tipo de evaluación.
    -- ? direccion: Sería la descripción del tipo de evaluación.
    -- ? status: Sería, claramente, el nombre del tipo de evaluación.
    -- ? empresa: Sería la descripción del tipo de evaluación.
INSERT INTO PLANTAS(nombre, direccion, status, empresa) VALUES
    ( 'Planta principal', 'Carretera Libre Tijuana-Tecate Km 10 Fracc. El Refugio, Quintas Campestre, 22253 Redondo, B.C.', true, 1 ); -- ! ID: 1

-- -------------------------------------------------------------------------- --

-- * 04: Posteriormente insertamos los departamentos.
    -- ? nombre: Nombre del departamento.
    -- ? descripcion: Pequeña descripción del departamento.
    -- ? status: Estado del departamento.
    -- ? planta: Planta a la cual pertenece el departamento.
INSERT INTO DEPARTAMENTOS(nombre, descripcion, status, planta) VALUES
    ( 'Desarrollo de Software', 'Departamento encargado de la producción de proyectos de software.', true, 1 ) -- ! ID: 1

-- -------------------------------------------------------------------------- --

-- * 05: Luego insertamos los puestos.
    -- ? nombre: Nombre del puesto.
    -- ? status: Estado del puesto.
    -- ? departamento: Departamento al que pertenece el puesto.
    -- ? descripcion: Pequeña descripción del puesto.
INSERT INTO PUESTOS(nombre, status, departamento, descripcion) VALUES
    ( 'Programador Senior', true, 1,
        'Lidera el diseño, desarrollo e implementación de software, mentorizando a programadores de menor experiencia.' ), -- ! ID: 1
    ( 'Programador Junior', true, 1,
        'Asiste en el desarrollo y mantenimiento de software, colaborando con equipos para escribir código y resolver problemas técnicos.' ); -- ! ID: 2

-- -------------------------------------------------------------------------- --

-- * 06: Y, por último, insertamos los empleados.
    -- ? nombre: Nombre(s) del empleado.
    -- ? apellido_paterno: Apellido paterno del empleaodo.
    -- ? apellido_materno: Apellido materno del empleaodo.
    -- ? email: Correo electrónico del empleaodo.
    -- ? telefono: Número de contacto del empleaodo.
    -- ? fecha_ingreso: Fecha de ingreso del empleaodo a la empresa (planta).
    -- ? status: Estado del empleaodo.
    -- ? puesto_id: Puesto del empleado.
INSERT INTO EMPLEADOS(nombre, apellido_paterno, apellido_materno, email, telefono, fecha_ingreso, status, puesto_id) VALUES
    ( 'Yael Alejandro', 'Contreras', 'Ríos', 'yael.contreras@code-wave.com', '5533445566', '2023-01-15', true, 1 ), -- ! ID: 1
    ( 'Amieva Ángel', 'Díaz', 'Cervantes', 'angel.amieva@code-wave.com', '5533445566', '2023-01-15', true, 1 ), -- ! ID: 2
    ( 'Fernanda', 'Díaz', 'Rios', 'fernanda.diaz@code-wave.com', '5533445566', '2023-01-15', true, 1  ), -- ! ID: 3
    ( 'Ernesto', 'García', 'Valenzuela', 'ernesto.garcia@code-wave.com', '5533445566', '2023-01-15', true, 1 ); -- ! ID: 4

-- INSERCIÓN DE DATILLOS DE LAS EVALUACIONES -------------------------------- --

-- * 01: Iniciamos por insertar los tipos de evaluación.
    -- ? nombre: Sería, claramente, el nombre del tipo de evaluación.
    -- ? descripcion: Sería la descripción del tipo de evaluación.
INSERT INTO TIPOS_EVALUACION(nombre, descripcion) VALUES
    ( 'Normativa', 'Evaluación estandarizada que cumple con normativas o estándares oficiales.' ), -- ! ID: 1
    ( 'Interna', 'Evaluación exclusiva de una empresa para su aplicación en el contexto interno de esta misma.' ); -- ! ID: 2

-- -------------------------------------------------------------------------- --

-- * 02: Creamos las evaluaciones base.
    -- ? titulo: Sería, claramente, el nombre de la evaluación.
    -- ? descripcion: Sería la descripción de la evaluación.
    -- ? instrucciones: Sería, claramente, el nombre del tipo de evaluación.
    -- ? contenido_informativo: Es un enlace a un archivo con contenido informativo.
    -- ? tiempo_limite: Sería la descripción del tipo de evaluación.
    -- ? umbral_aprobacion: Sería, claramente, el nombre del tipo de evaluación.
    -- ? estado: Sería la descripción del tipo de evaluación.
    -- ? tipo_evaluacion_id: Sería, claramente, el nombre del tipo de evaluación.
    -- ? empresa_id: Sería la empresa que ha creado la evaluación (de ser de tipo Interna).
    -- ? creado_por_id: Sería la descripción del tipo de evaluación.
INSERT INTO EVALUACIONES(titulo, descripcion, instrucciones, contenido_informativo, tiempo_limite,
    umbral_aprobacion, estado, tipo_evaluacion_id, empresa_id, creado_por_id) VALUES
    (
        'Factores de riesgo psicosocial: NOM-035 STPS 2018',
        'Evaluación diseñada para identificar los factores de riesgo psicosocial y evaluar el entorno organizacional en los centros de trabajo.',

        'Para responder de forma efectiva, por favor:
            Busca un lugar tranquilo y cómodo: Sin interrupciones para concentrarte.
            Sé totalmente honesto: Tu sinceridad es clave; no hay respuestas correctas o incorrectas.
            Lee con atención cada pregunta: Tómate tu tiempo para entender bien antes de responder.
            Considera tu experiencia general: Piensa en los últimos meses, no solo en eventos recientes.
        Tu honestidad y participación son muy importantes para mejorar nuestro entorno de trabajo.',

        'https://www.gob.mx/cms/uploads/attachment/file/503381/NOM035_guia.pdf',
        NULL, -- Esta evaluación no posee un tiempo límite para contestarla.
        NULL, -- Esta evaluación no posee un umbral de aprobación.
        'activa', -- Se registra la evaluación con un estado activo.
        1, -- Teniendo en cuenta que el tipo de evaluación normativo tiene este ID.
        NULL, -- Al ser una evaluación normativa no pertenece a una empresa específica.
        NULL -- Igualmente no se guarda un usuario creador.
    ), -- ! ID: 1
    (
        'Cumplimiento de la NOM-030 STPS 2009',
        'Evaluación destinada a la identificación y gestión de riesgos de seguridad y salud en un centro de trabajo.',

        'Para responder de forma efectiva, por favor:
            Busca un lugar tranquilo y cómodo: Sin interrupciones para concentrarte.
            Lee con atención cada pregunta: Tómate tu tiempo para entender bien antes de responder.
        Tu honestidad y participación son muy importantes para mejorar nuestro entorno de trabajo.',

        'https://repositorio.stps.gob.mx/SPS/DGSST/Documentos%20compartidos/46_Fracc_XLVI/GUIAS%20INFORMATIVAS/GUIA%20INFORMATIVA%20NOM-030%20vf.pdf',
        NULL, -- Esta evaluación no posee un tiempo límite para contestarla.
        80, -- El empleado debe contestar bien el 80% de las preguntas para ser considerado como aprobatorio.
        'activa', -- Se registra la evaluación con un estado activo.
        1, -- Teniendo en cuenta que el tipo de evaluación normativo tiene este ID.
        NULL, -- Al ser una evaluación normativa no pertenece a una empresa específica.
        NULL -- Igualmente no se guarda un usuario creador.
    ); -- ! ID: 2

-- -------------------------------------------------------------------------- --

-- * 03: Insertamos cada una de las secciones de la evaluación.
    -- ? nombre: Sería, claramente, el nombre de la sección.
    -- ? descripcion: Sería la descripción de la sección.
    -- ? numero_orden: Este es el número de orden que tiene esta sección en la evaluación.
    -- ? es_evaluable: Determina si el las preguntas de esta sección se toman en cuenta para una evaluación.
    -- ? evaluacion_id: Esta es la evaluación a la que pertenece la sección.
INSERT INTO SECCIONES_EVAL(nombre, descripcion, numero_orden, es_evaluable, evaluacion_id) VALUES
    (
        'Condiciones ambientales del centro de trabajo',
        'Para responder las preguntas siguientes considere las condiciones ambientales de su centro de trabajo.',
        1, -- Primer sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 1
    (
        'Cantidad y ritmo de trabajo',
        'Para responder a las preguntas siguientes piense en la cantidad y ritmo de trabajo que tiene.',
        2, -- Segunda sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 2
    (
        'Esfuerzo mental',
        'Las preguntas siguientes están relacionadas con el esfuerzo mental que le exige su trabajo.',
        3, -- Tercer sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 3
    (
        'Actividades y responsabilidades',
        'Las preguntas siguientes están relacionadas con las actividades que realiza en su trabajo y las responsabilidades que tiene.',
        4, -- Cuarta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 4
    (
        'Jornada de trabajo',
        'Las preguntas siguientes están relacionadas con su jornada de trabajo.',
        5, -- Quinta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 5
    (
        'Decisiones en el trabajo',
        'Las preguntas siguientes están relacionadas con las decisiones que puede tomar en su trabajo.',
        6, -- Sexta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 6
    (
        'Cambios en el trabajo',
        'Las preguntas siguientes están relacionadas con cualquier tipo de cambio que ocurra en su trabajo (considere los últimos cambios realizados).',
        7, -- Séptima sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 7
    (
        'Capacitación e información',
        'Las preguntas siguientes están relacionadas con la capacitación e información que se le proporciona sobre su trabajo.',
        8, -- Octava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 8
    (
        'Relación con los jefes',
        'Las preguntas siguientes están relacionadas con el o los jefes con quien tiene contacto.',
        9, -- Novena sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 9
    (
        'Relaciones con los compañeros',
        'Las preguntas siguientes se refieren a las relaciones con sus compañeros.',
        10, -- Décima sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 10
    (
        'Rendimiento, reconocimiento, pertenencia y estabilidad',
        'Las preguntas siguientes están relacionadas con la información que recibe sobre su rendimiento en el trabajo, el reconocimiento, el sentido de pertenencia y la estabilidad que le ofrece su trabajo.',
        11, -- Onceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 11
    (
        'Actos de violencia laboral',
        'Las preguntas siguientes están relacionadas con actos de violencia laboral (malos tratos, acoso, hostigamiento, acoso psicológico).',
        12, -- Doceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 12
    (
        'Atención a clientes y usuarios',
        'Las preguntas siguientes están relacionadas con la atención a clientes y usuarios.',
        13, -- Treceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 13
    (
        'Jefe de otros trabajadores',
        'Las preguntas siguientes están relacionadas con las actitudes de las personas que supervisa.',
        14, -- Catorceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ), -- ! ID: 14

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

-- -------------------------------------------------------------------------- --

-- * 04: Comenzamos a registrar cada una de las preguntas.
    -- ? texto_pregunta: Texto de la pregunta en sí.
    -- ? tipo_pregunta: Tipo de respuesta que se espera de esta pregunta.
    -- ? es_obligatoria: Define si la respuesta debe ser o no contestada.
    -- ? pregunta_padre: Determina la pregunta de la cual depende esta para ser mostrada.
    -- ? activador_padre: Este es el valor esperado de la pregunta padre para ser mostrada.
INSERT INTO PREGUNTAS(texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ( 'El espacio donde trabajo me permite realizar mis actividades de manera segura e higiénica', 'Escala', TRUE, NULL, NULL ), -- ! ID: 1
    ( 'Mi trabajo me exige hacer mucho esfuerzo físico', 'Escala', TRUE, NULL, NULL ), -- ! ID: 2
    ( 'Me preocupa sufrir un accidente en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 3
    ( 'Considero que en mi trabajo se aplican las normas de seguridad y salud en el trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 4
    ( 'Considero que las actividades que realizo son peligrosas', 'Escala', TRUE, NULL, NULL ), -- ! ID: 5

    ( 'Por la cantidad de trabajo que tengo debo quedarme tiempo adicional a mi turno', 'Escala', TRUE, NULL, NULL ), -- ! ID: 6
    ( 'Por la cantidad de trabajo que tengo debo trabajar sin parar', 'Escala', TRUE, NULL, NULL ), -- ! ID: 7
    ( 'Considero que es necesario mantener un ritmo de trabajo acelerado', 'Escala', TRUE, NULL, NULL ), -- ! ID: 8

    ( 'Mi trabajo exige que esté muy concentrado', 'Escala', TRUE, NULL, NULL ), -- ! ID: 9
    ( 'Mi trabajo requiere que memorice mucha información', 'Escala', TRUE, NULL, NULL ), -- ! ID: 10
    ( 'En mi trabajo tengo que tomar decisiones difíciles muy rápido', 'Escala', TRUE, NULL, NULL ), -- ! ID: 11
    ( 'Mi trabajo exige que atienda varios asuntos al mismo tiempo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 12

    ( 'En mi trabajo soy responsable de cosas de mucho valor', 'Escala', TRUE, NULL, NULL ), -- ! ID: 13
    ( 'Respondo ante mi jefe por los resultados de toda mi área de trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 14
    ( 'En el trabajo me dan órdenes contradictorias', 'Escala', TRUE, NULL, NULL ), -- ! ID: 15
    ( 'Considero que en mi trabajo me piden hacer cosas innecesarias', 'Escala', TRUE, NULL, NULL ), -- ! ID: 16

    ( 'Trabajo horas extras más de tres veces a la semana', 'Escala', TRUE, NULL, NULL ), -- ! ID: 17
    ( 'Mi trabajo me exige laborar en días de descanso, festivos o fines de semana', 'Escala', TRUE, NULL, NULL ), -- ! ID: 18
    ( 'Considero que el tiempo en el trabajo es mucho y perjudica mis actividades familiares o personales', 'Escala', TRUE, NULL, NULL ), -- ! ID: 19
    ( 'Debo atender asuntos de trabajo cuando estoy en casa', 'Escala', TRUE, NULL, NULL ), -- ! ID: 20
    ( 'Pienso en las actividades familiares o personales cuando estoy en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 21
    ( 'Pienso que mis responsabilidades familiares afectan mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 22

    ( 'Mi trabajo permite que desarrolle nuevas habilidades', 'Escala', TRUE, NULL, NULL ), -- ! ID: 23
    ( 'En mi trabajo puedo aspirar a un mejor puesto', 'Escala', TRUE, NULL, NULL ), -- ! ID: 24
    ( 'Durante mi jornada de trabajo puedo tomar pausas cuando las necesito', 'Escala', TRUE, NULL, NULL ), -- ! ID: 25
    ( 'Puedo decidir cuánto trabajo realizo durante la jornada laboral', 'Escala', TRUE, NULL, NULL ), -- ! ID: 26
    ( 'Puedo decidir la velocidad a la que realizo mis actividades en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 27
    ( 'Puedo cambiar el orden de las actividades que realizo en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 28

    ( 'Los cambios que se presentan en mi trabajo dificultan mi labor', 'Escala', TRUE, NULL, NULL ), -- ! ID: 29
    ( 'Cuando se presentan cambios en mi trabajo se tienen en cuenta mis ideas o aportaciones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 30

    ( 'Me informan con claridad cuáles son mis funciones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 31
    ( 'Me explican claramente los resultados que debo obtener en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 32
    ( 'Me explican claramente los objetivos de mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 33
    ( 'Me informan con quién puedo resolver problemas o asuntos de trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 34
    ( 'Me permiten asistir a capacitaciones relacionadas con mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 35
    ( 'Recibo capacitación útil para hacer mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 36

    ( 'Mi jefe ayuda a organizar mejor el trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 37
    ( 'Mi jefe tiene en cuenta mis puntos de vista y opiniones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 38
    ( 'Mi jefe me comunica a tiempo la información relacionada con el trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 39
    ( 'La orientación que me da mi jefe me ayuda a realizar mejor mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 40
    ( 'Mi jefe ayuda a solucionar los problemas que se presentan en el trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 41

    ( 'Puedo confiar en mis compañeros de trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 42
    ( 'Entre compañeros solucionamos los problemas de trabajo de forma respetuosa', 'Escala', TRUE, NULL, NULL ), -- ! ID: 43
    ( 'En mi trabajo me hacen sentir parte del grupo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 44
    ( 'Cuando tenemos que realizar trabajo de equipo los compañeros colaboran', 'Escala', TRUE, NULL, NULL ), -- ! ID: 45
    ( 'Mis compañeros de trabajo me ayudan cuando tengo dificultades', 'Escala', TRUE, NULL, NULL ), -- ! ID: 46

    ( 'Me informan sobre lo que hago bien en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 47
    ( 'La forma como evalúan mi trabajo en mi centro de trabajo me ayuda a mejorar mi desempeño', 'Escala', TRUE, NULL, NULL ), -- ! ID: 48
    ( 'En mi centro de trabajo me pagan a tiempo mi salario', 'Escala', TRUE, NULL, NULL ), -- ! ID: 49
    ( 'El pago que recibo es el que merezco por el trabajo que realizo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 50
    ( 'Si obtengo los resultados esperados en mi trabajo me recompensan o reconocen', 'Escala', TRUE, NULL, NULL ), -- ! ID: 51
    ( 'Las personas que hacen bien el trabajo pueden crecer laboralmente', 'Escala', TRUE, NULL, NULL ), -- ! ID: 52
    ( 'Considero que mi trabajo es estable', 'Escala', TRUE, NULL, NULL ), -- ! ID: 53
    ( 'En mi trabajo existe continua rotación de personal', 'Escala', TRUE, NULL, NULL ), -- ! ID: 54
    ( 'Siento orgullo de laborar en este centro de trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 55
    ( 'Me siento comprometido con mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 56

    ( 'En mi trabajo puedo expresarme libremente sin interrupciones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 57
    ( 'Recibo críticas constantes a mi persona y/o trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 58
    ( 'Recibo burlas, calumnias, difamaciones, humillaciones o ridiculizaciones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 59
    ( 'Se ignora mi presencia o se me excluye de las reuniones de trabajo y en la toma de decisiones', 'Escala', TRUE, NULL, NULL ), -- ! ID: 60
    ( 'Se manipulan las situaciones de trabajo para hacerme parecer un mal trabajador', 'Escala', TRUE, NULL, NULL ), -- ! ID: 61
    ( 'Se ignoran mis éxitos laborales y se atribuyen a otros trabajadores', 'Escala', TRUE, NULL, NULL ), -- ! ID: 62
    ( 'Me bloquean o impiden las oportunidades que tengo para obtener ascenso o mejora en mi trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 63
    ( 'He presenciado actos de violencia en mi centro de trabajo', 'Escala', TRUE, NULL, NULL ), -- ! ID: 64

    ( 'En mi trabajo debo brindar servicio a clientes o usuarios', 'Bool', TRUE, NULL, NULL ), -- ! ID: 65
    ( 'Atiendo clientes o usuarios muy enojados', 'Escala', FALSE, 65, TRUE), -- ! ID: 66
    ( 'Mi trabajo me exige atender personas muy necesitadas de ayuda o enfermas', 'Escala', FALSE, 65, TRUE), -- ! ID: 67
    ( 'Para hacer mi trabajo debo demostrar sentimientos distintos a los míos', 'Escala', FALSE, 65, TRUE), -- ! ID: 68
    ( 'Mi trabajo me exige atender situaciones de violencia', 'Escala', FALSE, 65, TRUE), -- ! ID: 69

    ( 'Soy jefe de otros trabajadores', 'Bool', TRUE, NULL, NULL ), -- ! ID: 70
    ( 'Comunican tarde los asuntos de trabajo', 'Escala', FALSE, 70, TRUE), -- ! ID: 71
    ( 'Dificultan el logro de los resultados del trabajo', 'Escala', FALSE, 70, TRUE), -- ! ID: 72
    ( 'Cooperan poco cuando se necesita', 'Escala', FALSE, 70, TRUE), -- ! ID: 73
    ( 'Ignoran las sugerencias para mejorar su trabajo', 'Escala', FALSE, 70, TRUE), -- ! ID: 74


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

-- -------------------------------------------------------------------------- --

-- * 05: Proseguimos a insertar los conjuntos de respuestas.
    -- ? nombre: Nombre del conjunto de respuestas.
    -- ? descripcion: Descripción del conjunto de respuestas.
    -- ? predefinido: Define si este conjunto puede ser globalmente utilizado en todas las evaluaciones.
INSERT INTO CONJUNTO_RESPUESTAS(nombre, descripcion, predefinido) VALUES
    ( 'Escala (Siempre/Nunca)', 'Opciones de respuesta para una escala de "Siempre" a "Nunca".', TRUE), -- ! ID: 1
    ( 'Booleano (Sí/No)', 'Opciones de respuesta para preguntas booleanas.', TRUE), -- ! ID: 2

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

-- -------------------------------------------------------------------------- --

-- * 06: Después ingresamos cada una de las posibles respuestas de estos conjuntos.
    -- ? texto_opcion: Texto de la opción (para las múltiples).
    -- ? valor_booleano: Valor booleano (para las de sí/no).
    -- ? valor_int: Valor enterno (para las de escala e incluso múltiples).
    -- ? valor_decimal: Valor decimal para respuestas con un valor decimal.
    -- ? numero_orden: Orden dentro del conjunto de respuestas.
    -- ? conjunto_respuestas: Conjunto de respuestas al que pertenece esta respuesta.
INSERT INTO RESPUESTAS_CONJUNTO(texto_opcion, valor_booleano, valor_int, valor_decimal, numero_orden, conjunto_respuestas) VALUES
    ( 'Siempre', NULL, 1, NULL, 1, 1), -- ! ID: 1
    ( 'Casi siempre', NULL, 2, NULL, 2, 1), -- ! ID: 2
    ( 'Algunas veces', NULL, 3, NULL, 3, 1), -- ! ID: 3
    ( 'Casi nunca', NULL, 4, NULL, 4, 1), -- ! ID: 4
    ( 'Nunca', NULL, 5, NULL, 5, 1), -- ! ID: 5

    ('Sí', TRUE, NULL, NULL, 1, 2), -- ! ID: 6
    ('No', FALSE, NULL, NULL, 2, 2), -- ! ID: 7


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

-- -------------------------------------------------------------------------- --

-- * 07: Iniciamos por insertar los tipos de evaluación.
    -- ? seccion_id: Sección de una evaluación en la cual estará la pregunta.
    -- ? pregunta_id: Preguntilla a asignar a una sección.
    -- ? conjunto_respuestas_id: Conjunto de posibles respuestas de la pregunta dada.
    -- ? respuesta_correcta_id: Respuesta correcta a la pregunta.
    -- ? numero_orden: Orden de las preguntas dentro de la sección.
INSERT INTO SECCION_PREGUNTAS (seccion_id, pregunta_id, conjunto_respuestas_id, respuesta_correcta_id, numero_orden) VALUES
    ( 1, 1, 1, NULL, 1),
    ( 1, 2, 1, NULL, 2),
    ( 1, 3, 1, NULL, 3),
    ( 1, 4, 1, NULL, 4),
    ( 1, 5, 1, NULL, 5),

    ( 2, 6, 1, NULL, 6),
    ( 2, 7, 1, NULL, 7),
    ( 2, 8, 1, NULL, 8),

    ( 3, 9, 1, NULL, 9),
    ( 3, 10, 1, NULL, 10),
    ( 3, 11, 1, NULL, 11),
    ( 3, 12, 1, NULL, 12),

    ( 4, 13, 1, NULL, 13),
    ( 4, 14, 1, NULL, 14),
    ( 4, 15, 1, NULL, 15),
    ( 4, 16, 1, NULL, 16),

    ( 5, 17, 1, NULL, 17),
    ( 5, 18, 1, NULL, 18),
    ( 5, 19, 1, NULL, 19),
    ( 5, 20, 1, NULL, 20),
    ( 5, 21, 1, NULL, 21),
    ( 5, 22, 1, NULL, 22),

    ( 6, 23, 1, NULL, 23),
    ( 6, 24, 1, NULL, 24),
    ( 6, 25, 1, NULL, 25),
    ( 6, 26, 1, NULL, 26),
    ( 6, 27, 1, NULL, 27),
    ( 6, 28, 1, NULL, 28),

    ( 7, 29, 1, NULL, 29),
    ( 7, 30, 1, NULL, 30),

    ( 8, 31, 1, NULL, 31),
    ( 8, 32, 1, NULL, 32),
    ( 8, 33, 1, NULL, 33),
    ( 8, 34, 1, NULL, 34),
    ( 8, 35, 1, NULL, 35),
    ( 8, 36, 1, NULL, 36),

    ( 9, 37, 1, NULL, 37),
    ( 9, 38, 1, NULL, 38),
    ( 9, 39, 1, NULL, 39),
    ( 9, 40, 1, NULL, 40),
    ( 9, 41, 1, NULL, 41),

    ( 10, 42, 1, NULL, 42),
    ( 10, 43, 1, NULL, 43),
    ( 10, 44, 1, NULL, 44),
    ( 10, 45, 1, NULL, 45),
    ( 10, 46, 1, NULL, 46),

    ( 11, 47, 1, NULL, 47),
    ( 11, 48, 1, NULL, 48),
    ( 11, 49, 1, NULL, 49),
    ( 11, 50, 1, NULL, 50),
    ( 11, 51, 1, NULL, 51),
    ( 11, 52, 1, NULL, 52),
    ( 11, 53, 1, NULL, 53),
    ( 11, 54, 1, NULL, 54),
    ( 11, 55, 1, NULL, 55),
    ( 11, 56, 1, NULL, 56),

    ( 12, 57, 1, NULL, 57),
    ( 12, 58, 1, NULL, 58),
    ( 12, 59, 1, NULL, 59),
    ( 12, 60, 1, NULL, 60),
    ( 12, 61, 1, NULL, 61),
    ( 12, 62, 1, NULL, 62),
    ( 12, 63, 1, NULL, 63),
    ( 12, 64, 1, NULL, 64),

    ( 13, 65, 2, NULL, 65),
    ( 13, 66, 1, NULL, 66),
    ( 13, 67, 1, NULL, 67),
    ( 13, 68, 1, NULL, 68),
    ( 13, 69, 1, NULL, 69),

    ( 14, 70, 2, NULL, 70),
    ( 14, 71, 1, NULL, 71),
    ( 14, 72, 1, NULL, 72),
    ( 14, 73, 1, NULL, 73),
    ( 14, 74, 1, NULL, 74),


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
    ( 19, 94, 20, 76, 3 );

-- -------------------------------------------------------------------------- --