#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT SIMPLE DE PRUEBA DE MODELOS
==================================
Prueba básica de creación de datos para verificar que los modelos funcionan.
"""

import os
import sys
import django
from datetime import datetime, date

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "axyoma.settings")
django.setup()

from django.contrib.auth.models import User
from apps.users.models import *

def test_basic_models():
    """Prueba básica de modelos"""
    print("🧪 Iniciando prueba básica de modelos...")
    
    # Verificar que podemos importar todos los modelos
    modelos = [
        PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta,
        TipoEvaluacion, Evaluacion, SeccionEval, Pregunta, ConjuntoRespuestas, 
        PosiblesRespuestas, SeccionPregunta, Asignacion, AsignacionEmpleado,
        RespuestaEmpleado, ResultadoEvaluacion
    ]
    
    print(f"✅ Todos los modelos importados correctamente: {len(modelos)} modelos")
    
    # Verificar conteos actuales
    for modelo in modelos:
        try:
            count = modelo.objects.count()
            print(f"   {modelo.__name__:20} : {count:3d} registros")
        except Exception as e:
            print(f"   ❌ Error en {modelo.__name__}: {str(e)}")
    
    print("✅ Prueba de modelos completada")

if __name__ == '__main__':
    try:
        test_basic_models()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
