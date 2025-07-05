#!/usr/bin/env python
"""
Test específico para el registro
"""
import requests
import json

def test_registro_correcto():
    print("=== PROBANDO REGISTRO CON CAMPOS CORRECTOS ===")
    url = 'http://127.0.0.1:8000/api/empresas/registro/'
    
    # Estos son los campos que requiere el serializer
    datos = {
        'nombre': 'Empresa Test Nueva',
        'rfc': 'TEST123456789',
        'direccion': 'Calle Test 123',
        'email_contacto': 'admin@test.com',
        'telefono_contacto': '555-1234',
        'usuario': 'admin_test_nuevo',
        'password': 'password123',
        'nombre_completo': 'Admin Test Nuevo'
    }
    
    print("Datos enviados:")
    print(json.dumps(datos, indent=2))
    
    try:
        response = requests.post(url, json=datos)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ REGISTRO EXITOSO!")
            return True
        else:
            print("❌ Error en registro")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    return False

def test_login_nuevo_usuario():
    print("\n=== PROBANDO LOGIN CON USUARIO RECIÉN CREADO ===")
    url = 'http://127.0.0.1:8000/api/auth/login/'
    
    datos = {
        'username': 'admin_test_nuevo',
        'password': 'password123'
    }
    
    try:
        response = requests.post(url, json=datos)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN EXITOSO!")
            return data.get('token')
        else:
            print("❌ Error en login")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

if __name__ == '__main__':
    # Probar registro
    registro_ok = test_registro_correcto()
    
    # Si el registro fue exitoso, probar login
    if registro_ok:
        token = test_login_nuevo_usuario()
        if token:
            print(f"\n🎉 TODO FUNCIONA! Token: {token[:20]}...")
    else:
        print("\n🔍 Revisando qué falta en el registro...")
