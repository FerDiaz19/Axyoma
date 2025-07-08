#!/usr/bin/env python
"""
Script para corregir pagos existentes que no tengan usuario asignado
"""

import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.subscriptions.models import Pago, SuscripcionEmpresa
from apps.users.models import Empresa, PerfilUsuario
from django.contrib.auth.models import User

def corregir_pagos_sin_usuario():
    """Corregir pagos que no tengan usuario asignado"""
    
    print("🔧 Corrigiendo pagos sin usuario asignado...")
    
    # Buscar pagos sin usuario
    pagos_sin_usuario = Pago.objects.filter(usuario__isnull=True)
    print(f"📊 Pagos sin usuario encontrados: {pagos_sin_usuario.count()}")
    
    if pagos_sin_usuario.count() == 0:
        print("✅ No hay pagos sin usuario que corregir")
        return
    
    pagos_corregidos = 0
    
    for pago in pagos_sin_usuario:
        try:
            # Obtener el administrador de la empresa de la suscripción
            empresa = pago.suscripcion.empresa
            admin_user = empresa.administrador.user if empresa.administrador else None
            
            if admin_user:
                print(f"🔄 Asignando usuario {admin_user.username} al pago {pago.pago_id} de ${pago.monto_pago}")
                pago.usuario = admin_user
                pago.save()
                pagos_corregidos += 1
            else:
                print(f"⚠️  No se pudo encontrar administrador para la empresa {empresa.nombre} (Pago ID: {pago.pago_id})")
                
        except Exception as e:
            print(f"❌ Error corrigiendo pago {pago.pago_id}: {str(e)}")
            
    print(f"\n✅ Pagos corregidos: {pagos_corregidos}")
    print(f"⚠️  Pagos sin corregir: {pagos_sin_usuario.count() - pagos_corregidos}")

def verificar_correcciones():
    """Verificar las correcciones realizadas"""
    
    print("\n🔍 Verificando correcciones...")
    
    # Contar pagos con y sin usuario
    pagos_con_usuario = Pago.objects.filter(usuario__isnull=False).count()
    pagos_sin_usuario = Pago.objects.filter(usuario__isnull=True).count()
    total_pagos = Pago.objects.count()
    
    print(f"📊 Resumen de pagos:")
    print(f"   • Total pagos: {total_pagos}")
    print(f"   • Pagos con usuario: {pagos_con_usuario}")
    print(f"   • Pagos sin usuario: {pagos_sin_usuario}")
    
    # Mostrar algunos ejemplos de pagos con usuario
    print(f"\n📝 Ejemplos de pagos con usuario:")
    pagos_ejemplo = Pago.objects.filter(usuario__isnull=False)[:5]
    
    for pago in pagos_ejemplo:
        print(f"   • Pago {pago.pago_id}: ${pago.monto_pago} - {pago.usuario.username} - {pago.suscripcion.empresa.nombre}")

if __name__ == '__main__':
    try:
        print("🚀 Iniciando corrección de pagos sin usuario...")
        
        corregir_pagos_sin_usuario()
        verificar_correcciones()
        
        print("\n🎉 ¡Corrección completada!")
        
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
