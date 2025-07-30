#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir la asociación del superadmin
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def corregir_superadmin():
    print("🔧 CORRIGIENDO ASOCIACIÓN DE SUPERADMIN")
    print("=" * 50)
    
    try:
        # Obtener el usuario Django 'superadmin'
        django_superadmin = User.objects.get(username='superadmin')
        print(f"✅ Usuario Django 'superadmin': {django_superadmin.email}")
        
        # Obtener el perfil con email superadmin@axyoma.com
        perfil_superadmin = PerfilUsuario.objects.get(correo='superadmin@axyoma.com')
        print(f"✅ PerfilUsuario: {perfil_superadmin.nivel_usuario}")
        print(f"📧 Email: {perfil_superadmin.correo}")
        print(f"👤 Usuario actual: {perfil_superadmin.user.username}")
        
        # Verificar si hay conflicto
        if perfil_superadmin.user.username != 'superadmin':
            print(f"⚠️ El perfil está asociado a '{perfil_superadmin.user.username}' en lugar de 'superadmin'")
            
            # Corregir la asociación
            print("🔄 Corrigiendo asociación...")
            perfil_superadmin.user = django_superadmin
            perfil_superadmin.save()
            print("✅ Asociación corregida")
        else:
            print("✅ La asociación ya es correcta")
        
        # Verificar que el usuario Django tenga los permisos correctos
        if not django_superadmin.is_staff:
            django_superadmin.is_staff = True
            django_superadmin.save()
            print("✅ Permisos de staff agregados")
        
        if not django_superadmin.is_superuser:
            django_superadmin.is_superuser = True
            django_superadmin.save()
            print("✅ Permisos de superuser agregados")
        
        print(f"\n🎯 CONFIGURACIÓN FINAL:")
        print(f"Usuario Django: {django_superadmin.username}")
        print(f"Email Django: {django_superadmin.email}")
        print(f"Staff: {django_superadmin.is_staff}")
        print(f"Superuser: {django_superadmin.is_superuser}")
        print(f"Perfil nivel: {perfil_superadmin.nivel_usuario}")
        print(f"Perfil email: {perfil_superadmin.correo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    corregir_superadmin()
