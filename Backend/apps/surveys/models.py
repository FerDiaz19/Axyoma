from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa, Planta, Empleado

# Modelos para surveys - implementación básica
class TipoEvaluacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        db_table = 'tipos_evaluacion'
        verbose_name = "Tipo de Evaluación"
        verbose_name_plural = "Tipos de Evaluación"
        
    def __str__(self):
        return self.nombre

class Evaluacion(models.Model):
    evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, default='normativa')
    estado = models.CharField(max_length=20, default='activa')
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tiempo_limite = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'evaluaciones'
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        
    def __str__(self):
        return self.nombre
