# -*- coding: utf-8 -*-
"""
Archivo para centralizar la importación de modelos
"""

from django.db import models

# Modelos simples que coinciden con la BD real
class Suscripcion(models.Model):
    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.IntegerField()
    plan = models.IntegerField()  
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='activa')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'suscripciones'

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField()  # días
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'planes'

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    suscripcion = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    estado_pago = models.CharField(max_length=20, default='pendiente')
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.IntegerField()
    
    class Meta:
        db_table = 'pagos'

# Importar modelos de usuarios
from apps.users.models import PerfilUsuario as Usuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta

# Importar otros modelos si existen
try:
    from core.models import *
except ImportError:
    pass
