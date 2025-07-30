#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración completa del sistema de respaldos
Muestra todas las funcionalidades implementadas
"""
import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"

def obtener_token():
    """Obtener token de autenticación"""
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'username': 'admin', 
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        return response.json()['token']
    return None

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*60)
    print("🛠️  SISTEMA DE RESPALDOS Y RESTAURACIÓN - AXYOMA")
    print("="*60)
    print("1. 📊 Ver información del sistema")
    print("2. 📋 Listar respaldos existentes")
    print("3. 💾 Crear respaldo de tablas específicas")
    print("4. 🗄️ Crear respaldo completo de BD")
    print("5. ⬇️ Descargar respaldo")
    print("6. 🔄 Restaurar respaldo")
    print("7. 🗑️ Eliminar respaldo")
    print("8. 🚪 Salir")
    print("="*60)

def info_sistema(headers):
    """Mostrar información del sistema"""
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/info/', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("\n📊 INFORMACIÓN DEL SISTEMA:")
        print(f"   🗄️ Base de datos: {data['base_datos']}")
        print(f"   🏠 Servidor: {data['host']}:{data['puerto']}")
        print(f"   📁 Directorio respaldos: {data['directorio_respaldos']}")
        print(f"   📦 Respaldos existentes: {data['cantidad_respaldos']}")
        print(f"   💾 Espacio usado: {data['espacio_usado_mb']} MB")
        print(f"   🔧 Herramientas: pg_dump ✅, psql ✅")

def listar_respaldos(headers):
    """Listar respaldos existentes"""
    response = requests.get(f'{BASE_URL}/admin-bd/respaldos/listar/', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"\n📋 RESPALDOS EXISTENTES ({data['total']}):")
        
        if not data['respaldos']:
            print("   📭 No hay respaldos disponibles")
            return []
        
        for i, backup in enumerate(data['respaldos'], 1):
            print(f"\n{i}. 📄 {backup['archivo']}")
            print(f"   📊 Tipo: {backup['tipo']}")
            print(f"   📅 Fecha: {backup['fecha_creacion'][:19]}")
            print(f"   💾 Tamaño: {backup.get('tamaño_mb', 0)} MB")
            print(f"   👤 Usuario: {backup.get('usuario', 'N/A')}")
            if backup.get('descripcion'):
                print(f"   📝 Descripción: {backup['descripcion']}")
            if backup['tipo'] == 'tablas' and 'tablas' in backup:
                print(f"   🏷️ Tablas: {', '.join(backup['tablas'])}")
        
        return data['respaldos']
    else:
        print(f"❌ Error: {response.status_code}")
        return []

def crear_respaldo_tablas(headers):
    """Crear respaldo de tablas específicas"""
    print("\n💾 CREAR RESPALDO DE TABLAS")
    print("Tablas disponibles: usuarios, empresas, empleados, plantas, departamentos, puestos")
    
    tablas_input = input("Ingrese las tablas separadas por comas: ").strip()
    if not tablas_input:
        print("❌ Debe especificar al menos una tabla")
        return
    
    tablas = [t.strip() for t in tablas_input.split(',')]
    incluir_datos = input("¿Incluir datos? (s/N): ").strip().lower() == 's'
    descripcion = input("Descripción (opcional): ").strip()
    
    payload = {
        "tablas": tablas,
        "incluir_datos": incluir_datos,
        "descripcion": descripcion
    }
    
    print("🔄 Creando respaldo...")
    response = requests.post(f'{BASE_URL}/admin-bd/respaldos/tablas/', 
                           headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Respaldo creado exitosamente:")
        print(f"   📄 Archivo: {data['archivo']}")
        print(f"   📊 Tablas: {', '.join(data['tablas'])}")
        print(f"   💾 Tamaño: {data['tamaño_mb']} MB")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def crear_respaldo_completo(headers):
    """Crear respaldo completo de BD"""
    print("\n🗄️ CREAR RESPALDO COMPLETO")
    
    incluir_datos = input("¿Incluir datos? (S/n): ").strip().lower() != 'n'
    descripcion = input("Descripción (opcional): ").strip()
    
    payload = {
        "incluir_datos": incluir_datos,
        "descripcion": descripcion
    }
    
    print("🔄 Creando respaldo completo...")
    response = requests.post(f'{BASE_URL}/admin-bd/respaldos/bd-completa/', 
                           headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Respaldo completo creado exitosamente:")
        print(f"   📄 Archivo: {data['archivo']}")
        print(f"   💾 Tamaño: {data['tamaño_mb']} MB")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def main():
    print("🚀 INICIANDO SISTEMA DE RESPALDOS...")
    
    token = obtener_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    while True:
        mostrar_menu()
        opcion = input("\n👉 Seleccione una opción: ").strip()
        
        if opcion == '1':
            info_sistema(headers)
        elif opcion == '2':
            listar_respaldos(headers)
        elif opcion == '3':
            crear_respaldo_tablas(headers)
        elif opcion == '4':
            crear_respaldo_completo(headers)
        elif opcion == '5':
            respaldos = listar_respaldos(headers)
            if respaldos:
                try:
                    idx = int(input("Número de respaldo a descargar: ")) - 1
                    archivo = respaldos[idx]['archivo']
                    print(f"⬇️ Para descargar: GET /admin-bd/respaldos/descargar/{archivo}/")
                except:
                    print("❌ Número inválido")
        elif opcion == '6':
            respaldos = listar_respaldos(headers)
            if respaldos:
                print("\n⚠️ ADVERTENCIA: La restauración puede sobrescribir datos existentes")
                confirmar = input("¿Desea continuar? (escriba 'CONFIRMAR'): ").strip()
                if confirmar == 'CONFIRMAR':
                    try:
                        idx = int(input("Número de respaldo a restaurar: ")) - 1
                        archivo = respaldos[idx]['archivo']
                        print(f"🔄 Para restaurar: POST /admin-bd/respaldos/restaurar/")
                        print(f"Body: {{'archivo': '{archivo}', 'confirmar': true, 'modo': 'replace'}}")
                    except:
                        print("❌ Número inválido")
                else:
                    print("❌ Restauración cancelada")
        elif opcion == '7':
            respaldos = listar_respaldos(headers)
            if respaldos:
                try:
                    idx = int(input("Número de respaldo a eliminar: ")) - 1
                    archivo = respaldos[idx]['archivo']
                    print(f"🗑️ Para eliminar: DELETE /admin-bd/respaldos/eliminar/{archivo}/")
                except:
                    print("❌ Número inválido")
        elif opcion == '8':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")
        
        input("\n⏸️ Presione Enter para continuar...")

if __name__ == "__main__":
    main()
