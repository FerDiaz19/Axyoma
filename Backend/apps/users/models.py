
# ---------------------------------------------------------------------------- #

import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.subscriptions.models import SuscripcionEmpresa

# ---------------------------------------------------------------------------- #

''' Modelos de usuarios, corregidos por Ed Rubio. '''

# ---------------------------------------------------------------------------- #

class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ( 'superadmin', 'Administrador principal' ),
        ( 'admin-empresa', 'Administrador de empresa '),
        ( 'admin-planta', 'Administrador de planta' ),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name='Nombre(s)')
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido materno")
    correo = models.EmailField(max_length=255, unique=True, verbose_name="Correo electrónico")
    nivel_usuario = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nivel de Usuario")
    status = models.BooleanField(default=True, verbose_name='Estado de acceso a la plataforma')

    admin_empresa = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        db_column='admin_empresa',
        verbose_name="Usuario creador (administrador de empresa)",
        help_text="Administrador de empresa que ha creado a este usuario."
    )

    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE,
        db_column='user_id',
        related_name='perfilusuario',
        verbose_name='ID del usaurio ligada a este perfil.'
    )

    # Metadatos:
    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = [ 'nombre', 'nivel_usuario' ]

        indexes = [
            models.Index(fields=['nivel_usuario']),
            models.Index(fields=['correo']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.nivel_usuario == 'admin-planta' and not self.admin_empresa:
            raise ValidationError("El usuario ha de tener un administrador de empresaa asignado.")
        if self.nivel_usuario == 'superadmin' and self.admin_empresa:
            raise ValidationError('Un administrador principal no puede estar lugador a un administrador de empresa.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        ''' Nombre completo formateado. '''
        nombres = [ self.nombre, self.apellido_paterno ]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} - ({self.get_nivel_usuario_display()})'

# ---------------------------------------------------------------------------- #

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=65, unique=True, verbose_name="Nombre de la empresa")
    rfc = models.CharField(max_length=16, unique=True, verbose_name="RFC de la empresa")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección física de la empresa")
    logotipo = models.URLField(max_length=255, blank=True, null=True, verbose_name="URL del Logotipo")
    email_contacto = models.EmailField(max_length=128, blank=True, null=True, verbose_name="Correo electrónico de contacto")
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de teléfono de contacto")

    # ! Olvidaste este campo.
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name='¿La empresa se encuentra activa en el sistema?')

    administrador = models.OneToOneField(
        PerfilUsuario, on_delete=models.PROTECT,
        db_column='administrador',
        verbose_name="Administrador de la empresa",
        limit_choices_to={ 'nivel_usuario': 'admin-empresa' }
    )

    class Meta:
        db_table = 'empresas'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = [ 'nombre', 'status' ]
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['rfc']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.administrador and self.administrador.nivel_usuario != 'admin-empresa':
            raise ValidationError("El administrador debe estar registrado como administrador de empresa.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def tiene_suscripcion_activa(self):
        ''' Verifica si la empresa tiene una suscripción activa. '''
        try:
            return SuscripcionEmpresa.objects.filter(
                empresa=self, estado='activa').exists()
        except ImportError:
            return False

    @property
    def suscripcion_activa(self):
        ''' Obtiene la suscripción activa más reciente. '''
        try:
            return SuscripcionEmpresa.objects.filter(
                empresa=self,
                estado='activa'
            ).order_by('-fecha_inicio').first()
        except ImportError:
            return None

    @property
    def total_plantas(self):
        ''' Número total de plantas activas. '''
        return self.plantas.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos. '''
        return sum(planta.total_empleados for planta in self.plantas.filter(status=True))

    def __str__(self):
        return f'{self.nombre} - ({self.status})'

# ---------------------------------------------------------------------------- #

class Planta(models.Model):
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre de la Planta")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    status = models.BooleanField(default=True, verbose_name="Activa")

    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE,
        db_column='empresa',
        related_name='plantas', verbose_name="Empresa"
    )

    class Meta:
        db_table = 'plantas'
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        ordering = [ 'empresa', 'nombre', 'status' ]
        unique_together = [[ 'empresa', 'nombre' ]]

        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['status'])
        ]

    @property
    def total_departamentos(self):
        ''' Número total de departamentos activos. '''
        return self.departamentos.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en la planta. '''
        return sum(depto.total_empleados for depto in self.departamentos.filter(status=True))

    def __str__(self):
        return f"{self.nombre} - ({self.empresa.nombre})"

# ---------------------------------------------------------------------------- #

class AdminPlanta(models.Model):
    id = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        PerfilUsuario, on_delete=models.CASCADE,
        db_column='usuario_id', verbose_name="Administrador de planta",
        limit_choices_to={ 'nivel_usuario': 'admin-planta' },
    )

    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE,
        db_column='planta_id', verbose_name="Planta asignada"
    )

    status = models.BooleanField(default=True, verbose_name='¿El usuario puede administrar esta planta?')

    password_temporal = models.CharField(
        max_length=128, blank=True, null=True,
        verbose_name="Contraseña temporal",
        help_text="Contraseña temporal generada automáticamente"
    )

    class Meta:
        db_table = 'admin_plantas'
        verbose_name = "Administrador de planta"
        verbose_name_plural = "Administradores de plantas"
        unique_together = [[ 'usuario', 'planta' ]]
        ordering = [ 'planta', 'usuario' ]
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['planta']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.usuario and self.usuario.nivel_usuario != 'admin-planta':
            raise ValidationError("El usuario debe estar registrado como administrador de planta.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.planta.nombre}"

# ---------------------------------------------------------------------------- #

class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, verbose_name="Nombre del departamento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    status = models.BooleanField(default=True, verbose_name="¿El departamento de esta empresa se encuentra acitvo?")

    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE,
        db_column='planta',
        related_name='departamentos', verbose_name="Planta"
    )

    class Meta:
        db_table = 'departamentos'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = [ 'planta', 'nombre' ]
        unique_together = [[ 'planta', 'nombre' ]]
        indexes = [
            models.Index(fields=['planta']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.nombre:
            self.nombre = self.nombre.strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_puestos(self):
        ''' Número total de puestos activos. '''
        return self.puestos.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en el departamento. '''
        return sum(puesto.total_empleados for puesto in self.puestos.filter(status=True))

    def __str__(self):
        return f"{self.nombre} - {self.planta.nombre}"


class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, verbose_name="Nombre del puesto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del puesto")
    status = models.BooleanField(default=True, verbose_name="¿El puesto se encuentra activo?")

    # Relación con departamento
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE,
        db_column='departamento',
        related_name='puestos', verbose_name="Departamento"
    )

    class Meta:
        db_table = 'puestos'
        verbose_name = "Puesto"
        verbose_name_plural = "Puestos"
        ordering = [ 'nombre' ]
        unique_together = [[ 'nombre', 'departamento' ]]
        indexes = [
            models.Index(fields=['departamento']),
            models.Index(fields=['status'])
        ]

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en el puesto. '''
        return self.empleados.filter(status=True).count()

    @property
    def empresa(self):
        ''' Empresa a la que pertenece el puesto. '''
        return self.departamento.planta.empresa

    @property
    def planta(self):
        ''' Planta a la que pertenece el puesto. '''
        return self.departamento.planta

    def __str__(self):
        return f"{self.nombre} - {self.departamento.nombre}"

# ---------------------------------------------------------------------------- #

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido materno")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de teléfono")
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de Ingreso")
    status = models.BooleanField(default=True, verbose_name="¿El empleado se encuentra activo?")

    puesto = models.ForeignKey(
        Puesto, on_delete=models.CASCADE,
        db_column='puesto',
        related_name='empleados', verbose_name="Puesto"
    )

    class Meta:
        db_table = 'empleados'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = [ 'nombre', 'puesto', 'status' ]
        indexes = [
            models.Index(fields=[ 'puesto' ]),
            models.Index(fields=[ 'email' ]),
            models.Index(fields=[ 'status' ])
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[ 'email' ],
                condition=models.Q(email__isnull=False) & ~models.Q(email=''),
                name='unique_employee_email'
            )
        ]

    @property
    def nombre_completo(self):
        ''' Nombre completo formateado. '''
        nombres = [ self.nombre, self.apellido_paterno ]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)

    @property
    def empresa(self):
        ''' Empresa a la que pertenece el empleado. '''
        return self.puesto.empresa

    @property
    def planta(self):
        ''' Planta a la que pertenece el empleado. '''
        return self.puesto.planta

    @property
    def departamento(self):
        ''' Departamento al que pertenece el empleado. '''
        return self.puesto.departamento

    def __str__(self):
        return f"{self.nombre_completo} - {self.puesto.nombre}"

# ---------------------------------------------------------------------------- #

class TipoEvaluacion(models.Model):
    tipo_evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=64, unique=True,
        verbose_name='Nombre',
        help_text='Nombre del tipo de evaluación (ej: Normativa, Interna, 360 Grados)'
    )
    descripcion = models.TextField(
        blank=True, null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del tipo de evaluación'
    )

    class Meta:
        db_table = 'tipos_evaluacion'
        verbose_name = 'Tipo de evaluación'
        verbose_name_plural = 'Tipos de evaluación'
        ordering = [ 'nombre' ]
        indexes = [
            models.Index(fields=[ 'nombre' ])
        ]

    def __str__(self):
        return f'{self.nombre}'

# ---------------------------------------------------------------------------- #

class Evaluacion(models.Model):
    evaluacion_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=128,
        verbose_name='Nombre',
        help_text='Nombre de la evaluación'
    )
    descripcion = models.TextField(
        blank=True, null=True,
        verbose_name='Descripción',
        help_text='Descripción de la evaluación'
    )
    instrucciones = models.TextField(
        blank=True, null=True,
        verbose_name='Instrucciones',
        help_text='Instrucciones para completar la evaluación'
    )
    contenido_informativo = models.TextField(
        blank=True, null=True,
        verbose_name='Contenido informativo',
        help_text='Enlace a contenido informativo de la evaluación'
    )
    tiempo_limite = models.IntegerField(
        blank=True, null=True,
        verbose_name='Tiempo Límite (min)',
        help_text='Tiempo máximo en minutos para completar la evaluación'
    )
    umbral_aprobacion = models.IntegerField(
        blank=True, null=True,
        verbose_name='Umbral de Aprobación (%)',
        help_text='Porcentaje mínimo para aprobar (ej: 70)'
    )
    estado = models.BooleanField(default=True, verbose_name="¿La evaluación se encuentraa activa?")

    # ! Olvidaste este campo.
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha en que se creó la evaluación")

    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última fecha de ctualización")

    tipo_evaluacion = models.ForeignKey(
        TipoEvaluacion, on_delete=models.PROTECT,
        db_column='tipo_evaluacion_id',
        verbose_name='Tipo de Evaluación',
        help_text='Tipo de evaluación al que pertenece'
    )
    empresa = models.ForeignKey(
        Empresa, null=True, blank=True,
        on_delete=models.CASCADE,
        db_column='empresa_id',
        verbose_name='Empresa',
        help_text='Empresa propietaria (en caso de ser Internas)'
    )
    creado_por = models.ForeignKey(
        PerfilUsuario, on_delete=models.SET_NULL,
        null=True, blank=True, db_column='creado_por_id',
        verbose_name='Creado por',
        help_text='Usuario que creó la evaluación'
    )

    class Meta:
        db_table = 'evaluaciones'
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = [ 'titulo', 'estado' ]
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_evaluacion']),
            models.Index(fields=['empresa']),
            models.Index(fields=['creado_por'])
        ]

    def clean(self):
        if self.umbral_aprobacion and (self.umbral_aprobacion < 0 or self.umbral_aprobacion > 100):
            raise ValidationError('El umbral de aprobación debe estar entre 0 y 100')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def es_normativa(self):
        ''' Indica si es una evaluación normativa. '''
        return self.tipo_evaluacion.nombre.lower() == 'normativa'

    @property
    def total_secciones(self):
        ''' Número total de secciones. '''
        return self.secciones.count()

    def __str__(self):
        return f"{self.titulo} ({self.tipo_evaluacion.nombre})"


class SeccionEval(models.Model):
    seccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64,
        verbose_name='Nombre',
        help_text='Nombre de la sección'
    )
    descripcion = models.TextField(
        blank=True, null=True,
        verbose_name='Descripción',
        help_text='Descripción de la sección'
    )
    numero_orden = models.IntegerField(
        verbose_name='Orden',
        help_text='Número de orden dentro de la evaluación'
    )
    es_evaluable = models.BooleanField(default=True,
        verbose_name='¿Es evaluable?',
        help_text='Define si las preguntas de esta sección se califican'
    )

    evaluacion = models.ForeignKey(
        Evaluacion, on_delete=models.CASCADE,
        related_name='secciones', db_column='evaluacion_id',
        verbose_name='Evaluación', help_text='Evaluación a la que pertenece esta sección'
    )

    class Meta:
        db_table = 'secciones_eval'
        verbose_name = 'Sección de una evaluación'
        verbose_name_plural = 'Secciones de las evaluaciones'
        ordering = [ 'evaluacion', 'numero_orden' ]
        unique_together = [[ 'evaluacion', 'numero_orden' ], [ 'evaluacion', 'nombre' ]]
        indexes = [
            models.Index(fields=['evaluacion']),
            models.Index(fields=['numero_orden'])
        ]

    @property
    def total_preguntas(self):
        ''' Número total de preguntas en la sección. '''
        return self.preguntas_seccion.count()

    def __str__(self):
        return f"{self.nombre} ({self.evaluacion.titulo})"

# ---------------------------------------------------------------------------- #

class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('Abierta', 'Pregunta abierta'),
        ('Múltiple', 'Preguna con opciones'),
        ('Escala', 'Pregunta con escala de calificación'),
        ('Bool', 'Pregunta de sí/no'),
    ]

    pregunta_id = models.AutoField(primary_key=True)
    texto_pregunta = models.TextField(
        verbose_name='Pregunta',
        help_text='Texto de la pregunta'
    )
    tipo_pregunta = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Pregunta',
        help_text='Tipo de respuesta esperada'
    )
    es_obligatoria = models.BooleanField(
        default=True,
        verbose_name='¿Es obligatoria?',
        help_text='Indica si la pregunta debe ser respondida'
    )

    pregunta_padre = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        db_column='pregunta_padre',
        related_name='preguntas_hijas', verbose_name='Pregunta padre',
        help_text='Pregunta de la cual depende esta pregunta'
    )
    activador_padre = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Activador',
        help_text='Valor que activa esta pregunta'
    )

    class Meta:
        db_table = 'preguntas'
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['pregunta_id']
        indexes = [
            models.Index(fields=['tipo_pregunta']),
            models.Index(fields=['pregunta_padre'])
        ]

    def __str__(self):
        texto_corto = self.texto_pregunta[:50]
        if len(self.texto_pregunta) > 50:
            texto_corto += "..."
        return f"{texto_corto} ({self.get_tipo_pregunta_display()})"

# ---------------------------------------------------------------------------- #

class ConjuntoRespuestas(models.Model):
    conjunto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Nombre del Conjunto',
        help_text='Nombre identificativo del conjunto (ej: Escala Likert 5 puntos)'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción del conjunto de respuestas'
    )
    predefinido = models.BooleanField(
        default=False,
        verbose_name='¿Es predefinido?',
        help_text='Indica si es un conjunto del sistema que no se puede modificar'
    )

    class Meta:
        db_table = 'conjunto_opciones'
        verbose_name = 'Conjunto de Respuestas'
        verbose_name_plural = 'Conjuntos de Respuestas'
        ordering = [ 'predefinido', 'nombre' ]
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['predefinido'])
        ]

    @property
    def total_opciones(self):
        """Número total de opciones en el conjunto"""
        return self.opciones.count()

    def __str__(self):
        return self.nombre


class PosiblesRespuestas(models.Model):
    opcion_conjunto_id = models.AutoField(primary_key=True)
    texto_opcion = models.CharField(
        max_length=256,
        verbose_name='Opción',
        help_text='Texto de la opción de respuesta'
    )
    valor_booleano = models.BooleanField(
        blank=True, null=True,
        verbose_name='Valor Booleano',
        help_text='Valor verdadero/falso asociado'
    )
    valor_numerico = models.IntegerField(
        blank=True, null=True,
        verbose_name='Valor Numérico',
        help_text='Valor numérico entero asociado'
    )

    # ! Olvidaste este camppo.
    valor_decimal = models.DecimalField(
        blank=True, null=True,
        max_digits=6, decimal_places=2,
        verbose_name='Valor Numérico',
        help_text='Valor numérico entero asociado'
    )

    numero_orden = models.IntegerField(
        verbose_name='Orden',
        help_text='Orden de la opción dentro del conjunto'
    )
    conjunto_respuestas = models.ForeignKey(
        ConjuntoRespuestas,
        on_delete=models.CASCADE,
        db_column='conjunto_respuestas',
        related_name='opciones',
        verbose_name='Conjunto de Respuestas'
    )

    class Meta:
        db_table = 'respuestas_conjunto'
        verbose_name = 'Opción de respuesta'
        verbose_name_plural = 'Opciones de respuesta'
        ordering = [ 'conjunto_respuestas', 'numero_orden' ]
        unique_together = [[ 'conjunto_respuestas', 'numero_orden' ]]
        indexes = [
            models.Index(fields=['conjunto_respuestas']),
            models.Index(fields=['numero_orden'])
        ]

    def __str__(self):
        return f"{self.texto_opcion} ({self.conjunto_respuestas.nombre})"

# ---------------------------------------------------------------------------- #

class SeccionPregunta(models.Model):
    seccion_pregunta_id = models.AutoField(primary_key=True)

    numero_orden = models.IntegerField(
        verbose_name='Orden en la sección',
        help_text='Orden de la pregunta dentro de la sección'
    )
    conjunto_respuestas = models.ForeignKey(
        ConjuntoRespuestas, blank=True, null=True,
        on_delete=models.SET_NULL, db_column='conjunto_respuestas_id',
        verbose_name='Conjunto de respuestas',
        help_text='Conjunto de opciones para esta pregunta'
    )
    pregunta = models.ForeignKey(
        Pregunta, on_delete=models.CASCADE,
        related_name='secciones_pregunta',
        db_column='pregunta_id',
        verbose_name='Pregunta'
    )
    respuesta_correcta = models.ForeignKey(
        PosiblesRespuestas, on_delete=models.SET_NULL,
        blank=True, null=True, db_column='respuesta_correcta_id',
        related_name='preguntas_con_respuesta_correcta',
        verbose_name='Respuesta correcta',
        help_text='Opción correcta para la pregunta dada'
    )
    seccion = models.ForeignKey(
        SeccionEval, on_delete=models.CASCADE,
        related_name='preguntas_seccion',
        verbose_name='Sección',
        db_column='seccion_id',
    )

    class Meta:
        db_table = 'seccion_preguntas'
        verbose_name = 'Pregunta de sección'
        verbose_name_plural = 'Preguntas de sección'
        ordering = [ 'seccion', 'numero_orden' ]
        unique_together = [
            [ 'seccion', 'pregunta' ],
            [ 'seccion', 'numero_orden' ]
        ]
        indexes = [
            models.Index(fields=['seccion']),
            models.Index(fields=['pregunta']),
            models.Index(fields=['numero_orden'])
        ]

    def clean(self):
        """Validaciones personalizadas"""
        if self.respuesta_correcta and self.conjunto_respuestas:
            if self.respuesta_correcta.conjunto_respuestas != self.conjunto_respuestas:
                raise ValidationError("La respuesta correcta debe pertenecer al conjunto de respuestas seleccionado")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        pregunta_corta = self.pregunta.texto_pregunta[:30]
        if len(self.pregunta.texto_pregunta) > 30:
            pregunta_corta += "..."
        return f"{self.seccion.nombre} - {pregunta_corta}"

# ---------------------------------------------------------------------------- #

class Asignacion(models.Model):
    asignacion_id = models.AutoField(primary_key=True)
    evaluacion = models.ForeignKey(
        'users.Evaluacion', on_delete=models.PROTECT,
        db_column='evaluacion_id',
        related_name='asignaciones',
        verbose_name='Evaluación'
    )
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de Inicio',
        help_text='Fecha en que la evaluación estará disponible'
    )
    fecha_fin = models.DateTimeField(
        verbose_name='Fecha de Fin',
        help_text='Fecha en que la evaluación dejará de estar disponible'
    )
    status = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='Indica si la asignación está activa'
    )

    # ! Olvidaste este campo:
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación de la asignación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    # Para evaluaciones 360:
    empleado_evaluado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE,
        blank=True, null=True, db_column='empleado_evaluado_id',
        related_name='evaluaciones_360_asignadas',
        verbose_name='Empleado Evaluado',
        help_text='Empleado sujeto de evaluación 360 grados'
    )
    puesto_al_momento = models.CharField(
        max_length=128, blank=True, null=True,
        db_column='puesto_empleado',
        verbose_name='Puesto al Momento',
        help_text='Puesto del empleado al momento de la asignación'
    )
    departamento_al_momento = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        db_column='departamento_empleado',
        verbose_name='Departamento al Momento',
        help_text='Departamento del empleado al momento de la asignación'
    )

    class Meta:
        db_table = 'asignaciones'
        verbose_name = 'Asignación de Evaluación'
        verbose_name_plural = 'Asignaciones de Evaluación'
        ordering = ['asignacion_id']
        indexes = [
            models.Index(fields=['evaluacion']),
            models.Index(fields=['status']),
            models.Index(fields=['fecha_inicio']),
            models.Index(fields=['fecha_fin'])
        ]

    def clean(self):
        """Validaciones personalizadas"""
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio >= self.fecha_fin:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def esta_activa(self):
        """Indica si la asignación está actualmente activa"""
        now = timezone.now()
        return (self.status and
                self.fecha_inicio <= now <= self.fecha_fin)

    @property
    def total_empleados_asignados(self):
        """Número total de empleados asignados"""
        return self.asignaciones_empleado.count()

    def __str__(self):
        return f"{self.evaluacion.titulo} - Asignación #{self.asignacion_id}"


class AsignacionEmpleado(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Expirada', 'Expirada'),
    ]

    asignacion_empleado_id = models.AutoField(primary_key=True)
    asignacion = models.ForeignKey(
        'users.Asignacion', on_delete=models.CASCADE,
        db_column='asignacion_id',
        related_name='asignaciones_empleado',
        verbose_name='Asignación'
    )
    empleado = models.ForeignKey(
        'users.Empleado', on_delete=models.CASCADE,
        db_column='empleado_id',
        related_name='evaluaciones_asignadas',
        verbose_name='Empleado'
    )
    token_acceso = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True,
        verbose_name='Token de acceso',
        help_text='Token único para acceder a la evaluación'
    )
    status = models.CharField(
        max_length=16, choices=ESTADO_CHOICES,
        default='Pendiente', verbose_name='Estado'
    )
    fecha_inicio = models.DateTimeField(
        auto_now_add=True,
        db_column='fecha_asignacion',
        verbose_name="Fecha de Inicio",
        help_text="Fecha de asignación de la evaluación al empleado"
    )
    fecha_completado = models.DateTimeField(
        blank=True, null=True,
        verbose_name="Fecha de finalización"
    )

    class Meta:
        db_table = 'asignaciones_empleado'
        verbose_name = 'Asignación de Empleado'
        verbose_name_plural = 'Asignaciones de Empleado'
        ordering = ['asignacion_empleado_id']
        unique_together = [['asignacion', 'empleado'] ]

        indexes = [
            models.Index(fields=['asignacion']),
            models.Index(fields=['empleado']),
            models.Index(fields=['status'])
        ]

    @property
    def progreso_porcentaje(self):
        """Porcentaje de progreso en la evaluación"""
        total_preguntas = sum(
            seccion.total_preguntas
            for seccion in self.asignacion.evaluacion.secciones.all()
        )
        if total_preguntas == 0:
            return 0

        respuestas_dadas = self.respuestas.count()
        return round((respuestas_dadas / total_preguntas) * 100, 2)

    @property
    def esta_completada(self):
        """Indica si la evaluación está completada"""
        return self.status == 'Completada'

    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.asignacion.evaluacion.titulo} ({self.status})"

# ---------------------------------------------------------------------------- #

class RespuestaEmpleado(models.Model):
    respuesta_empleado_id = models.AutoField(primary_key=True)
    asignacion_empleado = models.ForeignKey(
        AsignacionEmpleado, on_delete=models.CASCADE,
        db_column='asignacion_empleado_id',
        related_name='respuestas',
        verbose_name='Asignación del empleado'
    )
    seccion_pregunta = models.ForeignKey(
        SeccionPregunta, on_delete=models.CASCADE,
        db_column='seccion_pregunta_id',
        verbose_name='Pregunta de la sección'
    )
    opcion_seleccionada = models.ForeignKey(
        PosiblesRespuestas, on_delete=models.SET_NULL,
        blank=True, null=True, db_column='opcion_seleccionada_id',
        verbose_name='Opción Seleccionada',
        help_text='Opción elegida de las opciones predefinidas'
    )
    respuesta_texto = models.TextField(
        blank=True, null=True,
        verbose_name='Respuesta de Texto',
        help_text='Respuesta libre para preguntas abiertas'
    )
    respuesta_valor_numerico = models.IntegerField(
        blank=True, null=True,
        verbose_name='Valor Numérico'
    )
    respuesta_valor_decimal = models.DecimalField(
        blank=True, null=True,
        max_digits=16, decimal_places=2,
        verbose_name='Valor Decimal'
    )

    # ! Olvidaste este campo.
    respuesta_valor_booleano = models.BooleanField(
        blank=True, null=True,
        verbose_name='Valor Booleano'
    )

    es_correcta = models.BooleanField(
        blank=True, null=True,
        verbose_name='¿Es correcta?',
        help_text='Indica si la respuesta es correcta (para evaluaciones calificables)'
    )

    # ! Olvidaste este campo.
    fecha_respuesta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha en que se registró la respuesta')

    class Meta:
        db_table = 'respuestas_empleado'
        verbose_name = 'Respuesta de Empleado'
        verbose_name_plural = 'Respuestas de Empleados'
        ordering = [ 'asignacion_empleado', 'respuesta_empleado_id' ]
        unique_together = [['asignacion_empleado', 'seccion_pregunta']]
        indexes = [
            models.Index(fields=['asignacion_empleado']),
            models.Index(fields=['seccion_pregunta'])
        ]

    def clean(self):
        """Validaciones personalizadas"""
        # Verificar que hay al menos una respuesta
        respuestas = [
            self.opcion_seleccionada,
            self.respuesta_texto,
            self.respuesta_valor_numerico,
            self.respuesta_valor_decimal
        ]
        if not any(respuesta for respuesta in respuestas):
            raise ValidationError("Debe proporcionar al menos una respuesta")

    def save(self, *args, **kwargs):
        # Verificar si es correcta automáticamente
        if (self.seccion_pregunta.respuesta_correcta and
            self.opcion_seleccionada == self.seccion_pregunta.respuesta_correcta):
            self.es_correcta = True

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        pregunta_corta = self.seccion_pregunta.pregunta.texto_pregunta[:30]
        if len(self.seccion_pregunta.pregunta.texto_pregunta) > 30:
            pregunta_corta += "..."
        return f"{self.asignacion_empleado.empleado.nombre_completo} - {pregunta_corta}"

# ---------------------------------------------------------------------------- #

class ResultadoEvaluacion(models.Model):
    resultado_id = models.AutoField(primary_key=True)
    asignacion_empleado = models.OneToOneField(
        AsignacionEmpleado, on_delete=models.CASCADE,
        unique=True, db_column='asignacion_empleado_id',
        related_name='resultado',
        verbose_name='Asignación del empleado'
    )

    # Para cuando se puede evaluar:
    puntaje_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        blank=True, null=True,
        verbose_name='Puntaje Total'
    )
    num_respuestas_correctas = models.IntegerField(
        default=0, verbose_name='Respuestas Correctas'
    )
    num_preguntas_evaluables = models.IntegerField(
        default=0, verbose_name='Preguntas Evaluables'
    )
    porcentaje_correctas = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        verbose_name='Porcentaje de Aciertos'
    )
    aprobado = models.BooleanField(
        blank=True, null=True,
        verbose_name='¿Aprobado?'
    )

    class Meta:
        db_table = 'resultados_evaluacion'
        verbose_name = 'Resultado de evaluación'
        verbose_name_plural = 'Resultados de evaluación'
        ordering = [ 'asignacion_empleado' ]
        indexes = [
            models.Index(fields=['asignacion_empleado']),
            models.Index(fields=['aprobado'])
        ]

    def clean(self):
        """Validaciones personalizadas"""
        if self.porcentaje_correctas and (self.porcentaje_correctas < 0 or self.porcentaje_correctas > 100):
            raise ValidationError("El porcentaje debe estar entre 0 y 100")

    def save(self, *args, **kwargs):
        if self.asignacion_empleado:
            self.evaluacion = self.asignacion_empleado.asignacion.evaluacion.titulo

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        empleado_nombre = self.asignacion_empleado.empleado.nombre_completo
        evaluacion_nombre = self.asignacion_empleado.asignacion.evaluacion.titulo
        return f"Resultado: {empleado_nombre} - {evaluacion_nombre}"

# ---------------------------------------------------------------------------- #
