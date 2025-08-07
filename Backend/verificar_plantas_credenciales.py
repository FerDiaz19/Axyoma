#!/usr/bin/env python3
"""
Script para verificar plantas y sus usuarios administradores
"""
import os
import sys
import django

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Planta, AdminPlanta, PerfilUsuario
from django.contrib.auth.models import User

print("🔍 Verificando plantas existentes y sus credenciales...")

# Obtener todas las plantas
plantas = Planta.objects.all().order_by('-planta_id')

print(f"📊 Total de plantas: {plantas.count()}")
print("-" * 80)

for planta in plantas[:10]:  # Mostrar últimas 10 plantas
    print(f"🏭 Planta: {planta.nombre} (ID: {planta.planta_id})")
    print(f"   📍 Dirección: {planta.direccion}")
    print(f"   🏢 Empresa: {planta.empresa.nombre}")
    print(f"    Status: {'Activa' if planta.status else 'Suspendida'}")
    
    # Verificar si tiene administrador
    admin_plantas = AdminPlanta.objects.filter(planta=planta)
    
    if admin_plantas.exists():
        print(f"   👤 Administradores ({admin_plantas.count()}):")
        for admin_planta in admin_plantas:
            usuario = admin_planta.usuario
            django_user = usuario.user
            print(f"      - Usuario: {django_user.username}")
            print(f"      - Email: {django_user.email}")
            print(f"      - Nombre: {usuario.nombre} {usuario.apellido_paterno}")
            print(f"      - Status: {'Activo' if admin_planta.status else 'Inactivo'}")
    else:
        print(f"   ❌ SIN ADMINISTRADOR ASIGNADO")
    
    print("-" * 80)
