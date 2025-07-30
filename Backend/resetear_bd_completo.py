#!/usr/bin/env python
"""
Script para RESETEAR COMPLETAMENTE la base de datos
PELIGRO: Esto eliminará TODOS los datos y dejará la BD como el primer día
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import *

def confirmar_reset():
    """Confirmar que el usuario realmente quiere resetear la BD"""
    print("⚠️  ADVERTENCIA: RESETEO COMPLETO DE BASE DE DATOS")
    print("=" * 60)
    print("🚨 ESTO ELIMINARÁ TODOS LOS DATOS:")
    print("   - Todos los empleados")
    print("   - Todas las empresas")
    print("   - Todas las plantas")
    print("   - Todos los departamentos")
    print("   - Todos los puestos")
    print("   - Todos los usuarios (excepto superadmin)")
    print("   - Todas las evaluaciones")
    print("   - TODO EL CONTENIDO DE LA BASE DE DATOS")
    print("=" * 60)
    
    respuesta = input("¿Estás SEGURO de que quieres continuar? (escribe 'CONFIRMO' para continuar): ")
    
    if respuesta.strip().upper() != 'CONFIRMO':
        print("❌ Operación cancelada")
        return False
    
    respuesta2 = input("¿REALMENTE SEGURO? Esta acción NO se puede deshacer (escribe 'SI_ESTOY_SEGURO'): ")
    
    if respuesta2.strip().upper() != 'SI_ESTOY_SEGURO':
        print("❌ Operación cancelada")
        return False
    
    return True

def resetear_base_datos():
    """Resetear completamente la base de datos"""
    print("\n🔄 INICIANDO RESETEO COMPLETO...")
    print("=" * 60)
    
    try:
        # 1. Eliminar todos los empleados
        print("🗑️ Eliminando empleados...")
        Empleado.objects.all().delete()
        print("✅ Empleados eliminados")
        
        # 2. Eliminar puestos
        print("🗑️ Eliminando puestos...")
        Puesto.objects.all().delete()
        print("✅ Puestos eliminados")
        
        # 3. Eliminar departamentos
        print("🗑️ Eliminando departamentos...")
        Departamento.objects.all().delete()
        print("✅ Departamentos eliminados")
        
        # 4. Eliminar asignaciones de admin planta
        print("🗑️ Eliminando asignaciones admin planta...")
        AdminPlanta.objects.all().delete()
        print("✅ Asignaciones eliminadas")
        
        # 5. Eliminar plantas
        print("🗑️ Eliminando plantas...")
        Planta.objects.all().delete()
        print("✅ Plantas eliminadas")
        
        # 6. Eliminar empresas
        print("🗑️ Eliminando empresas...")
        Empresa.objects.all().delete()
        print("✅ Empresas eliminadas")
        
        # 7. Eliminar evaluaciones si existen
        try:
            from apps.users.models import Evaluacion, Asignacion, AsignacionEmpleado
            print("🗑️ Eliminando evaluaciones...")
            AsignacionEmpleado.objects.all().delete()
            Asignacion.objects.all().delete()
            Evaluacion.objects.all().delete()
            print("✅ Evaluaciones eliminadas")
        except:
            print("⚠️ No hay tablas de evaluaciones para eliminar")
        
        # 8. Eliminar usuarios (excepto superadmin)
        print("🗑️ Eliminando usuarios (excepto superadmin)...")
        User.objects.exclude(username='superadmin').delete()
        print("✅ Usuarios eliminados")
        
        # 9. Eliminar perfiles (excepto superadmin)
        print("🗑️ Eliminando perfiles...")
        superadmin_user = User.objects.get(username='superadmin')
        PerfilUsuario.objects.exclude(user=superadmin_user).delete()
        print("✅ Perfiles eliminados")
        
        # 10. Resetear secuencias de IDs
        print("🔄 Reseteando secuencias de IDs...")
        with connection.cursor() as cursor:
            # Resetear secuencias principales
            cursor.execute("ALTER SEQUENCE empleados_empleado_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE puestos_puesto_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE departamentos_departamento_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE plantas_planta_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE empresas_empresa_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE usuarios_id_seq RESTART WITH 2;")  # Dejar espacio para superadmin
        print("✅ Secuencias reseteadas")
        
        print("\n🎯 RESETEO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("✅ La base de datos ha sido reseteada al estado inicial")
        print("🔑 Solo queda el usuario superadmin: superadmin / 1234")
        print("📝 Para volver a tener datos de prueba, ejecuta: python crear_datos_completos.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el reseteo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔄 SCRIPT DE RESETEO COMPLETO DE BASE DE DATOS")
    print("=" * 60)
    
    if not confirmar_reset():
        return
    
    if resetear_base_datos():
        print("\n✅ ¡PROCESO COMPLETADO!")
    else:
        print("\n❌ Hubo errores durante el proceso")

if __name__ == "__main__":
    main()
