#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el sistema de respaldos directamente
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def probar_respaldos():
    print("🧪 PRUEBA DIRECTA DEL SISTEMA DE RESPALDOS")
    print("=" * 50)
    
    # Probar endpoint de verificación
    try:
        print("1. Probando endpoint de verificación...")
        
        # Necesitamos autenticarnos primero
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        verificar_url = "http://127.0.0.1:8000/api/admin-bd/respaldos/verificar/"
        
        # Login como superadmin
        login_data = {
            "username": "superadmin",
            "password": "1234"
        }
        
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json().get('access')
            print(f"✅ Login exitoso")
            
            # Probar verificación
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            verificar_response = requests.get(verificar_url, headers=headers)
            
            if verificar_response.status_code == 200:
                data = verificar_response.json()
                print("✅ Endpoint de verificación funciona")
                print(f"📁 Directorio: {data.get('directorio_respaldos')}")
                print(f"📁 Existe: {data.get('directorio_existe')}")
                print(f"🔐 Permisos: {data.get('permisos_escritura')}")
                print(f"🗄️ BD Config: {data.get('bd_config_ok')}")
                print(f"📄 Archivos: {data.get('archivos_respaldo_existentes')}")
                
                # Probar creación de respaldo
                print("\n2. Probando creación de respaldo completo...")
                
                respaldo_url = "http://127.0.0.1:8000/api/admin-bd/respaldos/bd-completa/"
                respaldo_data = {
                    "incluir_datos": True,
                    "descripcion": "Prueba desde script de verificación"
                }
                
                respaldo_response = requests.post(respaldo_url, headers=headers, json=respaldo_data)
                
                if respaldo_response.status_code == 200:
                    respaldo_result = respaldo_response.json()
                    print("✅ Respaldo completo creado exitosamente")
                    print(f"📄 Archivo: {respaldo_result.get('archivo')}")
                    print(f"📊 Tamaño: {respaldo_result.get('tamaño_mb')} MB")
                    print(f"📁 Ruta: {respaldo_result.get('ruta')}")
                else:
                    print(f"❌ Error al crear respaldo: {respaldo_response.status_code}")
                    error_data = respaldo_response.json()
                    print(f"Error: {error_data}")
                    
            else:
                print(f"❌ Error en verificación: {verificar_response.status_code}")
                print(f"Respuesta: {verificar_response.text}")
                
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Respuesta: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error en prueba: {str(e)}")

if __name__ == '__main__':
    probar_respaldos()
