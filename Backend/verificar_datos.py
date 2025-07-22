# -*- coding: utf-8 -*-
"""
Script para verificar el formato de datos del SuperAdmin
"""
import requests
import json

# Configuración del servidor Django
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/superadmin/"

# Token del SuperAdmin
TOKEN = "2c1787a8c17851aa39fefc7bd760ad8eb5305556"

# Headers para las peticiones
headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def verificar_formato_datos():
    """Verificar el formato de datos devuelto por los endpoints"""
    print("🔍 === VERIFICANDO FORMATO DE DATOS ===")
    
    # Empresas
    print("\n📊 EMPRESAS:")
    response = requests.get(f"{API_URL}listar_empresas/", headers=headers)
    if response.status_code == 200:
        empresas = response.json()
        print(f"   📋 Datos completos: {json.dumps(empresas, indent=2, ensure_ascii=False)}")
        if isinstance(empresas, list) and len(empresas) > 0:
            print(f"   🧩 Primer registro: {json.dumps(empresas[0], indent=2, ensure_ascii=False)}")
    
    # Empleados
    print("\n👨‍💼 EMPLEADOS:")
    response = requests.get(f"{API_URL}listar_empleados/", headers=headers)
    if response.status_code == 200:
        empleados = response.json()
        print(f"   📋 Datos completos: {json.dumps(empleados, indent=2, ensure_ascii=False)}")
        if isinstance(empleados, list) and len(empleados) > 0:
            print(f"   🧩 Primer registro: {json.dumps(empleados[0], indent=2, ensure_ascii=False)}")
    
    # Usuarios
    print("\n👤 USUARIOS:")
    response = requests.get(f"{API_URL}listar_usuarios/", headers=headers)
    if response.status_code == 200:
        usuarios = response.json()
        print(f"   📋 Datos completos: {json.dumps(usuarios, indent=2, ensure_ascii=False)}")
        if isinstance(usuarios, list) and len(usuarios) > 0:
            print(f"   🧩 Primer registro: {json.dumps(usuarios[0], indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    verificar_formato_datos()
