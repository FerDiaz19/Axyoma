#!/usr/bin/env python
"""
Script para probar el registro de empresa
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
import json

def test_registro_empresa():
    """Probar el registro de empresa"""
    print("=== PRUEBA REGISTRO DE EMPRESA ===\n")
    
    # URL base
    base_url = "http://localhost:8000"
    
    # Datos de registro
    datos_empresa = {
        "nombre": "Empresa Test Registro",
        "rfc": "TEST123456ABC",
        "direccion": "Dirección de prueba 123",
        "email_contacto": "admin@empresatest.com",
        "telefono_contacto": "555-1234567",
        "usuario": "admin_test_empresa",
        "password": "password123",
        "nombre_completo": "Admin Test Empresa"
    }
    
    print("Datos a enviar:")
    for key, value in datos_empresa.items():
        if key != 'password':
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: [OCULTO]")
    
    try:
        print("\nEnviando solicitud de registro...")
        response = requests.post(
            f"{base_url}/api/empresas/registro/",
            json=datos_empresa,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registro exitoso!")
            print(f"Empresa ID: {result.get('empresa_id')}")
            print(f"Nombre: {result.get('nombre')}")
            
            # Probar login con las credenciales creadas
            test_login_empresa_creada(datos_empresa['usuario'], datos_empresa['password'])
            
        else:
            print("❌ Error en registro:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
                
    except Exception as e:
        print(f"❌ Excepción durante la prueba: {str(e)}")

def test_login_empresa_creada(username, password):
    """Probar login con la empresa recién creada"""
    print(f"\n=== PRUEBA LOGIN EMPRESA CREADA ===")
    
    base_url = "http://localhost:8000"
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso!")
            print(f"Usuario: {result.get('usuario')}")
            print(f"Tipo dashboard: {result.get('tipo_dashboard')}")
            print(f"Empresa: {result.get('nombre_empresa')}")
            print(f"Token: {result.get('token', '')[:20]}...")
        else:
            print("❌ Error en login:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error durante login: {str(e)}")

if __name__ == "__main__":
    test_registro_empresa()
