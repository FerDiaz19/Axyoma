import requests
import json

TOKEN = "4396feb7d109b7f77a1a12ae8bb1ef65a866a6c0"  # Token del SuperAdmin
BASE_URL = "http://localhost:8000/api"

def test_endpoint(endpoint, descripcion):
    """Prueba un endpoint específico"""
    print(f"\n🔍 {descripcion}")
    print(f"   Endpoint: {endpoint}")
    
    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers={
                "Authorization": f"Token {TOKEN}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ FUNCIONA - {len(data) if isinstance(data, list) else 'OK'} registros")
            return True
        else:
            print(f"   ✗ ERROR {response.status_code}: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"   ✗ ERROR CONEXION: {e}")
        return False

def main():
    print("VERIFICANDO ENDPOINTS DEL PANEL SUPERADMIN")
    print("=" * 50)
    
    # Lista de endpoints a verificar
    endpoints = [
        ("/superadmin/listar_empresas/", "Listar Empresas"),
        ("/superadmin/listar_usuarios/", "Listar Usuarios"),
        ("/superadmin/listar_todas_plantas/", "Listar Plantas"),
        ("/superadmin/listar_todos_departamentos/", "Listar Departamentos"),
        ("/superadmin/listar_todos_puestos/", "Listar Puestos"),
        ("/superadmin/listar_todos_empleados/", "Listar Empleados"),
        ("/superadmin/estadisticas_sistema/", "Estadísticas del Sistema"),
        ("/suscripciones/planes/", "Planes de Suscripción"),
    ]
    
    exitosos = 0
    total = len(endpoints)
    
    for endpoint, descripcion in endpoints:
        if test_endpoint(endpoint, descripcion):
            exitosos += 1
    
    print(f"\n📊 RESUMEN: {exitosos}/{total} endpoints funcionan")
    
    if exitosos == total:
        print("🎉 TODOS LOS ENDPOINTS FUNCIONAN!")
    else:
        print("⚠️ Algunos endpoints necesitan corrección")

if __name__ == "__main__":
    main()
