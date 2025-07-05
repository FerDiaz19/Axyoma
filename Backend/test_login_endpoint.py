#!/usr/bin/env python
import requests
import json

# Test login endpoint
login_url = 'http://localhost:8000/api/auth/login/'
login_data = {
    'username': 'ed-rubio@axyoma.com',
    'password': '1234'
}

try:
    print("Testing login endpoint...")
    response = requests.post(login_url, json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"User: {data.get('usuario')}")
        print(f"Dashboard: {data.get('tipo_dashboard')}")
        print(f"Level: {data.get('nivel_usuario')}")
    else:
        print(f"❌ Login failed: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is Django running?")
except Exception as e:
    print(f"❌ Error: {e}")
