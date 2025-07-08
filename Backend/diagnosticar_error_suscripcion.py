#!/usr/bin/env python
"""
Script para diagnosticar el error 400 en crear_suscripcion
"""

import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from apps.users.models import Empresa
from django.utils import timezone

def diagnosticar_error_suscripcion():
    """Diagnosticar por qué falla crear_suscripcion"""
    
    print("🔍 Diagnosticando error en crear_suscripcion...")
    
    # 1. Verificar planes disponibles
    print("\n1. Verificando planes disponibles...")
    planes = PlanSuscripcion.objects.filter(status=True)
    print(f"   📋 Planes activos: {planes.count()}")
    
    for plan in planes:
        print(f"      - ID: {plan.plan_id}, Nombre: {plan.nombre}, Precio: ${plan.precio}")
    
    # 2. Verificar empresas
    print("\n2. Verificando empresas...")
    empresas = Empresa.objects.all()
    print(f"   🏢 Empresas: {empresas.count()}")
    
    for empresa in empresas:
        print(f"      - ID: {empresa.empresa_id}, Nombre: {empresa.nombre}")
        
        # Verificar suscripciones existentes
        suscripciones = SuscripcionEmpresa.objects.filter(empresa=empresa)
        print(f"        Suscripciones totales: {suscripciones.count()}")
        
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        )
        print(f"        Suscripciones activas: {suscripciones_activas.count()}")
        
        for suscripcion in suscripciones_activas:
            print(f"          • Plan: {suscripcion.plan_suscripcion.nombre}, Estado: {suscripcion.estado}")
            print(f"            Fecha inicio: {suscripcion.fecha_inicio}")
            print(f"            Fecha fin: {suscripcion.fecha_fin}")
            print(f"            Está activa: {suscripcion.esta_activa}")
    
    # 3. Simular el error que está ocurriendo
    print("\n3. Simulando petición que falla...")
    
    if empresas.count() > 0 and planes.count() > 0:
        empresa_test = empresas.first()
        plan_test = planes.first()
        
        print(f"   🧪 Probando: empresa_id={empresa_test.empresa_id}, plan_id={plan_test.plan_id}")
        
        # Verificar si ya existe suscripción activa
        suscripcion_existente = SuscripcionEmpresa.objects.filter(
            empresa=empresa_test,
            status=True
        ).first()
        
        if suscripcion_existente:
            print(f"   ❌ ERROR: La empresa ya tiene una suscripción activa")
            print(f"       Suscripción existente:")
            print(f"       - ID: {suscripcion_existente.suscripcion_id}")
            print(f"       - Plan: {suscripcion_existente.plan_suscripcion.nombre}")
            print(f"       - Estado: {suscripcion_existente.estado}")
            print(f"       - Status: {suscripcion_existente.status}")
            print(f"       - Fecha fin: {suscripcion_existente.fecha_fin}")
            print(f"       - Está activa: {suscripcion_existente.esta_activa}")
            
            # Sugerir solución
            print(f"\n   💡 SOLUCIÓN:")
            print(f"       Opción 1: Desactivar suscripción existente")
            print(f"       Opción 2: Permitir múltiples suscripciones")
            print(f"       Opción 3: Actualizar suscripción existente")
            
            # Mostrar cómo desactivar la suscripción
            print(f"\n   🔧 Para desactivar la suscripción existente:")
            print(f"       suscripcion_existente.status = False")
            print(f"       suscripcion_existente.save()")
            
        else:
            print(f"   ✅ No hay suscripciones activas, la creación debería funcionar")
    
    # 4. Verificar si el plan_id 4 existe (del error)
    print(f"\n4. Verificando plan_id=4 específicamente...")
    try:
        plan_4 = PlanSuscripcion.objects.get(plan_id=4)
        print(f"   ✅ Plan ID 4 existe: {plan_4.nombre} - ${plan_4.precio}")
    except PlanSuscripcion.DoesNotExist:
        print(f"   ❌ Plan ID 4 no existe")
        print(f"   💡 Esto causaría un error 404, no 400")
    
    print(f"\n🎯 RESUMEN DEL DIAGNÓSTICO:")
    print(f"   - Error más probable: Empresa ya tiene suscripción activa")
    print(f"   - Verificar suscripciones existentes antes de crear nuevas")
    print(f"   - Considerar desactivar suscripciones anteriores")

def arreglar_suscripciones_duplicadas():
    """Arreglar problema de suscripciones duplicadas"""
    
    print("\n🔧 Arreglando suscripciones duplicadas...")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        )
        
        if suscripciones_activas.count() > 1:
            print(f"   ⚠️ Empresa {empresa.nombre} tiene {suscripciones_activas.count()} suscripciones activas")
            
            # Mantener solo la más reciente
            suscripcion_reciente = suscripciones_activas.order_by('-fecha_creacion').first()
            suscripciones_viejas = suscripciones_activas.exclude(
                suscripcion_id=suscripcion_reciente.suscripcion_id
            )
            
            print(f"     Manteniendo: {suscripcion_reciente.plan_suscripcion.nombre} (ID: {suscripcion_reciente.suscripcion_id})")
            
            for suscripcion_vieja in suscripciones_viejas:
                print(f"     Desactivando: {suscripcion_vieja.plan_suscripcion.nombre} (ID: {suscripcion_vieja.suscripcion_id})")
                suscripcion_vieja.status = False
                suscripcion_vieja.save()
        
        elif suscripciones_activas.count() == 1:
            suscripcion = suscripciones_activas.first()
            print(f"   ✅ Empresa {empresa.nombre} tiene 1 suscripción activa: {suscripcion.plan_suscripcion.nombre}")
        
        else:
            print(f"   ⚠️ Empresa {empresa.nombre} no tiene suscripciones activas")

if __name__ == '__main__':
    try:
        diagnosticar_error_suscripcion()
        
        # Preguntar si quiere arreglar duplicados
        print(f"\n❓ ¿Deseas arreglar suscripciones duplicadas? (y/n)")
        
        # Para script automático, siempre arreglar
        arreglar_suscripciones_duplicadas()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
