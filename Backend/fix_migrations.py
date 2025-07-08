#!/usr/bin/env python
"""
Script para solucionar problemas de migraciones inconsistentes
Este script resuelve conflictos entre migraciones de users y subscriptions
"""

import os
import django
import sys
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

def reset_migrations():
    """Resetear migraciones problemáticas"""
    print("🔧 Solucionando problemas de migraciones...")
    
    try:
        # 1. Verificar conexión a la base de datos
        print("📡 Verificando conexión a la base de datos...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD exitosa")
        
        # 2. Marcar subscriptions como no aplicado
        print("🔄 Desmarcando migraciones de subscriptions...")
        try:
            execute_from_command_line(['manage.py', 'migrate', '--fake', 'subscriptions', 'zero'])
            print("✅ Migraciones de subscriptions desmarcadas")
        except Exception as e:
            print(f"⚠️ Warning al desmarcar subscriptions: {e}")
        
        # 3. Aplicar migraciones de users primero
        print("📦 Aplicando migraciones de users...")
        execute_from_command_line(['manage.py', 'migrate', 'users'])
        print("✅ Migraciones de users aplicadas")
        
        # 4. Aplicar migraciones de subscriptions
        print("💳 Aplicando migraciones de subscriptions...")
        execute_from_command_line(['manage.py', 'migrate', 'subscriptions'])
        print("✅ Migraciones de subscriptions aplicadas")
        
        # 5. Aplicar todas las demás migraciones
        print("🚀 Aplicando migraciones restantes...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Todas las migraciones aplicadas")
        
        print("\n🎉 ¡Problema de migraciones solucionado!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_plans():
    """Crear planes de ejemplo"""
    try:
        print("📋 Creando planes de ejemplo...")
        execute_from_command_line(['manage.py', 'crear_planes_ejemplo'])
        print("✅ Planes de ejemplo creados")
        return True
    except Exception as e:
        print(f"⚠️ Warning creando planes: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🛠️  SOLUCIONADOR DE MIGRACIONES AXYOMA")
    print("=" * 50)
    
    success = reset_migrations()
    
    if success:
        print("\n" + "=" * 50)
        print("🎯 CREANDO DATOS INICIALES")
        print("=" * 50)
        create_plans()
        
        print("\n" + "=" * 50)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 50)
        print("🚀 Para iniciar el sistema ejecuta: python manage.py runserver")
        print("🌐 Accede a: http://localhost:8000/api")
    else:
        print("\n❌ Error en la configuración. Revisa los mensajes anteriores.")
        sys.exit(1)
