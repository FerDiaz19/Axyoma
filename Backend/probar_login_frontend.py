#!/usr/bin/env python
"""
SCRIPT DE PRUEBA DE LOGIN
========================
Verifica que las credenciales funcionen correctamente
"""

import requests
import json

# URL del backend
BASE_URL = "http://localhost:8000/api"

def test_login(username, password, descripcion):
    """Prueba login con credenciales específicas"""
    print(f"\n🔍 Probando: {descripcion}")
    print(f"   Usuario: {username}")
    print(f"   Password: {'*' * len(password)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={
                "username": username,
                "password": password
            },
            headers={
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ LOGIN EXITOSO")
            print(f"   👤 Usuario: {data.get('usuario')}")
            print(f"   🏷️ Tipo: {data.get('nivel_usuario')}")
            print(f"   🎯 Dashboard: {data.get('tipo_dashboard')}")
            
            if data.get('empresa_id'):
                print(f"   🏢 Empresa: {data.get('nombre_empresa')} (ID: {data.get('empresa_id')})")
            
            if data.get('planta_id'):
                print(f"   📍 Planta: {data.get('nombre_planta')} (ID: {data.get('planta_id')})")
                
            return True
        else:
            print(f"   ❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   📝 Detalles: {error_data}")
            except:
                print(f"   📝 Detalles: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ ERROR DE CONEXIÓN: No se pudo conectar al servidor")
        print(f"   💡 Asegúrate de que Django esté ejecutándose en {BASE_URL}")
        return False
    except Exception as e:
        print(f"   ❌ ERROR INESPERADO: {e}")
        return False

def main():
    print("🧪 PRUEBA DE CREDENCIALES DEL SISTEMA AXYOMA")
    print("=" * 60)
    
    # Lista de credenciales a probar
    credenciales = [
        ("superadmin", "admin123", "SuperAdmin del Sistema"),
        ("admin_technomex", "admin123", "Admin de TechnoMex Industries"),
        ("admin_manu_gonzalez", "admin123", "Admin de Manufactura González"),
        ("admin_axis", "admin123", "Admin de Industrias AXIS"),
        ("admin_mdn", "admin123", "Admin de Manufacturas del Norte"),
        ("admin_techcorp", "admin123", "Admin de TechCorp Solutions"),
        # Algunos usuarios de plantas
        ("admin_planta_1_1", "admin123", "Admin Planta TechCorp Solutions - Planta 1"),
        ("admin_planta_2_1", "admin123", "Admin Planta Industrias AXIS - Planta 1"),
    ]
    
    exitosos = 0
    total = len(credenciales)
    
    for username, password, descripcion in credenciales:
        if test_login(username, password, descripcion):
            exitosos += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {exitosos}/{total} credenciales funcionan correctamente")
    
    if exitosos == total:
        print("🎉 ¡TODAS LAS CREDENCIALES FUNCIONAN!")
    elif exitosos > 0:
        print("⚠️ Algunas credenciales tienen problemas")
    else:
        print("❌ NINGUNA CREDENCIAL FUNCIONA - Revisar configuración")

if __name__ == "__main__":
    main()
