# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# USUARIOS - Según el esquema SQL original
class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ('superadmin', 'Super Administrador'),
        ('admin-empresa', 'Administrador de Empresa'),
        ('admin-planta', 'Administrador de Planta'),
    ]
    
    # Campos según USUARIOS table
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    apellido_paterno = models.CharField(max_length=64)
    apellido_materno = models.CharField(max_length=64, blank=True, null=True)
    correo = models.EmailField(max_length=255, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nivel_usuario = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    status = models.BooleanField(default=True)
    admin_empresa = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Relación con Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    class Meta:
        db_table = 'usuarios'

# EMPRESAS - Según el esquema SQL original
class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=65, unique=True)
    rfc = models.CharField(max_length=16, unique=True)
    direccion = models.TextField(blank=True, null=True)
    logotipo = models.CharField(max_length=128, blank=True, null=True)
    email_contacto = models.CharField(max_length=128, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    administrador = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'empresas'

# PLANTAS - Según el esquema SQL original
class Planta(models.Model):
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)  # No unique según SQL
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='empresa_id')
    
    class Meta:
        db_table = 'plantas'

# ADMIN_PLANTAS - Tabla intermedia para admins de plantas
class AdminPlanta(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    password_temporal = models.CharField(max_length=128, blank=True, null=True, help_text="Contraseña temporal generada automáticamente")
    
    class Meta:
        db_table = 'admin_plantas'
        unique_together = ('usuario', 'planta')

# DEPARTAMENTOS - Según el esquema SQL original
class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'departamentos'
        unique_together = ['nombre', 'planta']  # Nombre único solo dentro de la misma planta

# PUESTOS - Según el esquema SQL original
class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    descripcion = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'puestos'
        unique_together = ['nombre', 'departamento']  # Nombre único solo dentro del mismo departamento
        db_table = 'puestos'

# EMPLEADOS - Según el esquema SQL original
class Empleado(models.Model):
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]
    
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    apellido_paterno = models.CharField(max_length=64)
    apellido_materno = models.CharField(max_length=64, blank=True, null=True)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    antiguedad = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'empleados'
