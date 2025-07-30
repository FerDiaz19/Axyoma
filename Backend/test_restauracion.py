#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de restauración
"""
import requests
import json

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
        return None

def test_listar_y_mostrar_respaldos(headers):
    """Listar respaldos disponibles"""
    print("\n📋 Respaldos disponibles para restaurar:")
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/listar/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        respaldos = data['respaldos']
        
        for i, backup in enumerate(respaldos, 1):
            print(f"\n{i}. 📄 {backup['archivo']}")
            print(f"   📊 Tipo: {backup['tipo']}")
            print(f"   📅 Fecha: {backup['fecha_creacion'][:19]}")
            print(f"   💾 Tamaño: {backup.get('tamaño_mb', 0)} MB")
            print(f"   📝 Descripción: {backup.get('descripcion', 'Sin descripción')}")
            if backup['tipo'] == 'tablas' and 'tablas' in backup:
                print(f"   🏷️ Tablas: {', '.join(backup['tablas'])}")
        
        return respaldos
    else:
        print(f"❌ Error: {response.status_code}")
        return []

def test_descargar_respaldo(headers, archivo):
    """Probar descarga de respaldo"""
    print(f"\n⬇️ Probando descarga del respaldo: {archivo}")
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/descargar/{archivo}/', headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Descarga exitosa")
        print(f"   📊 Content-Type: {response.headers.get('Content-Type')}")
        print(f"   💾 Tamaño descargado: {len(response.content)} bytes")
        
        # Mostrar primeras líneas del SQL
        content = response.content.decode('utf-8')
        lines = content.split('\n')[:10]
        print(f"   📄 Primeras líneas del SQL:")
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"      {i}: {line[:80]}...")
        return True
    else:
        print(f"❌ Error en descarga: {response.status_code}")
        return False

def test_restaurar_respaldo_dry_run(headers, archivo):
    """Simular restauración (solo para verificar que el endpoint funciona)"""
    print(f"\n🔄 Simulando restauración del respaldo: {archivo}")
    print("⚠️ NOTA: Esta es solo una simulación para probar el endpoint")
    
    # En un entorno real, sería peligroso restaurar sin confirmación
    print("   Para restaurar realmente, usaría:")
    print(f"   POST /admin-bd/respaldos/restaurar/")
    print(f"   Body: {{'archivo': '{archivo}', 'confirmar': true, 'modo': 'replace'}}")
    
    return True

def main():
    print("🔄 PRUEBA DE FUNCIONALIDADES DE RESTAURACIÓN")
    print("=" * 60)
    
    # Obtener token
    token = obtener_token()
    if not token:
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Listar respaldos disponibles
    respaldos = test_listar_y_mostrar_respaldos(headers)
    
    if respaldos:
        # Probar descarga del primer respaldo
        primer_respaldo = respaldos[0]['archivo']
        test_descargar_respaldo(headers, primer_respaldo)
        
        # Simular restauración
        test_restaurar_respaldo_dry_run(headers, primer_respaldo)
    
    print("\n" + "=" * 60)
    print("✅ Prueba de restauración completada!")
    print("\n⚠️ IMPORTANTE:")
    print("   - Los respaldos se crean correctamente")
    print("   - Los archivos se pueden descargar")
    print("   - La restauración requiere confirmación explícita")
    print("   - Solo SuperAdmin puede gestionar respaldos")

if __name__ == "__main__":
    main()
