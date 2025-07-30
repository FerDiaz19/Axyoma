
-- INSERCIÓN DE DATILLOS DE LAS EVALUACIONES -------------------------------- --

-- * 01: Iniciamos por insertar los tipos de evaluación.
    -- ? nombre: Sería, claramente, el nombre del tipo de evaluación.
    -- ? descripcion: Sería la descripción del tipo de evaluación.
INSERT INTO TIPOS_EVALUACION(nombre, descripcion) VALUES
    ( 'Normativa', 'Evaluación estandarizada que cumple con normativas o estándares oficiales.' ),
    ( 'Interna', 'Evaluación exclusiva de una empresa para su aplicación en el contexto interno de esta misma.' );


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
        'Factores de riesgo psicosocial: NOM-035 STPS 2018',

        'Evaluación diseñada para identificar los factores de riesgo psicosocial y evaluar el entorno organizacional en los centros de trabajo',

        'Para responder de forma efectiva, por favor:
            Busca un lugar tranquilo y cómodo: Sin interrupciones para concentrarte.
            Sé totalmente honesto: Tu sinceridad es clave; no hay respuestas correctas o incorrectas.
            Lee con atención cada pregunta: Tómate tu tiempo para entender bien antes de responder.
            Considera tu experiencia general: Piensa en los últimos meses, no solo en eventos recientes.
        Tu honestidad y participación son muy importantes para mejorar nuestro entorno de trabajo.',

        NULL, -- Esta evaluación no posee un tiempo límite para contestarla.
        NULL, -- Esta evaluación no posee un umbral de aprobación, pues no se califican 'respuestas correctas'.
        TRUE, -- Se registra la evaluación con un estado activo.
        1, -- Teniendo en cuenta que el tipo de evaluación normativo tiene este ID.
        NULL, -- Al ser una evaluación normativa no pertenece a una empresa específica.
        NULL -- Igualmente no se guarda un usuario creador.
    );


-- * 03: Insertamos cada una de las secciones de la evaluación.
    -- ? nombre: Sería, claramente, el nombre de la sección.
    -- ? descripcion: Sería la descripción de la sección.
    -- ? numero_orden: Este es el número de orden que tiene esta sección en la evaluación.
    -- ? es_evaluable: Determina si el las preguntas de esta sección se toman en cuenta para una evaluación.
    -- ? evaluacion: Esta es la evaluación a la que pertenece la sección.
INSERT INTO SECCIONES_EVAL(nombre, descripcion, numero_orden, es_evaluable, evaluacion) VALUES
    (
        'Condiciones ambientales del centro de trabajo',
        'Para responder las preguntas siguientes considere las condiciones ambientales de su centro de trabajo.',
        1, -- Primer sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Cantidad y ritmo de trabajo',
        'Para responder a las preguntas siguientes piense en la cantidad y ritmo de trabajo que tiene.',
        2, -- Segunda sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Esfuerzo mental',
        'Las preguntas siguientes están relacionadas con el esfuerzo mental que le exige su trabajo.',
        3, -- Tercer sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Actividades y responsabilidades',
        'Las preguntas siguientes están relacionadas con las actividades que realiza en su trabajo y las responsabilidades que tiene.',
        4, -- Cuarta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Jornada de trabajo',
        'Las preguntas siguientes están relacionadas con su jornada de trabajo.',
        5, -- Quinta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Decisiones en el trabajo',
        'Las preguntas siguientes están relacionadas con las decisiones que puede tomar en su trabajo.',
        6, -- Sexta sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Cambios en el trabajo',
        'Las preguntas siguientes están relacionadas con cualquier tipo de cambio que ocurra en su trabajo (considere los últimos cambios realizados).',
        7, -- Séptima sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Capacitación e información',
        'Las preguntas siguientes están relacionadas con la capacitación e información que se le proporciona sobre su trabajo.',
        8, -- Octava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Relación con los jefes',
        'Las preguntas siguientes están relacionadas con el o los jefes con quien tiene contacto.',
        9, -- Novena sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Relaciones con los compañeros',
        'Las preguntas siguientes se refieren a las relaciones con sus compañeros.',
        10, -- Décima sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Rendimiento, reconocimiento, pertenencia y estabilidad',
        'Las preguntas siguientes están relacionadas con la información que recibe sobre su rendimiento en el trabajo, el reconocimiento, el sentido de pertenencia y la estabilidad que le ofrece su trabajo.',
        11, -- Onceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Actos de violencia laboral',
        'Las preguntas siguientes están relacionadas con actos de violencia laboral (malos tratos, acoso, hostigamiento, acoso psicológico).',
        12, -- Doceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Atención a clientes y usuarios',
        'Las preguntas siguientes están relacionadas con la atención a clientes y usuarios.',
        13, -- Treceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    ),
    (
        'Jefe de otros trabajadores',
        'Las preguntas siguientes están relacionadas con las actitudes de las personas que supervisa.',
        14, -- Catorceava sección de la evaluación.
        FALSE, -- Las respuestas no son evaluables.
        1 -- Teniendo en ceunta que esta es la ID de la evaluación NOM-035.
    );


-- * 04: Comenzamos a registrar cada una de las preguntas.
    -- ? texto_pregunta: Texto de la pregunta en sí.
    -- ? tipo_pregunta: Tipo de respuesta que se espera de esta pregunta.
    -- ? es_obligatoria: Define si la respuesta debe ser o no contestada.
    -- ? pregunta_padre: Determina la pregunta de la cual depende esta para ser mostrada.
    -- ? activador_padre: Este es el valor esperado de la pregunta padre para ser mostrada.
INSERT INTO PREGUNTAS(texto_pregunta, tipo_pregunta, es_obligatoria, pregunta_padre, activador_padre) VALUES
    ( 'El espacio donde trabajo me permite realizar mis actividades de manera segura e higiénica', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi trabajo me exige hacer mucho esfuerzo físico', 'Escala', TRUE, NULL, NULL ),
    ( 'Me preocupa sufrir un accidente en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que en mi trabajo se aplican las normas de seguridad y salud en el trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que las actividades que realizo son peligrosas', 'Escala', TRUE, NULL, NULL ),

    ( 'Por la cantidad de trabajo que tengo debo quedarme tiempo adicional a mi turno', 'Escala', TRUE, NULL, NULL ),
    ( 'Por la cantidad de trabajo que tengo debo trabajar sin parar', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que es necesario mantener un ritmo de trabajo acelerado', 'Escala', TRUE, NULL, NULL ),

    ( 'Mi trabajo exige que esté muy concentrado', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi trabajo requiere que memorice mucha información', 'Escala', TRUE, NULL, NULL ),
    ( 'En mi trabajo tengo que tomar decisiones difíciles muy rápido', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi trabajo exige que atienda varios asuntos al mismo tiempo', 'Escala', TRUE, NULL, NULL ),

    ( 'En mi trabajo soy responsable de cosas de mucho valor', 'Escala', TRUE, NULL, NULL ),
    ( 'Respondo ante mi jefe por los resultados de toda mi área de trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'En el trabajo me dan órdenes contradictorias', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que en mi trabajo me piden hacer cosas innecesarias', 'Escala', TRUE, NULL, NULL ),

    ( 'Trabajo horas extras más de tres veces a la semana', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi trabajo me exige laborar en días de descanso, festivos o fines de semana', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que el tiempo en el trabajo es mucho y perjudica mis actividades familiares o personales', 'Escala', TRUE, NULL, NULL ),
    ( 'Debo atender asuntos de trabajo cuando estoy en casa', 'Escala', TRUE, NULL, NULL ),
    ( 'Pienso en las actividades familiares o personales cuando estoy en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Pienso que mis responsabilidades familiares afectan mi trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'Mi trabajo permite que desarrolle nuevas habilidades', 'Escala', TRUE, NULL, NULL ),
    ( 'En mi trabajo puedo aspirar a un mejor puesto', 'Escala', TRUE, NULL, NULL ),
    ( 'Durante mi jornada de trabajo puedo tomar pausas cuando las necesito', 'Escala', TRUE, NULL, NULL ),
    ( 'Puedo decidir cuánto trabajo realizo durante la jornada laboral', 'Escala', TRUE, NULL, NULL ),
    ( 'Puedo decidir la velocidad a la que realizo mis actividades en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Puedo cambiar el orden de las actividades que realizo en mi trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'Los cambios que se presentan en mi trabajo dificultan mi labor', 'Escala', TRUE, NULL, NULL ),
    ( 'Cuando se presentan cambios en mi trabajo se tienen en cuenta mis ideas o aportaciones', 'Escala', TRUE, NULL, NULL ),

    ( 'Me informan con claridad cuáles son mis funciones', 'Escala', TRUE, NULL, NULL ),
    ( 'Me explican claramente los resultados que debo obtener en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Me explican claramente los objetivos de mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Me informan con quién puedo resolver problemas o asuntos de trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Me permiten asistir a capacitaciones relacionadas con mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Recibo capacitación útil para hacer mi trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'Mi jefe ayuda a organizar mejor el trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi jefe tiene en cuenta mis puntos de vista y opiniones', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi jefe me comunica a tiempo la información relacionada con el trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'La orientación que me da mi jefe me ayuda a realizar mejor mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Mi jefe ayuda a solucionar los problemas que se presentan en el trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'Puedo confiar en mis compañeros de trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Entre compañeros solucionamos los problemas de trabajo de forma respetuosa', 'Escala', TRUE, NULL, NULL ),
    ( 'En mi trabajo me hacen sentir parte del grupo', 'Escala', TRUE, NULL, NULL ),
    ( 'Cuando tenemos que realizar trabajo de equipo los compañeros colaboran', 'Escala', TRUE, NULL, NULL ),
    ( 'Mis compañeros de trabajo me ayudan cuando tengo dificultades', 'Escala', TRUE, NULL, NULL ),

    ( 'Me informan sobre lo que hago bien en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'La forma como evalúan mi trabajo en mi centro de trabajo me ayuda a mejorar mi desempeño', 'Escala', TRUE, NULL, NULL ),
    ( 'En mi centro de trabajo me pagan a tiempo mi salario', 'Escala', TRUE, NULL, NULL ),
    ( 'El pago que recibo es el que merezco por el trabajo que realizo', 'Escala', TRUE, NULL, NULL ),
    ( 'Si obtengo los resultados esperados en mi trabajo me recompensan o reconocen', 'Escala', TRUE, NULL, NULL ),
    ( 'Las personas que hacen bien el trabajo pueden crecer laboralmente', 'Escala', TRUE, NULL, NULL ),
    ( 'Considero que mi trabajo es estable', 'Escala', TRUE, NULL, NULL ),
    ( 'En mi trabajo existe continua rotación de personal', 'Escala', TRUE, NULL, NULL ),
    ( 'Siento orgullo de laborar en este centro de trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Me siento comprometido con mi trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'En mi trabajo puedo expresarme libremente sin interrupciones', 'Escala', TRUE, NULL, NULL ),
    ( 'Recibo críticas constantes a mi persona y/o trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'Recibo burlas, calumnias, difamaciones, humillaciones o ridiculizaciones', 'Escala', TRUE, NULL, NULL ),
    ( 'Se ignora mi presencia o se me excluye de las reuniones de trabajo y en la toma de decisiones', 'Escala', TRUE, NULL, NULL ),
    ( 'Se manipulan las situaciones de trabajo para hacerme parecer un mal trabajador', 'Escala', TRUE, NULL, NULL ),
    ( 'Se ignoran mis éxitos laborales y se atribuyen a otros trabajadores', 'Escala', TRUE, NULL, NULL ),
    ( 'Me bloquean o impiden las oportunidades que tengo para obtener ascenso o mejora en mi trabajo', 'Escala', TRUE, NULL, NULL ),
    ( 'He presenciado actos de violencia en mi centro de trabajo', 'Escala', TRUE, NULL, NULL ),

    ( 'En mi trabajo debo brindar servicio a clientes o usuarios', 'Bool', TRUE, NULL, NULL ),
    ( 'Atiendo clientes o usuarios muy enojados', 'Escala', FALSE, 65, TRUE),
    ( 'Mi trabajo me exige atender personas muy necesitadas de ayuda o enfermas', 'Escala', FALSE, 65, TRUE),
    ( 'Para hacer mi trabajo debo demostrar sentimientos distintos a los míos', 'Escala', FALSE, 65, TRUE),
    ( 'Mi trabajo me exige atender situaciones de violencia', 'Escala', FALSE, 65, TRUE),

    ( 'Soy jefe de otros trabajadores', 'Bool', TRUE, NULL, NULL ),
    ( 'Comunican tarde los asuntos de trabajo', 'Escala', FALSE, 70, TRUE),
    ( 'Dificultan el logro de los resultados del trabajo', 'Escala', FALSE, 70, TRUE),
    ( 'Cooperan poco cuando se necesita', 'Escala', FALSE, 70, TRUE),
    ( 'Ignoran las sugerencias para mejorar su trabajo', 'Escala', FALSE, 70, TRUE);


-- * 05: Proseguimos a insertar los conjuntos de respuestas.
    -- ? nombre: Nombre del conjunto de respuestas.
    -- ? descripcion: Descripción del conjunto de respuestas.
    -- ? predefinido: Define si este conjunto puede ser globalmente utilizado en todas las evaluaciones.
INSERT INTO CONJUNTO_RESPUESTAS(nombre, descripcion, predefinido) VALUES
    ( 'Escala (Siempre/Nunca)', 'Opciones de respuesta para una escala de "Siempre" a "Nunca".', TRUE),
    ( 'Booleano (Sí/No)', 'Opciones de respuesta para preguntas booleanas.', TRUE);


-- * 06: Después ingresamos cada una de las posibles respuestas de estos conjuntos.
    -- ? nombre: Nombre del conjunto de respuestas.
    -- ? descripcion: Descripción del conjunto de respuestas.
    -- ? predefinido: Define si este conjunto puede ser globalmente utilizado en todas las evaluaciones.
INSERT INTO POSIBLES_RESPUESTAS(texto_opcion, valor_booleano, valor_int, valor_decimal, numero_orden, conjunto_respuestas) VALUES
    ( 'Siempre', NULL, NULL, NULL, 1, 1),
    ( 'Casi siempre', NULL, NULL, NULL, 2, 1),
    ( 'Algunas veces', NULL, NULL, NULL, 3, 1),
    ( 'Casi nunca', NULL, NULL, NULL, 4, 1),
    ( 'Nunca', NULL, NULL, NULL, 5, 1),

    ('Sí', TRUE, NULL, NULL, 1, 2),
    ('No', FALSE, NULL, NULL, 2, 2);


-- * 07: Iniciamos por insertar los tipos de evaluación.
    -- ? seccion: Sección de una evaluación en la cual estará la pregunta.
    -- ? pregunta: Preguntilla a asignar a una sección.
    -- ? conjunto_respuestas: Conjunto de posibles respuestas de la pregunta dada.
    -- ? respuesta_correcta: Respuesta correcta a la pregunta.
    -- ? numero_orden: Orden de las preguntas dentro de la sección.
INSERT INTO SECCION_PREGUNTAS (seccion, pregunta, conjunto_respuestas, respuesta_correcta, numero_orden) VALUES
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
    ( 14, 74, 1, NULL, 74);

-- -------------------------------------------------------------------------- --
