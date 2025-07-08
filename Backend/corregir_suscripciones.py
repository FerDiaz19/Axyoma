#!/usr/bin/env python
"""
Script para diagnosticar y corregir problemas de información faltante en suscripciones
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from apps.users.models import Empresa
from django.utils import timezone
from datetime import timedelta

def diagnosticar_suscripciones_problematicas():
    """Diagnosticar suscripciones con información faltante"""
    
    print("🔍 Diagnosticando suscripciones con información faltante...")
    
    # 1. Verificar todas las suscripciones
    print("\n1. Verificando todas las suscripciones...")
    
    suscripciones = SuscripcionEmpresa.objects.all()
    print(f"   📊 Total suscripciones: {suscripciones.count()}")
    
    problematicas = []
    
    for suscripcion in suscripciones:
        tiene_problema = False
        problemas = []
        
        # Verificar empresa
        if not suscripcion.empresa:
            problemas.append("Sin empresa")
            tiene_problema = True
        elif not suscripcion.empresa.nombre:
            problemas.append("Empresa sin nombre")
            tiene_problema = True
        
        # Verificar plan
        if not suscripcion.plan_suscripcion:
            problemas.append("Sin plan")
            tiene_problema = True
        elif not suscripcion.plan_suscripcion.nombre:
            problemas.append("Plan sin nombre")
            tiene_problema = True
        
        # Verificar precio
        if suscripcion.plan_suscripcion and suscripcion.plan_suscripcion.precio == 0:
            problemas.append("Precio $0.00")
            tiene_problema = True
        
        if tiene_problema:
            problematicas.append({
                'suscripcion': suscripcion,
                'problemas': problemas
            })
            
        print(f"   ID: {suscripcion.suscripcion_id}")
        print(f"      Empresa: {suscripcion.empresa.nombre if suscripcion.empresa else 'NONE'}")
        print(f"      Plan: {suscripcion.plan_suscripcion.nombre if suscripcion.plan_suscripcion else 'NONE'}")
        print(f"      Precio: ${suscripcion.plan_suscripcion.precio if suscripcion.plan_suscripcion else 'NONE'}")
        print(f"      Estado: {suscripcion.estado}")
        print(f"      Status: {suscripcion.status}")
        if problemas:
            print(f"      ⚠️ Problemas: {', '.join(problemas)}")
        print()
    
    return problematicas

def diagnosticar_planes():
    """Diagnosticar planes de suscripción"""
    
    print("\n2. Verificando planes de suscripción...")
    
    planes = PlanSuscripcion.objects.all()
    print(f"   📋 Total planes: {planes.count()}")
    
    for plan in planes:
        print(f"   ID: {plan.plan_id}")
        print(f"      Nombre: {plan.nombre}")
        print(f"      Precio: ${plan.precio}")
        print(f"      Duración: {plan.duracion} días")
        print(f"      Status: {plan.status}")
        print()
    
    return planes

def diagnosticar_empresas():
    """Diagnosticar empresas"""
    
    print("\n3. Verificando empresas...")
    
    empresas = Empresa.objects.all()
    print(f"   🏢 Total empresas: {empresas.count()}")
    
    for empresa in empresas:
        print(f"   ID: {empresa.empresa_id}")
        print(f"      Nombre: {empresa.nombre}")
        print(f"      RFC: {empresa.rfc}")
        print(f"      Status: {empresa.status}")
        print()
    
    return empresas

def corregir_suscripciones_problematicas():
    """Corregir suscripciones con información faltante"""
    
    print("\n4. Corrigiendo suscripciones problemáticas...")
    
    # Obtener planes válidos
    planes_validos = PlanSuscripcion.objects.filter(status=True, precio__gt=0)
    
    if planes_validos.count() == 0:
        print("   ⚠️ No hay planes válidos. Creando planes básicos...")
        
        plan_basico = PlanSuscripcion.objects.create(
            nombre="Básico",
            descripcion="Plan básico para empresas pequeñas",
            duracion=30,
            precio=499.00,
            status=True
        )
        
        plan_profesional = PlanSuscripcion.objects.create(
            nombre="Profesional", 
            descripcion="Plan profesional para empresas medianas",
            duracion=30,
            precio=999.00,
            status=True
        )
        
        plan_empresarial = PlanSuscripcion.objects.create(
            nombre="Empresarial",
            descripcion="Plan empresarial para grandes corporaciones",
            duracion=30,
            precio=1999.00,
            status=True
        )
        
        planes_validos = [plan_basico, plan_profesional, plan_empresarial]
        print("   ✅ Planes básicos creados")
    
    # Obtener empresas válidas
    empresas_validas = Empresa.objects.filter(status=True)
    
    # Corregir suscripciones problemáticas
    suscripciones_problematicas = SuscripcionEmpresa.objects.filter(
        plan_suscripcion__precio=0
    )
    
    print(f"   🔧 Corrigiendo {suscripciones_problematicas.count()} suscripciones problemáticas...")
    
    for suscripcion in suscripciones_problematicas:
        print(f"      Corrigiendo suscripción ID: {suscripcion.suscripcion_id}")
        
        # Asignar empresa si falta
        if not suscripcion.empresa and empresas_validas.count() > 0:
            suscripcion.empresa = empresas_validas.first()
            print(f"         Asignada empresa: {suscripcion.empresa.nombre}")
        
        # Asignar plan si falta o tiene precio 0
        if not suscripcion.plan_suscripcion or suscripcion.plan_suscripcion.precio == 0:
            plan_valido = planes_validos[0] if isinstance(planes_validos, list) else planes_validos.first()
            suscripcion.plan_suscripcion = plan_valido
            print(f"         Asignado plan: {plan_valido.nombre} (${plan_valido.precio})")
        
        # Corregir fechas si es necesario
        if not suscripcion.fecha_inicio:
            suscripcion.fecha_inicio = timezone.now().date()
        
        if not suscripcion.fecha_fin:
            suscripcion.fecha_fin = suscripcion.fecha_inicio + timedelta(days=suscripcion.plan_suscripcion.duracion)
        
        suscripcion.save()
        print(f"         ✅ Suscripción corregida")

def verificar_estado_final():
    """Verificar el estado final después de las correcciones"""
    
    print("\n5. Verificando estado final...")
    
    suscripciones = SuscripcionEmpresa.objects.all()
    
    for suscripcion in suscripciones:
        print(f"   ID: {suscripcion.suscripcion_id}")
        print(f"      Empresa: {suscripcion.empresa.nombre if suscripcion.empresa else 'NONE'}")
        print(f"      Plan: {suscripcion.plan_suscripcion.nombre if suscripcion.plan_suscripcion else 'NONE'}")
        print(f"      Precio: ${suscripcion.plan_suscripcion.precio if suscripcion.plan_suscripcion else 'NONE'}")
        print(f"      Estado: {suscripcion.estado}")
        print(f"      Fecha inicio: {suscripcion.fecha_inicio}")
        print(f"      Fecha fin: {suscripcion.fecha_fin}")
        print(f"      Días restantes: {suscripcion.dias_restantes}")
        print(f"      Está activa: {suscripcion.esta_activa}")
        print()

if __name__ == '__main__':
    try:
        print("🔧 Iniciando diagnóstico y corrección de suscripciones...")
        
        # Diagnosticar problemas
        problematicas = diagnosticar_suscripciones_problematicas()
        planes = diagnosticar_planes()
        empresas = diagnosticar_empresas()
        
        # Corregir problemas
        if problematicas:
            print(f"\n⚠️ Se encontraron {len(problematicas)} suscripciones problemáticas")
            corregir_suscripciones_problematicas()
        else:
            print("\n✅ No se encontraron suscripciones problemáticas")
        
        # Verificar estado final
        verificar_estado_final()
        
        print("\n🎉 Diagnóstico y corrección completados")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
