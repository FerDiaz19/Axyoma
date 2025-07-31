# -*- coding: utf-8 -*-
"""
MODELOS AXYOMA - VERSIÓN DEFINITIVA
=================================
Diseño robusto y consistente para evitar errores de dependencias.
Estructura optimizada para respaldos, restauración e inserción de datos.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

# =============================================================================
# SISTEMA DE USUARIOS Y AUTENTICACIÓN
# =============================================================================

class PerfilUsuario(models.Model):
    """
    Perfil de usuario unificado que extiende Django User.
    Tabla principal: usuarios
    """
    NIVEL_CHOICES = [
        ('superadmin', 'Super Administrador'),
        ('admin-empresa', 'Administrador de Empresa'),
        ('admin-planta', 'Administrador de Planta'),
    ]
    
    # Campos principales
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido Materno")
    correo = models.EmailField(max_length=255, unique=True, verbose_name="Correo Electrónico")
    nivel_usuario = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nivel de Usuario")
    status = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relación jerárquica (admin-planta pertenece a admin-empresa)
    admin_empresa = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='admin_empresa',
        verbose_name="Administrador de Empresa",
        help_text="Para admin-planta: especifica a qué admin-empresa pertenece"
    )
    
    # Relación con Django User (obligatoria y única)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='perfil',
        verbose_name="Usuario Django"
    )
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['nombre', 'apellido_paterno']
        indexes = [
            models.Index(fields=['nivel_usuario']),
            models.Index(fields=['correo']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.nivel_usuario == 'admin-planta' and not self.admin_empresa:
            raise ValidationError("Admin de planta debe tener un admin de empresa asignado")
        if self.nivel_usuario == 'superadmin' and self.admin_empresa:
            raise ValidationError("SuperAdmin no puede tener admin de empresa")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def nombre_completo(self):
        """Nombre completo formateado"""
        nombres = [self.nombre, self.apellido_paterno]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.get_nivel_usuario_display()})"

# =============================================================================
# SISTEMA DE EMPRESAS Y ORGANIZACIONES
# =============================================================================

class Empresa(models.Model):
    """
    Empresa registrada en el sistema.
    Tabla principal: empresas
    """
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=65, unique=True, verbose_name="Nombre de la Empresa")
    rfc = models.CharField(max_length=16, unique=True, verbose_name="RFC")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    logotipo = models.URLField(max_length=255, blank=True, null=True, verbose_name="URL del Logotipo")
    email_contacto = models.EmailField(max_length=128, blank=True, null=True, verbose_name="Email de Contacto")
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono de Contacto")
    status = models.BooleanField(default=True, verbose_name="Activa")
    
    # Relación con administrador (debe ser admin-empresa)
    administrador = models.OneToOneField(
        PerfilUsuario, 
        on_delete=models.PROTECT,  # Cambio a PROTECT para evitar eliminaciones accidentales
        db_column='administrador',
        verbose_name="Administrador de la Empresa",
        limit_choices_to={'nivel_usuario': 'admin-empresa'}
    )
    
    class Meta:
        db_table = 'empresas'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['rfc']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.administrador and self.administrador.nivel_usuario != 'admin-empresa':
            raise ValidationError("El administrador debe ser de nivel 'admin-empresa'")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def tiene_suscripcion_activa(self):
        """Verifica si la empresa tiene una suscripción activa"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa
            return SuscripcionEmpresa.objects.filter(
                empresa=self,
                estado='activa'
            ).exists()
        except ImportError:
            return False
    
    @property
    def suscripcion_activa(self):
        """Obtiene la suscripción activa más reciente"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa
            return SuscripcionEmpresa.objects.filter(
                empresa=self,
                estado='activa'
            ).order_by('-fecha_inicio').first()
        except ImportError:
            return None
    
    @property
    def total_plantas(self):
        """Número total de plantas"""
        return self.plantas.filter(status=True).count()
    
    @property
    def total_empleados(self):
        """Número total de empleados activos"""
        return sum(planta.total_empleados for planta in self.plantas.filter(status=True))
    
    def __str__(self):
        return self.nombre


class Planta(models.Model):
    """
    Planta o sucursal de una empresa.
    Tabla principal: plantas
    """
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre de la Planta")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    status = models.BooleanField(default=True, verbose_name="Activa")
    
    # Relación con empresa
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        db_column='empresa',
        related_name='plantas',
        verbose_name="Empresa"
    )
    
    class Meta:
        db_table = 'plantas'
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        ordering = ['empresa', 'nombre']
        unique_together = [['empresa', 'nombre']]  # Nombre único por empresa
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['status']),
        ]
    
    @property
    def total_departamentos(self):
        """Número total de departamentos activos"""
        return self.departamentos.filter(status=True).count()
    
    @property
    def total_empleados(self):
        """Número total de empleados activos en la planta"""
        return sum(depto.total_empleados for depto in self.departamentos.filter(status=True))
    
    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"


class Departamento(models.Model):
    """
    Departamento dentro de una planta.
    Tabla principal: departamentos
    """
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre del Departamento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    status = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relación con planta
    planta = models.ForeignKey(
        Planta, 
        on_delete=models.CASCADE, 
        db_column='planta',
        related_name='departamentos',
        verbose_name="Planta"
    )
    
    class Meta:
        db_table = 'departamentos'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['planta', 'nombre']
        unique_together = [['planta', 'nombre']]  # Nombre único por planta
        indexes = [
            models.Index(fields=['planta']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.nombre:
            self.nombre = self.nombre.strip()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def total_puestos(self):
        """Número total de puestos activos"""
        return self.puestos.filter(status=True).count()
    
    @property
    def total_empleados(self):
        """Número total de empleados activos en el departamento"""
        return sum(puesto.total_empleados for puesto in self.puestos.filter(status=True))
    
    def __str__(self):
        return f"{self.nombre} - {self.planta.nombre}"


class Puesto(models.Model):
    """
    Puesto de trabajo dentro de un departamento.
    Tabla principal: puestos
    """
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre del Puesto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    status = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relación con departamento
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        db_column='departamento',
        related_name='puestos',
        verbose_name="Departamento"
    )
    
    class Meta:
        db_table = 'puestos'
        verbose_name = "Puesto"
        verbose_name_plural = "Puestos"
        ordering = ['departamento', 'nombre']
        unique_together = [['departamento', 'nombre']]  # Nombre único por departamento
        indexes = [
            models.Index(fields=['departamento']),
            models.Index(fields=['status']),
        ]
    
    @property
    def total_empleados(self):
        """Número total de empleados activos en el puesto"""
        return self.empleados.filter(status=True).count()
    
    @property
    def empresa(self):
        """Empresa a la que pertenece el puesto"""
        return self.departamento.planta.empresa
    
    @property
    def planta(self):
        """Planta a la que pertenece el puesto"""
        return self.departamento.planta
    
    def __str__(self):
        return f"{self.nombre} - {self.departamento.nombre}"


class Empleado(models.Model):
    """
    Empleado asignado a un puesto específico.
    Tabla principal: empleados
    """
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido Materno")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de Ingreso")
    status = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relación con puesto
    puesto = models.ForeignKey(
        Puesto, 
        on_delete=models.CASCADE, 
        db_column='puesto',
        related_name='empleados',
        verbose_name="Puesto"
    )
    
    class Meta:
        db_table = 'empleados'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellido_paterno', 'nombre']
        indexes = [
            models.Index(fields=['puesto']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'], 
                condition=models.Q(email__isnull=False) & ~models.Q(email=''),
                name='unique_employee_email'
            )
        ]
    
    @property
    def nombre_completo(self):
        """Nombre completo formateado"""
        nombres = [self.nombre, self.apellido_paterno]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)
    
    @property
    def empresa(self):
        """Empresa a la que pertenece el empleado"""
        return self.puesto.empresa
    
    @property
    def planta(self):
        """Planta a la que pertenece el empleado"""
        return self.puesto.planta
    
    @property
    def departamento(self):
        """Departamento al que pertenece el empleado"""
        return self.puesto.departamento
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.puesto.nombre}"


class AdminPlanta(models.Model):
    """
    Tabla intermedia para administradores de plantas.
    Tabla principal: admin_plantas
    """
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.CASCADE, 
        db_column='usuario_id',
        limit_choices_to={'nivel_usuario': 'admin-planta'},
        verbose_name="Usuario Admin Planta"
    )
    planta = models.ForeignKey(
        Planta, 
        on_delete=models.CASCADE, 
        db_column='planta_id',
        verbose_name="Planta Asignada"
    )
    status = models.BooleanField(default=True, verbose_name="Activo")
    password_temporal = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        verbose_name="Contraseña Temporal",
        help_text="Contraseña temporal generada automáticamente"
    )
    
    class Meta:
        db_table = 'admin_plantas'
        verbose_name = "Administrador de Planta"
        verbose_name_plural = "Administradores de Plantas"
        unique_together = [['usuario', 'planta']]
        ordering = ['planta', 'usuario']
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['planta']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.usuario and self.usuario.nivel_usuario != 'admin-planta':
            raise ValidationError("El usuario debe ser de nivel 'admin-planta'")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.planta.nombre}"


# =============================================================================
# SISTEMA DE EVALUACIONES - MODELOS PRINCIPALES
# =============================================================================

class TipoEvaluacion(models.Model):
    """
    Tipos de evaluación disponibles en el sistema.
    Tabla principal: tipos_evaluacion
    """
    tipo_evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=32, 
        unique=True,
        verbose_name='Nombre', 
        help_text='Nombre del tipo de evaluación (ej: Normativa, Interna, 360 Grados)'
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción', 
        help_text='Descripción detallada del tipo de evaluación'
    )

    class Meta:
        db_table = 'tipos_evaluacion'
        verbose_name = 'Tipo de Evaluación'
        verbose_name_plural = 'Tipos de Evaluación'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.nombre


class Evaluacion(models.Model):
    """
    Evaluaciones disponibles en el sistema.
    Tabla principal: evaluaciones
    """
    evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=128,
        verbose_name='Nombre', 
        help_text='Nombre de la evaluación'
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción', 
        help_text='Descripción de la evaluación'
    )
    instrucciones = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Instrucciones', 
        help_text='Instrucciones para completar la evaluación'
    )
    tiempo_limite = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Tiempo Límite (min)', 
        help_text='Tiempo máximo en minutos para completar la evaluación'
    )
    umbral_aprobacion = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Umbral de Aprobación (%)', 
        help_text='Porcentaje mínimo para aprobar (ej: 70)'
    )
    status = models.BooleanField(default=True, verbose_name="Activa")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # Relaciones
    tipo_evaluacion = models.ForeignKey(
        TipoEvaluacion, 
        on_delete=models.PROTECT,
        verbose_name='Tipo de Evaluación',
        help_text='Tipo de evaluación al que pertenece'
    )
    empresa = models.ForeignKey(
        Empresa, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        verbose_name='Empresa', 
        help_text='Empresa propietaria (NULL para evaluaciones normativas)'
    )
    creado_por = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Creado por', 
        help_text='Usuario que creó la evaluación'
    )

    class Meta:
        db_table = 'evaluaciones'
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['evaluacion_id']
        indexes = [
            models.Index(fields=['tipo_evaluacion']),
            models.Index(fields=['empresa']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        """Validaciones personalizadas"""
        if self.umbral_aprobacion and (self.umbral_aprobacion < 0 or self.umbral_aprobacion > 100):
            raise ValidationError("El umbral de aprobación debe estar entre 0 y 100")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def es_normativa(self):
        """Indica si es una evaluación normativa"""
        return self.tipo_evaluacion.nombre.lower() == 'normativa'

    @property
    def total_secciones(self):
        """Número total de secciones"""
        return self.secciones.count()

    def __str__(self):
        return f"{self.nombre} ({self.tipo_evaluacion.nombre})"


class SeccionEval(models.Model):
    """
    Secciones que organizan las preguntas dentro de una evaluación.
    Tabla principal: secciones_eval
    """
    seccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=255,
        verbose_name='Nombre', 
        help_text='Nombre de la sección'
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción', 
        help_text='Descripción de la sección'
    )
    numero_orden = models.IntegerField(
        verbose_name='Orden', 
        help_text='Número de orden dentro de la evaluación'
    )
    es_evaluable = models.BooleanField(
        default=True, 
        verbose_name='¿Es evaluable?', 
        help_text='Define si las preguntas de esta sección se califican'
    )

    # Relación con evaluación
    evaluacion = models.ForeignKey(
        Evaluacion, 
        on_delete=models.CASCADE,
        related_name='secciones',
        verbose_name='Evaluación', 
        help_text='Evaluación a la que pertenece esta sección'
    )

    class Meta:
        db_table = 'secciones_eval'
        verbose_name = 'Sección de Evaluación'
        verbose_name_plural = 'Secciones de Evaluación'
        ordering = ['evaluacion', 'numero_orden']
        unique_together = [['evaluacion', 'numero_orden']]
        indexes = [
            models.Index(fields=['evaluacion']),
            models.Index(fields=['numero_orden']),
        ]

    @property
    def total_preguntas(self):
        """Número total de preguntas en la sección"""
        return self.preguntas_seccion.count()

    def __str__(self):
        return f"{self.nombre} ({self.evaluacion.nombre})"


class Pregunta(models.Model):
    """
    Preguntas reutilizables del sistema.
    Tabla principal: preguntas
    """
    TIPO_CHOICES = [
        ('Abierta', 'Pregunta Abierta'),
        ('Múltiple', 'Opción Múltiple'),
        ('Escala', 'Escala de Calificación'),
        ('Bool', 'Sí/No'),
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

    # Preguntas condicionales
    pregunta_padre = models.ForeignKey(
        'self', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE,
        db_column='pregunta_padre', 
        related_name='preguntas_hijas',
        verbose_name='Pregunta Padre', 
        help_text='Pregunta de la cual depende esta pregunta'
    )
    activador_padre = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
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
            models.Index(fields=['pregunta_padre']),
        ]

    def __str__(self):
        texto_corto = self.texto_pregunta[:50]
        if len(self.texto_pregunta) > 50:
            texto_corto += "..."
        return f"{texto_corto} ({self.get_tipo_pregunta_display()})"


class ConjuntoRespuestas(models.Model):
    """
    Conjuntos de opciones de respuesta reutilizables.
    Tabla principal: conjunto_respuestas
    """
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
        db_table = 'conjuntos_opciones'
        verbose_name = 'Conjunto de Respuestas'
        verbose_name_plural = 'Conjuntos de Respuestas'
        ordering = ['predefinido', 'nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['predefinido']),
        ]

    @property
    def total_opciones(self):
        """Número total de opciones en el conjunto"""
        return self.opciones.count()

    def __str__(self):
        return self.nombre


class PosiblesRespuestas(models.Model):
    """
    Opciones específicas dentro de cada conjunto de respuestas.
    Tabla principal: opciones_conjunto
    """
    opcion_conjunto_id = models.AutoField(primary_key=True)
    texto_opcion = models.CharField(
        max_length=256,
        verbose_name='Opción', 
        help_text='Texto de la opción de respuesta'
    )

    # Valores asociados a la opción
    valor_booleano = models.BooleanField(
        blank=True, 
        null=True,
        verbose_name='Valor Booleano', 
        help_text='Valor verdadero/falso asociado'
    )
    valor_numerico = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Valor Numérico', 
        help_text='Valor numérico entero asociado'
    )
    puntuaje_escala = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Puntaje de Escala', 
        help_text='Puntaje en escala asociado'
    )

    # Orden dentro del conjunto
    numero_orden = models.IntegerField(
        verbose_name='Orden', 
        help_text='Orden de la opción dentro del conjunto'
    )

    # Relación con conjunto
    conjunto_respuestas = models.ForeignKey(
        ConjuntoRespuestas, 
        on_delete=models.CASCADE,
        db_column='conjunto_opciones', 
        related_name='opciones',
        verbose_name='Conjunto de Respuestas'
    )

    class Meta:
        db_table = 'opciones_conjunto'
        verbose_name = 'Opción de Respuesta'
        verbose_name_plural = 'Opciones de Respuesta'
        ordering = ['conjunto_respuestas', 'numero_orden']
        unique_together = [['conjunto_respuestas', 'numero_orden']]
        indexes = [
            models.Index(fields=['conjunto_respuestas']),
            models.Index(fields=['numero_orden']),
        ]

    def __str__(self):
        return f"{self.texto_opcion} ({self.conjunto_respuestas.nombre})"


class SeccionPregunta(models.Model):
    """
    Relación entre secciones y preguntas con sus opciones de respuesta.
    Tabla principal: seccion_preguntas
    """
    seccion_pregunta_id = models.AutoField(primary_key=True)

    # Relaciones principales
    seccion = models.ForeignKey(
        SeccionEval, 
        on_delete=models.CASCADE,
        related_name='preguntas_seccion', 
        verbose_name='Sección'
    )
    pregunta = models.ForeignKey(
        Pregunta, 
        on_delete=models.CASCADE, 
        related_name='secciones_pregunta',
        verbose_name='Pregunta'
    )

    # Opciones de respuesta
    conjunto_respuestas = models.ForeignKey(
        ConjuntoRespuestas, 
        blank=True, 
        null=True,
        on_delete=models.SET_NULL, 
        verbose_name='Conjunto de Respuestas',
        help_text='Conjunto de opciones para esta pregunta'
    )
    respuesta_correcta = models.ForeignKey(
        PosiblesRespuestas, 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True, 
        related_name='preguntas_con_respuesta_correcta',
        verbose_name='Respuesta Correcta', 
        help_text='Opción correcta para evaluaciones calificables'
    )

    # Orden dentro de la sección
    numero_orden = models.IntegerField(
        verbose_name='Orden en la Sección', 
        help_text='Orden de la pregunta dentro de la sección'
    )

    class Meta:
        db_table = 'seccion_preguntas'
        verbose_name = 'Pregunta de Sección'
        verbose_name_plural = 'Preguntas de Sección'
        ordering = ['seccion', 'numero_orden']
        unique_together = [
            ['seccion', 'pregunta'],
            ['seccion', 'numero_orden']
        ]
        indexes = [
            models.Index(fields=['seccion']),
            models.Index(fields=['pregunta']),
            models.Index(fields=['numero_orden']),
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

# =============================================================================
# SISTEMA DE ASIGNACIONES Y RESPUESTAS
# =============================================================================

class Asignacion(models.Model):
    """
    Asignación de evaluaciones a empleados o grupos.
    Tabla principal: asignaciones
    """
    asignacion_id = models.AutoField(primary_key=True)
    evaluacion = models.ForeignKey(
        Evaluacion, 
        on_delete=models.PROTECT,
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
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # Para evaluaciones 360 grados
    empleado_evaluado = models.ForeignKey(
        Empleado, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='evaluaciones_360_asignadas', 
        verbose_name='Empleado Evaluado',
        help_text='Empleado sujeto de evaluación 360 grados'
    )
    puesto_al_momento = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
        verbose_name='Puesto al Momento', 
        help_text='Puesto del empleado al momento de la asignación'
    )
    departamento_al_momento = models.CharField(
        max_length=128, 
        blank=True, 
        null=True,
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
            models.Index(fields=['fecha_fin']),
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
        return f"{self.evaluacion.nombre} - Asignación #{self.asignacion_id}"


class AsignacionEmpleado(models.Model):
    """
    Asignación específica de una evaluación a un empleado individual.
    Tabla principal: asignaciones_empleado
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completada', 'Completada'),
        ('Expirada', 'Expirada'),
    ]

    asignacion_empleado_id = models.AutoField(primary_key=True)
    asignacion = models.ForeignKey(
        Asignacion, 
        on_delete=models.CASCADE,
        related_name='asignaciones_empleado',
        verbose_name='Asignación'
    )
    empleado = models.ForeignKey(
        Empleado, 
        on_delete=models.CASCADE,
        related_name='evaluaciones_asignadas',
        verbose_name='Empleado'
    )
    token_acceso = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        verbose_name='Token de Acceso', 
        help_text='Token único para acceder a la evaluación'
    )
    status = models.CharField(
        max_length=16, 
        choices=ESTADO_CHOICES, 
        default='Pendiente',
        verbose_name='Estado'
    )
    fecha_inicio = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Fecha de Inicio",
        help_text="Cuando el empleado comenzó la evaluación"
    )
    fecha_completado = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Fecha de Finalización"
    )

    class Meta:
        db_table = 'asignaciones_empleado'
        verbose_name = 'Asignación de Empleado'
        verbose_name_plural = 'Asignaciones de Empleado'
        ordering = ['asignacion_empleado_id']
        unique_together = [['asignacion', 'empleado']]
        indexes = [
            models.Index(fields=['asignacion']),
            models.Index(fields=['empleado']),
            models.Index(fields=['status']),
            models.Index(fields=['token_acceso']),
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
        return f"{self.empleado.nombre_completo} - {self.asignacion.evaluacion.nombre} ({self.status})"


class RespuestaEmpleado(models.Model):
    """
    Respuestas individuales de empleados a preguntas específicas.
    Tabla principal: respuestas_empleado
    """
    respuesta_empleado_id = models.AutoField(primary_key=True)
    asignacion_empleado = models.ForeignKey(
        AsignacionEmpleado, 
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Asignación del Empleado'
    )
    seccion_pregunta = models.ForeignKey(
        SeccionPregunta, 
        on_delete=models.CASCADE,
        verbose_name='Pregunta de la Sección'
    )

    # Diferentes tipos de respuesta
    opcion_seleccionada = models.ForeignKey(
        PosiblesRespuestas, 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True, 
        verbose_name='Opción Seleccionada',
        help_text='Opción elegida de las opciones predefinidas'
    )
    respuesta_texto = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Respuesta de Texto', 
        help_text='Respuesta libre para preguntas abiertas'
    )
    respuesta_valor_numerico = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Valor Numérico'
    )
    respuesta_valor_decimal = models.DecimalField(
        blank=True, 
        null=True, 
        max_digits=16, 
        decimal_places=2,
        verbose_name='Valor Decimal'
    )

    # Metadatos de la respuesta
    es_correcta = models.BooleanField(
        default=False,
        verbose_name='¿Es Correcta?', 
        help_text='Indica si la respuesta es correcta (para evaluaciones calificables)'
    )

    class Meta:
        db_table = 'respuestas_empleado'
        verbose_name = 'Respuesta de Empleado'
        verbose_name_plural = 'Respuestas de Empleados'
        ordering = ['asignacion_empleado', 'respuesta_empleado_id']
        unique_together = [['asignacion_empleado', 'seccion_pregunta']]
        indexes = [
            models.Index(fields=['asignacion_empleado']),
            models.Index(fields=['seccion_pregunta']),
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


class ResultadoEvaluacion(models.Model):
    """
    Resultados finales de evaluaciones completadas.
    Tabla principal: resultados_evaluacion
    """
    resultado_id = models.AutoField(primary_key=True)
    asignacion_empleado = models.OneToOneField(
        AsignacionEmpleado, 
        on_delete=models.CASCADE, 
        unique=True,
        related_name='resultado',
        verbose_name='Asignación del Empleado'
    )

    # Puntajes y estadísticas
    puntaje_total = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name='Puntaje Total'
    )
    num_respuestas_correctas = models.IntegerField(
        default=0,
        verbose_name='Respuestas Correctas'
    )
    num_preguntas_evaluables = models.IntegerField(
        default=0,
        verbose_name='Preguntas Evaluables'
    )
    porcentaje_correctas = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name='Porcentaje de Aciertos'
    )
    aprobado = models.BooleanField(
        blank=True, 
        null=True,
        verbose_name='¿Aprobado?'
    )

    # Metadatos
    observaciones = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Observaciones'
    )

    class Meta:
        db_table = 'resultados_evaluacion'
        verbose_name = 'Resultado de Evaluación'
        verbose_name_plural = 'Resultados de Evaluación'
        ordering = ['resultado_id']
        indexes = [
            models.Index(fields=['asignacion_empleado']),
            models.Index(fields=['aprobado']),
        ]

    def clean(self):
        """Validaciones personalizadas"""
        if self.porcentaje_correctas and (self.porcentaje_correctas < 0 or self.porcentaje_correctas > 100):
            raise ValidationError("El porcentaje debe estar entre 0 y 100")

    def save(self, *args, **kwargs):
        # Calcular automáticamente el porcentaje si no está establecido
        if self.num_preguntas_evaluables > 0 and self.porcentaje_correctas is None:
            self.porcentaje_correctas = round(
                (self.num_respuestas_correctas / self.num_preguntas_evaluables) * 100, 
                2
            )
        
        # Determinar si aprobó
        if (self.porcentaje_correctas is not None and 
            self.asignacion_empleado.asignacion.evaluacion.umbral_aprobacion):
            self.aprobado = self.porcentaje_correctas >= self.asignacion_empleado.asignacion.evaluacion.umbral_aprobacion
        
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        empleado_nombre = self.asignacion_empleado.empleado.nombre_completo
        evaluacion_nombre = self.asignacion_empleado.asignacion.evaluacion.nombre
        return f"Resultado: {empleado_nombre} - {evaluacion_nombre}"
