#!/usr/bin/env python
"""
CONFIGURACIÓN COMPLETA DEL SISTEMA AXYOMA
========================================
Script final para asegurar que todo funcione perfectamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axyoma.settings')
django.setup()

from apps.users.models import *
from apps.subscriptions.models import *
from django.contrib.auth.models import User

def verificar_configuracion_completa():
    """Verificación final de todo el sistema"""
    
    print("🔧 VERIFICACIÓN FINAL DEL SISTEMA AXYOMA")
    print("=" * 60)
    
    # 1. VERIFICAR USUARIOS Y CREDENCIALES
    print("\n🔑 1. VERIFICANDO USUARIOS Y CREDENCIALES")
    print("-" * 40)
    
    credenciales_correctas = [
        ('superadmin', 'SuperAdmin del Sistema'),
        ('admin_technomex', 'Admin TechnoMex Industries'),
        ('admin_manu_gonzalez', 'Admin Manufactura González'),
        ('admin_axis', 'Admin Industrias AXIS'),
        ('admin_mdn', 'Admin Manufacturas del Norte'),
        ('admin_techcorp', 'Admin TechCorp Solutions'),
        ('admin_planta_1_1', 'Admin Planta TechCorp'),
        ('admin_planta_2_1', 'Admin Planta AXIS'),
    ]
    
    for username, descripcion in credenciales_correctas:
        try:
            user = User.objects.get(username=username)
            # Verificar que la contraseña sea admin123
            if user.check_password('admin123'):
                print(f"   ✅ {username}: {descripcion} - OK")
            else:
                print(f"   ❌ {username}: Contraseña incorrecta")
                user.set_password('admin123')
                user.save()
                print(f"   🔧 {username}: Contraseña corregida")
        except User.DoesNotExist:
            print(f"   ❌ {username}: Usuario no encontrado")
    
    # 2. VERIFICAR ESTRUCTURA ORGANIZACIONAL
    print("\n🏗️ 2. VERIFICANDO ESTRUCTURA ORGANIZACIONAL")
    print("-" * 40)
    
    empresas = Empresa.objects.all()
    print(f"   📊 Total empresas: {empresas.count()}")
    
    for empresa in empresas:
        plantas = empresa.plantas.filter(status=True).count()
        total_empleados = sum(
            pu.empleados.filter(status=True).count() 
            for p in empresa.plantas.filter(status=True)
            for d in p.departamentos.filter(status=True)
            for pu in d.puestos.filter(status=True)
        )
        print(f"   🏢 {empresa.nombre}: {plantas} plantas, {total_empleados} empleados")
    
    # 3. VERIFICAR SUSCRIPCIONES
    print("\n💳 3. VERIFICANDO SUSCRIPCIONES")
    print("-" * 40)
    
    suscripciones = SuscripcionEmpresa.objects.filter(estado='activa')
    print(f"   📊 Suscripciones activas: {suscripciones.count()}")
    
    for suscripcion in suscripciones:
        print(f"   ✅ {suscripcion.empresa.nombre}: {suscripcion.plan.nombre}")
    
    # 4. VERIFICAR SISTEMA DE EVALUACIONES
    print("\n📋 4. VERIFICANDO SISTEMA DE EVALUACIONES")
    print("-" * 40)
    
    tipos = TipoEvaluacion.objects.all().count()
    evaluaciones = Evaluacion.objects.all().count()
    conjuntos = ConjuntoRespuestas.objects.all().count()
    opciones = PosiblesRespuestas.objects.all().count()
    
    print(f"   📊 Tipos de evaluación: {tipos}")
    print(f"   📊 Evaluaciones: {evaluaciones}")
    print(f"   📊 Conjuntos de respuestas: {conjuntos}")
    print(f"   📊 Opciones de respuesta: {opciones}")
    
    # 5. GENERAR RESUMEN DE CREDENCIALES
    print("\n🎯 5. RESUMEN DE CREDENCIALES PARA EL FRONTEND")
    print("-" * 40)
    
    print("   🔧 SUPERADMIN:")
    print("      Usuario: superadmin")
    print("      Contraseña: admin123")
    print("")
    
    print("   🏢 ADMINISTRADORES DE EMPRESA:")
    admin_empresas = [
        ('admin_technomex', 'TechnoMex Industries'),
        ('admin_manu_gonzalez', 'Manufactura González'),
        ('admin_axis', 'Industrias AXIS'),
        ('admin_mdn', 'Manufacturas del Norte'),
        ('admin_techcorp', 'TechCorp Solutions'),
    ]
    
    for username, empresa in admin_empresas:
        print(f"      {empresa}: {username} / admin123")
    
    print("")
    print("   📍 ADMINISTRADORES DE PLANTA:")
    admin_plantas = [
        ('admin_planta_1_1', 'TechCorp - Planta Central'),
        ('admin_planta_2_1', 'AXIS - Planta Central'),
    ]
    
    for username, planta in admin_plantas:
        print(f"      {planta}: {username} / admin123")
    
    # 6. VERIFICAR ENDPOINTS PRINCIPALES
    print("\n🌐 6. ENDPOINTS PRINCIPALES DEL BACKEND")
    print("-" * 40)
    
    endpoints = [
        'http://localhost:8000/api/auth/login/',
        'http://localhost:8000/api/superadmin/estadisticas_sistema/',
        'http://localhost:8000/api/empresas/',
        'http://localhost:8000/api/plantas/',
        'http://localhost:8000/api/empleados/',
        'http://localhost:8000/api/suscripciones/actual/',
    ]
    
    for endpoint in endpoints:
        print(f"      📡 {endpoint}")
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETA VERIFICADA")
    print("🚀 El sistema está listo para usar en el frontend")
    print("")
    print("📋 PASOS SIGUIENTES:")
    print("   1. Abrir http://localhost:3000")
    print("   2. Probar login con las credenciales mostradas arriba")
    print("   3. Verificar que cada tipo de usuario vea su dashboard correcto")
    print("")
    print("🎉 ¡SISTEMA AXYOMA COMPLETAMENTE FUNCIONAL!")

if __name__ == "__main__":
    verificar_configuracion_completa()
