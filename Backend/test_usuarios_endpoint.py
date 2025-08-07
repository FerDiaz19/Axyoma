#!/usr/bin/env python
import os
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def test_usuarios_endpoint():
    """Probar el endpoint de usuarios directamente"""
    print("🧪 PROBANDO ENDPOINT DE USUARIOS")
    print("=" * 50)
    
    try:
        # 1. Login para obtener token
        print("1. Obteniendo token de autenticación...")
        login_data = {
            "username": "admin",
            "password": "1234"
        }
        
        try:
            login_response = requests.post(
                "http://localhost:8000/api/auth/login/", 
                json=login_data,
                timeout=30
            )
            
            print(f"Login Status Code: {login_response.status_code}")
            print(f"Login Response: {login_response.text[:200]}...")
            
        except Exception as e:
            print(f"❌ Error en login: {str(e)}")
            return
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"✅ Token obtenido: {token[:20]}...")
            
            # 2. Probar endpoint de usuarios
            print("\n2. Probando endpoint de usuarios...")
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            try:
                usuarios_response = requests.get(
                    "http://localhost:8000/api/superadmin/listar_usuarios/",
                    headers=headers,
                    timeout=30
                )
                
                print(f"Usuarios Status Code: {usuarios_response.status_code}")
                
                if usuarios_response.status_code == 200:
                    usuarios_data = usuarios_response.json()
                    usuarios = usuarios_data.get('usuarios', [])
                    print(f"✅ Usuarios encontrados: {len(usuarios)}")
                    print(f"✅ Total reportado: {usuarios_data.get('total', 0)}")
                    
                    for i, usuario in enumerate(usuarios[:3]):  # Mostrar primeros 3
                        print(f"  {i+1}. {usuario.get('nombre_completo', 'N/A')} ({usuario.get('username', 'N/A')}) - {usuario.get('nivel_usuario', 'N/A')}")
                else:
                    print(f"❌ Error: {usuarios_response.status_code}")
                    print(f"Respuesta completa: {usuarios_response.text}")
                    
            except Exception as e:
                print(f"❌ Error en solicitud de usuarios: {str(e)}")
                
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Respuesta: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_usuarios_endpoint()
