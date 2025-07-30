# -*- coding: utf-8 -*-
"""
Configuración del panel de administración de Django para la app users
Incluye acciones especiales para SuperAdmin como resetear la BD
"""
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import transaction
import subprocess
import os

from .models import (
    PerfilUsuario, Empresa, Planta, AdminPlanta, 
    Departamento, Puesto, Empleado
)

# Admin para PerfilUsuario
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido_paterno', 'correo', 'nivel_usuario', 'status', 'fecha_registro']
    list_filter = ['nivel_usuario', 'status', 'fecha_registro']
    search_fields = ['nombre', 'apellido_paterno', 'correo']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 'correo')
        }),
        ('Configuración del Sistema', {
            'fields': ('nivel_usuario', 'status', 'user')
        }),
        ('Información Adicional', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('resetear-bd/', self.admin_site.admin_view(self.resetear_bd_view), name='users_resetear_bd'),
            path('cargar-datos/', self.admin_site.admin_view(self.cargar_datos_view), name='users_cargar_datos'),
        ]
        return custom_urls + urls
    
    def resetear_bd_view(self, request):
        """Vista para resetear completamente la base de datos"""
        # Solo SuperAdmin puede acceder
        if not (hasattr(request.user, 'perfil') and request.user.perfil.nivel_usuario == 'superadmin'):
            messages.error(request, 'Solo SuperAdmin puede resetear la base de datos')
            return HttpResponseRedirect('../')
        
        if request.method == 'POST':
            confirmacion = request.POST.get('confirmacion', '')
            if confirmacion != 'CONFIRMO RESETEO':
                messages.error(request, 'Debe escribir exactamente "CONFIRMO RESETEO" para continuar')
                return render(request, 'admin/users/resetear_bd.html', {
                    'title': 'Resetear Base de Datos',
                    'subtitle': 'ESTA ACCIÓN ES IRREVERSIBLE',
                    'opts': self.model._meta,
                    'has_permission': True,
                })
            
            try:
                # Ejecutar script de reseteo
                script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resetear_bd_completo.py')
                result = subprocess.run(['python', script_path], 
                                      capture_output=True, text=True, cwd=os.path.dirname(script_path))
                
                if result.returncode == 0:
                    messages.success(request, '✅ Base de datos reseteada exitosamente. Solo queda el usuario superadmin.')
                else:
                    messages.error(request, f'❌ Error al resetear: {result.stderr}')
                    
            except Exception as e:
                messages.error(request, f'❌ Error ejecutando reseteo: {str(e)}')
            
            return HttpResponseRedirect('../')
        
        context = {
            'title': 'Resetear Base de Datos',
            'subtitle': 'ESTA ACCIÓN ES IRREVERSIBLE',
            'opts': self.model._meta,
            'has_permission': True,
        }
        return render(request, 'admin/users/resetear_bd.html', context)
    
    def cargar_datos_view(self, request):
        """Vista para cargar datos de prueba"""
        # Solo SuperAdmin puede acceder
        if not (hasattr(request.user, 'perfil') and request.user.perfil.nivel_usuario == 'superadmin'):
            messages.error(request, 'Solo SuperAdmin puede cargar datos de prueba')
            return HttpResponseRedirect('../')
        
        if request.method == 'POST':
            try:
                # Ejecutar script de datos completos
                script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crear_datos_completos.py')
                result = subprocess.run(['python', script_path], 
                                      capture_output=True, text=True, cwd=os.path.dirname(script_path))
                
                if result.returncode == 0:
                    messages.success(request, '✅ Datos de prueba cargados exitosamente. TechnoMex Industries con 138+ empleados.')
                else:
                    messages.error(request, f'❌ Error al cargar datos: {result.stderr}')
                    
            except Exception as e:
                messages.error(request, f'❌ Error ejecutando carga de datos: {str(e)}')
            
            return HttpResponseRedirect('../')
        
        context = {
            'title': 'Cargar Datos de Prueba',
            'subtitle': 'Empresa completa con empleados, plantas, departamentos y puestos',
            'opts': self.model._meta,
            'has_permission': True,
        }
        return render(request, 'admin/users/cargar_datos.html', context)

# Admin para Empresa
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rfc', 'status', 'fecha_registro', 'tiene_suscripcion_activa']
    list_filter = ['status', 'fecha_registro']
    search_fields = ['nombre', 'rfc']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('nombre', 'rfc', 'direccion', 'telefono_contacto', 'email_contacto')
        }),
        ('Configuración', {
            'fields': ('administrador', 'logotipo')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

# Admin para Planta
@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'status', 'fecha_registro']
    list_filter = ['status', 'empresa', 'fecha_registro']
    search_fields = ['nombre', 'empresa__nombre']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información de la Planta', {
            'fields': ('nombre', 'empresa', 'direccion')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

# Admin para Departamento
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'planta', 'descripcion', 'status']
    list_filter = ['status', 'planta__empresa']
    search_fields = ['nombre', 'planta__nombre', 'planta__empresa__nombre']
    
    fieldsets = (
        ('Información del Departamento', {
            'fields': ('nombre', 'planta', 'descripcion')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
    )

# Admin para Puesto
@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'status']
    list_filter = ['status', 'departamento__planta__empresa']
    search_fields = ['nombre', 'departamento__nombre']
    
    fieldsets = (
        ('Información del Puesto', {
            'fields': ('nombre', 'departamento', 'descripcion')
        }),
        ('Estado', {
            'fields': ('status',)
        }),
    )

# Admin para Empleado
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido_paterno', 'puesto', 'email', 'status', 'fecha_ingreso']
    list_filter = ['status', 'puesto__departamento__planta__empresa', 'fecha_ingreso']
    search_fields = ['nombre', 'apellido_paterno', 'email', 'puesto__nombre']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('puesto', 'fecha_ingreso', 'status')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimizar consultas con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'puesto__departamento__planta__empresa'
        )

# Admin para AdminPlanta
@admin.register(AdminPlanta)
class AdminPlantaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'planta', 'status', 'fecha_asignacion']
    list_filter = ['status', 'fecha_asignacion', 'planta__empresa']
    search_fields = ['usuario__nombre', 'planta__nombre']
    readonly_fields = ['fecha_asignacion']
