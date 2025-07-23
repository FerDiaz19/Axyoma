#!/usr/bin/env python
"""
Script para consultar la API de AXYOMA y mostrar los resultados
Ayuda a entender la estructura de datos que devuelve la API
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin
from pprint import pprint

# Configuración base
BASE_URL = "http://localhost:8000/"
TOKEN = None  # Se pedirá al usuario o se intentará obtener
HEADERS = {"Content-Type": "application/json"}

def mostrar_titulo(texto):
    """Muestra un título formateado"""
    print("\n" + "=" * 80)
    print(f" {texto} ".center(80, "="))
    print("=" * 80 + "\n")

def solicitar_token():
    """Solicitar token de autenticación al usuario"""
    global TOKEN, HEADERS
    print("Para consultar la API necesitas un token de autenticación.")
    print("Puedes:")
    print("1) Introducir un token existente")
    print("2) Iniciar sesión para obtener uno nuevo")
    
    opcion = input("\nSelecciona una opción (1/2): ")
    
    if opcion == "1":
        TOKEN = input("Introduce tu token: ")
        HEADERS["Authorization"] = f"Token {TOKEN}"
        return True
    elif opcion == "2":
        return iniciar_sesion()
    else:
        print("⚠️ Opción inválida.")
        return False

def iniciar_sesion():
    """Iniciar sesión para obtener token"""
    global TOKEN, HEADERS
    
    print("\n--- INICIAR SESIÓN ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    try:
        login_data = {"username": username, "password": password}
        url = urljoin(BASE_URL, "api/auth/login/")
        
        print(f"🔄 Iniciando sesión como {username}...")
        response = requests.post(url, json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                TOKEN = data["token"]
                HEADERS["Authorization"] = f"Token {TOKEN}"
                print(f"✅ Sesión iniciada como {data.get('usuario', username)}")
                print(f"🔑 Token: {TOKEN}")
                return True
            else:
                print("❌ La respuesta no contiene un token.")
                return False
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {str(e)}")
        return False

def consultar_api(endpoint, params=None):
    """Consulta un endpoint de la API y devuelve la respuesta"""
    url = urljoin(BASE_URL, endpoint)
    
    try:
        print(f"🔄 Consultando {url}...")
        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error al consultar API: {str(e)}")
        return None

def mostrar_resultados(data, formato="json"):
    """Muestra los resultados de la API"""
    if data is None:
        print("❌ No hay datos para mostrar.")
        return
        
    if formato == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        pprint(data)

def consultar_empresas():
    """Consulta el listado de empresas"""
    mostrar_titulo("EMPRESAS")
    data = consultar_api("api/superadmin/listar_empresas/")
    
    if data and "empresas" in data:
        print(f"📊 Total de empresas: {len(data['empresas'])}")
        
        for i, empresa in enumerate(data["empresas"], 1):
            print(f"\n--- Empresa {i}: {empresa.get('nombre', 'Sin nombre')} ---")
            print(f"ID: {empresa.get('empresa_id')}")
            print(f"RFC: {empresa.get('rfc', 'No disponible')}")
            print(f"Status: {'✅ Activa' if empresa.get('status') else '❌ Inactiva'}")
            
            if empresa.get("administrador"):
                admin = empresa["administrador"]
                print(f"Admin: {admin.get('nombre_completo', admin.get('username', 'N/A'))}")
            
            print(f"Plantas: {empresa.get('plantas_count', 0)}")
            print(f"Empleados: {empresa.get('empleados_count', 0)}")
    
    return data

def consultar_estadisticas():
    """Consulta las estadísticas del sistema"""
    mostrar_titulo("ESTADÍSTICAS DEL SISTEMA")
    data = consultar_api("api/superadmin/estadisticas_sistema/")
    
    if data:
        print(f"📊 EMPRESAS:")
        print(f"  Total: {data.get('total_empresas', 0)}")
        print(f"  Activas: {data.get('empresas_activas', 0)}")
        
        print(f"\n👤 USUARIOS:")
        print(f"  Total: {data.get('total_usuarios', 0)}")
        
        if "usuarios_por_nivel" in data:
            niveles = data["usuarios_por_nivel"]
            print(f"  SuperAdmin: {niveles.get('superadmin', 0)}")
            print(f"  Admin Empresa: {niveles.get('admin-empresa', 0)}")
            print(f"  Admin Planta: {niveles.get('admin-planta', 0)}")
            
        print(f"\n🏭 PLANTAS:")
        print(f"  Total: {data.get('total_plantas', 0)}")
        print(f"  Activas: {data.get('plantas_activas', 0)}")
        
        print(f"\n👥 EMPLEADOS:")
        print(f"  Total: {data.get('total_empleados', 0)}")
        print(f"  Activos: {data.get('empleados_activos', 0)}")
    
    return data

def consultar_usuarios():
    """Consulta el listado de usuarios"""
    mostrar_titulo("USUARIOS")
    data = consultar_api("api/superadmin/listar_usuarios/")
    
    if data and "usuarios" in data:
        print(f"📊 Total de usuarios: {len(data['usuarios'])}")
        
        for i, usuario in enumerate(data["usuarios"], 1):
            print(f"\n--- Usuario {i}: {usuario.get('username', 'Sin nombre')} ---")
            print(f"ID: {usuario.get('user_id')}")
            print(f"Email: {usuario.get('email', 'No disponible')}")
            print(f"Nombre: {usuario.get('nombre_completo', 'No disponible')}")
            print(f"Nivel: {usuario.get('nivel_usuario', 'No disponible')}")
            print(f"Status: {'✅ Activo' if usuario.get('is_active') else '❌ Inactivo'}")
            
if usuario.get("empresa"):
    empresa = usuario["empresa"]
    nombre_empresa = empresa.get("nombre")
    if nombre_empresa:
        print(f"Empresa: {nombre_empresa}")
    else:
        print(f"Empresa: ID: {empresa.get('id', 'N/A')}")

if usuario.get("planta"):
    planta = usuario["planta"]
    nombre_planta = planta.get("nombre")
    if nombre_planta:
        print(f"Planta: {nombre_planta}")
    else:
        print(f"Planta: ID: {planta.get('id', 'N/A')}")
    return data

def consultar_plantas():
    """Consulta el listado de plantas"""
    mostrar_titulo("PLANTAS")
    data = consultar_api("api/superadmin/listar_todas_plantas/")
    
    if data and "plantas" in data:
        print(f"📊 Total de plantas: {len(data['plantas'])}")
        
        for i, planta in enumerate(data["plantas"], 1):
            print(f"\n--- Planta {i}: {planta.get('nombre', 'Sin nombre')} ---")
            print(f"ID: {planta.get('planta_id')}")
            print(f"Dirección: {planta.get('direccion', 'No disponible')}")
            print(f"Status: {'✅ Activa' if planta.get('status') else '❌ Inactiva'}")
            
            if planta.get("empresa"):
                empresa = planta["empresa"]
                print(f"Empresa: {empresa.get('nombre', f'ID: {empresa.get(\"id\", \"N/A\")}')}")
            
            print(f"Departamentos: {planta.get('departamentos_count', 0)}")
            print(f"Empleados: {planta.get('empleados_count', 0)}")
    
    return data

def consultar_planes():
    """Consulta los planes de suscripción"""
    mostrar_titulo("PLANES DE SUSCRIPCIÓN")
    data = consultar_api("api/suscripciones/listar_planes/")
    
    if data:
        print(f"📊 Total de planes: {len(data)}")
        
        for i, plan in enumerate(data, 1):
            print(f"\n--- Plan {i}: {plan.get('nombre', 'Sin nombre')} ---")
            print(f"ID: {plan.get('plan_id')}")
            print(f"Descripción: {plan.get('descripcion', 'No disponible')}")
            print(f"Precio: ${plan.get('precio', '0')}")
            print(f"Duración: {plan.get('duracion', '0')} días")
            print(f"Status: {'✅ Activo' if plan.get('status') else '❌ Inactivo'}")
    
    return data

def consultar_suscripciones():
    """Consulta las suscripciones"""
    mostrar_titulo("SUSCRIPCIONES")
    data = consultar_api("api/suscripciones/listar_suscripciones/")
    
    if data:
        print(f"📊 Total de suscripciones: {len(data)}")
        
        for i, suscripcion in enumerate(data, 1):
            print(f"\n--- Suscripción {i} ---")
            print(f"ID: {suscripcion.get('suscripcion_id')}")
            print(f"Empresa: {suscripcion.get('empresa__nombre', f'ID: {suscripcion.get(\"empresa__empresa_id\", \"N/A\")}')}")
            print(f"Plan: {suscripcion.get('plan_suscripcion__nombre', 'No disponible')}")
            print(f"Precio: ${suscripcion.get('plan_suscripcion__precio', '0')}")
            print(f"Fecha Inicio: {suscripcion.get('fecha_inicio', 'No disponible')}")
            print(f"Fecha Fin: {suscripcion.get('fecha_fin', 'No disponible')}")
            print(f"Estado: {suscripcion.get('estado', 'No disponible')}")
    
    return data

def menu_principal():
    """Muestra el menú principal y maneja las opciones"""
    while True:
        mostrar_titulo("INSPECTOR DE API AXYOMA")
        print("1. Ver Empresas")
        print("2. Ver Estadísticas del Sistema")
        print("3. Ver Usuarios")
        print("4. Ver Plantas")
        print("5. Ver Departamentos")
        print("6. Ver Puestos")
        print("7. Ver Empleados")
        print("8. Ver Planes de Suscripción")
        print("9. Ver Suscripciones")
        print("10. Consulta Personalizada")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            consultar_empresas()
        elif opcion == "2":
            consultar_estadisticas()
        elif opcion == "3":
            consultar_usuarios()
        elif opcion == "4":
            consultar_plantas()
        elif opcion == "5":
            data = consultar_api("api/superadmin/listar_todos_departamentos/")
            mostrar_resultados(data)
        elif opcion == "6":
            data = consultar_api("api/superadmin/listar_todos_puestos/")
            mostrar_resultados(data)
        elif opcion == "7":
            data = consultar_api("api/superadmin/listar_todos_empleados/")
            mostrar_resultados(data)
        elif opcion == "8":
            consultar_planes()
        elif opcion == "9":
            consultar_suscripciones()
        elif opcion == "10":
            consulta_personalizada()
        elif opcion == "0":
            print("\n¡Hasta luego! 👋")
            break
        else:
            print("\n⚠️ Opción inválida. Intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

def consulta_personalizada():
    """Permite realizar una consulta personalizada a la API"""
    mostrar_titulo("CONSULTA PERSONALIZADA")
    
    print("Ejemplos de endpoints:")
    print("- api/superadmin/estadisticas_sistema/")
    print("- api/superadmin/listar_empresas/")
    print("- api/superadmin/listar_usuarios/")
    print("- api/suscripciones/listar_planes/")
    print("- api/auth/login/ (POST)")
    
    endpoint = input("\nIntroduce el endpoint a consultar (sin la base URL): ")
    
    if not endpoint:
        print("⚠️ Endpoint vacío. Operación cancelada.")
        return
    
    params_str = input("Parámetros (formato: key1=value1&key2=value2) [opcional]: ")
    params = {}
    
    if params_str:
        for param in params_str.split("&"):
            if "=" in param:
                k, v = param.split("=", 1)
                params[k.strip()] = v.strip()
    
    data = consultar_api(endpoint, params)
    if data:
        mostrar_resultados(data)

def main():
    """Función principal"""
    mostrar_titulo("CONSULTOR DE API AXYOMA")
    print("Esta herramienta te permite explorar los datos de la API de AXYOMA.")
    print("Te ayudará a entender la estructura de datos y qué información está disponible.")
    
    # Solicitar token de autenticación
    if not solicitar_token():
        print("\n❌ No se pudo obtener un token válido. No es posible continuar.")
        return
    
    # Mostrar menú principal
    menu_principal()

if __name__ == "__main__":
    main()
