#!/usr/bin/env python
"""
Script para limpiar suscripciones problemáticas
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

def limpiar_suscripciones():
    """Limpiar suscripciones duplicadas y problemáticas"""
    
    print("🧹 Limpiando suscripciones problemáticas...")
    
    # 1. Verificar y corregir suscripciones duplicadas
    print("\n1. Verificando suscripciones duplicadas...")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        ).order_by('-fecha_creacion')
        
        if suscripciones_activas.count() > 1:
            print(f"   ⚠️ {empresa.nombre} tiene {suscripciones_activas.count()} suscripciones activas")
            
            # Mantener solo la más reciente
            suscripcion_actual = suscripciones_activas.first()
            suscripciones_viejas = suscripciones_activas[1:]
            
            print(f"     ✅ Manteniendo: {suscripcion_actual.plan_suscripcion.nombre}")
            
            for suscripcion_vieja in suscripciones_viejas:
                print(f"     ❌ Desactivando: {suscripcion_vieja.plan_suscripcion.nombre}")
                suscripcion_vieja.status = False
                suscripcion_vieja.save()
        
        elif suscripciones_activas.count() == 1:
            suscripcion = suscripciones_activas.first()
            print(f"   ✅ {empresa.nombre}: {suscripcion.plan_suscripcion.nombre}")
        
        else:
            print(f"   ⚠️ {empresa.nombre}: Sin suscripciones activas")
    
    # 2. Verificar planes disponibles
    print("\n2. Verificando planes disponibles...")
    
    planes = PlanSuscripcion.objects.filter(status=True)
    
    if planes.count() == 0:
        print("   ⚠️ No hay planes activos. Creando planes básicos...")
        
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
        
        print("   ✅ Planes básicos creados")
    
    else:
        print(f"   ✅ {planes.count()} planes activos disponibles")
        for plan in planes:
            print(f"     - ID: {plan.plan_id}, {plan.nombre}: ${plan.precio}")
    
    # 3. Verificar estado final
    print("\n3. Estado final del sistema...")
    
    for empresa in empresas:
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        )
        
        if suscripciones_activas.count() == 1:
            suscripcion = suscripciones_activas.first()
            print(f"   ✅ {empresa.nombre}: {suscripcion.plan_suscripcion.nombre} (ID: {suscripcion.suscripcion_id})")
        elif suscripciones_activas.count() == 0:
            print(f"   ⚠️ {empresa.nombre}: Sin suscripciones activas")
        else:
            print(f"   ❌ {empresa.nombre}: {suscripciones_activas.count()} suscripciones activas (ERROR)")
    
    print("\n🎉 Limpieza completada")

def crear_suscripcion_basica_si_no_existe():
    """Crear suscripción básica para empresas que no tienen ninguna"""
    
    print("\n🔄 Creando suscripciones básicas para empresas sin suscripción...")
    
    plan_basico = PlanSuscripcion.objects.filter(
        nombre__icontains="básico",
        status=True
    ).first()
    
    if not plan_basico:
        plan_basico = PlanSuscripcion.objects.create(
            nombre="Básico",
            descripcion="Plan básico automático",
            duracion=30,
            precio=499.00,
            status=True
        )
        print(f"   ✅ Plan básico creado: {plan_basico.nombre}")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        )
        
        if suscripciones_activas.count() == 0:
            print(f"   🔄 Creando suscripción básica para {empresa.nombre}...")
            
            # Crear suscripción básica
            fecha_inicio = timezone.now().date()
            fecha_fin = fecha_inicio + timedelta(days=plan_basico.duracion)
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan_suscripcion=plan_basico,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado='Activa',
                status=True
            )
            
            # Crear pago automático
            pago = Pago.objects.create(
                suscripcion=suscripcion,
                costo=plan_basico.precio,
                monto_pago=plan_basico.precio,
                estado_pago='Completado',
                fecha_pago=timezone.now(),
                transaccion_id=f"AUTO-{empresa.empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )
            
            print(f"   ✅ Suscripción creada: {suscripcion.suscripcion_id}")

if __name__ == '__main__':
    try:
        limpiar_suscripciones()
        crear_suscripcion_basica_si_no_existe()
        print("\n🎉 ¡Limpieza completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
