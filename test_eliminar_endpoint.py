#!/usr/bin/env python3
"""
Script para probar directamente el endpoint de eliminar planta
"""

import requests
import json

def test_eliminar_planta():
    print("🧪 PROBANDO ENDPOINT ELIMINAR PLANTA")
    print("=" * 50)

    # Configuración
    base_url = "http://localhost:8000"
    
    # Credenciales de prueba (ajustar según sea necesario)
    username = "admin_prueba"  # O el usuario que tengas
    password = "admin123"
    
    try:
        # 1. Login
        print("1. 🔑 Haciendo login...")
        login_data = {
            "username": username,
            "password": password
        }
        
        login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        login_result = login_response.json()
        token = login_result.get('token')
        user_data = login_result.get('user')
        
        print(f"✅ Login exitoso!")
        print(f"   Usuario: {user_data.get('username')}")
        print(f"   Nivel: {user_data.get('nivel_usuario')}")
        print(f"   Empresa ID: {user_data.get('empresa_id')}")
        
        # Headers para requests autenticados
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        # 2. Obtener plantas disponibles
        print("\n2. 📋 Obteniendo plantas disponibles...")
        plantas_params = ""
        if user_data.get('empresa_id'):
            plantas_params = f"?empresa_id={user_data.get('empresa_id')}&incluir_suspendidas=true"
        
        plantas_response = requests.get(f"{base_url}/api/plantas/{plantas_params}", headers=headers)
        
        if plantas_response.status_code != 200:
            print(f"❌ Error obteniendo plantas: {plantas_response.status_code}")
            print(f"Response: {plantas_response.text}")
            return
        
        plantas = plantas_response.json()
        print(f"✅ Plantas encontradas: {len(plantas)}")
        
        for planta in plantas:
            print(f"   - ID: {planta['planta_id']} | Nombre: {planta['nombre']} | Status: {planta['status']}")
        
        if not plantas:
            print("❌ No hay plantas para probar")
            return
        
        # 3. Seleccionar una planta para probar (la primera que no sea "Planta Principal")
        planta_prueba = None
        for planta in plantas:
            if planta['nombre'] != 'Planta Principal':
                planta_prueba = planta
                break
        
        if not planta_prueba:
            print("❌ No hay plantas adecuadas para probar (solo Planta Principal)")
            print("ℹ️  Evitamos eliminar la Planta Principal por seguridad")
            return
        
        print(f"\n3. 🎯 Planta seleccionada para prueba:")
        print(f"   ID: {planta_prueba['planta_id']}")
        print(f"   Nombre: {planta_prueba['nombre']}")
        print(f"   Status: {planta_prueba['status']}")
        
        # 4. Probar endpoint (SIN ELIMINAR REALMENTE)
        print(f"\n4. 🧪 Probando endpoint (método OPTIONS)...")
        options_response = requests.options(
            f"{base_url}/api/plantas/{planta_prueba['planta_id']}/eliminar_planta_completa/", 
            headers=headers
        )
        
        print(f"✅ OPTIONS response: {options_response.status_code}")
        
        # 5. Confirmación antes de eliminar
        print(f"\n⚠️  CONFIRMACIÓN:")
        print(f"¿Desea REALMENTE eliminar la planta '{planta_prueba['nombre']}'?")
        print(f"Esta acción es IRREVERSIBLE.")
        
        confirm = input("Escriba 'ELIMINAR' para continuar, o Enter para cancelar: ")
        
        if confirm != 'ELIMINAR':
            print("✅ Operación cancelada por el usuario")
            return
        
        # 6. Eliminar planta
        print(f"\n6. 🗑️ Eliminando planta...")
        delete_response = requests.delete(
            f"{base_url}/api/plantas/{planta_prueba['planta_id']}/eliminar_planta_completa/", 
            headers=headers
        )
        
        print(f"Response status: {delete_response.status_code}")
        
        if delete_response.status_code == 200:
            result = delete_response.json()
            print(f"✅ Planta eliminada exitosamente!")
            print(f"Mensaje: {result.get('message')}")
            print(f"Entidades eliminadas:")
            for key, value in result.get('entidades_eliminadas', {}).items():
                print(f"  - {key}: {value}")
        else:
            print(f"❌ Error eliminando planta:")
            print(f"Status: {delete_response.status_code}")
            print(f"Response: {delete_response.text}")
        
    except Exception as e:
        print(f"❌ Error en el script: {e}")

if __name__ == '__main__':
    test_eliminar_planta()
