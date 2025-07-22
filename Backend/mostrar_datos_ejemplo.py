#!/usr/bin/env python
"""
Script para mostrar datos de ejemplo de los endpoints
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

def mostrar_datos_ejemplo():
    """Mostrar datos de ejemplo de los endpoints principales"""
    
    print("📊 MOSTRANDO DATOS DE EJEMPLO...")
    
    # Obtener token de superadmin
    try:
        superadmin = User.objects.filter(is_superuser=True).first()
        token, created = Token.objects.get_or_create(user=superadmin)
        headers = {'Authorization': f'Token {token.key}'}
        base_url = 'http://localhost:8000/api/superadmin'
        
    except Exception as e:
        print(f"❌ Error obteniendo token: {str(e)}")
        return
    
    # 1. ESTADÍSTICAS DEL SISTEMA
    print("\n" + "="*60)
    print("📈 ESTADÍSTICAS DEL SISTEMA")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/estadisticas_sistema/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            totales = data.get('totales', {})
            print(f"👥 Usuarios: {totales.get('usuarios', 0)}")
            print(f"🏢 Empresas: {totales.get('empresas', 0)}")
            print(f"🏭 Plantas: {totales.get('plantas', 0)}")
            print(f"🏬 Departamentos: {totales.get('departamentos', 0)}")
            print(f"💼 Puestos: {totales.get('puestos', 0)}")
            print(f"👤 Empleados: {totales.get('empleados', 0)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 2. PLANTAS
    print("\n" + "="*60)
    print("🏭 PLANTAS REGISTRADAS")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/listar_todas_plantas/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            plantas = data.get('plantas', [])
            print(f"Total de plantas: {len(plantas)}")
            
            for i, planta in enumerate(plantas[:5], 1):  # Mostrar primeras 5
                print(f"{i}. {planta.get('nombre', 'Sin nombre')}")
                print(f"   Empresa: {planta.get('empresa_nombre', 'Sin empresa')}")
                print(f"   ID: {planta.get('planta_id', 'N/A')}")
                print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 3. DEPARTAMENTOS
    print("\n" + "="*60)
    print("🏬 DEPARTAMENTOS REGISTRADOS")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/listar_todos_departamentos/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            departamentos = data.get('departamentos', [])
            print(f"Total de departamentos: {len(departamentos)}")
            
            for i, dept in enumerate(departamentos[:8], 1):  # Mostrar primeros 8
                print(f"{i}. {dept.get('nombre', 'Sin nombre')}")
                print(f"   Planta: {dept.get('planta_nombre', 'Sin planta')}")
                print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 4. EMPLEADOS
    print("\n" + "="*60)
    print("👤 EMPLEADOS REGISTRADOS")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/listar_todos_empleados/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            empleados = data.get('empleados', [])
            print(f"Total de empleados: {len(empleados)}")
            
            for i, emp in enumerate(empleados[:10], 1):  # Mostrar primeros 10
                nombre_completo = emp.get('nombre_completo', f"{emp.get('nombre', '')} {emp.get('apellido_paterno', '')} {emp.get('apellido_materno', '')}").strip()
                print(f"{i}. {nombre_completo}")
                print(f"   Puesto: {emp.get('puesto_nombre', 'Sin puesto')}")
                print(f"   Departamento: {emp.get('departamento_nombre', 'Sin departamento')}")
                print(f"   Planta: {emp.get('planta_nombre', 'Sin planta')}")
                print(f"   Email: {emp.get('email', 'Sin email')}")
                # Telefono removido según solicitud
                print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 5. USUARIOS
    print("\n" + "="*60)
    print("👥 USUARIOS DEL SISTEMA")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/listar_usuarios/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            print(f"Total de usuarios: {len(usuarios)}")
            
            for i, user in enumerate(usuarios, 1):
                nombre_completo = user.get('nombre_completo', user.get('username', 'Sin nombre'))
                print(f"{i}. {nombre_completo}")
                print(f"   Username: {user.get('username', 'Sin username')}")
                print(f"   Nivel: {user.get('nivel_usuario', 'Sin nivel')}")
                print(f"   Email: {user.get('email', 'Sin email')}")
                print(f"   Activo: {'Sí' if user.get('is_active', False) else 'No'}")
                if user.get('empresa'):
                    print(f"   Empresa: {user['empresa']['nombre']}")
                if user.get('planta'):
                    print(f"   Planta: {user['planta']['nombre']}")
                print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    mostrar_datos_ejemplo()
