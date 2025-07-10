from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa, Planta, Empleado

# Modelos para surveys - implementación básica compatible con la BD
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
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'evaluaciones'
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        
    def __str__(self):
        return self.nombre
