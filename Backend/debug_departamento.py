#!/usr/bin/env python
"""
Script para debugging de creación de departamentos
"""
import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario, Empresa, Planta
from rest_framework.authtoken.models import Token

def test_departamento_creation():
    print("🔍 DEBUG: Creación de Departamentos")
    print("="*50)
    
    # 1. Obtener datos de prueba
    try:
        # Buscar admin de empresa de prueba
        admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
        if not admin_empresa:
            print("❌ No se encontró admin de empresa")
            return
            
        print(f"✅ Admin encontrado: {admin_empresa.nombre} (ID: {admin_empresa.id})")
        
        # Buscar empresa
        empresa = Empresa.objects.filter(administrador=admin_empresa).first()
        if not empresa:
            print("❌ No se encontró empresa para el admin")
            return
            
        print(f"✅ Empresa encontrada: {empresa.nombre} (ID: {empresa.empresa_id})")
        
        # Buscar planta
        planta = Planta.objects.filter(empresa=empresa).first()
        if not planta:
            print("❌ No se encontró planta para la empresa")
            return
            
        print(f"✅ Planta encontrada: {planta.nombre} (ID: {planta.planta_id})")
        
        # Obtener token
        token, created = Token.objects.get_or_create(user=admin_empresa.user)
        print(f"✅ Token obtenido: {token.key[:10]}...")
        
    except Exception as e:
        print(f"❌ Error obteniendo datos: {e}")
        return
    
    # 2. Probar creación via API
    print("\n🌐 Probando creación via API...")
    
    url = "http://127.0.0.1:8000/api/departamentos/"
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }
    
    # Datos para crear departamento
    data = {
        'nombre': 'Departamento de Prueba Debug',
        'descripcion': 'Departamento creado para debugging',
        'planta_id': planta.planta_id
    }
    
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📝 Response Text: {response.text}")
        
        if response.status_code == 201:
            print("✅ Departamento creado exitosamente!")
            result = response.json()
            print(f"   ID: {result.get('departamento_id')}")
            print(f"   Nombre: {result.get('nombre')}")
        else:
            print("❌ Error en la creación:")
            try:
                error_data = response.json()
                print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error Text: {response.text}")
                
    except Exception as e:
        print(f"❌ Error en la petición: {e}")

if __name__ == "__main__":
    test_departamento_creation()
