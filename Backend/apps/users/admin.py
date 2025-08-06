
# ---------------------------------------------------------------------------- #

import os
import subprocess

from django.urls import path
from django.shortcuts import render
from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .models import *

# -- INLINES ----------------------------------------------------------------- #

class PlantaInline(admin.StackedInline):
    model = Planta
    extra = 1

class DepartamentoInline(admin.StackedInline):
    model = Departamento
    extra = 1

class PuestoInline(admin.TabularInline):
    model = Puesto
    extra = 1

class EmpleadoInline(admin.TabularInline):
    model = Empleado
    extra = 1

# -- REGISTRO DE MODELOS ----------------------------------------------------- #

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [ 'nombre', 'apellido_paterno', 'correo', 'nivel_usuario', 'status' ]
    list_filter = [ 'nivel_usuario', 'status' ]
    search_fields = [ 'nombre', 'apellido_paterno', 'correo', 'apellido_materno' ]
    readonly_fields = [ 'id' ]

    fieldsets = (
        ('Información personal', {
            'fields': ('id', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo')
        }),
        ('Configuración del sistema', {
            'fields': ('nivel_usuario', 'status', 'admin_empresa', 'user_id')
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
        ''' Vista para resetear completamente la base de datos. '''
        if not (hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.nivel_usuario == 'superadmin'):
            messages.error(request, 'Solo un administrador principal puede resetear la base de datos')
            return HttpResponseRedirect('../')

        if request.method == 'POST':
            confirmacion = request.POST.get('confirmacion', '')

            if confirmacion != 'CONFIRMO RESETEO':
                messages.error(request, 'Debe escribir exactamente "CONFIRMO RESETEO" para continuar')
                return render(request, 'admin/users/resetear_bd.html', {
                    'title': 'Resetear base de datos',
                    'subtitle': 'ESTA ACCIÓN ES IRREVERSIBLE',
                    'opts': self.model._meta,
                    'has_permission': True,
                })

            try: # Ejecuta script de reseteo.
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
            'title': 'Resetear base de datos',
            'subtitle': 'ESTA ACCIÓN ES IRREVERSIBLE',
            'opts': self.model._meta,
            'has_permission': True,
        }

        return render(request, 'admin/users/resetear_bd.html', context)

    def cargar_datos_view(self, request):
        ''' Vista para cargar datos de prueba '''
        if not (hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.nivel_usuario == 'superadmin'):
            messages.error(request, 'Solo un administradr principal puede cargar datos de prueba')
            return HttpResponseRedirect('../')

        if request.method == 'POST':
            try: # Ejecuta script de datos completos.
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
            'title': 'Cargar datos de prueba',
            'subtitle': 'Empresa completa con empleados, plantas, departamentos y puestos',
            'opts': self.model._meta,
            'has_permission': True,
        }
        return render(request, 'admin/users/cargar_datos.html', context)

# ---------------------------------------------------------------------------- #

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rfc', 'status', 'tiene_suscripcion_activa', 'total_plantas', 'total_empleados']
    list_filter = ['status']
    search_fields = ['nombre', 'rfc']
    readonly_fields = ['fecha_registro']
    inlines = [PlantaInline]

    fieldsets = (
        ('Información de la empresa', {
            'fields': ('nombre', 'rfc', 'direccion', 'logotipo')
        }),
        ('Contacto', {
            'fields': ('email_contacto', 'telefono_contacto')
        }),
        ('Configuración del sistema', {
            'fields': ('administrador', 'status', 'fecha_registro')
        }),
    )

# ---------------------------------------------------------------------------- #

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'status', 'total_departamentos', 'total_empleados']
    list_filter = ['status', 'empresa']
    search_fields = ['nombre', 'empresa__nombre']
    readonly_fields = ['planta_id']
    inlines = [DepartamentoInline]

# ---------------------------------------------------------------------------- #

@admin.register(AdminPlanta)
class AdminPlantaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'planta', 'status']
    list_filter = ['status', 'planta']
    search_fields = ['usuario__nombre', 'planta__nombre']

# ---------------------------------------------------------------------------- #

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'planta', 'status', 'total_puestos', 'total_empleados']
    list_filter = ['status', 'planta__empresa']
    search_fields = ['nombre', 'planta__nombre', 'planta__empresa__nombre']
    inlines = [PuestoInline]

# ---------------------------------------------------------------------------- #

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento', 'status', 'total_empleados']
    list_filter = ['status', 'departamento']
    search_fields = ['nombre', 'departamento__nombre', 'departamento__planta__nombre']
    inlines = [EmpleadoInline]

# ---------------------------------------------------------------------------- #

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'puesto', 'email', 'status', 'fecha_ingreso']
    list_filter = ['status', 'puesto__departamento__planta__empresa']
    search_fields = ['nombre', 'apellido_paterno', 'email']

# ---------------------------------------------------------------------------- #
