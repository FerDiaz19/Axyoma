#!/usr/bin/env python
"""
Script para debugear el endpoint usuarios-planta
"""
import os
import sys
import django

# Configurar Django
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
import json

def test_endpoint():
    """Test del endpoint usuarios-planta"""
    print("🔍 Testing endpoint usuarios-planta...")
    
    # URL del endpoint
    url = "http://localhost:8000/api/plantas/usuarios-planta/"
    
    # Headers básicos
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Test sin autenticación primero
    print("\n1. Test sin autenticación:")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return
    
    # Test con empresa_id específica
    print("\n2. Test con empresa_id=10:")
    try:
        response = requests.get(f"{url}?empresa_id=10", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 500:
            print("❌ Error 500 - Verificando estructura de base de datos...")
            # Verificar que la empresa existe
            from apps.users.models import Empresa, Planta, AdminPlanta
            
            empresa = Empresa.objects.filter(empresa_id=10).first()
            if empresa:
                print(f"✅ Empresa encontrada: {empresa.nombre}")
                plantas = Planta.objects.filter(empresa=empresa)
                print(f"✅ Plantas encontradas: {plantas.count()}")
                for planta in plantas:
                    print(f"  - {planta.nombre} (ID: {planta.planta_id})")
                    admin_plantas = AdminPlanta.objects.filter(planta=planta)
                    print(f"    Admins: {admin_plantas.count()}")
            else:
                print("❌ Empresa con ID 10 no encontrada")
                
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error interno: {e}")

def check_database():
    """Verificar estructura de la base de datos"""
    print("\n🔍 Verificando estructura de la base de datos...")
    
    from apps.users.models import Empresa, Planta, AdminPlanta, PerfilUsuario
    
    try:
        print(f"Empresas en total: {Empresa.objects.count()}")
        print(f"Plantas en total: {Planta.objects.count()}")
        print(f"AdminPlanta en total: {AdminPlanta.objects.count()}")
        
        # Verificar empresa 10 específicamente
        empresa = Empresa.objects.filter(empresa_id=10).first()
        if empresa:
            print(f"\n📋 Empresa 10: {empresa.nombre}")
            print(f"  Administrador: {empresa.administrador}")
            print(f"  Status: {empresa.status}")
            
            plantas = Planta.objects.filter(empresa=empresa)
            print(f"  Plantas: {plantas.count()}")
            
            for planta in plantas:
                print(f"    - {planta.nombre} (ID: {planta.planta_id}, Status: {planta.status})")
                
                # Verificar admins de planta
                try:
                    admin_plantas = AdminPlanta.objects.filter(planta=planta)
                    print(f"      AdminPlanta records: {admin_plantas.count()}")
                    
                    for admin_planta in admin_plantas:
                        print(f"        - Usuario: {admin_planta.usuario}")
                        print(f"          User asociado: {admin_planta.usuario.user if admin_planta.usuario else 'None'}")
                        print(f"          Status: {admin_planta.status}")
                        
                except Exception as e:
                    print(f"      ❌ Error accessing AdminPlanta: {e}")
        else:
            print("❌ Empresa 10 no encontrada")
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
    test_endpoint()
