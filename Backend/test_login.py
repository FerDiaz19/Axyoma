#!/usr/bin/env python
"""
Script para probar las credenciales de login directamente contra el backend
"""

import os
import sys
import django
import json
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import connection

def test_database_users():
    """Probar usuarios directamente en la base de datos"""
    print("\n===== VERIFICANDO USUARIOS EN BASE DE DATOS =====")
    
    # Listar todos los usuarios
    try:
        users = User.objects.all()
        print(f"Total usuarios encontrados: {len(users)}")
        
        for user in users:
            print(f"\nUsuario: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Activo: {user.is_active}")
            print(f"  Staff: {user.is_staff}")
            print(f"  Superuser: {user.is_superuser}")
            
            # Probar contraseñas comunes
            passwords_to_try = ['1234', 'admin123', 'password', 'testpass123']
            for password in passwords_to_try:
                auth_result = authenticate(username=user.username, password=password)
                if auth_result:
                    print(f"  ✅ Contraseña encontrada: '{password}'")
                    break
            else:
                print(f"  ❌ No se encontró una contraseña válida")
            
            # Verificar si tiene perfil
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT nivel_usuario FROM usuarios WHERE user_id = %s",
                        [user.id]
                    )
                    result = cursor.fetchone()
                    if result:
                        print(f"  Nivel: {result[0]}")
                    else:
                        print("  ⚠️ No tiene perfil en la tabla usuarios")
            except Exception as e:
                print(f"  ⚠️ Error verificando perfil: {e}")
    
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {e}")

def test_api_login():
    """Probar credenciales usando la API directamente"""
    print("\n===== PROBANDO LOGIN VIA API =====")
    
    test_users = [
        {'username': 'superadmin', 'password': '1234'},
        {'username': 'admin_empresa', 'password': '1234'},
        {'username': 'admin_planta', 'password': '1234'},
        {'username': 'testuser', 'password': 'testpass123'}
    ]
    
    for user_data in test_users:
        try:
            response = requests.post(
                'http://localhost:8000/api/auth/login/',
                json=user_data
            )
            
            print(f"\nProbando {user_data['username']}/{user_data['password']}:")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Login exitoso")
                try:
                    # Intentar mostrar respuesta JSON
                    data = response.json()
                    if 'token' in data:
                        print(f"  Token: {data['token'][:10]}...")
                    if 'nivel_usuario' in data:
                        print(f"  Nivel: {data['nivel_usuario']}")
                except:
                    pass
            else:
                try:
                    error_data = response.json()
                    print(f"  ❌ Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"  ❌ Error: {response.text[:100]}")
        
        except Exception as e:
            print(f"❌ Error en la petición: {e}")

if __name__ == '__main__':
    print("\n🔍 VERIFICADOR DE CREDENCIALES AXYOMA")
    
    # Probar ambos métodos
    test_database_users()
    test_api_login()
    
    print("\n✅ Verificación completada")
