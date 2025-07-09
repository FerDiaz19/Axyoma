from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa, Planta, Empleado
from datetime import datetime, timedelta
from django.utils import timezone

class Evaluacion(models.Model):
    """
    Modelo para evaluaciones que pueden ser de dos tipos:
    - Normativas: Creadas por SuperAdmin, visibles y aplicables por todas las empresas
    - Internas: Creadas por AdminEmpresa/AdminPlanta, solo visibles en su empresa
    """
    TIPO_EVALUACION_CHOICES = [
        ('normativa', 'Normativa'),
        ('interna', 'Interna'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]
    
    # Información básica
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_EVALUACION_CHOICES, default='interna')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Relaciones
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluaciones_creadas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, 
                               help_text="Solo para evaluaciones internas")
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True,
                              help_text="Solo para evaluaciones internas de planta específica")
    
    # Configuración de la evaluación
    instrucciones = models.TextField(blank=True, verbose_name="Instrucciones")
    tiempo_limite = models.PositiveIntegerField(null=True, blank=True, 
                                              help_text="Tiempo límite en minutos")
    
    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
    
    @property
    def tipo_display(self):
        return self.get_tipo_display()
        
    @property
    def estado_display(self):
        return self.get_estado_display()
    
    @property
    def creado_por_nombre(self):
        return f"{self.creado_por.first_name} {self.creado_por.last_name}".strip() or self.creado_por.username
    
    @property
    def empresa_nombre(self):
        return self.empresa.nombre if self.empresa else None
    
    @property
    def planta_nombre(self):
        return self.planta.nombre if self.planta else None
    
    @property
    def total_preguntas(self):
        return self.preguntas.count()
    
    def is_normativa(self):
        return self.tipo == 'normativa'
        return self.tipo == 'normativa'
    
    def is_interna(self):
        return self.tipo == 'interna'
    
    def can_user_edit(self, user):
        """
        Determina si un usuario puede editar esta evaluación
        """
        if user.is_superuser:
            return self.is_normativa()
        
        if hasattr(user, 'perfil'):
            perfil = user.perfil
            if perfil.nivel_usuario in ['admin-empresa', 'admin-planta']:
                return self.is_interna() and self.empresa == perfil.administrador_empresa
        
        return False
    
    def can_user_view(self, user):
        """
        Determina si un usuario puede ver esta evaluación
        """
        if user.is_superuser:
            return True
        
        if hasattr(user, 'perfil'):
            perfil = user.perfil
            if perfil.nivel_usuario in ['admin-empresa', 'admin-planta']:
                return (self.is_normativa() or 
                       (self.is_interna() and self.empresa == perfil.administrador_empresa))
        
        return False

class PreguntaEvaluacion(models.Model):
    """
    Preguntas que forman parte de una evaluación
    """
    TIPO_PREGUNTA_CHOICES = [
        ('texto', 'Texto libre'),
        ('multiple', 'Opción múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('escala', 'Escala numérica'),
        ('fecha', 'Fecha'),
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    orden = models.PositiveIntegerField(default=1)
    texto = models.TextField(verbose_name="Texto de la pregunta")
    tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA_CHOICES)
    es_requerida = models.BooleanField(default=True)
    
    # Para preguntas de opción múltiple
    opciones = models.JSONField(default=list, blank=True, 
                               help_text="Lista de opciones para preguntas múltiples")
    
    # Para preguntas de escala
    escala_min = models.IntegerField(null=True, blank=True)
    escala_max = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Pregunta de Evaluación"
        verbose_name_plural = "Preguntas de Evaluación"
        ordering = ['orden']
        
    def __str__(self):
        return f"{self.evaluacion.titulo} - Pregunta {self.orden}"

class AplicacionEvaluacion(models.Model):
    """
    Registro de cuando se aplica una evaluación a empleados
    """
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='aplicaciones')
    empleados = models.ManyToManyField(Empleado, related_name='evaluaciones_aplicadas')
    
    # Fechas
    fecha_programada = models.DateTimeField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    
    # Metadatos
    aplicada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Aplicación de Evaluación"
        verbose_name_plural = "Aplicaciones de Evaluación"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.evaluacion.titulo} - {self.fecha_programada.strftime('%d/%m/%Y')}"

class RespuestaEvaluacion(models.Model):
    """
    Respuestas individuales de empleados a evaluaciones
    """
    aplicacion = models.ForeignKey(AplicacionEvaluacion, on_delete=models.CASCADE, related_name='respuestas')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaEvaluacion, on_delete=models.CASCADE)
    
    # Diferentes tipos de respuesta
    respuesta_texto = models.TextField(blank=True)
    respuesta_numero = models.IntegerField(null=True, blank=True)
    respuesta_fecha = models.DateField(null=True, blank=True)
    respuesta_multiple = models.CharField(max_length=500, blank=True)
    
    # Metadatos
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Respuesta de Evaluación"
        verbose_name_plural = "Respuestas de Evaluación"
        unique_together = ['aplicacion', 'empleado', 'pregunta']
        
    def __str__(self):
        return f"{self.empleado} - {self.pregunta.evaluacion.titulo}"