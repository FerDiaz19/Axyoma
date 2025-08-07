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

def verificar_usuarios():
    """
    Verificar usuarios existentes y sus credenciales
    """
    print("🔍 VERIFICANDO USUARIOS EXISTENTES...")
    
    # Usuarios a verificar
    test_users = ['superadmin', 'admin', 'Ernesto']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"\n👤 Usuario: {username}")
            print(f"   ✅ Existe: Sí")
            print(f"   🔓 Activo: {user.is_active}")
            print(f"   👨‍💼 Staff: {user.is_staff}")
            print(f"   🔑 Superuser: {user.is_superuser}")
            
            # Verificar perfil
            try:
                perfil = PerfilUsuario.objects.get(user_id=user)
                print(f"   📝 Perfil: {perfil.nombre_completo}")
                print(f"   🎯 Nivel: {perfil.nivel_usuario}")
                print(f"   ✅ Status: {perfil.status}")
            except PerfilUsuario.DoesNotExist:
                print(f"   ❌ Sin perfil PerfilUsuario")
            
            # Probar autenticación
            auth_user = authenticate(username=username, password='1234')
            if auth_user:
                print(f"   🎉 LOGIN CON '1234': ✅ ÉXITO")
            else:
                print(f"   ❌ LOGIN CON '1234': FALLO")
                
        except User.DoesNotExist:
            print(f"\n👤 Usuario: {username}")
            print(f"   ❌ No existe")

def probar_login_api():
    """
    Simular el login que hace el frontend
    """
    print("\n" + "="*50)
    print("🧪 PROBANDO LOGIN COMO EL FRONTEND")
    print("="*50)
    
    import json
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    # Datos de login (igual que el frontend)
    login_data = {
        'username': 'superadmin',
        'password': '1234'
    }
    
    try:
        # Hacer POST a la ruta de login
        response = client.post(
            '/api/auth/login/',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📝 Response: {response.content.decode()}")
        
        if response.status_code == 200:
            print("🎉 LOGIN API: ✅ ÉXITO")
        else:
            print("❌ LOGIN API: FALLO")
            
    except Exception as e:
        print(f"❌ Error probando API: {str(e)}")

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DE LOGIN")
    print("-" * 30)
    
    verificar_usuarios()
    probar_login_api()
    
    print("\n" + "="*50)
    print("💡 RECOMENDACIÓN:")
    print("Si todos fallan, usa: python crear_superadmin_simple.py")
    print("="*50)
