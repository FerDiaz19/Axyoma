#!/usr/bin/env python
"""
Script para probar login directo via API sin frontend
"""
import requests
import json

def test_login_directo():
    """
    Probar login directo contra la API
    """
    print("🧪 PROBANDO LOGIN DIRECTO VIA API")
    print("-" * 40)
    
    # URL de la API
    url = "http://localhost:8000/api/auth/login/"
    
    # Credenciales a probar
    credenciales = [
        {"username": "superadmin", "password": "1234"},
        {"username": "admin", "password": "1234"},
        {"username": "Ernesto", "password": "1234"}
    ]
    
    for creds in credenciales:
        print(f"\n🔍 Probando: {creds['username']}")
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                url,
                data=json.dumps(creds),
                headers=headers,
                timeout=10
            )
            
            print(f"   📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ LOGIN EXITOSO!")
                print(f"   🎯 Nivel: {data.get('nivel_usuario')}")
                print(f"   🔑 Token: {data.get('token', 'N/A')[:20]}...")
                print(f"   👤 Nombre: {data.get('nombre_completo')}")
                print(f"   🏢 Dashboard: {data.get('tipo_dashboard')}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️ No se pudo conectar - ¿Servidor corriendo?")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    test_login_directo()
