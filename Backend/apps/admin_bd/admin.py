# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import LogRespaldo, ConfiguracionBD


# @admin.register(LogRespaldo)
# class LogRespaldoAdmin(admin.ModelAdmin):
#     list_display = [
#         'tipo', 'usuario', 'empresa', 'archivo_nombre',
#         'fecha_creacion', 'exitoso', 'archivo_tamaño'
#     ]
#     list_filter = ['tipo', 'exitoso', 'fecha_creacion', 'empresa']
#     search_fields = ['archivo_nombre', 'usuario__username', 'empresa__nombre']
#     readonly_fields = ['fecha_creacion', 'archivo_tamaño', 'archivo_ruta']
#     ordering = ['-fecha_creacion']

#     fieldsets = (
#         ('Información General', {
#             'fields': ('tipo', 'usuario', 'empresa', 'exitoso')
#         }),
#         ('Detalles del Respaldo', {
#             'fields': ('archivo_nombre', 'archivo_ruta', 'archivo_tamaño', 'tablas_incluidas')
#         }),
#         ('Metadatos', {
#             'fields': ('fecha_creacion', 'detalles', 'mensaje_error'),
#             'classes': ('collapse',)
#         }),
#     )

#     def has_add_permission(self, request):
#         # Los logs se crean automáticamente, no manualmente
#         return False

#     def has_change_permission(self, request, obj=None):
#         # Los logs no se deben modificar
#         return False


# @admin.register(ConfiguracionBD)
# class ConfiguracionBDAdmin(admin.ModelAdmin):
#     list_display = [
#         'nombre_bd', 'host', 'puerto', 'directorio_respaldos',
#         'habilitar_respaldos_automaticos', 'frecuencia_respaldo_dias'
#     ]

#     fieldsets = (
#         ('Configuración de Conexión', {
#             'fields': ('nombre_bd', 'host', 'puerto', 'usuario_admin')
#         }),
#         ('Configuración de Respaldos', {
#             'fields': (
#                 'directorio_respaldos', 'max_respaldos_mantener',
#                 'habilitar_respaldos_automaticos', 'frecuencia_respaldo_dias'
#             )
#         }),
#     )

#     def has_add_permission(self, request):
#         # Solo permitir una configuración
#         return not ConfiguracionBD.objects.exists()

#     def has_delete_permission(self, request, obj=None):
#         # No permitir eliminar la configuración
#         return False
