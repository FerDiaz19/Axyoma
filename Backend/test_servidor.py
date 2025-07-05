#!/usr/bin/env python
"""
Script simple para verificar conexión al servidor
"""
import requests

try:
    response = requests.get("http://localhost:8000")
    print(f"Servidor respondió: {response.status_code}")
    if response.status_code == 200:
        print("✅ Servidor funcionando")
    else:
        print("⚠️ Servidor respondió pero con error")
except Exception as e:
    print(f"❌ No se puede conectar al servidor: {str(e)}")
    print("Asegúrate de que el servidor Django esté corriendo con:")
    print("python manage.py runserver")
