#!/usr/bin/env python
import requests

try:
    r = requests.get("http://localhost:8000/api/auth/", timeout=3)
    print(f"Auth endpoint: {r.status_code}")
    
    login_data = {"username": "admin_empresa_1", "password": "admin123"}
    r2 = requests.post("http://localhost:8000/api/auth/login/", json=login_data)
    print(f"Login: {r2.status_code}")
    if r2.status_code == 200:
        result = r2.json()
        print(f"✅ Login OK - Usuario: {result.get('usuario')}")
    else:
        print(f"❌ Login error: {r2.text}")
        
    # Probar registro
    reg_data = {
        "nombre": "Test Quick",
        "rfc": "QUICK123",
        "direccion": "Dir quick",
        "email_contacto": "quick@test.com",
        "telefono_contacto": "555-QUICK",
        "usuario": "admin_quick",
        "password": "quick123",
        "nombre_completo": "Admin Quick"
    }
    r3 = requests.post("http://localhost:8000/api/empresas/registro/", json=reg_data)
    print(f"Registro: {r3.status_code}")
    if r3.status_code == 201:
        print("✅ Registro OK")
    else:
        print(f"❌ Registro error: {r3.text}")
        
except Exception as e:
    print(f"Error: {e}")
