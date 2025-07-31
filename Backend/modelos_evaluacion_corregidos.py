# MODELOS DE EVALUACIÓN CORREGIDOS PARA LA BASE DE DATOS EXISTENTE

import uuid
from django.db import models
from django.core.exceptions import ValidationError

# Importar modelos necesarios de users
# (Se asume que estos modelos ya están definidos correctamente)


class TipoEvaluacion(models.Model):
    """Tipos de evaluación (NOM-030, NOM-035, etc.)"""
    tipo_evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, blank=False, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        db_table = 'tipos_evaluacion'
        verbose_name_plural = 'Tipos de evaluación'

    def __str__(self):
        return f'{self.nombre}'


class Evaluacion(models.Model):
    """Evaluaciones principales del sistema"""
    evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, blank=False)
    descripcion = models.TextField(blank=True, null=True)
    instrucciones = models.TextField(blank=True, null=True)
    tiempo_limite = models.IntegerField(blank=True, null=True)
    umbral_aprobacion = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Foreign Keys (sin constraints por ahora para simplicidad)
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT)
    empresa = models.ForeignKey('Empresa', null=True, blank=True, on_delete=models.CASCADE)
    creado_por = models.ForeignKey('PerfilUsuario', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'evaluaciones'
        ordering = ['fecha_registro']
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return f'{self.nombre} ({self.tipo_evaluacion.nombre})'


class ConjuntoRespuestas(models.Model):
    """Conjuntos de opciones reutilizables"""
    conjunto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    predefinido = models.BooleanField(default=False)

    class Meta:
        ordering = ['predefinido']
        db_table = 'conjuntos_opciones'
        verbose_name_plural = 'Conjuntos de opciones'

    def __str__(self):
        return f'{self.nombre}'


class PosiblesRespuestas(models.Model):
    """Opciones individuales para cada conjunto"""
    opcion_conjunto_id = models.AutoField(primary_key=True)
    texto_opcion = models.CharField(max_length=256, blank=False, null=False)
    valor_booleano = models.BooleanField(blank=True, null=True)
    valor_numerico = models.IntegerField(blank=True, null=True)
    puntuaje_escala = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2)
    numero_orden = models.IntegerField()
    conjunto_respuestas = models.ForeignKey(ConjuntoRespuestas, on_delete=models.CASCADE, db_column='conjunto_opciones', related_name='opciones')

    class Meta:
        db_table = 'opciones_conjunto'
        verbose_name_plural = 'Posibles respuestas'
        ordering = ['conjunto_respuestas', 'numero_orden']

    def __str__(self):
        return f'{self.texto_opcion} ({self.conjunto_respuestas.nombre})'
