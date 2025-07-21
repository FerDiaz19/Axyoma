#!/usr/bin/env python3
import requests
import json

# Configuración base
BASE_URL = "http://127.0.0.1:8000/api"
headers = {"Content-Type": "application/json"}

def test_endpoint(url, description):
    print(f"\n🧪 Probando: {description}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"📋 Resultados: {len(data)} elementos")
                if data:
                    print(f"🔍 Primer elemento: {json.dumps(data[0], indent=2)[:200]}...")
            elif isinstance(data, dict):
                print(f"📋 Datos: {json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"❌ Error: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    except Exception as e:
        print(f"🚨 Error: {e}")

def test_auth():
    print("\n🔐 Probando autenticación con superadmin...")
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {
        "username": "superadmin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(login_url, json=login_data, headers=headers, timeout=5)
        print(f"✅ Login Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"🎫 Token obtenido: {data.get('token', 'No token')[:50]}...")
            return data.get('token')
        else:
            print(f"❌ Login Error: {response.text}")
    except Exception as e:
        print(f"🚨 Login Error: {e}")
    return None

# Tests principales
if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DE ENDPOINTS DEL SISTEMA AXYOMA")
    print("=" * 60)
    
    # Test de autenticación
    token = test_auth()
    
    if token:
        headers["Authorization"] = f"Token {token}"
        print("\n🔓 Token agregado a headers para requests autenticados")
    
    # Tests de endpoints principales
    endpoints = [
        (f"{BASE_URL}/empresas/", "📊 Empresas"),
        (f"{BASE_URL}/usuarios/", "👥 Usuarios"),  
        (f"{BASE_URL}/empleados/", "👤 Empleados"),
        (f"{BASE_URL}/plantas/", "🏭 Plantas"),
        (f"{BASE_URL}/departamentos/", "🏢 Departamentos"),
        (f"{BASE_URL}/puestos/", "💼 Puestos"),
        (f"{BASE_URL}/evaluaciones/", "📋 Evaluaciones"),
        (f"{BASE_URL}/subscriptions/", "💳 Suscripciones"),
    ]
    
    for url, description in endpoints:
        test_endpoint(url, description)
    
    # Test de endpoint de estadísticas si existe
    test_endpoint(f"{BASE_URL}/empresas/estadisticas/", "📈 Estadísticas del Sistema")
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
