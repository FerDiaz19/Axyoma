# -*- coding: utf-8 -*-
"""
🗄️ MODELOS DE ADMINISTRACIÓN DE BASE DE DATOS
=============================================

Modelos Django para gestión de logs y configuración de respaldos.
Sistema de auditoría y configuración para funciones de SuperAdmin.

📋 Responsable: Yael Contreras
📅 Fecha: Enero 2025
🔢 Versión: 2.0

🚀 Modelos incluidos:
- LogRespaldo: Registro de todas las operaciones de respaldo
- ConfiguracionBD: Configuración del sistema de respaldos

🔒 Seguridad: Logs de auditoría para SuperAdmin
"""
from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Empresa


class LogRespaldo(models.Model):
    """Log de respaldos realizados"""
    TIPO_RESPALDO = [
        ('completo', 'Respaldo Completo'),
        ('parcial', 'Respaldo Parcial'),
        ('restauracion', 'Restauración'),
        ('punto_inicial', 'Restauración a Punto Inicial'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_RESPALDO)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    archivo_nombre = models.CharField(max_length=255)
    archivo_ruta = models.CharField(max_length=500, blank=True, null=True)
    archivo_tamaño = models.BigIntegerField(null=True, blank=True)  # bytes
    tablas_incluidas = models.JSONField(default=list, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    exitoso = models.BooleanField(default=True)
    detalles = models.TextField(blank=True)
    mensaje_error = models.TextField(blank=True)  # Mantenido para compatibilidad
    
    class Meta:
        verbose_name = "Log de Respaldo"
        verbose_name_plural = "Logs de Respaldos"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.tipo} - {self.usuario.username} - {self.fecha_creacion}"


class ConfiguracionBD(models.Model):
    """Configuración de la base de datos"""
    nombre_bd = models.CharField(max_length=100, default='axyomadb')
    host = models.CharField(max_length=100, default='localhost')
    puerto = models.IntegerField(default=5432)
    usuario_admin = models.CharField(max_length=100, default='postgres')
    directorio_respaldos = models.CharField(max_length=255, default='config/backups/')
    max_respaldos_mantener = models.IntegerField(default=10)
    habilitar_respaldos_automaticos = models.BooleanField(default=False)
    frecuencia_respaldo_dias = models.IntegerField(default=7)
    
    class Meta:
        verbose_name = "Configuración de BD"
        verbose_name_plural = "Configuración de BD"
        
    def __str__(self):
        return f"Config BD - {self.nombre_bd}"
