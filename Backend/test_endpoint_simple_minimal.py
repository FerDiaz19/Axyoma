import requests

def test_simple():
    try:
        # El frontend está autenticado, usar la misma sesión
        response = requests.get('http://localhost:8000/api/superadmin/test_simple/')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple()
