import requests
import json

def test_plantas_detailed():
    """Prueba el endpoint de plantas paso a paso"""
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
    
    print("PROBANDO ENDPOINT DE PLANTAS CON DEBUG")
    print("=" * 50)
    
    # Test básico
    url = "http://localhost:8000/api/superadmin/listar_todas_plantas/"
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            data = response.json()
            print(f"Total plantas: {data.get('total', 0)}")
            if 'plantas' in data and data['plantas']:
                print("Primera planta:")
                primera = data['plantas'][0]
                for key, value in primera.items():
                    print(f"  {key}: {value}")
        else:
            print("❌ ERROR!")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response text: {response.text[:500]}...")
            
            # Si es HTML, buscar el error específico
            if 'html' in response.headers.get('content-type', ''):
                text = response.text
                if 'FieldError' in text:
                    print("\n🔍 FIELD ERROR DETECTADO:")
                    # Buscar la línea con el error
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if 'FieldError' in line or 'Cannot resolve keyword' in line:
                            print(f"  {line.strip()}")
                            # Mostrar contexto
                            for j in range(max(0, i-2), min(len(lines), i+3)):
                                if j != i:
                                    print(f"    {lines[j].strip()}")
                                    
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_plantas_detailed()
