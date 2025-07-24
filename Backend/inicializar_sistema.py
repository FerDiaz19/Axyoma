#!/usr/bin/env python
"""
Script de inicialización del sistema Axyoma
Ejecuta todas las tareas necesarias para que el sistema funcione
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def main():
    """Función principal de inicialización"""
    print("🚀 Inicializando sistema Axyoma...")
    
    try:
        # Verificar que la base de datos esté accesible
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Conexión a base de datos exitosa")
        
        # Ejecutar migraciones si es necesario
        from django.core.management import execute_from_command_line
        print("🔄 Verificando migraciones...")
        execute_from_command_line(['manage.py', 'migrate', '--check'])
        print("✅ Migraciones al día")
        
        # Verificar si existen datos iniciales
        from apps.models import PlanSuscripcion
        if not PlanSuscripcion.objects.exists():
            print("📋 Creando datos iniciales...")
            from crear_datos_iniciales import crear_datos_iniciales
            crear_datos_iniciales()
            print("✅ Datos iniciales creados")
        else:
            print("✅ Datos iniciales ya existen")
            
        print("🎉 Sistema inicializado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo y la BD 'axyomadb' exista")
        return False

if __name__ == '__main__':
    main()
