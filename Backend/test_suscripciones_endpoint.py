#!/usr/bin/env python
import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def test_suscripciones_endpoint():
    """Probar el endpoint de suscripciones directamente"""
    print("🧪 PROBANDO ENDPOINT DE SUSCRIPCIONES")
    print("=" * 50)
    
    try:
        # 1. Login para obtener token
        print("1. Obteniendo token de autenticación...")
        login_data = {
            "username": "admin",
            "password": "1234"
        }
        
        login_response = requests.post(
            "http://localhost:8000/api/auth/login/", 
            json=login_data
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"✅ Token obtenido: {token[:20]}...")
            
            # 2. Probar endpoint de suscripciones
            print("\n2. Probando endpoint de suscripciones...")
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            suscripciones_response = requests.get(
                "http://localhost:8000/api/suscripciones/listar_suscripciones/",
                headers=headers
            )
            
            print(f"Status Code: {suscripciones_response.status_code}")
            print(f"Response: {suscripciones_response.text}")
            
            if suscripciones_response.status_code == 200:
                suscripciones = suscripciones_response.json()
                print(f"✅ Suscripciones encontradas: {len(suscripciones)}")
                
                for i, suscripcion in enumerate(suscripciones[:3]):  # Mostrar primeras 3
                    print(f"  {i+1}. {suscripcion.get('empresa_nombre', 'N/A')} - {suscripcion.get('plan_nombre', 'N/A')}")
            else:
                print(f"❌ Error: {suscripciones_response.status_code}")
                print(f"Respuesta: {suscripciones_response.text}")
                
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Respuesta: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error en prueba: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_suscripciones_endpoint()
