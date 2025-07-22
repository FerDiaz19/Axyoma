#!/usr/bin/env python
"""
Script para probar todos los endpoints CRUD del SuperAdmin
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

def probar_crud_superadmin():
    """Probar todos los endpoints CRUD del SuperAdmin"""
    
    print("🧪 PROBANDO ENDPOINTS CRUD SUPERADMIN...")
    
    # Obtener token de superadmin
    try:
        superadmin = User.objects.filter(is_superuser=True).first()
        token, created = Token.objects.get_or_create(user=superadmin)
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        base_url = 'http://localhost:8000/api/superadmin'
        
        print(f"🔑 Usando token: {token.key}")
        
    except Exception as e:
        print(f"❌ Error obteniendo token: {str(e)}")
        return
    
    # Lista de endpoints CRUD a probar
    crud_endpoints = {
        'EMPRESAS': {
            'editar': 'editar_empresa',
            'eliminar': 'eliminar_empresa',
            'suspender': 'suspender_empresa'
        },
        'PLANTAS': {
            'editar': 'editar_planta',
            'eliminar': 'eliminar_planta',
            'suspender': 'suspender_planta'
        },
        'DEPARTAMENTOS': {
            'editar': 'editar_departamento', 
            'eliminar': 'eliminar_departamento',
            'suspender': 'suspender_departamento'
        },
        'PUESTOS': {
            'editar': 'editar_puesto',
            'eliminar': 'eliminar_puesto',
            'suspender': 'suspender_puesto'
        },
        'EMPLEADOS': {
            'editar': 'editar_empleado',
            'eliminar': 'eliminar_empleado',
            'suspender': 'suspender_empleado'
        },
        'USUARIOS': {
            'editar': 'editar_usuario',
            'eliminar': 'eliminar_usuario', 
            'suspender': 'suspender_usuario'
        }
    }
    
    resultados = {}
    
    for seccion, endpoints in crud_endpoints.items():
        print(f"\n{'='*50}")
        print(f"🔍 PROBANDO SECCIÓN: {seccion}")
        print(f"{'='*50}")
        
        resultados[seccion] = {}
        
        for operacion, endpoint in endpoints.items():
            try:
                url = f"{base_url}/{endpoint}/"
                print(f"\n📋 {operacion.upper()}: {endpoint}")
                print(f"   URL: {url}")
                
                # Hacer una request OPTIONS para verificar si el endpoint existe
                response = requests.options(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ Endpoint existe y acepta solicitudes")
                    resultados[seccion][operacion] = 'DISPONIBLE'
                elif response.status_code == 405:
                    # Method not allowed - el endpoint existe pero no acepta OPTIONS
                    print(f"   ✅ Endpoint existe (405 en OPTIONS es normal)")
                    resultados[seccion][operacion] = 'DISPONIBLE'
                elif response.status_code == 404:
                    print(f"   ❌ Endpoint NO EXISTE (404)")
                    resultados[seccion][operacion] = 'NO_EXISTE'
                else:
                    print(f"   ⚠️ Respuesta inesperada: {response.status_code}")
                    resultados[seccion][operacion] = f'STATUS_{response.status_code}'
                
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Error de conexión: {str(e)}")
                resultados[seccion][operacion] = 'ERROR_CONEXION'
            except Exception as e:
                print(f"   ❌ Error inesperado: {str(e)}")
                resultados[seccion][operacion] = 'ERROR'
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE ENDPOINTS CRUD")
    print(f"{'='*60}")
    
    total_endpoints = 0
    disponibles = 0
    no_existen = 0
    
    for seccion, endpoints in resultados.items():
        print(f"\n🏷️ {seccion}:")
        for operacion, estado in endpoints.items():
            icono = "✅" if estado == 'DISPONIBLE' else "❌" if estado == 'NO_EXISTE' else "⚠️"
            print(f"   {icono} {operacion}: {estado}")
            
            total_endpoints += 1
            if estado == 'DISPONIBLE':
                disponibles += 1
            elif estado == 'NO_EXISTE':
                no_existen += 1
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"✅ Disponibles: {disponibles}/{total_endpoints}")
    print(f"❌ No existen: {no_existen}/{total_endpoints}")
    print(f"⚠️ Otros: {total_endpoints - disponibles - no_existen}/{total_endpoints}")
    
    if disponibles == total_endpoints:
        print("🎉 ¡TODOS LOS ENDPOINTS CRUD ESTÁN DISPONIBLES!")
    elif disponibles > total_endpoints * 0.8:
        print("✅ La mayoría de endpoints están disponibles")
    else:
        print("🚨 Muchos endpoints faltan por implementar")
        
    return resultados

if __name__ == "__main__":
    probar_crud_superadmin()
