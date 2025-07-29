#!/usr/bin/env python3
import requests

# Obtener nuevo token
response = requests.post('http://127.0.0.1:8000/api/auth/login/', json={
    'username': 'admin', 
    'password': 'admin123'
})

if response.status_code == 200:
    data = response.json()
    print(f"Token: {data['token']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
