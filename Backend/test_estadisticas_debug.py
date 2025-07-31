import requests

def test_estadisticas_debug():
    """Debug específico del endpoint de estadísticas"""
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
    
    print("DEBUGGEANDO ENDPOINT DE ESTADÍSTICAS")
    print("=" * 50)
    
    url = "http://localhost:8000/api/superadmin/estadisticas_sistema/"
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
                                print(f"    {lines[j].strip()}")
                            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_estadisticas_debug()
