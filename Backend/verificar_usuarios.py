#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar usuarios existentes
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

def verificar_usuarios():
    print("👥 USUARIOS EXISTENTES")
    print("=" * 40)
    
    # Django Users
    print("📋 Usuarios Django:")
    django_users = User.objects.all()
    for user in django_users:
        print(f"- {user.username}: {user.email}")
    
    print("\n📋 Perfiles de Usuario:")
    perfiles = PerfilUsuario.objects.all()
    for perfil in perfiles:
        user_info = ""
        try:
            user_info = f" (Django: {perfil.user.username})"
        except:
            user_info = " (Sin usuario Django)"
        print(f"- {perfil.correo}: {perfil.nivel_usuario}{user_info}")
    
    # Buscar superadmin
    print("\n🔍 BUSCANDO SUPERADMIN:")
    
    # Por Django User
    try:
        django_superadmin = User.objects.get(username='superadmin')
        print(f"✅ Django User 'superadmin' existe: {django_superadmin.email}")
        
        # Buscar perfil asociado
        try:
            perfil = PerfilUsuario.objects.get(user=django_superadmin)
            print(f"✅ Perfil asociado: {perfil.nivel_usuario}")
        except PerfilUsuario.DoesNotExist:
            print("❌ No tiene perfil asociado")
            
    except User.DoesNotExist:
        print("❌ No existe Django User 'superadmin'")
    
    # Por email en PerfilUsuario
    try:
        perfil_superadmin = PerfilUsuario.objects.get(correo='superadmin@axyoma.com')
        print(f"✅ PerfilUsuario con email 'superadmin@axyoma.com': {perfil_superadmin.nivel_usuario}")
        
        try:
            django_user = perfil_superadmin.user
            print(f"✅ Usuario Django asociado: {django_user.username}")
        except:
            print("❌ No tiene usuario Django asociado")
            
    except PerfilUsuario.DoesNotExist:
        print("❌ No existe PerfilUsuario con email 'superadmin@axyoma.com'")

if __name__ == '__main__':
    verificar_usuarios()
