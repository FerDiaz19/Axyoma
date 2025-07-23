#!/usr/bin/env python
"""
Script para crear un superadmin con credenciales por defecto
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario

def crear_superadmin():
    """Crear un superadmin con credenciales por defecto"""
    print("🔑 Creando usuario SuperAdmin...")
    
    try:
        with transaction.atomic():
            # Verificar si ya existe
            if User.objects.filter(username='superadmin').exists():
                print("⚠️ El usuario superadmin ya existe. Actualizando contraseña...")
                user = User.objects.get(username='superadmin')
                user.set_password('1234')
                user.save()
                superadmin = user
            else:
                # Crear usuario
                superadmin = User.objects.create_user(
                    username='superadmin',
                    email='superadmin@axyoma.com',
                    password='1234',
                    first_name='Super',
                    last_name='Admin',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
            
            # Verificar o crear perfil
            try:
                perfil = PerfilUsuario.objects.get(user=superadmin)
                print("✅ Perfil de superadmin ya existe.")
            except PerfilUsuario.DoesNotExist:
                perfil = PerfilUsuario.objects.create(
                    user=superadmin,
                    nombre='Super',
                    apellido_paterno='Admin',
                    correo='superadmin@axyoma.com',
                    nivel_usuario='superadmin',
                    status=True
                )
                print("✅ Perfil de superadmin creado.")
                
            print("\n🎉 Usuario SuperAdmin listo para usar!")
            print("=" * 50)
            print("📝 CREDENCIALES:")
            print(f"   Username: superadmin")
            print(f"   Password: 1234")
            print(f"   Email: superadmin@axyoma.com")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ Error creando superadmin: {str(e)}")

if __name__ == "__main__":
    crear_superadmin()
