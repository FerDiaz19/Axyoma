import requests

def debug_import_planes():
    """Debug del import de planes"""
    print("DEBUGGEANDO IMPORT DE PLANES")
    print("=" * 50)
    
    try:
        # Test directo del import
        print("1. Probando import de PlanSuscripcion...")
        from apps.subscriptions.models import PlanSuscripcion
        print("   ✅ Import exitoso")
        
        # Test de conteo
        print("2. Contando planes...")
        count = PlanSuscripcion.objects.count()
        print(f"   ✅ Total planes: {count}")
        
        # Test de filtrado
        print("3. Filtrando planes activos...")
        planes_activos = PlanSuscripcion.objects.filter(status=True).count()
        print(f"   ✅ Planes activos: {planes_activos}")
        
        # Test de serialización básica
        print("4. Probando serialización...")
        if count > 0:
            primer_plan = PlanSuscripcion.objects.first()
            print(f"   ✅ Primer plan: {primer_plan.nombre} - ${primer_plan.precio}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_endpoint_planes_minimo():
    """Test mínimo del endpoint"""
    if not debug_import_planes():
        return
    
    print("\nPROBANDO ENDPOINT DE PLANES...")
    print("=" * 50)
    
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
    
    url = "http://localhost:8000/api/suscripciones/planes/"
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            data = response.json()
            print(f"Response: {data}")
        else:
            print("❌ ERROR!")
            print(f"Response: {response.text[:500]}...")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_endpoint_planes_minimo()
