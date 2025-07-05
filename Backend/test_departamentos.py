#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba específica de departamentos y empleados
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_departamentos():
    print("🏢 PROBANDO DEPARTAMENTOS Y EMPLEADOS")
    print("=" * 50)
    
    # 1. Login
    login_data = {'username': 'juan.perez@codewave.com', 'password': '1234'}
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login falló: {response.status_code}")
        return
    
    token = response.json().get('token')
    headers = {'Authorization': f'Token {token}'}
    print(f"✅ Login exitoso, token obtenido")
    
    # 2. Obtener plantas disponibles
    print("\n📋 Obteniendo plantas disponibles...")
    response = requests.get(f'{BASE_URL}/plantas/', headers=headers)
    if response.status_code == 200:
        plantas = response.json()
        print(f"✅ {len(plantas)} plantas disponibles")
        if plantas:
            primera_planta = plantas[0]
            planta_id = primera_planta['planta_id']
            print(f"📍 Usando planta: {primera_planta['nombre']} (ID: {planta_id})")
        else:
            print("❌ No hay plantas disponibles")
            return
    else:
        print(f"❌ Error obteniendo plantas: {response.status_code}")
        return
    
    # 3. Crear departamento
    print("\n🏭 Creando departamento...")
    dept_data = {
        'nombre': 'Departamento de Prueba API',
        'descripcion': 'Departamento creado desde script de prueba',
        'planta_id': planta_id
    }
    response = requests.post(f'{BASE_URL}/departamentos/', json=dept_data, headers=headers)
    if response.status_code == 201:
        nuevo_dept = response.json()
        dept_id = nuevo_dept['departamento_id']
        print(f"✅ Departamento creado: {nuevo_dept['nombre']} (ID: {dept_id})")
    else:
        print(f"❌ Error creando departamento: {response.status_code}")
        print(f"📄 Respuesta: {response.text}")
        return
    
    # 4. Crear puesto
    print("\n💼 Creando puesto...")
    puesto_data = {
        'nombre': 'Puesto de Prueba API',
        'descripcion': 'Puesto creado desde script de prueba',
        'departamento_id': dept_id
    }
    response = requests.post(f'{BASE_URL}/puestos/', json=puesto_data, headers=headers)
    if response.status_code == 201:
        nuevo_puesto = response.json()
        puesto_id = nuevo_puesto['puesto_id']
        print(f"✅ Puesto creado: {nuevo_puesto['nombre']} (ID: {puesto_id})")
    else:
        print(f"❌ Error creando puesto: {response.status_code}")
        print(f"📄 Respuesta: {response.text}")
        return
    
    # 5. Crear empleado
    print("\n👤 Creando empleado...")
    empleado_data = {
        'nombre': 'Juan Carlos',
        'apellido_paterno': 'Pérez',
        'apellido_materno': 'González',
        'genero': 'Masculino',
        'antiguedad': 2,
        'puesto': puesto_id,
        'departamento': dept_id,
        'planta': planta_id
    }
    response = requests.post(f'{BASE_URL}/empleados/', json=empleado_data, headers=headers)
    if response.status_code == 201:
        nuevo_empleado = response.json()
        print(f"✅ Empleado creado: {nuevo_empleado['nombre']} {nuevo_empleado['apellido_paterno']}")
    else:
        print(f"❌ Error creando empleado: {response.status_code}")
        print(f"📄 Respuesta: {response.text}")
    
    # 6. Probar endpoints de datos disponibles
    print("\n📊 Probando endpoints de datos disponibles...")
    
    endpoints = [
        ('plantas_disponibles', f'{BASE_URL}/empleados/plantas_disponibles/'),
        ('departamentos_disponibles', f'{BASE_URL}/empleados/departamentos_disponibles/'),
        ('puestos_disponibles', f'{BASE_URL}/empleados/puestos_disponibles/')
    ]
    
    for nombre, url in endpoints:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {nombre}: {len(data)} items")
        else:
            print(f"❌ {nombre}: Error {response.status_code}")
    
    print("\n🎉 PRUEBA DE DEPARTAMENTOS Y EMPLEADOS COMPLETADA")

if __name__ == '__main__':
    test_departamentos()
