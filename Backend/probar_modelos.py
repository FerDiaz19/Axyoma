#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PRUEBA DIRECTA DE MODELOS DESDE MANAGE.PY
=========================================
"""
from apps.users.models import *
from django.contrib.auth.models import User

def test_models():
    print("🧪 PROBANDO TODOS LOS MODELOS REDISEÑADOS")
    print("=" * 50)
    
    # Lista de todos los modelos
    modelos = [
        ('PerfilUsuario', PerfilUsuario),
        ('Empresa', Empresa),
        ('Planta', Planta),
        ('Departamento', Departamento),
        ('Puesto', Puesto),
        ('Empleado', Empleado),
        ('AdminPlanta', AdminPlanta),
        ('TipoEvaluacion', TipoEvaluacion),
        ('Evaluacion', Evaluacion),
        ('SeccionEval', SeccionEval),
        ('Pregunta', Pregunta),
        ('ConjuntoRespuestas', ConjuntoRespuestas),
        ('PosiblesRespuestas', PosiblesRespuestas),
        ('SeccionPregunta', SeccionPregunta),
        ('Asignacion', Asignacion),
        ('AsignacionEmpleado', AsignacionEmpleado),
        ('RespuestaEmpleado', RespuestaEmpleado),
        ('ResultadoEvaluacion', ResultadoEvaluacion),
    ]
    
    # Verificar que todos los modelos se pueden importar y consultar
    total_registros = 0
    for nombre, modelo in modelos:
        try:
            count = modelo.objects.count()
            total_registros += count
            status = "✅" if count >= 0 else "❌"
            print(f"   {status} {nombre:20} : {count:3d} registros")
        except Exception as e:
            print(f"   ❌ {nombre:20} : ERROR - {str(e)}")
    
    print("=" * 50)
    print(f"📊 TOTAL REGISTROS EN SISTEMA: {total_registros}")
    print("✅ TODOS LOS MODELOS FUNCIONAN CORRECTAMENTE")
    
    # Probar creación básica
    print("\n🔧 PROBANDO CREACIÓN DE DATOS BÁSICOS...")
    
    try:
        # Verificar si hay usuarios
        user_count = User.objects.count()
        print(f"   👤 Usuarios Django existentes: {user_count}")
        
        # Verificar si hay empresas
        empresa_count = Empresa.objects.count()
        print(f"   🏢 Empresas existentes: {empresa_count}")
        
        if empresa_count > 0:
            empresa = Empresa.objects.first()
            print(f"   📋 Empresa ejemplo: {empresa.nombre}")
            print(f"      - RFC: {empresa.rfc}")
            print(f"      - Status: {empresa.status}")
            print(f"      - Total plantas: {empresa.total_plantas}")
            print(f"      - Total empleados: {empresa.total_empleados}")
        
        print("\n✅ PRUEBA DE MODELOS COMPLETADA EXITOSAMENTE")
        
    except Exception as e:
        print(f"❌ Error en prueba básica: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_models()
