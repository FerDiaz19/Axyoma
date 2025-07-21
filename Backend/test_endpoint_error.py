#!/usr/bin/env python
import requests
import os
import django

# Setup Django para obtener token
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def test_evaluaciones_endpoint():
    """Probar endpoint de evaluaciones activas para generar error"""
    print('🔍 PROBANDO ENDPOINT DE EVALUACIONES ACTIVAS')
    print('=' * 50)
    
    # Obtener token de admin_empresa
    try:
        user = User.objects.get(username='admin_empresa')
        token, created = Token.objects.get_or_create(user=user)
        print(f'✅ Token obtenido para {user.username}')
    except User.DoesNotExist:
        print('❌ Usuario admin_empresa no encontrado')
        return
    
    # Probar endpoint
    BASE_URL = 'http://localhost:8000'
    headers = {'Authorization': f'Token {token.key}'}
    
    print('\n📡 Haciendo request a evaluaciones activas...')
    try:
        response = requests.get(f'{BASE_URL}/api/evaluaciones/asignaciones/evaluaciones_activas/', headers=headers)
        
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Respuesta exitosa - {len(data)} evaluaciones encontradas')
            for eval in data[:2]:  # Mostrar primeras 2
                print(f'   - {eval.get("titulo", "Sin título")}')
        else:
            print(f'❌ Error {response.status_code}')
            print(f'Response: {response.text[:500]}')
            
    except requests.exceptions.ConnectionError:
        print('❌ Error de conexión - ¿Está corriendo el servidor?')
    except Exception as e:
        print(f'❌ Error inesperado: {e}')

if __name__ == '__main__':
    test_evaluaciones_endpoint()
