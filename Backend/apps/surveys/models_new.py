# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa, Empleado
import uuid

class TipoEvaluacion(models.Model):
    """
    Tipos de evaluación: Normativa, Interna, 360 Grados
    Corresponde a TIPOS_EVALUACION en la BD
    """
    TIPOS_CHOICES = [
        ('normativa', 'Normativa'),
        ('interna', 'Interna'),
        ('360_grados', '360 Grados'),
    ]
    
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Evaluación'
        verbose_name_plural = 'Tipos de Evaluación'
        db_table = 'tipos_evaluacion'

class Evaluacion(models.Model):
    """
    Evaluaciones principales del sistema
    Corresponde a EVALUACIONES en la BD
    """
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]
    
    nombre = models.CharField(max_length=128, verbose_name="Título")
    descripcion = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Relaciones
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True,
                               help_text="Solo para evaluaciones internas y 360 grados")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluaciones_creadas')
    
    # Campos adicionales para compatibilidad con el frontend
    instrucciones = models.TextField(blank=True)
    tiempo_limite = models.IntegerField(null=True, blank=True, help_text="Tiempo límite en minutos")
    
    def __str__(self):
        return self.nombre
    
    @property
    def titulo(self):
        """Compatibilidad con el frontend"""
        return self.nombre
    
    @property
    def tipo(self):
        """Devuelve el tipo de evaluación como string"""
        tipo_map = {
            'Normativa': 'normativa',
            'Interna': 'interna',
            '360 Grados': '360_grados'
        }
        return tipo_map.get(self.tipo_evaluacion.nombre, 'interna')
    
    @property
    def tipo_display(self):
        return self.tipo_evaluacion.nombre
    
    @property
    def estado(self):
        """Compatibilidad con el frontend"""
        return 'activa' if self.status else 'inactiva'
        
    @property
    def estado_display(self):
        return 'Activa' if self.status else 'Inactiva'
    
    @property
    def creado_por_nombre(self):
        return f"{self.creado_por.first_name} {self.creado_por.last_name}".strip() or self.creado_por.username
    
    @property
    def empresa_nombre(self):
        return self.empresa.nombre if self.empresa else None
    
    @property
    def total_preguntas(self):
        return sum(seccion.preguntas.count() for seccion in self.secciones.all())
    
    @property
    def fecha_creacion(self):
        """Compatibilidad con el frontend"""
        return self.fecha_registro
    
    @property
    def fecha_actualizacion(self):
        """Compatibilidad con el frontend"""
        return self.fecha_registro

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        db_table = 'evaluaciones'

class SeccionEvaluacion(models.Model):
    """
    Secciones dentro de una evaluación
    Corresponde a SECCIONES_EVAL en la BD
    """
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    numero_orden = models.IntegerField()
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='secciones')
    
    def __str__(self):
        return f"{self.evaluacion.nombre} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Sección de Evaluación'
        verbose_name_plural = 'Secciones de Evaluación'
        ordering = ['numero_orden']
        db_table = 'secciones_eval'

class ConjuntoOpciones(models.Model):
    """
    Conjuntos de opciones para respuestas (ej: Escala Likert, Sí/No)
    Corresponde a CONJUNTOS_OPCIONES en la BD
    """
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True)
    predefinido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Conjunto de Opciones'
        verbose_name_plural = 'Conjuntos de Opciones'
        db_table = 'conjuntos_opciones'

class OpcionConjunto(models.Model):
    """
    Opciones específicas dentro de un conjunto
    Corresponde a OPCIONES_CONJUNTO en la BD
    """
    texto_opcion = models.CharField(max_length=256)
    valor_booleano = models.BooleanField(null=True, blank=True)
    valor_numerico = models.IntegerField(null=True, blank=True)
    puntuaje_escala = models.IntegerField(null=True, blank=True)
    numero_orden = models.IntegerField()
    conjunto_opciones = models.ForeignKey(ConjuntoOpciones, on_delete=models.CASCADE, related_name='opciones')
    
    def __str__(self):
        return self.texto_opcion
    
    class Meta:
        verbose_name = 'Opción de Conjunto'
        verbose_name_plural = 'Opciones de Conjunto'
        ordering = ['numero_orden']
        db_table = 'opciones_conjunto'

class Pregunta(models.Model):
    """
    Preguntas generales del sistema
    Corresponde a PREGUNTAS en la BD
    """
    TIPO_CHOICES = [
        ('Abierta', 'Abierta'),
        ('Múltiple', 'Múltiple'),
        ('Escala', 'Escala'),
        ('Bool', 'Bool'),
    ]
    
    texto_pregunta = models.TextField()
    tipo_pregunta = models.CharField(max_length=20, choices=TIPO_CHOICES)
    es_obligatoria = models.BooleanField(default=True)
    pregunta_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    activador_padre = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.texto_pregunta[:100]
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        db_table = 'preguntas'

class SeccionPregunta(models.Model):
    """
    Relación entre secciones y preguntas con sus opciones
    Corresponde a SECCION_PREGUNTAS en la BD
    """
    seccion = models.ForeignKey(SeccionEvaluacion, on_delete=models.CASCADE, related_name='preguntas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    conjunto_opciones = models.ForeignKey(ConjuntoOpciones, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Pregunta de Sección'
        verbose_name_plural = 'Preguntas de Sección'
        unique_together = ['seccion', 'pregunta']
        db_table = 'seccion_preguntas'

class AsignacionEvaluacion(models.Model):
    """
    Asignaciones de evaluaciones a empleados
    Corresponde a ASIGNACIONES en la BD
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Vencida', 'Vencida'),
    ]
    
    token_acceso = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asignaciones_evaluacion')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='asignaciones')
    evaluado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True, 
                                related_name='evaluaciones_recibidas')
    
    def __str__(self):
        return f"{self.empleado} - {self.evaluacion.nombre}"
    
    class Meta:
        verbose_name = 'Asignación de Evaluación'
        verbose_name_plural = 'Asignaciones de Evaluación'
        db_table = 'asignaciones'

class RespuestaEvaluacion(models.Model):
    """
    Respuestas de empleados a las evaluaciones
    Corresponde a RESPUESTAS en la BD
    """
    respuesta_abierta = models.TextField(null=True, blank=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(OpcionConjunto, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(AsignacionEvaluacion, on_delete=models.CASCADE, related_name='respuestas')
    
    def __str__(self):
        return f"{self.empleado} - {self.pregunta.texto_pregunta[:50]}"
    
    class Meta:
        verbose_name = 'Respuesta de Evaluación'
        verbose_name_plural = 'Respuestas de Evaluación'
        unique_together = ['evaluacion', 'pregunta']
        db_table = 'respuestas'

class ResultadoEvaluacion(models.Model):
    """
    Resultados finales de las evaluaciones
    Corresponde a RESULTADOS_EVAL en la BD
    """
    puntaje = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    asignacion = models.OneToOneField(AsignacionEvaluacion, on_delete=models.CASCADE, related_name='resultado')
    
    def __str__(self):
        return f"Resultado: {self.asignacion.empleado} - {self.asignacion.evaluacion.nombre}"
    
    class Meta:
        verbose_name = 'Resultado de Evaluación'
        verbose_name_plural = 'Resultados de Evaluación'
        db_table = 'resultados_eval'

# Modelo simplificado para el frontend (mantener compatibilidad)
class PreguntaEvaluacion(models.Model):
    """
    Modelo simplificado para compatibilidad con el frontend actual
    """
    TIPO_CHOICES = [
        ('texto', 'Texto libre'),
        ('multiple', 'Opción múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('escala', 'Escala numérica'),
        ('fecha', 'Fecha'),
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    orden = models.IntegerField()
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto')
    es_requerida = models.BooleanField(default=True)
    
    # Para preguntas de opción múltiple
    opciones = models.JSONField(default=list, blank=True)
    
    # Para preguntas de escala
    escala_min = models.IntegerField(null=True, blank=True)
    escala_max = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.evaluacion.titulo} - {self.texto[:50]}"
    
    class Meta:
        verbose_name = 'Pregunta de Evaluación'
        verbose_name_plural = 'Preguntas de Evaluación'
        ordering = ['orden']

class AplicacionEvaluacion(models.Model):
    """
    Modelo simplificado para compatibilidad con el frontend actual
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
        ('vencida', 'Vencida'),
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='aplicaciones')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='evaluaciones_aplicadas')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    token_acceso = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Para evaluaciones 360 grados
    evaluado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='evaluaciones_360_recibidas')
    
    def __str__(self):
        return f"{self.empleado} - {self.evaluacion.titulo}"
    
    class Meta:
        verbose_name = 'Aplicación de Evaluación'
        verbose_name_plural = 'Aplicaciones de Evaluación'
