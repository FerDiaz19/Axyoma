import requests
import json

def test_superadmin_login():
    """Prueba específica del SuperAdmin"""
    print("VERIFICANDO LOGIN SUPERADMIN")
    print("=" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login/",
            json={
                "username": "superadmin",
                "password": "admin123"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ LOGIN EXITOSO")
            print(f"Usuario: {data.get('usuario')}")
            print(f"Tipo: {data.get('nivel_usuario')}")
            print(f"Dashboard: {data.get('tipo_dashboard')}")
            print(f"Token: {data.get('token')[:20]}...")
            return data.get('token')
        else:
            print(f"✗ ERROR: {response.status_code}")
            print(f"Detalles: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ ERROR DE CONEXION: {e}")
        return None

if __name__ == "__main__":
    test_superadmin_login()
