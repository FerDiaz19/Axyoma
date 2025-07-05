# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    NIVEL_CHOICES = [
        ('superadmin', 'Super Administrador'),
        ('admin-empresa', 'Administrador de Empresa'),
        ('admin-planta', 'Administrador de Planta'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nombre = models.CharField(max_length=128)
    apellido_paterno = models.CharField(max_length=64)
    apellido_materno = models.CharField(max_length=64, blank=True, null=True)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nivel_usuario = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    status = models.BooleanField(default=True)
    admin_empresa = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'usuarios'

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=65, unique=True)
    rfc = models.CharField(max_length=16, unique=True)
    direccion = models.TextField(blank=True, null=True)
    logotipo = models.URLField(max_length=128, blank=True, null=True)
    email_contacto = models.EmailField(max_length=128, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    administrador = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'empresas'

class Planta(models.Model):
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, unique=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'plantas'

class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'departamentos'

class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'puestos'

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
