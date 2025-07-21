#!/usr/bin/env python
import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = 'http://localhost:8000'
USERNAME = 'admin_empresa'
PASSWORD = 'admin123'

def login_and_get_token():
    """Obtener token de autenticación"""
    print('🔐 Iniciando sesión...')
    
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    response = requests.post(f'{BASE_URL}/api/auth/login/', json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f'✅ Login exitoso - Token obtenido')
        return token
    else:
        print(f'❌ Error en login: {response.status_code}')
        print(response.text)
        return None

def test_evaluaciones_activas(token):
    """Probar endpoint de evaluaciones activas mejorado"""
    print('\n🧪 PROBANDO: Evaluaciones activas mejoradas')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/evaluaciones/asignaciones/evaluaciones_activas/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Evaluaciones obtenidas: {len(data)}')
        
        for evaluacion in data:
            print(f'\n📊 {evaluacion["titulo"]}')
            print(f'   ID: {evaluacion["id"]}')
            print(f'   Tipo: {evaluacion["tipo_evaluacion_nombre"]}')
            print(f'   Identificador único: {evaluacion.get("identificador_unico", "No disponible")}')
            print(f'   Total empleados asignados: {evaluacion.get("total_empleados_asignados", 0)}')
            print(f'   Estados de asignaciones: {evaluacion.get("asignaciones_por_estado", {})}')
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text)

def test_empleados_asignados(token, evaluacion_id):
    """Probar endpoint de empleados asignados a evaluación específica"""
    print(f'\n🧪 PROBANDO: Empleados asignados a evaluación {evaluacion_id}')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/evaluaciones/asignaciones/{evaluacion_id}/empleados_asignados/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Datos obtenidos para: {data["evaluacion_titulo"]}')
        print(f'   Tipo: {data["evaluacion_tipo"]}')
        print(f'   Total empleados: {data["total_empleados_asignados"]}')
        print(f'   Resumen estados: {data["resumen_estados"]}')
        
        print('\n👥 Empleados asignados:')
        for empleado in data['empleados']:
            print(f'   - {empleado["nombre"]} {empleado["apellido"]}')
            print(f'     Email: {empleado["email"]}')
            print(f'     Departamento: {empleado["departamento"]}')
            print(f'     Estado: {empleado["estado_asignacion"]}')
            print(f'     Duración: {empleado["duracion_dias"]} días / {empleado["duracion_horas"]} horas')
            print(f'     Días restantes: {empleado["dias_restantes"]}')
            print()
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text)

def test_asignacion_masiva_mejorada(token):
    """Probar asignación masiva con nuevos campos"""
    print('\n🧪 PROBANDO: Asignación masiva mejorada')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Datos de prueba con nuevos campos
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=20)
    
    asignacion_data = {
        'evaluacion_id': 3,  # NOM-030 original
        'empleados_ids': [1, 2],  # IDs de empleados existentes
        'fecha_inicio': fecha_inicio.isoformat(),
        'fecha_fin': fecha_fin.isoformat(),
        'duracion_dias': 20,
        'duracion_horas': 3,
        'instrucciones_especiales': 'Evaluación prioritaria - completar antes del cierre del trimestre'
    }
    
    response = requests.post(f'{BASE_URL}/api/evaluaciones/asignaciones/asignar_masivo/', 
                           json=asignacion_data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Asignación masiva exitosa')
        print(f'   Asignaciones creadas: {data.get("asignaciones_creadas", 0)}')
        print(f'   Tokens generados: {data.get("tokens_generados", 0)}')
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text)

def test_tokens_mejorados(token):
    """Probar endpoint de tokens con información mejorada"""
    print('\n🧪 PROBANDO: Tokens con información de empleados')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/api/evaluaciones/tokens/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Tokens obtenidos: {len(data)}')
        
        for token_info in data[:3]:  # Mostrar solo los primeros 3
            print(f'\n🎫 Token: {token_info["token"][:20]}...')
            print(f'   Empleado: {token_info["empleado_nombre"]} {token_info["empleado_apellido"]}')
            print(f'   Email: {token_info["empleado_email"]}')
            print(f'   Número empleado: {token_info["empleado_numero_empleado"]}')
            print(f'   Puesto: {token_info["empleado_puesto"]}')
            print(f'   Departamento: {token_info["empleado_departamento"]}')
            print(f'   Evaluación: {token_info["evaluacion_titulo"]}')
            print(f'   Tipo evaluación: {token_info["evaluacion_tipo"]}')
            print(f'   Estado: {token_info["estado_asignacion"]}')
            print(f'   Duración: {token_info["duracion_dias"]} días / {token_info["duracion_horas"]} horas')
            print(f'   {token_info["tiempo_restante_texto"]}')
    else:
        print(f'❌ Error: {response.status_code}')
        print(response.text)

def main():
    print('🚀 PRUEBA DE FUNCIONALIDADES MEJORADAS DE EVALUACIONES')
    print('=' * 60)
    
    # 1. Login
    token = login_and_get_token()
    if not token:
        return
    
    # 2. Probar evaluaciones activas mejoradas
    test_evaluaciones_activas(token)
    
    # 3. Probar empleados asignados a evaluación específica
    test_empleados_asignados(token, 3)  # Probar con evaluación ID 3
    
    # 4. Probar asignación masiva mejorada
    test_asignacion_masiva_mejorada(token)
    
    # 5. Probar tokens mejorados
    test_tokens_mejorados(token)
    
    print('\n🎉 Pruebas completadas')

if __name__ == '__main__':
    main()
