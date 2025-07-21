#!/usr/bin/env python3
import requests
import json

def test_login(username, password):
    print(f"\n=== Probando login con: {username} ===")
    
    url = "http://127.0.0.1:8000/api/auth/login/"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LOGIN EXITOSO!")
            print(f"   Token: {result.get('token')}")
            print(f"   Usuario: {result.get('username')}")
            print(f"   Email: {result.get('email')}")
            
            empresa = result.get('empresa')
            if empresa:
                print(f"   Empresa: {empresa.get('nombre')}")
            else:
                print("   Empresa: No asignada")
                
            return result.get('token')
        else:
            print(f"❌ ERROR: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

if __name__ == "__main__":
    print("🔐 PROBANDO CREDENCIALES DISPONIBLES")
    
    # Probar las credenciales principales
    credenciales = [
        ("admin_empresa", "admin123"),
        ("superadmin", "admin123"), 
        ("demo_admin", "admin123")
    ]
    
    for username, password in credenciales:
        token = test_login(username, password)
        if token:
            print(f"✅ {username} funciona correctamente!")
        else:
            print(f"❌ {username} no funciona")
    
    print("\n🎯 RECOMENDACIÓN: Usa 'admin_empresa' con password 'admin123'")
