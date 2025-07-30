
# ---------------------------------------------------------------------------- #

import uuid
from django.db import models
from apps.users.models import Empresa, PerfilUsuario, Empleado

# ---------------------------------------------------------------------------- #

''' Esto permite designar a una evaluación como normativa o interna. '''
class TipoEvaluacion(models.Model):
    tipo_evaluacion_id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=32, blank=False, unique=True,
        verbose_name='Nombre', help_text='Nombre del tipo de evaluación.')

    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción del tipo de evaluación.')

    class Meta:
        ordering = [ 'nombre' ]
        db_table = 'tipos_evaluacion'
        verbose_name_plural = 'Tipos de evaluación'

    def __str__(self):
        return f'{self.nombre}'

# ---------------------------------------------------------------------------- #

''' Guarda la información general necesaria al crear una evaluación '''
class Evaluacion(models.Model):
    evaluacion_id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=128, blank=False,
        verbose_name='Nombre', help_text='Nombre de la evaluación.')

    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción de la evaluación.')

    instrucciones = models.TextField(blank=True, null=True,
        verbose_name='Instrucciones', help_text='Instrucciones de la evaluación.')

    tiempo_limite = models.IntegerField(blank=True, null=True,
        verbose_name='Tiempo límite', help_text='Tiempo máximo para contestar la evaluación.')

    umbral_aprobacion = models.IntegerField(blank=True, null=True,
        verbose_name='Umbral de aprobación', help_text='70 (%)')

    status = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT,
        verbose_name='Tipo de evaluación', help_text='Asignación de tipo de evaluación.')

    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.CASCADE,
        verbose_name='Empresa títular', help_text='Campo único de evaluaciones internas.')

    creado_por = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL,
        verbose_name='Usuario creador', help_text='Campo único de evaluaciones internas.')

    class Meta:
        db_table = 'evaluaciones'
        ordering = [ 'fecha_registro' ]
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return f'{self.nombre} ({self.tipo_evaluacion.nombre})'

# ---------------------------------------------------------------------------- #

''' Permite definir las secciones de una evaluación. '''
class SeccionEval(models.Model):
    seccion_id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=64, blank=False,
        verbose_name='Nombre', help_text='Nombre de la sección.')

    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción de la sección.')

    numero_orden = models.IntegerField(verbose_name='Orden', help_text='Número de orden dentro de la evaluación')
    es_evaluable = models.BooleanField(default=True, verbose_name='¿Evaluable?', help_text='Define si el contenido de esta sección es evaluable')

    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE,
        verbose_name='Evaluación', help_text='Evaluación a la que pertenece esta sección.')

    class Meta:
        db_table = 'secciones_eval'
        ordering = [ 'evaluacion' ]
        verbose_name_plural = 'Secciones'
        constraints = [
            models.UniqueConstraint(fields=['evaluacion', 'numero_orden'], name='unique_section_orden')
        ]

    def __str__(self):
        return f'{self.nombre} ({self.evaluacion.nombre})'

# ---------------------------------------------------------------------------- #

''' Define sencillamente las preguntas, pudiendo ser reutilizadas. '''
class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('Abierta', 'Abierta'),
        ('Múltiple', 'Múltiple'),
        ('Escala', 'Escala'),
        ('Bool', 'Bool'),
    ]

    pregunta_id = models.AutoField(primary_key=True)

    texto_pregunta = models.TextField(blank=False, null=False,
        verbose_name='Pregunta', help_text='Descripción de la pregunta.')

    tipo_pregunta = models.CharField(max_length=20, choices=TIPO_CHOICES,
        verbose_name='Tipo de pregunta', help_text='Define el tipo de pregunta.')

    es_obligatoria = models.BooleanField(default=True,
        verbose_name='¿Es obligatoria?', help_text='Define si la pregunta debe ser contestada obligatoriamente.')

    # A continuación se define si esta pregunta depende del resultado de otra.
    # Por ejemplo, para mostrar una dependiendo del resultado de otra.
    pregunta_padre = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
        db_column='pregunta_padre', related_name='preguntas_hijas',
        verbose_name='Pregunta padre', help_text='Pregunta de la cual esta pregunta depende.')

    activador_padre = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Activador padre', help_text='Valor que activa esta pregunta cuando la pregunta padre es contestada.')

    class Meta:
        db_table = 'preguntas'
        ordering = [ 'pregunta_id' ]
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return f'{self.texto_pregunta[:32]}...'

# ---------------------------------------------------------------------------- #

''' Define un conjunto de posibles respuestas.
    Su función principal es la reusabilidad, pues por ejemplo...
    ...podría reutilizarse un conjunto de respuestas tipo escala. '''
class ConjuntoRespuestas(models.Model):
    conjunto_id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=64, unique=True,
        verbose_name='Nombre del conjunto', help_text='Ej. Escala (malo, bueno)')

    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción del conjunto de respuestas')

    predefinido = models.BooleanField(default=False, verbose_name='¿Predefinido?',
        help_text='Indica si el conjunto de opciones es predefinido del sistema.')

    class Meta:
        ordering = [ 'predefinido' ]
        db_table = 'conjunto_respuestas'
        verbose_name_plural = 'Conjuntos de opciones'

    def __str__(self):
        return f'{self.nombre}'

# ---------------------------------------------------------------------------- #

''' Guarda cada una de las posibles respuestas. '''
class PosiblesRespuestas(models.Model):
    opcion_conjunto_id = models.AutoField(primary_key=True)

    texto_opcion = models.CharField(max_length=256, blank=False, null=False,
        verbose_name='Respuesta', help_text='Descripción/Valor de la respuesta.')

    # Dependiendo del tipo de valor que se espere guardar:
    valor_booleano = models.BooleanField(blank=True, null=True,
        verbose_name='Valor booleano', help_text='Valor booleano asociado a la opción.')

    valor_int = models.IntegerField(blank=True, null=True,
        verbose_name='Valor numérico', help_text='Valor numérico asociado a la opción.')

    valor_decimal = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2,
        verbose_name='Valor decimal', help_text='Valor númerico decimal asociado a la opción.')

    # Número de orden, dentro del conjunto de respuestas.
    numero_orden = models.IntegerField(verbose_name='Orden', help_text='Orden de la opción dentro del conjunto.')

    conjunto_respuestas = models.ForeignKey(ConjuntoRespuestas, on_delete=models.CASCADE,
        db_column='conjunto_respuestas', related_name='opciones',
        verbose_name='Conjunto de opciones', help_text='Conjunto de opciones al que pertenece esta respuesta.')

    class Meta:
        db_table = 'posibles_respuestas'
        verbose_name_plural = 'Posibles respuestas'
        ordering = [ 'conjunto_respuestas', 'numero_orden' ]
        constraints = [
            models.UniqueConstraint(fields=['conjunto_respuestas', 'numero_orden'], name='unique_opcion_orden')
        ]

    def __str__(self):
        return f'{self.texto_opcion} ({self.conjunto_respuestas.nombre})'

# ---------------------------------------------------------------------------- #

''' Asigna preguntas (con sus posibles respuestas) a la sección de una evaluación. '''
class SeccionPregunta(models.Model):
    seccion_pregunta_id = models.AutoField(primary_key=True)

    seccion = models.ForeignKey(SeccionEval, on_delete=models.CASCADE,
        related_name='preguntas_seccion', verbose_name='Sección', help_text='Sección a la que se asigna la pregunta.')

    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='secciones_pregunta',
        verbose_name='Pregunta', help_text='Pregunta a asignar a la sección.')

    conjunto_respuestas = models.ForeignKey(ConjuntoRespuestas, blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name='Conjunto de respuestas',
        help_text='Conjunto de respuestas para la pregunta anteriormente seleccionada.')

    respuesta_correcta = models.ForeignKey(PosiblesRespuestas, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='preguntas_con_respuesta_correcta',
        verbose_name='Respuesta correcta', help_text='Opción correcta para esta pregunta en particular, si aplica.'
    )

    numero_orden = models.IntegerField(verbose_name='Orden de la pregunta', help_text='Orden de la pregunta dentro de la sección.')

    class Meta:
        db_table = 'seccion_preguntas'
        verbose_name_plural = 'Preguntas por sección'
        ordering = [ 'seccion', 'numero_orden' ]
        constraints = [
            models.UniqueConstraint(fields=['seccion', 'pregunta'], name='unique_seccion_pregunta'),
            models.UniqueConstraint(fields=['seccion', 'numero_orden'], name='unique_seccion_orden')
        ]

    def __str__(self):
        return f'Sección: {self.seccion.nombre} - Pregunta: {self.pregunta.texto_pregunta[:32]}...'

# ---------------------------------------------------------------------------- #

''' Inicia la asignación de una evaluación. '''
class Asignacion(models.Model):
    asignacion_id = models.AutoField(primary_key=True)

    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.PROTECT,
        verbose_name='Evaluación', help_text='Evaluación asignada.')

    fecha_inicio = models.DateTimeField(verbose_name='Fecha de inicio',
        help_text='Fecha exacta en que la evaluación estará disponible.')

    fecha_fin = models.DateTimeField(verbose_name='Fecha de fin',
        help_text='Fecha exacta en que la evaluación dejará de estar disponible.')

    status = models.BooleanField(default=True, verbose_name='¿Se encuentra activa?', help_text='Indica si la asignación está activa actualmente.')

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Para evaluaciones 360:
    empleado_evaluado = models.ForeignKey(Empleado, on_delete=models.CASCADE, blank=True, null=True,
        related_name='evaluaciones_360_asignadas', verbose_name='Empleado evaluado',
        help_text='Empleado que será el sujeto de esta evaluación 360. Un campo obligatorio para evaluaciones 360.')

    puesto = models.CharField(max_length=64, blank=True, null=True,
        verbose_name='Puesto del empleado', help_text='Puesto del empleado evaluado en el momento de la asignación.')

    departamento = models.CharField(max_length=64, blank=True, null=True,
        verbose_name='Departamento del empleado', help_text='Departamento del empleado evaluado en el momento de la asignación.')

    class Meta:
        db_table = 'asignaciones'
        ordering = [ '-fecha_registro' ]
        verbose_name_plural = 'Asignaciones'

    def __str__(self):
        return f'Asignación de {self.evaluacion.nombre} ({self.evaluacion.tipo_evaluacion.nombre})'

# ---------------------------------------------------------------------------- #

''' Registra la asignación específica de cada empleadoa a una evaluación. '''
class AsignacionEmpleado(models.Model):
    ESTADO_CHOICES = [
        ('Expirada', 'Expirada'),
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
    ]

    asignacion_empleado_id = models.AutoField(primary_key=True)

    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE,
        verbose_name='Asignación', help_text='Asignación de evaluación a la que pertenece.')

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,
        verbose_name='Empleado', help_text='Empleado al que se le asignó la evaluación.')

    token_acceso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
        verbose_name='Token de acceso', help_text='Token único para que el empleado acceda a la evaluación.')


    status = models.CharField(max_length=16, choices=ESTADO_CHOICES, default='Pendiente',
        verbose_name='Estado de la asignación', help_text='Estado actual de la asignación para el empleado.')

    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'asignaciones_empleado'
        ordering = [ '-fecha_asignacion' ]
        unique_together = ( 'asignacion', 'empleado' )
        verbose_name_plural = 'Asignaciones por empleado'

    def __str__(self):
        return f'{self.empleado.nombre} - {self.asignacion.evaluacion.nombre} ({self.status})'

# ---------------------------------------------------------------------------- #

''' Registra cada respuesta dada por un empleado en una evaluación asignada. '''
class RespuestaEmpleado(models.Model):
    respuesta_empleado_id = models.AutoField(primary_key=True)

    asignacion_empleado = models.ForeignKey('AsignacionEmpleado', on_delete=models.CASCADE,
        verbose_name='Asignación del empleado', help_text='Asignación específica a la que pertenece esta respuesta.')

    seccion_pregunta = models.ForeignKey('SeccionPregunta', on_delete=models.CASCADE,
        verbose_name='Pregunta de la sección', help_text='La pregunta a la que se le dio respuesta.')

    # Valor de la respuesta dada por el empleado:
    opcion_seleccionada = models.ForeignKey('PosiblesRespuestas', on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='Opción seleccionada',
        help_text='La opción predefinida que el empleado seleccionó (si aplica).')

    respuesta_texto = models.TextField(blank=True, null=True,
        verbose_name='Respuesta de texto', help_text='Respuesta de texto libre para preguntas abiertas.')

    respuesta_valor_numerico = models.IntegerField(blank=True, null=True,
        verbose_name='Valor numérico', help_text='Valor numérico dado como respuesta.')

    respuesta_valor_decimal = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2,
        verbose_name='Valor decimal', help_text='Valor decimal dado como respuesta.')

    es_correcta = models.BooleanField(default=False,
        verbose_name='¿Es correcta?', help_text='Indica si la respuesta dada por el empleado es la correcta.')

    fecha_respuesta = models.DateTimeField(auto_now_add=True,
        verbose_name='Fecha de respuesta', help_text='Fecha exacta en que se registró esta respuesta.')

    class Meta:
        db_table = 'respuestas_empleado'
        verbose_name_plural = 'Respuestas de empleados'
        ordering = [ 'asignacion_empleado', 'fecha_respuesta' ]
        unique_together = ( 'asignacion_empleado', 'seccion_pregunta' )

    def __str__(self):
        return f'Respuesta de {self.asignacion_empleado.empleado.nombre} para {self.seccion_pregunta.pregunta.texto_pregunta[:32]}...'

# ---------------------------------------------------------------------------- #

''' Registra el resultado obtenido por un empleado al completar una evaluación. '''
class ResultadoEvaluacion(models.Model):
    resultado_id = models.AutoField(primary_key=True)

    asignacion_empleado = models.OneToOneField('AsignacionEmpleado', on_delete=models.CASCADE, unique=True,
        verbose_name='Asignación del Empleado', help_text='Asignación específica a la que corresponde este resultado.')

    puntaje_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
        verbose_name='Puntaje total', help_text='Puntaje total obtenido en la evaluación.')

    num_respuestas_correctas = models.IntegerField(default=0,
        verbose_name='Respuestas correctas', help_text='Número de respuestas correctas dadas en secciones evaluables.')

    num_preguntas_evaluables = models.IntegerField(default=0,
        verbose_name='Preguntas evaluables', help_text='Número total de preguntas en secciones evaluables con respuesta correcta definida.')

    porcentaje_correctas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
        verbose_name='Porcentaje correctas', help_text='Porcentaje de respuestas correctas sobre preguntas evaluables.')

    fecha_calculo = models.DateTimeField(auto_now_add=True,
        verbose_name='Fecha de cálculo', help_text='Fecha en que se calculó este resultado.')

    aprobado = models.BooleanField(blank=True, null=True,
        verbose_name='¿Aprobado?', help_text='Indica si el empleado aprobó la evaluación (según un criterio predefinido).')

    class Meta:
        ordering = [ '-fecha_calculo' ]
        db_table = 'resultados_evaluacion'
        verbose_name_plural = 'Resultados de Evaluación'

    def __str__(self):
        return f'Resultado de {self.asignacion_empleado.empleado.user.get_full_name()} para {self.asignacion_empleado.asignacion.evaluacion.nombre}'

# ---------------------------------------------------------------------------- #
