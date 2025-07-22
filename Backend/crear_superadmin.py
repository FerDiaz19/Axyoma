#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT ULTRA SIMPLE - Solo crear usuario superadmin
"""

import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def main():
    print("🚀 CREANDO USUARIO SUPERADMIN")
    print("=" * 40)
    
    try:
        # Solo crear usuario sin eliminar
        print("👤 Creando usuario superadmin...")
        
        # Verificar si ya existe
        if User.objects.filter(username='superadmin').exists():
            user = User.objects.get(username='superadmin')
            print("⚠️ Usuario ya existe, actualizando...")
            user.set_password('admin123')
            user.is_staff = True
            user.is_superuser = True
            user.save()
        else:
            user = User.objects.create_user(
                username='superadmin',
                email='admin@axyoma.com',
                password='admin123'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("✅ Usuario Django creado")
        
        # Crear perfil
        print("📋 Creando perfil de usuario...")
        try:
            perfil = PerfilUsuario.objects.get(user=user)
            print("⚠️ Perfil ya existe, actualizando...")
            perfil.nivel_usuario = 'superadmin'
            perfil.save()
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre='Super Admin',
                apellido_paterno='Sistema',
                correo='admin@axyoma.com',
                nivel_usuario='superadmin'
            )
            print("✅ Perfil creado")
        
        # Verificar autenticación
        print("🔑 Verificando autenticación...")
        from django.contrib.auth import authenticate
        test_user = authenticate(username='superadmin', password='admin123')
        if test_user:
            print("✅ Autenticación exitosa")
            if hasattr(test_user, 'perfil'):
                print(f"✅ Perfil vinculado: {test_user.perfil.nivel_usuario}")
            else:
                print("❌ Sin perfil vinculado")
        else:
            print("❌ Autenticación falló")
        
        print("\n" + "=" * 40)
        print("✅ USUARIO CREADO")
        print("📋 CREDENCIALES:")
        print("   Usuario: superadmin")
        print("   Contraseña: admin123")
        print("=" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
