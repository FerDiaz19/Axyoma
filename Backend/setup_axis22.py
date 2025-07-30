#!/usr/bin/env python3
"""
Script para limpiar datos problemáticos y crear estructura completa para axis22
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta
from django.contrib.auth.models import User
from django.db import transaction
import random
import string

def limpiar_usuarios_problematicos():
    """Eliminar usuarios sin user asociado"""
    print("🧹 Limpiando usuarios problemáticos...")
    try:
        usuarios_sin_user = PerfilUsuario.objects.filter(user__isnull=True)
        count = usuarios_sin_user.count()
        if count > 0:
            usuarios_sin_user.delete()
            print(f"   ✅ Eliminados {count} usuarios sin user asociado")
        else:
            print("   ✅ No hay usuarios problemáticos")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def crear_datos_axis22():
    """Crear estructura completa para axis22"""
    print("🏢 Configurando datos para axis22...")
    
    try:
        # Buscar empresa axis22
        axis22 = None
        empresas_axis = Empresa.objects.filter(nombre__icontains='axis')
        print("Empresas con 'axis' en el nombre:")
        for emp in empresas_axis:
            print(f"   - {emp.nombre} (ID: {emp.empresa_id})")
            if 'axis22' in emp.nombre.lower() or emp.empresa_id == 16:
                axis22 = emp
                break
        
        if not axis22:
            print("   ❌ No se encontró axis22")
            return
        
        print(f"   ✅ Usando empresa: {axis22.nombre} (ID: {axis22.empresa_id})")
        
        # Verificar/crear planta
        planta = Planta.objects.filter(empresa=axis22).first()
        if not planta:
            planta = Planta.objects.create(
                nombre="Planta Principal axis22",
                direccion="Av. Principal #123, Ciudad México",
                empresa=axis22
            )
            print(f"   ✅ Planta creada: {planta.nombre}")
        else:
            print(f"   ✅ Planta existente: {planta.nombre}")
        
        # Crear departamentos si no existen
        departamentos_base = [
            ("Recursos Humanos", "Gestión del personal y nómina"),
            ("Tecnología", "Desarrollo de software y sistemas"),
            ("Ventas", "Gestión comercial y clientes"),
            ("Producción", "Operaciones y manufactura"),
        ]
        
        departamentos_creados = []
        for nombre, desc in departamentos_base:
            depto, created = Departamento.objects.get_or_create(
                nombre=nombre,
                planta=planta,
                defaults={'descripcion': desc}
            )
            departamentos_creados.append(depto)
            if created:
                print(f"   ✅ Departamento creado: {nombre}")
            else:
                print(f"   ✅ Departamento existente: {nombre}")
        
        # Crear puestos para cada departamento
        puestos_por_depto = {
            "Recursos Humanos": ["Gerente RH", "Analista RH", "Asistente RH"],
            "Tecnología": ["Jefe de Desarrollo", "Desarrollador Senior", "Desarrollador Junior"],
            "Ventas": ["Gerente Ventas", "Ejecutivo Ventas", "Asistente Comercial"],
            "Producción": ["Supervisor Producción", "Operario", "Control Calidad"],
        }
        
        puestos_creados = []
        for depto in departamentos_creados:
            if depto.nombre in puestos_por_depto:
                for nombre_puesto in puestos_por_depto[depto.nombre]:
                    puesto, created = Puesto.objects.get_or_create(
                        nombre=nombre_puesto,
                        departamento=depto,
                        defaults={'descripcion': f'Puesto de {nombre_puesto} en {depto.nombre}'}
                    )
                    puestos_creados.append(puesto)
                    if created:
                        print(f"   ✅ Puesto creado: {nombre_puesto} ({depto.nombre})")
        
        # Crear algunos empleados de ejemplo
        empleados_base = [
            ("Ana", "García", "López", "Femenino", "Gerente RH"),
            ("Carlos", "Martínez", "Ruiz", "Masculino", "Jefe de Desarrollo"),
            ("María", "López", "González", "Femenino", "Ejecutivo Ventas"),
            ("José", "Hernández", "Silva", "Masculino", "Supervisor Producción"),
            ("Laura", "Rodríguez", "Morales", "Femenino", "Desarrollador Senior"),
        ]
        
        for nombre, ap_pat, ap_mat, genero, nombre_puesto in empleados_base:
            # Buscar el puesto
            puesto = None
            for p in puestos_creados:
                if p.nombre == nombre_puesto:
                    puesto = p
                    break
            
            if puesto:
                empleado, created = Empleado.objects.get_or_create(
                    nombre=nombre,
                    apellido_paterno=ap_pat,
                    planta=planta,
                    defaults={
                        'apellido_materno': ap_mat,
                        'genero': genero,
                        'departamento': puesto.departamento,
                        'puesto': puesto,
                        'antiguedad': random.randint(1, 10)
                    }
                )
                if created:
                    print(f"   ✅ Empleado creado: {nombre} {ap_pat} - {nombre_puesto}")
        
        print("🎉 Estructura completa creada para axis22!")
        
    except Exception as e:
        print(f"   ❌ Error creando datos: {e}")
        import traceback
        traceback.print_exc()

def mostrar_resumen():
    """Mostrar resumen de la estructura"""
    print("\n📊 RESUMEN FINAL:")
    try:
        axis22 = Empresa.objects.filter(nombre__icontains='axis22').first()
        if axis22:
            print(f"🏢 Empresa: {axis22.nombre}")
            
            plantas = Planta.objects.filter(empresa=axis22)
            print(f"🏭 Plantas: {plantas.count()}")
            
            departamentos = Departamento.objects.filter(planta__empresa=axis22)
            print(f"🏛️ Departamentos: {departamentos.count()}")
            for d in departamentos:
                print(f"   - {d.nombre}")
            
            puestos = Puesto.objects.filter(departamento__planta__empresa=axis22)
            print(f"💼 Puestos: {puestos.count()}")
            
            empleados = Empleado.objects.filter(planta__empresa=axis22)
            print(f"👥 Empleados: {empleados.count()}")
            
            usuarios_totales = PerfilUsuario.objects.filter(user__isnull=False).count()
            print(f"👤 Usuarios válidos en el sistema: {usuarios_totales}")
        
    except Exception as e:
        print(f"❌ Error mostrando resumen: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 LIMPIEZA Y CONFIGURACIÓN DE DATOS AXIS22")
    print("=" * 60)
    
    limpiar_usuarios_problematicos()
    crear_datos_axis22()
    mostrar_resumen()
    
    print("\n✅ ¡Proceso completado!")
