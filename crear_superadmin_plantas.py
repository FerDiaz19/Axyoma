#!/usr/bin/env python3
"""
Script para crear/verificar usuario superadmin y asegurar acceso
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def main():
    print("🔍 VERIFICANDO USUARIOS Y CREANDO SUPERADMIN")
    print("=" * 50)

    # 1. Listar usuarios existentes
    print("\n1. 👥 Usuarios existentes:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username} | superuser: {user.is_superuser} | staff: {user.is_staff}")

    # 2. Crear/verificar superadmin
    print("\n2. 🔑 Verificando superadmin...")
    
    superadmin_username = 'superadmin'
    superadmin_password = 'admin123'
    
    try:
        superadmin = User.objects.get(username=superadmin_username)
        print(f"✅ Superadmin encontrado: {superadmin.username}")
        
        # Asegurar que tenga permisos de superuser
        if not superadmin.is_superuser:
            superadmin.is_superuser = True
            superadmin.is_staff = True
            superadmin.save()
            print("🔧 Permisos de superuser activados")
        
    except User.DoesNotExist:
        print("❌ Superadmin no encontrado. Creando...")
        superadmin = User.objects.create_superuser(
            username=superadmin_username,
            email='superadmin@test.com',
            password=superadmin_password
        )
        print(f"✅ Superadmin creado: {superadmin.username}")

    # 3. Crear/verificar token
    print("\n3. 🎫 Verificando token...")
    token, created = Token.objects.get_or_create(user=superadmin)
    if created:
        print(f"✅ Token creado: {token.key}")
    else:
        print(f"✅ Token existente: {token.key}")

    # 4. Mostrar credenciales
    print("\n4. 🔐 CREDENCIALES PARA LOGIN:")
    print(f"   Username: {superadmin_username}")
    print(f"   Password: {superadmin_password}")
    print(f"   Token: {token.key}")
    
    print("\n✅ LISTO PARA USAR!")
    print("🎯 Ahora puedes hacer login con estas credenciales para ver el botón de eliminar")

if __name__ == '__main__':
    main()
