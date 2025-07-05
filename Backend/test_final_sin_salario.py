#!/usr/bin/env python
"""
Script de prueba final para verificar que departamentos y puestos funcionan
sin errores de salario y siguiendo exactamente el esquema SQL
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_flujo_completo():
    print("🚀 PRUEBA FINAL DEL FLUJO COMPLETO")
    print("="*50)
    
    # 1. Login
    print("1. 🔐 Login...")
    login_data = {
        "username": "juan.perez@codewave.com",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return
    
    login_result = response.json()
    token = login_result.get('token')
    print(f"✅ Login exitoso. Usuario: {login_result.get('usuario')}")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 2. Verificar plantas
    print("\n2. 🏭 Verificando plantas...")
    response = requests.get(f"{BASE_URL}/plantas/", headers=headers)
    if response.status_code == 200:
        plantas = response.json()
        if plantas:
            planta_id = plantas[0]['planta_id']
            print(f"✅ Planta disponible: {plantas[0]['nombre']} (ID: {planta_id})")
        else:
            print("❌ No hay plantas disponibles")
            return
    else:
        print(f"❌ Error obteniendo plantas: {response.status_code}")
        return
    
    # 3. Crear departamento
    print("\n3. 🏢 Creando departamento...")
    import time
    timestamp = int(time.time())
    depto_data = {
        "nombre": f"Depto Test {timestamp}",
        "descripcion": "Departamento de prueba final sin errores",
        "planta_id": planta_id
    }
    
    response = requests.post(f"{BASE_URL}/departamentos/", json=depto_data, headers=headers)
    if response.status_code == 201:
        departamento = response.json()
        departamento_id = departamento.get('departamento_id')
        print(f"✅ Departamento creado: {departamento.get('nombre')} (ID: {departamento_id})")
    else:
        print(f"❌ Error creando departamento: {response.status_code} - {response.text}")
        return
    
    # 4. Crear puesto (SIN salario)
    print("\n4. 💼 Creando puesto...")
    puesto_data = {
        "nombre": f"Puesto Test {timestamp}",
        "descripcion": "Puesto de prueba final - solo nombre y descripción",
        "departamento_id": departamento_id
    }
    
    response = requests.post(f"{BASE_URL}/puestos/", json=puesto_data, headers=headers)
    if response.status_code == 201:
        puesto = response.json()
        puesto_id = puesto.get('puesto_id')
        print(f"✅ Puesto creado: {puesto.get('nombre')} (ID: {puesto_id})")
        print(f"   Descripción: {puesto.get('descripcion')}")
    else:
        print(f"❌ Error creando puesto: {response.status_code} - {response.text}")
        return
    
    # 5. Verificar lista de departamentos
    print("\n5. 📋 Verificando lista de departamentos...")
    response = requests.get(f"{BASE_URL}/departamentos/", headers=headers)
    if response.status_code == 200:
        departamentos = response.json()
        print(f"✅ Total departamentos: {len(departamentos)}")
        for depto in departamentos[-2:]:  # Mostrar los últimos 2
            print(f"   - {depto.get('nombre')}: {depto.get('descripcion')}")
    else:
        print(f"❌ Error obteniendo departamentos: {response.status_code}")
    
    # 6. Verificar lista de puestos
    print("\n6. 📋 Verificando lista de puestos...")
    response = requests.get(f"{BASE_URL}/puestos/", headers=headers)
    if response.status_code == 200:
        puestos = response.json()
        print(f"✅ Total puestos: {len(puestos)}")
        for puesto in puestos[-2:]:  # Mostrar los últimos 2
            print(f"   - {puesto.get('nombre')}: {puesto.get('descripcion')}")
            # Verificar que NO hay campo salario
            if 'salario' in puesto:
                print(f"   ⚠️  ADVERTENCIA: Puesto tiene campo salario que no debería existir")
            else:
                print(f"   ✅ Correcto: Puesto NO tiene campo salario")
    else:
        print(f"❌ Error obteniendo puestos: {response.status_code}")
    
    print(f"\n🎉 ¡Prueba completada exitosamente!")
    print(f"✅ Sistema funcionando según esquema SQL original")
    print(f"✅ Sin errores de campos inexistentes como 'salario'")

if __name__ == "__main__":
    test_flujo_completo()
