#!/usr/bin/env python
"""
Script para limpiar suscripciones duplicadas y corregir problemas
"""

import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.subscriptions.models import Pago, SuscripcionEmpresa, PlanSuscripcion
from apps.users.models import Empresa, PerfilUsuario
from django.contrib.auth.models import User
from django.utils import timezone

def limpiar_suscripciones_duplicadas():
    """Limpiar suscripciones duplicadas dejando solo la más reciente por empresa"""
    
    print("🧹 LIMPIANDO SUSCRIPCIONES DUPLICADAS")
    print("=" * 60)
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        print(f"🏢 Procesando empresa: {empresa.nombre}")
        
        # Obtener suscripciones activas de la empresa
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True,
            estado='Activa'
        ).order_by('-fecha_inicio')
        
        print(f"   📊 Suscripciones activas: {suscripciones_activas.count()}")
        
        if suscripciones_activas.count() > 1:
            print("   ⚠️  Múltiples suscripciones activas encontradas")
            
            # Mantener solo la más reciente
            suscripcion_principal = suscripciones_activas.first()
            suscripciones_duplicadas = suscripciones_activas[1:]
            
            print(f"   ✅ Manteniendo: {suscripcion_principal.plan_suscripcion.nombre} (ID: {suscripcion_principal.suscripcion_id})")
            
            for suscripcion_duplicada in suscripciones_duplicadas:
                print(f"   🗑️  Desactivando: {suscripcion_duplicada.plan_suscripcion.nombre} (ID: {suscripcion_duplicada.suscripcion_id})")
                
                # Desactivar en lugar de eliminar para mantener historial
                suscripcion_duplicada.status = False
                suscripcion_duplicada.estado = 'Cancelada'
                suscripcion_duplicada.save()
        
        elif suscripciones_activas.count() == 1:
            print("   ✅ Una suscripción activa (correcto)")
        else:
            print("   ❌ No hay suscripciones activas")
        
        print()

def corregir_pagos_sin_usuario():
    """Corregir pagos que no tienen usuario asignado"""
    
    print("🔧 CORRIGIENDO PAGOS SIN USUARIO")
    print("=" * 60)
    
    pagos_sin_usuario = Pago.objects.filter(usuario__isnull=True)
    print(f"📊 Pagos sin usuario: {pagos_sin_usuario.count()}")
    
    for pago in pagos_sin_usuario:
        empresa = pago.suscripcion.empresa
        admin_user = empresa.administrador.user if empresa.administrador else None
        
        if admin_user:
            print(f"🔄 Asignando usuario {admin_user.username} al pago {pago.pago_id}")
            pago.usuario = admin_user
            pago.save()
        else:
            print(f"⚠️  No se pudo asignar usuario al pago {pago.pago_id}")

def verificar_correcciones():
    """Verificar que las correcciones fueron exitosas"""
    
    print("🔍 VERIFICANDO CORRECCIONES")
    print("=" * 60)
    
    # Verificar empresas con múltiples suscripciones activas
    empresas_con_multiples = 0
    
    for empresa in Empresa.objects.all():
        suscripciones_activas = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True,
            estado='Activa'
        ).count()
        
        if suscripciones_activas > 1:
            empresas_con_multiples += 1
            print(f"⚠️  {empresa.nombre} tiene {suscripciones_activas} suscripciones activas")
    
    print(f"📊 Empresas con múltiples suscripciones activas: {empresas_con_multiples}")
    
    # Verificar pagos sin usuario
    pagos_sin_usuario = Pago.objects.filter(usuario__isnull=True).count()
    print(f"📊 Pagos sin usuario: {pagos_sin_usuario}")
    
    # Verificar propiedades de empresas
    print("\n🔍 Verificando propiedades de empresas:")
    
    for empresa in Empresa.objects.all():
        if empresa.suscripcion_activa:
            print(f"✅ {empresa.nombre}: {empresa.suscripcion_activa.plan_suscripcion.nombre} - {empresa.dias_restantes_suscripcion} días")
        else:
            print(f"❌ {empresa.nombre}: Sin suscripción activa")

def mostrar_resumen_final():
    """Mostrar resumen final después de las correcciones"""
    
    print("\n📊 RESUMEN FINAL")
    print("=" * 60)
    
    # Estadísticas generales
    empresas_total = Empresa.objects.count()
    suscripciones_activas = SuscripcionEmpresa.objects.filter(status=True, estado='Activa').count()
    pagos_total = Pago.objects.count()
    pagos_con_usuario = Pago.objects.filter(usuario__isnull=False).count()
    
    print(f"🏢 Empresas: {empresas_total}")
    print(f"📋 Suscripciones activas: {suscripciones_activas}")
    print(f"💰 Pagos totales: {pagos_total}")
    print(f"👤 Pagos con usuario: {pagos_con_usuario}")
    
    # Tabla de suscripciones para dashboard
    print("\n📋 TABLA PARA DASHBOARD SUPERADMIN:")
    print("-" * 80)
    print("ID | Empresa               | Plan        | Precio   | Estado | Días | Usuario")
    print("-" * 80)
    
    for suscripcion in SuscripcionEmpresa.objects.filter(status=True, estado='Activa').order_by('-fecha_inicio'):
        ultimo_pago = Pago.objects.filter(suscripcion=suscripcion).order_by('-fecha_pago').first()
        usuario_pago = ultimo_pago.usuario.username if ultimo_pago and ultimo_pago.usuario else "N/A"
        
        print(f"{suscripcion.suscripcion_id:2d} | {suscripcion.empresa.nombre[:20]:20s} | {suscripcion.plan_suscripcion.nombre[:10]:10s} | ${suscripcion.plan_suscripcion.precio:7.2f} | {suscripcion.estado[:6]:6s} | {suscripcion.dias_restantes:4d} | {usuario_pago}")

if __name__ == '__main__':
    try:
        print("🚀 Iniciando limpieza y corrección de suscripciones...")
        print()
        
        limpiar_suscripciones_duplicadas()
        corregir_pagos_sin_usuario()
        verificar_correcciones()
        mostrar_resumen_final()
        
        print("\n🎉 ¡Limpieza y corrección completadas!")
        
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
