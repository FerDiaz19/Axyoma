#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    # Configure Django
    django.setup()
    
    print("✅ Django setup successful!")
    print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
    print(f"✅ Database: {settings.DATABASES['default']['NAME']}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ Database connection successful!")
    
    # Test if our apps are loaded
    from django.apps import apps
    app_configs = apps.get_app_configs()
    print(f"✅ Apps loaded: {[app.name for app in app_configs]}")
    
    # Test if our models are accessible
    try:
        from apps.evaluaciones.models import PreguntasOficial
        from apps.oficiales.models import Empleado
        print("✅ Models imported successfully!")
        
        # Count some records
        preguntas_count = PreguntasOficial.objects.count()
        empleados_count = Empleado.objects.count()
        print(f"✅ Database has {preguntas_count} preguntas and {empleados_count} empleados")
        
    except Exception as e:
        print(f"❌ Error importing models: {e}")
    
    print("\n🚀 Django is ready! You can start the server with:")
    print("python manage.py runserver 8000")
    
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
