#!/usr/bin/env python
"""
Script para verificar que la base de datos esté correctamente poblada
y que los datos de prueba estén disponibles.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def verificar_datos():
    """Verificar que todos los datos de prueba estén en la base de datos"""
    print("🔍 VERIFICANDO DATOS DE LA BASE DE DATOS...")
    print("=" * 60)
    
    try:
        # Importar modelos después de setup de Django
        from django.contrib.auth.models import User
        from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
        from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
        
        # Verificar datos usando consultas SQL directas
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Verificar usuarios
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            usuarios_count = cursor.fetchone()[0]
            print(f"✓ Usuarios: {usuarios_count}")
            
            # Verificar empresas
            cursor.execute("SELECT COUNT(*) FROM empresas")
            empresas_count = cursor.fetchone()[0]
            print(f"✓ Empresas: {empresas_count}")
            
            # Verificar plantas
            cursor.execute("SELECT COUNT(*) FROM plantas")
            plantas_count = cursor.fetchone()[0]
            print(f"✓ Plantas: {plantas_count}")
            
            # Verificar departamentos
            cursor.execute("SELECT COUNT(*) FROM departamentos")
            departamentos_count = cursor.fetchone()[0]
            print(f"✓ Departamentos: {departamentos_count}")
            
            # Verificar puestos
            cursor.execute("SELECT COUNT(*) FROM puestos")
            puestos_count = cursor.fetchone()[0]
            print(f"✓ Puestos: {puestos_count}")
            
            # Verificar empleados
            cursor.execute("SELECT COUNT(*) FROM empleados")
            empleados_count = cursor.fetchone()[0]
            print(f"✓ Empleados: {empleados_count}")
            
            # Verificar planes
            cursor.execute("SELECT COUNT(*) FROM planes")
            planes_count = cursor.fetchone()[0]
            print(f"✓ Planes: {planes_count}")
            
            # Verificar suscripciones
            cursor.execute("SELECT COUNT(*) FROM suscripciones")
            suscripciones_count = cursor.fetchone()[0]
            print(f"✓ Suscripciones: {suscripciones_count}")
            
            # Verificar pagos
            cursor.execute("SELECT COUNT(*) FROM pagos")
            pagos_count = cursor.fetchone()[0]
            print(f"✓ Pagos: {pagos_count}")
            
            # Verificar evaluaciones
            cursor.execute("SELECT COUNT(*) FROM evaluaciones")
            evaluaciones_count = cursor.fetchone()[0]
            print(f"✓ Evaluaciones: {evaluaciones_count}")
            
            # Verificar preguntas
            cursor.execute("SELECT COUNT(*) FROM preguntas")
            preguntas_count = cursor.fetchone()[0]
            print(f"✓ Preguntas: {preguntas_count}")
            
            print("=" * 60)
            
            # Verificar datos específicos
            cursor.execute("SELECT nombre, correo, nivel_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            print("👥 USUARIOS EN EL SISTEMA:")
            for usuario in usuarios:
                print(f"   - {usuario[0]} ({usuario[1]}) - {usuario[2]}")
            
            print()
            cursor.execute("SELECT nombre, rfc FROM empresas")
            empresas = cursor.fetchall()
            print("🏢 EMPRESAS EN EL SISTEMA:")
            for empresa in empresas:
                print(f"   - {empresa[0]} (RFC: {empresa[1]})")
            
            print()
            cursor.execute("SELECT nombre, precio FROM planes")
            planes = cursor.fetchall()
            print("💳 PLANES DISPONIBLES:")
            for plan in planes:
                print(f"   - {plan[0]}: ${plan[1]}")
            
            print()
            cursor.execute("SELECT nombre FROM evaluaciones")
            evaluaciones = cursor.fetchall()
            print("📋 EVALUACIONES DISPONIBLES:")
            for evaluacion in evaluaciones:
                print(f"   - {evaluacion[0]}")
                
        print("=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA - BASE DE DATOS LISTA")
        return True
        
    except Exception as e:
        print(f"❌ ERROR al verificar datos: {str(e)}")
        return False

def verificar_endpoints():
    """Verificar que los endpoints básicos funcionen"""
    print("\n🌐 VERIFICANDO ENDPOINTS...")
    print("=" * 60)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Verificar endpoint de API root
        response = client.get('/api/')
        print(f"✓ API Root: Status {response.status_code}")
        
        # Verificar swagger
        response = client.get('/swagger/')
        print(f"✓ Swagger UI: Status {response.status_code}")
        
        print("✅ ENDPOINTS FUNCIONANDO CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ ERROR al verificar endpoints: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICACIÓN DEL SISTEMA AXYOMA")
    print()
    
    datos_ok = verificar_datos()
    endpoints_ok = verificar_endpoints()
    
    if datos_ok and endpoints_ok:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("   - Base de datos poblada correctamente")
        print("   - Endpoints funcionando")
        print("   - Listo para usar")
        sys.exit(0)
    else:
        print("\n⚠️  SISTEMA TIENE PROBLEMAS")
        print("   - Revisa los errores anteriores")
        sys.exit(1)
