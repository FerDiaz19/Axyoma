#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el sistema completo de respaldos y restauración
Prueba todas las funcionalidades paso a paso
"""
import requests
import json
import time

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"

def obtener_token():
    """Obtener token de autenticación"""
    print("🔑 Obteniendo token de autenticación...")
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'username': 'admin', 
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        token = response.json()['token']
        print(f"✅ Token obtenido: {token[:20]}...")
        return token
    else:
        print(f"❌ Error al obtener token: {response.status_code}")
        print(response.text)
        return None

def test_info_sistema(headers):
    """Probar información del sistema de respaldos"""
    print("\n📊 Probando información del sistema...")
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/info/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Información del sistema obtenida:")
        print(f"   📁 Directorio: {data['directorio_respaldos']}")
        print(f"   🗄️ Base de datos: {data['base_datos']}")
        print(f"   🏠 Host: {data['host']}:{data['puerto']}")
        print(f"   📦 Respaldos existentes: {data['cantidad_respaldos']}")
        print(f"   💾 Espacio usado: {data['espacio_usado_mb']} MB")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_listar_respaldos(headers):
    """Probar listado de respaldos"""
    print("\n📋 Probando listado de respaldos...")
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/listar/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respaldos encontrados: {data['total']}")
        if data['respaldos']:
            for backup in data['respaldos'][:3]:  # Mostrar solo los primeros 3
                print(f"   📄 {backup['archivo']} ({backup.get('tamaño_mb', 0)} MB)")
                print(f"      Tipo: {backup['tipo']} | Fecha: {backup['fecha_creacion'][:19]}")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_respaldo_tablas(headers):
    """Probar respaldo de tablas específicas"""
    print("\n💾 Probando respaldo de tablas específicas...")
    
    payload = {
        "tablas": ["usuarios", "empresas"],
        "incluir_datos": True,
        "descripcion": "Respaldo de prueba - usuarios y empresas"
    }
    
    response = requests.post(f'{BASE_URL}/admin-bd/respaldos/tablas/', 
                           headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Respaldo de tablas creado exitosamente:")
        print(f"   📄 Archivo: {data['archivo']}")
        print(f"   📊 Tablas: {', '.join(data['tablas'])}")
        print(f"   💾 Tamaño: {data['tamaño_mb']} MB")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_respaldo_bd_completa(headers):
    """Probar respaldo de BD completa"""
    print("\n🗄️ Probando respaldo de BD completa...")
    
    payload = {
        "incluir_datos": True,
        "descripcion": "Respaldo completo de prueba"
    }
    
    response = requests.post(f'{BASE_URL}/admin-bd/respaldos/bd-completa/', 
                           headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Respaldo completo creado exitosamente:")
        print(f"   📄 Archivo: {data['archivo']}")
        print(f"   💾 Tamaño: {data['tamaño_mb']} MB")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🚀 PRUEBA DEL SISTEMA DE RESPALDOS Y RESTAURACIÓN")
    print("=" * 60)
    
    # Obtener token
    token = obtener_token()
    if not token:
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Probar todas las funcionalidades
    info_sistema = test_info_sistema(headers)
    respaldos_existentes = test_listar_respaldos(headers)
    
    # Crear respaldos de prueba
    respaldo_tablas = test_respaldo_tablas(headers)
    time.sleep(2)  # Esperar un poco entre respaldos
    respaldo_completo = test_respaldo_bd_completa(headers)
    
    # Listar respaldos después de crear nuevos
    print("\n📋 Listando respaldos después de crear nuevos...")
    respaldos_nuevos = test_listar_respaldos(headers)
    
    print("\n" + "=" * 60)
    print("✅ Prueba del sistema de respaldos completada!")
    print("\n📝 RESUMEN:")
    if info_sistema:
        print(f"   🗄️ Base de datos: {info_sistema['base_datos']}")
        print(f"   📁 Directorio: {info_sistema['directorio_respaldos']}")
    if respaldos_nuevos:
        print(f"   📦 Total de respaldos: {respaldos_nuevos['total']}")
    if respaldo_tablas:
        print(f"   ✅ Respaldo de tablas: {respaldo_tablas['archivo']}")
    if respaldo_completo:
        print(f"   ✅ Respaldo completo: {respaldo_completo['archivo']}")

if __name__ == "__main__":
    main()
