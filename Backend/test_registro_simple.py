#!/usr/bin/env python
"""
Test simple para registro
"""
import requests
import time

def test_registro_simple():
    print("=== TEST REGISTRO SIMPLE ===")
    
    url = 'http://127.0.0.1:8000/api/empresas/registro/'
    
    datos = {
        'nombre': f'Empresa Test {int(time.time())}',
        'rfc': f'RFC{int(time.time())}',
        'direccion': 'Dirección Test',
        'email_contacto': 'test@empresa.com',
        'telefono_contacto': '555-1234',
        'usuario': f'admin_test_{int(time.time())}',
        'password': 'password123',
        'nombre_completo': 'Admin Test'
    }
    
    print("Datos a enviar:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post(url, json=datos, timeout=10)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ REGISTRO EXITOSO!")
        else:
            print("❌ Error en registro")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_registro_simple()
