import requests
import json

def test_empleado_get():
    """Probar GET endpoint del empleado"""
    
    # Primero obtener un token válido
    login_url = "http://localhost:8000/api/login/"
    login_data = {
        "email": "super@admin.com",
        "password": "superadmin123"
    }
    
    try:
        # Login
        print("=== LOGIN ===")
        response = requests.post(login_url, json=login_data, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"Token obtenido: {token[:20]}...")
            
            # Headers con token
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            # Probar GET empleado específico directamente
            print(f"\n=== GET EMPLEADO 1 ===")
            detail_url = f"http://localhost:8000/api/empleados/1/"
            response = requests.get(detail_url, headers=headers, timeout=5)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                empleado = response.json()
                print("✅ GET empleado específico exitoso")
                print(f"Nombre: {empleado.get('nombre')} {empleado.get('apellido_paterno')}")
                print(f"Empresa: {empleado.get('empresa_nombre')}")
            else:
                print(f"❌ Error en GET empleado específico: {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose Django?")
    except requests.exceptions.Timeout:
        print("❌ Error: Timeout en la conexión")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_empleado_get()
