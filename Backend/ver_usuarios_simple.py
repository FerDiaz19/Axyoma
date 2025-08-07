#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario
from django.contrib.auth import authenticate

def verificar_usuarios_simple():
    """
    Verificación simple de usuarios
    """
    print("🔍 VERIFICANDO USUARIOS...")
    
    # Verificar todos los usuarios
    usuarios = User.objects.all()
    print(f"\n📊 Total usuarios en sistema: {usuarios.count()}")
    
    for user in usuarios:
        print(f"\n👤 {user.username}:")
        print(f"   📧 Email: {user.email}")
        print(f"   ✅ Activo: {user.is_active}")
        print(f"   🔐 Staff: {user.is_staff}")
        print(f"   🎯 Superuser: {user.is_superuser}")
        
        # Verificar perfil
        try:
            perfil = PerfilUsuario.objects.get(user_id=user)
            print(f"   📝 Perfil: {perfil.nombre_completo}")
            print(f"   🎖️ Nivel: {perfil.nivel_usuario}")
        except:
            print(f"   ❌ Sin perfil")
        
        # Probar login con contraseña 1234
        auth_test = authenticate(username=user.username, password='1234')
        if auth_test:
            print(f"   🎉 Login con '1234': ✅ FUNCIONA")
        else:
            print(f"   ❌ Login con '1234': No funciona")

if __name__ == "__main__":
    verificar_usuarios_simple()
