#!/usr/bin/env python
"""
Script para probar el endpoint de usuarios de planta
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
import json
from apps.users.models import AdminPlanta, PerfilUsuario

def test_endpoint_usuarios_planta():
    """Probar el endpoint de usuarios de planta"""
    print("=== PRUEBA ENDPOINT USUARIOS DE PLANTA ===\n")
    
    # URL base
    base_url = "http://localhost:8000"
    
    # Datos de login del admin de empresa
    login_data = {
        "username": "admin_empresa_1",
        "password": "admin123"
    }
    
    # Login
    print("1. Realizando login...")
    try:
        login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('token')
            print(f"   ✓ Login exitoso. Token: {token[:20]}...")
            
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            # Probar endpoint de usuarios de planta
            print("\n2. Obteniendo usuarios de planta...")
            usuarios_response = requests.get(f"{base_url}/plantas/usuarios_planta/", headers=headers)
            
            if usuarios_response.status_code == 200:
                usuarios_data = usuarios_response.json()
                print(f"   ✓ Endpoint funcionando. Usuarios encontrados: {len(usuarios_data)}")
                
                for i, usuario in enumerate(usuarios_data, 1):
                    print(f"\n   Usuario {i}:")
                    print(f"     Planta: {usuario['planta_nombre']} (ID: {usuario['planta_id']})")
                    if usuario['status']:
                        print(f"     Username: {usuario['username']}")
                        print(f"     Email: {usuario['email']}")
                        print(f"     Nombre: {usuario['nombre_completo']}")
                        print(f"     Fecha creación: {usuario['fecha_creacion']}")
                    else:
                        print(f"     ⚠ Sin usuario asignado")
            else:
                print(f"   ✗ Error en endpoint: {usuarios_response.status_code}")
                print(f"     Respuesta: {usuarios_response.text}")
                
        else:
            print(f"   ✗ Error en login: {login_response.status_code}")
            print(f"     Respuesta: {login_response.text}")
            
    except Exception as e:
        print(f"   ✗ Error durante la prueba: {str(e)}")

def mostrar_usuarios_db():
    """Mostrar usuarios directamente de la base de datos"""
    print("\n=== USUARIOS EN BASE DE DATOS ===\n")
    
    admin_plantas = AdminPlanta.objects.all()
    
    if admin_plantas.exists():
        for i, admin_planta in enumerate(admin_plantas, 1):
            usuario = admin_planta.usuario.user
            planta = admin_planta.planta
            
            print(f"{i}. Planta: {planta.nombre} (ID: {planta.planta_id})")
            print(f"   Usuario: {usuario.username}")
            print(f"   Email: {usuario.email}")
            print(f"   Nombre: {usuario.first_name} {usuario.last_name}")
            print(f"   Fecha asignación: {admin_planta.fecha_asignacion}")
            print(f"   Status: {'Activo' if admin_planta.status else 'Inactivo'}")
            print()
    else:
        print("No hay usuarios de planta en la base de datos.")

if __name__ == "__main__":
    mostrar_usuarios_db()
    test_endpoint_usuarios_planta()
