# -*- coding: utf-8 -*-
"""
Script simple para probar conexión al servidor Django
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def probar_conexion():
    """Probar conexión básica al servidor"""
    try:
        # Probar endpoint básico
        response = requests.get(f"{BASE_URL}/api/")
        print(f"✅ Servidor Django ejecutándose: {response.status_code}")
        
        # Probar endpoint de evaluaciones existentes
        response = requests.get(f"{BASE_URL}/api/evaluaciones/")
        if response.status_code == 200:
            print(f"✅ API de evaluaciones accesible: {response.status_code}")
        else:
            print(f"⚠️ API de evaluaciones: {response.status_code}")
        
        # Probar endpoint oficial sin autenticación (debería dar 401)
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/")
        if response.status_code == 401:
            print(f"✅ API oficial protegida correctamente: {response.status_code}")
        else:
            print(f"⚠️ API oficial: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor Django")
        print("   Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
        return False

if __name__ == '__main__':
    print("🔍 Probando conexión al servidor Django...")
    if probar_conexion():
        print("\n🎉 Servidor accesible!")
        print("\n📋 URLs para probar manualmente:")
        print("   - API base: http://127.0.0.1:8000/api/")
        print("   - Evaluaciones existentes: http://127.0.0.1:8000/api/evaluaciones/")
        print("   - APIs oficiales (requieren auth): http://127.0.0.1:8000/api/evaluaciones/oficial/superadmin/")
    else:
        print("\n❌ Servidor no accesible")
