#!/usr/bin/env python
"""
Script para probar login de usuarios de planta creados automáticamente
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

def test_login_usuarios_planta():
    """Probar login de usuarios de planta"""
    print("=== PRUEBA DE LOGIN USUARIOS DE PLANTA ===\n")
    
    # URL base
    base_url = "http://localhost:8000"
    
    # Obtener usuarios de planta
    admin_plantas = AdminPlanta.objects.all()
    
    if not admin_plantas.exists():
        print("No hay usuarios de planta para probar")
        return
    
    for admin_planta in admin_plantas:
        usuario = admin_planta.usuario.user
        planta = admin_planta.planta
        
        print(f"Probando login para: {usuario.username}")
        print(f"  Planta: {planta.nombre}")
        print(f"  Email: {usuario.email}")
        
        # Las contraseñas fueron generadas automáticamente, por lo que necesitamos
        # establecer una conocida para la prueba
        usuario.set_password("test123")
        usuario.save()
        
        # Datos de login
        login_data = {
            "username": usuario.username,
            "password": "test123"
        }
        
        # Intentar login
        try:
            login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"  ✓ Login exitoso")
                print(f"    Token: {login_result.get('token', '')[:20]}...")
                print(f"    Tipo dashboard: {login_result.get('tipo_dashboard', 'N/A')}")
                print(f"    Nivel usuario: {login_result.get('nivel_usuario', 'N/A')}")
                print(f"    Permisos: {login_result.get('permisos', [])}")
            else:
                print(f"  ✗ Error en login: {login_response.status_code}")
                print(f"    Respuesta: {login_response.text}")
                
        except Exception as e:
            print(f"  ✗ Excepción durante login: {str(e)}")
        
        print()

def mostrar_credenciales_actuales():
    """Mostrar las credenciales actuales de usuarios de planta"""
    print("=== CREDENCIALES DE USUARIOS DE PLANTA ===\n")
    
    admin_plantas = AdminPlanta.objects.all()
    
    if admin_plantas.exists():
        for i, admin_planta in enumerate(admin_plantas, 1):
            usuario = admin_planta.usuario.user
            planta = admin_planta.planta
            
            print(f"{i}. Usuario: {usuario.username}")
            print(f"   Planta: {planta.nombre}")
            print(f"   Email: {usuario.email}")
            print(f"   Nombre: {usuario.first_name} {usuario.last_name}")
            print(f"   Nivel: {admin_planta.usuario.nivel_usuario}")
            print(f"   Password para pruebas: test123")
            print()
    else:
        print("No hay usuarios de planta registrados.")

if __name__ == "__main__":
    mostrar_credenciales_actuales()
    test_login_usuarios_planta()
