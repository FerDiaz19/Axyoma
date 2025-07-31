import requests

def test_planes_debug():
    """Debug específico del endpoint de planes"""
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
    
    print("DEBUGGEANDO ENDPOINT DE PLANES")
    print("=" * 50)
    
    url = "http://localhost:8000/api/suscripciones/planes/"
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            data = response.json()
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("❌ ERROR!")
            text = response.text
            if 'AttributeError' in text:
                print("\n🔍 ATTRIBUTE ERROR DETECTADO:")
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if 'AttributeError' in line or "has no attribute" in line:
                        print(f"  {line.strip()}")
                        # Contexto
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            if j != i and 'AttributeError' not in lines[j]:
                                clean_line = lines[j].strip()
                                if clean_line and len(clean_line) < 100:
                                    print(f"    {clean_line}")
                            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_planes_debug()
