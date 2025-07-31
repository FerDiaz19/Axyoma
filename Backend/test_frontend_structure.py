import requests
import json

def test_all_endpoints_structure():
    """Prueba la estructura de todos los endpoints para actualizar frontend"""
    # Obtener token
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={"username": "superadmin", "password": "admin123"}
    )
    
    if response.status_code != 200:
        print(f"Error en login: {response.text}")
        return
    
    token = response.json().get('token')
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    endpoints = [
        ("Empresas", "http://localhost:8000/api/superadmin/listar_empresas/"),
        ("Usuarios", "http://localhost:8000/api/superadmin/listar_usuarios/"), 
        ("Plantas", "http://localhost:8000/api/superadmin/listar_todas_plantas/"),
        ("Departamentos", "http://localhost:8000/api/superadmin/listar_todos_departamentos/"),
        ("Puestos", "http://localhost:8000/api/superadmin/listar_todos_puestos/"),
        ("Empleados", "http://localhost:8000/api/superadmin/listar_todos_empleados/"),
        ("Planes", "http://localhost:8000/api/suscripciones/planes/")
    ]
    
    print("ESTRUCTURA DE RESPUESTAS PARA FRONTEND")
    print("=" * 60)
    
    for nombre, url in endpoints:
        print(f"\n📋 {nombre.upper()}:")
        print("-" * 40)
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Mostrar estructura principal
                if isinstance(data, dict):
                    print("🔧 Estructura (diccionario):")
                    for key in data.keys():
                        if isinstance(data[key], list) and data[key]:
                            print(f"  - {key}: Lista con {len(data[key])} elementos")
                            if data[key]:
                                primer_elemento = data[key][0]
                                if isinstance(primer_elemento, dict):
                                    print(f"    Campos del primer elemento:")
                                    for field in primer_elemento.keys():
                                        valor = primer_elemento[field]
                                        tipo = type(valor).__name__
                                        print(f"      • {field}: {tipo}")
                        else:
                            valor = data[key]
                            tipo = type(valor).__name__
                            print(f"  - {key}: {tipo}")
                
                elif isinstance(data, list):
                    print(f"🔧 Lista con {len(data)} elementos")
                    if data:
                        primer_elemento = data[0]
                        if isinstance(primer_elemento, dict):
                            print("  Campos del primer elemento:")
                            for field in primer_elemento.keys():
                                valor = primer_elemento[field]
                                tipo = type(valor).__name__
                                print(f"    • {field}: {tipo}")
                
            else:
                print(f"❌ Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    test_all_endpoints_structure()
