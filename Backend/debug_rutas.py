#!/usr/bin/env python
"""
Script para probar rutas del backend directamente
"""
import requests
import json

def test_rutas_backend():
    """Probar que las rutas del backend están funcionando"""
    print("=== PRUEBA DE RUTAS BACKEND ===\n")
    
    base_url = "http://localhost:8000"
    
    # Rutas a probar
    rutas_test = [
        {"ruta": "/", "descripcion": "Ruta raíz"},
        {"ruta": "/api/", "descripcion": "API base"},
        {"ruta": "/api/auth/", "descripcion": "Auth endpoints"},
        {"ruta": "/api/empresas/", "descripcion": "Empresas endpoints"},
        {"ruta": "/api/plantas/", "descripcion": "Plantas endpoints"},
    ]
    
    print("🌐 Probando conectividad...")
    
    for ruta_info in rutas_test:
        ruta = ruta_info["ruta"]
        descripcion = ruta_info["descripcion"]
        
        try:
            response = requests.get(f"{base_url}{ruta}", timeout=5)
            print(f"  {ruta} ({descripcion}): {response.status_code}")
            
            if response.status_code == 405:
                print(f"    ✅ Método no permitido (endpoint existe)")
            elif response.status_code == 200:
                print(f"    ✅ OK")
            elif response.status_code == 401:
                print(f"    ✅ No autorizado (endpoint existe, requiere auth)")
            elif response.status_code == 404:
                print(f"    ❌ No encontrado")
            else:
                print(f"    ⚠️  Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"  {ruta}: ❌ No se puede conectar al servidor")
            print("    💡 ¿Está corriendo el servidor Django?")
            break
        except Exception as e:
            print(f"  {ruta}: ❌ Error: {str(e)}")

def test_auth_login():
    """Probar específicamente el endpoint de login"""
    print(f"\n=== PRUEBA LOGIN ENDPOINT ===\n")
    
    base_url = "http://localhost:8000"
    
    # Datos de login válidos
    login_data = {
        "username": "admin_empresa_1",
        "password": "admin123"
    }
    
    print("🔐 Probando login con credenciales conocidas...")
    
    try:
        # Probar POST a login
        response = requests.post(
            f"{base_url}/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Login exitoso")
            result = response.json()
            print(f"  Usuario: {result.get('usuario', 'N/A')}")
            print(f"  Token: {result.get('token', 'N/A')[:20]}...")
        elif response.status_code == 404:
            print("  ❌ Endpoint no encontrado")
            print("  💡 Verificar configuración de URLs")
        elif response.status_code == 401:
            print("  ❌ Credenciales inválidas")
        elif response.status_code == 400:
            print("  ❌ Bad Request")
            print(f"  Respuesta: {response.text}")
        else:
            print(f"  ⚠️  Status inesperado: {response.status_code}")
            print(f"  Respuesta: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error durante login: {str(e)}")

def test_registro_empresa():
    """Probar endpoint de registro de empresa"""
    print(f"\n=== PRUEBA REGISTRO EMPRESA ===\n")
    
    base_url = "http://localhost:8000"
    
    # Datos de registro
    registro_data = {
        "nombre": "Empresa Test Debug",
        "rfc": "TESTDEBUG123",
        "direccion": "Dir test debug",
        "email_contacto": "admin@testdebug.com",
        "telefono_contacto": "555-DEBUG",
        "usuario": "admin_test_debug",
        "password": "debug123",
        "nombre_completo": "Admin Test Debug"
    }
    
    print("🏢 Probando registro de empresa...")
    
    try:
        response = requests.post(
            f"{base_url}/api/empresas/registro/",
            json=registro_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("  ✅ Registro exitoso")
            result = response.json()
            print(f"  Empresa: {result.get('nombre', 'N/A')}")
        elif response.status_code == 404:
            print("  ❌ Endpoint no encontrado")
        elif response.status_code == 400:
            print("  ❌ Bad Request")
            print(f"  Respuesta: {response.text}")
        else:
            print(f"  ⚠️  Status inesperado: {response.status_code}")
            print(f"  Respuesta: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error durante registro: {str(e)}")

if __name__ == "__main__":
    test_rutas_backend()
    test_auth_login() 
    test_registro_empresa()
