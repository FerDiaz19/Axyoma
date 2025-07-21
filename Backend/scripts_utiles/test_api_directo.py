#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def get_or_create_token(username):
    """Obtener o crear token para usuario"""
    try:
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        return token.key
    except User.DoesNotExist:
        return None

def test_apis_directamente():
    """Probar APIs usando token directo de Django"""
    print('🚀 PRUEBA DIRECTA DE FUNCIONALIDADES MEJORADAS')
    print('=' * 60)
    
    # Obtener token directamente
    token_key = get_or_create_token('admin_empresa')
    if not token_key:
        print('❌ No se pudo obtener token')
        return
    
    print(f'✅ Token obtenido: {token_key[:20]}...')
    
    BASE_URL = 'http://localhost:8000'
    headers = {'Authorization': f'Token {token_key}'}
    
    # 1. Probar evaluaciones activas mejoradas
    print('\n🧪 PROBANDO: Evaluaciones activas mejoradas')
    try:
        response = requests.get(f'{BASE_URL}/api/evaluaciones/asignaciones/evaluaciones_activas/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Evaluaciones obtenidas: {len(data)}')
            
            for evaluacion in data[:2]:  # Mostrar solo las primeras 2
                print(f'\n📊 {evaluacion["titulo"]}')
                print(f'   ID: {evaluacion["id"]}')
                print(f'   Tipo: {evaluacion.get("tipo_evaluacion_nombre", "No disponible")}')
                print(f'   Identificador único: {evaluacion.get("identificador_unico", "No disponible")}')
                print(f'   Total empleados asignados: {evaluacion.get("total_empleados_asignados", 0)}')
                print(f'   Estados de asignaciones: {evaluacion.get("asignaciones_por_estado", {})}')
        else:
            print(f'❌ Error: {response.status_code}')
            print(response.text[:200])
    except Exception as e:
        print(f'❌ Error en evaluaciones activas: {e}')
    
    # 2. Probar empleados asignados
    print('\n🧪 PROBANDO: Empleados asignados a evaluación ID 3')
    try:
        response = requests.get(f'{BASE_URL}/api/evaluaciones/asignaciones/3/empleados_asignados/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Datos obtenidos para: {data["evaluacion_titulo"]}')
            print(f'   Total empleados: {data["total_empleados_asignados"]}')
            print(f'   Resumen estados: {data["resumen_estados"]}')
            
            if data['empleados']:
                empleado = data['empleados'][0]  # Mostrar primer empleado
                print(f'\n👤 Primer empleado:')
                print(f'   Nombre: {empleado["nombre"]} {empleado["apellido"]}')
                print(f'   Estado: {empleado["estado_asignacion"]}')
                print(f'   Duración: {empleado["duracion_dias"]} días / {empleado["duracion_horas"]} horas')
                print(f'   Días restantes: {empleado["dias_restantes"]}')
        else:
            print(f'❌ Error: {response.status_code}')
            print(response.text[:200])
    except Exception as e:
        print(f'❌ Error en empleados asignados: {e}')
    
    # 3. Probar tokens mejorados
    print('\n🧪 PROBANDO: Tokens con información mejorada')
    try:
        response = requests.get(f'{BASE_URL}/api/evaluaciones/tokens/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Tokens obtenidos: {len(data)}')
            
            if data:
                token_info = data[0]  # Mostrar primer token
                print(f'\n🎫 Primer token:')
                print(f'   Empleado: {token_info.get("empleado_nombre", "N/A")} {token_info.get("empleado_apellido", "")}')
                print(f'   Email: {token_info.get("empleado_email", "N/A")}')
                print(f'   Evaluación: {token_info.get("evaluacion_titulo", "N/A")}')
                print(f'   Tipo: {token_info.get("evaluacion_tipo", "N/A")}')
                print(f'   Estado: {token_info.get("estado_asignacion", "N/A")}')
                print(f'   Tiempo restante: {token_info.get("tiempo_restante_texto", "N/A")}')
        else:
            print(f'❌ Error: {response.status_code}')
            print(response.text[:200])
    except Exception as e:
        print(f'❌ Error en tokens: {e}')
    
    print('\n🎉 Pruebas completadas')

if __name__ == '__main__':
    test_apis_directamente()
