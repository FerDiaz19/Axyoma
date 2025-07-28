#!/usr/bin/env python
"""
Script para configurar la base de datos con datos iniciales
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def setup_database():
    """Configurar la base de datos completa"""
    print("🚀 CONFIGURANDO BASE DE DATOS AXYOMA")
    print("=" * 50)
    
    # 1. Aplicar migraciones
    print("1. Aplicando migraciones...")
    os.system("python manage.py migrate")
    
    # 2. Cargar datos iniciales
    print("\n2. Cargando datos iniciales...")
    os.system("python manage.py load_initial_data")
    
    # 3. Crear fixtures para compartir
    print("\n3. Creando fixtures...")
    try:
        os.system("python manage.py dumpdata apps.subscriptions > fixtures/subscriptions_data.json")
        os.system("python manage.py dumpdata auth.User apps.users > fixtures/users_data.json")
        print("✅ Fixtures creados en carpeta fixtures/")
    except:
        print("⚠️  No se pudieron crear todos los fixtures")
    
    print("\n✅ BASE DE DATOS CONFIGURADA CORRECTAMENTE")
    print("=" * 50)
    print("Usuarios de prueba:")
    print("- SuperAdmin: superadmin / 1234")
    print("- Admin Empresa: admin_empresa / 1234")
    print("=" * 50)

if __name__ == "__main__":
    setup_database()
