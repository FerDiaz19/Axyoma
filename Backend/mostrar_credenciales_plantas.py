#!/usr/bin/env python
"""
Script para mostrar todas las credenciales de usuarios de planta existentes
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import AdminPlanta

def mostrar_credenciales():
    print("🏭 CREDENCIALES DE USUARIOS DE PLANTA")
    print("=" * 60)
    
    admin_plantas = AdminPlanta.objects.filter(status=True).select_related('usuario', 'planta')
    
    if not admin_plantas.exists():
        print("❌ No hay usuarios de planta registrados")
        return
    
    for i, admin_planta in enumerate(admin_plantas, 1):
        print(f"\n{i}. PLANTA: {admin_planta.planta.nombre}")
        print(f"   📧 Usuario: {admin_planta.usuario.correo}")
        print(f"   🔑 Contraseña: {admin_planta.password_temporal}")
        print(f"   🏢 Empresa: {admin_planta.planta.empresa.nombre}")
        print(f"   📅 Fecha asignación: {admin_planta.fecha_asignacion.strftime('%Y-%m-%d %H:%M')}")
        print(f"   🆔 ID AdminPlanta: {admin_planta.id}")
    
    print(f"\n📊 Total: {admin_plantas.count()} usuarios de planta")
    print("\n💡 Estas credenciales pueden usarse para login en el sistema")

if __name__ == '__main__':
    mostrar_credenciales()
