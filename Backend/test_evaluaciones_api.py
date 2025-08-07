#!/usr/bin/env python3
"""
Script para probar la API de evaluaciones y verificar la estructura de datos
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import json

def test_evaluaciones_api():
    """Probar la API de evaluaciones"""
    
    # Obtener token de usuario
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ No se encontró un superusuario")
        return
    
    token, created = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token.key}'}
    
    print(f"🔑 Usando token: {token.key}")
    print(f"👤 Usuario: {user.username}")
    print("-" * 50)
    
    # Probar endpoint de evaluaciones
    try:
        response = requests.get('http://localhost:8000/api/appraisal/evaluaciones/', headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta exitosa")
            print(f"🔢 Total evaluaciones: {len(data)}")
            
            # Mostrar estructura de la primera evaluación
            if data:
                print("\n📋 Estructura de la primera evaluación:")
                first_eval = data[0]
                for key, value in first_eval.items():
                    print(f"   {key}: {value}")
                
                # Verificar campos requeridos por el frontend
                required_fields = ['evaluacion_id', 'titulo', 'descripcion']
                print(f"\n🔍 Verificando campos requeridos:")
                for field in required_fields:
                    if field in first_eval:
                        print(f"   ✅ {field}: {first_eval[field]}")
                    else:
                        print(f"   ❌ {field}: FALTANTE")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📋 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    test_evaluaciones_api()
