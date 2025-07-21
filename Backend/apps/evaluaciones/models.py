# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa, Empleado, Departamento, Planta

class TipoEvaluacion(models.Model):
    """Tipos de evaluación: NOM-035, NOM-030, 360°"""
    TIPOS_EVALUACION = [
        ('NOM-035', 'NOM-035 - Factores de Riesgo Psicosocial'),
        ('NOM-030', 'NOM-030 - Servicios Preventivos de Seguridad'),
        ('360', 'Evaluación 360° - Competencias y Desempeño'),
    ]
    
    nombre = models.CharField(max_length=50, choices=TIPOS_EVALUACION, unique=True)
    descripcion = models.TextField()
    normativa_oficial = models.BooleanField(default=True)  # True para NOM, False para internas
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tipo de Evaluación"
        verbose_name_plural = "Tipos de Evaluación"
        
    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    """Preguntas para las evaluaciones"""
    TIPO_RESPUESTA = [
        ('multiple', 'Opción Múltiple'),
        ('escala', 'Escala Likert'),
        ('si_no', 'Sí/No'),
        ('texto', 'Texto Libre'),
    ]
    
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE, related_name='preguntas')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)  # Null para preguntas oficiales
    texto_pregunta = models.TextField()
    tipo_respuesta = models.CharField(max_length=20, choices=TIPO_RESPUESTA)
    opciones_respuesta = models.JSONField(default=list, blank=True)  # Para opciones múltiples
    es_obligatoria = models.BooleanField(default=True)
    orden = models.IntegerField(default=1)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ['tipo_evaluacion', 'orden']
        
    def __str__(self):
        return f"{self.tipo_evaluacion.nombre} - {self.texto_pregunta[:50]}..."

class EvaluacionCompleta(models.Model):
    """Evaluaciones completas creadas por las empresas"""
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='evaluaciones_nuevas', null=True, blank=True)
    preguntas = models.ManyToManyField(Pregunta, through='EvaluacionPregunta')
    
    # Configuración de alcance
    plantas = models.ManyToManyField(Planta, blank=True)
    departamentos = models.ManyToManyField(Departamento, blank=True)
    empleados_objetivo = models.ManyToManyField(Empleado, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    es_anonima = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        
    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre}"

class EvaluacionPregunta(models.Model):
    """Tabla intermedia para preguntas en evaluaciones"""
    evaluacion = models.ForeignKey(EvaluacionCompleta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    orden = models.IntegerField()
    es_obligatoria = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['evaluacion', 'pregunta']
        ordering = ['orden']

class RespuestaEvaluacion(models.Model):
    """Respuestas de los empleados a las evaluaciones"""
    evaluacion = models.ForeignKey(EvaluacionCompleta, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)  # Null si es anónima
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)
    tiempo_completado = models.IntegerField(null=True, blank=True)  # minutos
    
    class Meta:
        unique_together = ['evaluacion', 'empleado']
        verbose_name = "Respuesta a Evaluación"
        verbose_name_plural = "Respuestas a Evaluaciones"
        
    def __str__(self):
        empleado_nombre = self.empleado.nombre if self.empleado else "Anónimo"
        return f"{self.evaluacion.titulo} - {empleado_nombre}"

class DetalleRespuesta(models.Model):
    """Respuestas específicas a cada pregunta"""
    respuesta_evaluacion = models.ForeignKey(RespuestaEvaluacion, on_delete=models.CASCADE, related_name='detalles')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta_texto = models.TextField(blank=True)
    respuesta_numerica = models.IntegerField(null=True, blank=True)
    respuesta_multiple = models.JSONField(default=list, blank=True)
    
    class Meta:
        unique_together = ['respuesta_evaluacion', 'pregunta']
        verbose_name = "Detalle de Respuesta"
        verbose_name_plural = "Detalles de Respuestas"

class ResultadoEvaluacion(models.Model):
    """Resultados consolidados de las evaluaciones"""
    evaluacion = models.ForeignKey(EvaluacionCompleta, on_delete=models.CASCADE)
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    total_respuestas = models.IntegerField()
    porcentaje_participacion = models.DecimalField(max_digits=5, decimal_places=2)
    puntuacion_promedio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resultados_detallados = models.JSONField(default=dict)  # Resultados por pregunta/categoría
    recomendaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Resultado de Evaluación"
        verbose_name_plural = "Resultados de Evaluaciones"
        
    def __str__(self):
        return f"Resultados - {self.evaluacion.titulo}"

class AsignacionEvaluacion(models.Model):
    """Asignación de evaluaciones a empleados específicos"""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('expirada', 'Expirada'),
        ('cancelada', 'Cancelada'),
    ]
    
    evaluacion = models.ForeignKey(EvaluacionCompleta, on_delete=models.CASCADE, related_name='asignaciones')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='evaluaciones_asignadas')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    asignado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    # Nuevos campos para duración y seguimiento
    duracion_dias = models.IntegerField(null=True, blank=True, help_text="Duración máxima en días para completar")
    duracion_horas = models.IntegerField(null=True, blank=True, help_text="Tiempo estimado en horas para responder")
    instrucciones_especiales = models.TextField(null=True, blank=True, help_text="Instrucciones adicionales")
    fecha_ultimo_acceso = models.DateTimeField(null=True, blank=True, help_text="Último acceso del empleado")
    intentos_acceso = models.IntegerField(default=0, help_text="Número de veces que ha accedido")
    
    class Meta:
        unique_together = ['evaluacion', 'empleado']
        verbose_name = "Asignación de Evaluación"
        verbose_name_plural = "Asignaciones de Evaluaciones"
        
    def __str__(self):
        return f"{self.evaluacion.titulo} - {self.empleado.nombre}"
    
    @property
    def dias_restantes(self):
        """Calcular días restantes para completar"""
        from django.utils import timezone
        if self.estado in ['completada', 'expirada', 'cancelada']:
            return 0
        dias = (self.fecha_fin - timezone.now()).days
        return max(0, dias)
    
    @property
    def porcentaje_tiempo_usado(self):
        """Porcentaje del tiempo total que ya ha pasado"""
        from django.utils import timezone
        total_tiempo = (self.fecha_fin - self.fecha_inicio).total_seconds()
        tiempo_usado = (timezone.now() - self.fecha_inicio).total_seconds()
        return min(100, max(0, (tiempo_usado / total_tiempo) * 100))

class TokenEvaluacion(models.Model):
    """Tokens únicos para acceso de empleados a evaluaciones"""
    asignacion = models.OneToOneField(AsignacionEvaluacion, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)
    usado = models.BooleanField(default=False)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    ip_acceso = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Token de Evaluación"
        verbose_name_plural = "Tokens de Evaluaciones"
        
    def __str__(self):
        return f"Token - {self.asignacion.empleado.nombre} - {self.token[:10]}..."
