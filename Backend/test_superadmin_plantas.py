#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario
import requests

def test_superadmin_endpoint():
    print("🔍 Testing SuperAdmin listar_todas_plantas endpoint...")
    
    try:
        # Buscar usuario superadmin
        superadmin_user = User.objects.filter(is_superuser=True).first()
        if not superadmin_user:
            print("❌ No superuser found in database")
            return
            
        print(f"✅ Found superuser: {superadmin_user.username}")
        
        # Hacer la request usando la sesión de Django directamente
        from django.test import Client
        client = Client()
        client.force_login(superadmin_user)
        
        response = client.get('/api/superadmin/listar_todas_plantas/')
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            print(f"✅ SUCCESS! Found {len(data)} plantas")
            
            # Mostrar primer planta como ejemplo
            if data:
                primera_planta = data[0]
                print(f"📋 Ejemplo planta: {primera_planta['nombre']} - Empresa: {primera_planta['empresa']['nombre']}")
        else:
            print(f"❌ Error response: {response.content}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_superadmin_endpoint()
