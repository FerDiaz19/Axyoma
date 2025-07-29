# -*- coding: utf-8 -*-
"""
Modelos simples para gestión de BD que mapean directamente a las tablas existentes
"""
from django.db import models

class EmpleadoSimple(models.Model):
    """
    Modelo simple para tabla empleados existente
    """
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    fecha_registro = models.DateTimeField()
    status = models.BooleanField()
    puesto = models.IntegerField()  # FK simple

    class Meta:
        db_table = 'empleados'
        managed = False  # No dejar que Django gestione esta tabla

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class EmpresaSimple(models.Model):
    """
    Modelo simple para tabla empresas existente
    """
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=20)
    email_contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    class Meta:
        db_table = 'empresas'
        managed = False

    def __str__(self):
        return self.nombre

class PlantaSimple(models.Model):
    """
    Modelo simple para tabla plantas existente
    """
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    empresa = models.IntegerField()  # FK simple

    class Meta:
        db_table = 'plantas'
        managed = False

    def __str__(self):
        return self.nombre

class DepartamentoSimple(models.Model):
    """
    Modelo simple para tabla departamentos existente
    """
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    planta = models.IntegerField()  # FK simple

    class Meta:
        db_table = 'departamentos'
        managed = False

    def __str__(self):
        return self.nombre

class PuestoSimple(models.Model):
    """
    Modelo simple para tabla puestos existente
    """
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.IntegerField()  # FK simple

    class Meta:
        db_table = 'puestos'
        managed = False

    def __str__(self):
        return self.nombre
