#!/usr/bin/env python3
"""
Script de prueba completa del flujo de asignación de evaluaciones
"""

import requests
import json

# Configuración
TOKEN = '5d653054f4356e1a4b165772e6c3af1244dc7b14'
BASE_URL = 'http://localhost:8000/api'
HEADERS = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_flujo_completo():
    print("🚀 Iniciando prueba completa del flujo de asignación")
    print("=" * 60)
    
    # 1. Obtener evaluaciones disponibles
    print("1️⃣ Obteniendo evaluaciones disponibles...")
    try:
        response = requests.get(f'{BASE_URL}/appraisal/evaluaciones/', headers=HEADERS)
        if response.status_code == 200:
            evaluaciones = response.json()
            print(f"   ✅ {len(evaluaciones)} evaluaciones encontradas")
            evaluacion_id = evaluaciones[0]['evaluacion_id']
            evaluacion_titulo = evaluaciones[0]['titulo']
            print(f"   📋 Usando evaluación: {evaluacion_titulo} (ID: {evaluacion_id})")
        else:
            print(f"   ❌ Error obteniendo evaluaciones: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return
    
    # 2. Obtener empleados disponibles
    print("\n2️⃣ Obteniendo empleados disponibles...")
    try:
        response = requests.get(f'{BASE_URL}/empleados/', headers=HEADERS)
        if response.status_code == 200:
            empleados = response.json()
            empleados_activos = [emp for emp in empleados if emp['status']]
            print(f"   ✅ {len(empleados_activos)} empleados activos encontrados")
            if empleados_activos:
                empleado_id = empleados_activos[0]['empleado_id']
                empleado_nombre = f"{empleados_activos[0]['nombre']} {empleados_activos[0]['apellido_paterno']}"
                print(f"   👤 Usando empleado: {empleado_nombre} (ID: {empleado_id})")
        else:
            print(f"   ❌ Error obteniendo empleados: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return
    
    # 3. Crear asignación
    print("\n3️⃣ Creando asignación...")
    try:
        asignacion_data = {
            'evaluacion': evaluacion_id,
            'fecha_inicio': '2025-08-07',
            'fecha_fin': '2025-09-07',
            'status': True
        }
        response = requests.post(f'{BASE_URL}/appraisal/asignaciones/', 
                               headers=HEADERS, json=asignacion_data)
        if response.status_code == 201:
            asignacion = response.json()
            asignacion_id = asignacion['asignacion_id']
            print(f"   ✅ Asignación creada con ID: {asignacion_id}")
        else:
            print(f"   ❌ Error creando asignación: {response.status_code}")
            print(f"   📋 Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return
    
    # 4. Asignar empleados
    print("\n4️⃣ Asignando empleados a la evaluación...")
    try:
        empleados_data = {'empleado_ids': [empleado_id]}
        response = requests.post(f'{BASE_URL}/appraisal/asignaciones/{asignacion_id}/asignar_empleados/', 
                               headers=HEADERS, json=empleados_data)
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Empleados asignados exitosamente")
            print(f"   📋 Mensaje: {result.get('status', 'Éxito')}")
        else:
            print(f"   ❌ Error asignando empleados: {response.status_code}")
            print(f"   📋 Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return
    
    # 5. Verificar asignaciones
    print("\n5️⃣ Verificando asignaciones creadas...")
    try:
        response = requests.get(f'{BASE_URL}/appraisal/asignaciones/', headers=HEADERS)
        if response.status_code == 200:
            asignaciones = response.json()
            print(f"   ✅ {len(asignaciones)} asignaciones totales en el sistema")
            # Buscar nuestra asignación
            nuestra_asignacion = next((a for a in asignaciones if a['asignacion_id'] == asignacion_id), None)
            if nuestra_asignacion:
                empleados_asignados = len(nuestra_asignacion.get('asignaciones_empleado', []))
                print(f"   👥 Empleados asignados a nuestra evaluación: {empleados_asignados}")
        else:
            print(f"   ❌ Error verificando asignaciones: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Prueba completa finalizada exitosamente!")
    print(f"📊 Resumen: Evaluación '{evaluacion_titulo}' asignada a empleado '{empleado_nombre}'")

if __name__ == "__main__":
    test_flujo_completo()
