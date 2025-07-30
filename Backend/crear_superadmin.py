#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear o verificar el usuario SuperAdmin
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

def crear_superadmin():
    print("👤 CONFIGURACIÓN DE SUPERADMIN")
    print("=" * 40)
    
    try:
        # Buscar usuario existente
        try:
            superadmin = User.objects.get(username='superadmin')
            print(f"✅ Usuario superadmin ya existe: {superadmin.email}")
        except User.DoesNotExist:
            print("📝 Creando usuario superadmin...")
            superadmin = User.objects.create_user(
                username='superadmin',
                email='superadmin@axyoma.com',
                password='1234',
                first_name='Super',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )
            print("✅ Usuario superadmin creado")
        
        # Verificar perfil
        try:
            perfil = PerfilUsuario.objects.get(user=superadmin)
            print(f"✅ Perfil existe: {perfil.nivel_usuario}")
            if perfil.nivel_usuario != 'superadmin':
                perfil.nivel_usuario = 'superadmin'
                perfil.save()
                print("✅ Nivel actualizado a superadmin")
        except PerfilUsuario.DoesNotExist:
            print("📝 Creando perfil de superadmin...")
            perfil = PerfilUsuario.objects.create(
                user=superadmin,
                nombre='Super',
                apellido_paterno='Admin',
                correo='superadmin@axyoma.com',
                nivel_usuario='superadmin'
            )
            print("✅ Perfil de superadmin creado")
        
        print(f"\n🎯 CREDENCIALES DE ACCESO:")
        print(f"Usuario: superadmin")
        print(f"Password: 1234")
        print(f"Nivel: {perfil.nivel_usuario}")
        print(f"Email: {superadmin.email}")
        
        # Verificar otros usuarios admin
        print(f"\n👥 OTROS USUARIOS ADMIN:")
        admins = User.objects.filter(perfil__nivel_usuario__in=['admin-empresa', 'admin-planta'])
        for admin in admins:
            perfil_admin = admin.perfil
            print(f"- {admin.username}: {perfil_admin.nivel_usuario}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al configurar superadmin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    crear_superadmin()
