import requests
import json

def get_fresh_token():
    """Obtiene un token fresco del SuperAdmin"""
    print("OBTENIENDO TOKEN FRESCO...")
    
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={
            "username": "superadmin",
            "password": "admin123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"Token obtenido: {token}")
        return token
    else:
        print(f"Error obteniendo token: {response.text}")
        return None

def test_with_token(token):
    """Prueba endpoints con el token fresco"""
    print(f"\nPROBANDO CON TOKEN: {token[:20]}...")
    
    # Probar endpoint simple primero
    response = requests.get(
        "http://localhost:8000/api/superadmin/listar_empresas/",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")

if __name__ == "__main__":
    token = get_fresh_token()
    if token:
        test_with_token(token)
