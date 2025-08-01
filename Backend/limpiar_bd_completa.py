#!/usr/bin/env python
"""
🧹 LIMPIAR BASE DE DATOS COMPLETAMENTE
=====================================
Este script limpia COMPLETAMENTE la base de datos
antes de ejecutar una nueva configuración.
"""

import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def limpiar_completamente():
    """Limpiar completamente la base de datos"""
    print("🧹 LIMPIEZA COMPLETA DE BASE DE DATOS")
    print("=" * 50)
    print("⚠️  ATENCIÓN: Esto eliminará TODOS los datos")
    print("=" * 50)
    print()
    
    respuesta = input("¿Estás seguro de continuar? (s/n): ").lower().strip()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Limpieza cancelada")
        return False
    
    try:
        print("\n🔥 PASO 1: Eliminando todos los datos...")
        execute_from_command_line(['manage.py', 'flush', '--noinput'])
        print("✅ Datos eliminados")
        
        print("\n🔧 PASO 2: Reinicializando estructura...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Estructura reinicializada")
        
        print("\n🔄 PASO 3: Aplicando migraciones limpias...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones aplicadas")
        
        # Verificar que no hay datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM empresas")
            empresas = cursor.fetchone()[0]
            
            print(f"\n📊 VERIFICACIÓN:")
            print(f"  👤 Usuarios: {users}")
            print(f"  🏢 Empresas: {empresas}")
            
            if users == 0 and empresas == 0:
                print("✅ Base de datos completamente limpia")
                return True
            else:
                print("⚠️ Advertencia: Aún hay algunos datos")
                return True
        
    except Exception as e:
        print(f"❌ Error durante limpieza: {e}")
        return False

def main():
    print("🎯 PREPARACIÓN PARA NUEVA CONFIGURACIÓN")
    print("=" * 60)
    print("Este script preparará la base de datos para una")
    print("configuración completamente nueva del sistema Axyoma.")
    print()
    
    if limpiar_completamente():
        print("\n🎉 ¡BASE DE DATOS LISTA!")
        print("=" * 30)
        print("✅ Base de datos completamente limpia")
        print("✅ Lista para nueva configuración")
        print()
        print("🚀 SIGUIENTE PASO:")
        print("   python sistema_completo_listo.py")
        print()
        print("   O ejecutar el configurador completo:")
        print("   python configurar_nueva_laptop.py")
        print("=" * 30)
    else:
        print("\n❌ Error en la limpieza")

if __name__ == "__main__":
    main()
