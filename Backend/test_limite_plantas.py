#!/usr/bin/env python
"""
Script para probar el límite de plantas y creación automática de usuario de planta
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
import json
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def test_limite_plantas():
    """Probar el límite de 5 plantas por empresa"""
    print("=== PRUEBA DE LÍMITE DE PLANTAS ===\n")
    
    # URL base
    base_url = "http://localhost:8000"
    
    # Datos de login del admin de empresa
    login_data = {
        "username": "admin_empresa_1",
        "password": "admin123"
    }
    
    # Login
    print("1. Realizando login...")
    login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result.get('token')
        print(f"   ✓ Login exitoso. Token: {token[:20]}...")
        
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        # Obtener plantas actuales
        print("\n2. Obteniendo plantas actuales...")
        plantas_response = requests.get(f"{base_url}/plantas/", headers=headers)
        if plantas_response.status_code == 200:
            plantas_actuales = plantas_response.json()
            print(f"   ✓ Plantas actuales: {len(plantas_actuales)}")
            
            for i, planta in enumerate(plantas_actuales, 1):
                print(f"     {i}. {planta['nombre']} (ID: {planta['planta_id']})")
        
        # Intentar crear plantas hasta llegar al límite
        print("\n3. Intentando crear plantas...")
        
        for i in range(6):  # Intentar crear 6 plantas para probar el límite
            planta_data = {
                "nombre": f"Planta Test {i+1}",
                "direccion": f"Dirección de prueba {i+1}"
            }
            
            print(f"\n   Creando planta {i+1}: {planta_data['nombre']}")
            create_response = requests.post(f"{base_url}/plantas/", 
                                          json=planta_data, 
                                          headers=headers)
            
            if create_response.status_code == 201:
                planta_creada = create_response.json()
                print(f"     ✓ Planta creada exitosamente (ID: {planta_creada['planta_id']})")
                
                # Verificar que se creó el usuario de planta
                verificar_usuario_planta(planta_creada['planta_id'])
                
            elif create_response.status_code == 400:
                error_data = create_response.json()
                print(f"     ⚠ Error al crear planta: {error_data}")
                if "No se pueden crear más de 5 plantas" in str(error_data):
                    print("     ✓ Límite de plantas funcionando correctamente")
                    break
            else:
                print(f"     ✗ Error inesperado: {create_response.status_code}")
                print(f"       Respuesta: {create_response.text}")
        
        # Verificar estado final
        print("\n4. Estado final de plantas...")
        plantas_final_response = requests.get(f"{base_url}/plantas/", headers=headers)
        if plantas_final_response.status_code == 200:
            plantas_final = plantas_final_response.json()
            print(f"   ✓ Total de plantas: {len(plantas_final)}")
            
            for i, planta in enumerate(plantas_final, 1):
                print(f"     {i}. {planta['nombre']} (ID: {planta['planta_id']})")
        
    else:
        print(f"   ✗ Error en login: {login_response.status_code}")
        print(f"     Respuesta: {login_response.text}")

def verificar_usuario_planta(planta_id):
    """Verificar que se creó el usuario de planta"""
    try:
        planta = Planta.objects.get(planta_id=planta_id)
        admin_planta = AdminPlanta.objects.filter(planta=planta).first()
        
        if admin_planta:
            usuario = admin_planta.usuario.user
            print(f"     ✓ Usuario de planta creado:")
            print(f"       - Username: {usuario.username}")
            print(f"       - Email: {usuario.email}")
            print(f"       - Nombre: {usuario.first_name} {usuario.last_name}")
        else:
            print(f"     ⚠ No se encontró usuario de planta para planta ID {planta_id}")
            
    except Exception as e:
        print(f"     ✗ Error verificando usuario de planta: {str(e)}")

def listar_usuarios_planta():
    """Listar todos los usuarios de planta creados"""
    print("\n=== USUARIOS DE PLANTA CREADOS ===\n")
    
    admin_plantas = AdminPlanta.objects.all()
    
    if admin_plantas.exists():
        for i, admin_planta in enumerate(admin_plantas, 1):
            usuario = admin_planta.usuario.user
            planta = admin_planta.planta
            print(f"{i}. Usuario: {usuario.username}")
            print(f"   Planta: {planta.nombre}")
            print(f"   Email: {usuario.email}")
            print(f"   Nombre completo: {usuario.first_name} {usuario.last_name}")
            print()
    else:
        print("No hay usuarios de planta registrados.")

if __name__ == "__main__":
    try:
        test_limite_plantas()
        listar_usuarios_planta()
        
        print("\n=== RESUMEN ===")
        print("✓ Test de límite de plantas completado")
        print("✓ Verificación de creación automática de usuarios completada")
        
    except Exception as e:
        print(f"Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
