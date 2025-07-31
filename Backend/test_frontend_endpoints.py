import requests
import json

def test_frontend_endpoints():
    """Prueba endpoints exactos del frontend"""
    # Obtener token fresco
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={
            "username": "superadmin",
            "password": "admin123"
        }
    )
    
    if response.status_code != 200:
        print(f"Error obteniendo token: {response.text}")
        return
    
    token = response.json().get('token')
    print(f"Token obtenido: {token[:20]}...")
    
    # Headers exactos que usa el frontend
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Endpoints exactos del frontend
    endpoints = [
        ("Listar Empresas", "http://localhost:8000/api/superadmin/listar_empresas/"),
        ("Listar Usuarios", "http://localhost:8000/api/superadmin/listar_usuarios/"),
        ("Listar Plantas", "http://localhost:8000/api/superadmin/listar_todas_plantas/"),
        ("Listar Departamentos", "http://localhost:8000/api/superadmin/listar_todos_departamentos/"),
        ("Listar Puestos", "http://localhost:8000/api/superadmin/listar_todos_puestos/"),
        ("Listar Empleados", "http://localhost:8000/api/superadmin/listar_todos_empleados/"),
        ("Estadísticas", "http://localhost:8000/api/superadmin/estadisticas_sistema/"),
        ("Planes", "http://localhost:8000/api/suscripciones/planes/")
    ]
    
    print("\nPROBANDO ENDPOINTS DEL FRONTEND:")
    print("=" * 50)
    
    for nombre, url in endpoints:
        print(f"\n{nombre}:")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ OK - Status: {response.status_code}")
                data = response.json()
                if isinstance(data, dict):
                    for key in list(data.keys())[:3]:  # Mostrar primeras 3 claves
                        print(f"   - {key}: {str(data[key])[:50]}...")
                elif isinstance(data, list):
                    print(f"   - Lista con {len(data)} elementos")
                    if data:
                        if isinstance(data[0], dict):
                            for key in list(data[0].keys())[:3]:
                                print(f"   - Primer elemento {key}: {str(data[0][key])[:30]}...")
            else:
                print(f"❌ Error - Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Excepción: {str(e)}")

if __name__ == "__main__":
    test_frontend_endpoints()
