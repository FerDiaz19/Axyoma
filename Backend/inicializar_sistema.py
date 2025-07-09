#!/usr/bin/env python
"""
Script de inicialización que se ejecuta automáticamente al iniciar el sistema
para asegurar que las evaluaciones oficiales estén disponibles.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.surveys.models import Evaluacion

def verificar_evaluaciones_oficiales():
    """Verifica que las evaluaciones oficiales estén disponibles"""
    evaluaciones_oficiales = [
        'NOM-035 - Evaluación de Riesgos Psicosociales',
        'NOM-030 - Evaluación de Servicios Preventivos de Seguridad',
        'Evaluación 360 Grados - Competencias Laborales'
    ]
    
    evaluaciones_existentes = Evaluacion.objects.filter(
        tipo='normativa',
        titulo__in=evaluaciones_oficiales
    ).count()
    
    return evaluaciones_existentes == len(evaluaciones_oficiales)

def main():
    """Función principal de inicialización"""
    print("🔄 Iniciando verificación del sistema...")
    
    try:
        # Verificar que las evaluaciones oficiales estén disponibles
        if not verificar_evaluaciones_oficiales():
            print("⚠️  Las evaluaciones oficiales no están completas. Creándolas...")
            
            # Ejecutar el script de creación de evaluaciones oficiales
            script_path = os.path.join(os.path.dirname(__file__), 'crear_evaluaciones_oficiales.py')
            exec(open(script_path).read())
        else:
            print("✅ Las evaluaciones oficiales están disponibles")
        
        # Ejecutar migraciones si es necesario
        print("🔄 Verificando migraciones...")
        execute_from_command_line(['manage.py', 'migrate', '--check'])
        
        print("🎉 Sistema inicializado correctamente")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
