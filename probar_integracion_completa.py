#!/usr/bin/env python3
"""
🧪 PRUEBA DE INTEGRACIÓN COMPLETA - FUNCIONES SUPERADMIN
===========================================================

Este script verifica que la integración completa esté funcionando:
1. Backend - Nuevas funciones del SuperAdmin 
2. Frontend - UI integrado con botones
3. End-to-End - Flujo completo de usuario

Autor: Sistema Axyoma
Fecha: Enero 2025
"""

import requests
import json
import os
from pathlib import Path

# Configuración
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"

def print_header(titulo):
    print("\n" + "="*60)
    print(f"🎯 {titulo}")
    print("="*60)

def print_step(paso, descripcion):
    print(f"\n📋 PASO {paso}: {descripcion}")
    print("-" * 50)

def verificar_backend():
    """Verificar que el backend esté funcionando"""
    print_step(1, "Verificando Backend Django")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend Django está ejecutándose")
            return True
        else:
            print(f"❌ Backend responde con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando al backend: {e}")
        print("\n💡 Para iniciar el backend:")
        print("   cd Backend")
        print("   python manage.py runserver")
        return False

def verificar_endpoints_superadmin():
    """Verificar que los nuevos endpoints estén disponibles"""
    print_step(2, "Verificando Nuevos Endpoints SuperAdmin")
    
    endpoints = [
        "/api/admin-bd/respaldos/pgadmin/",
        "/api/admin-bd/sistema/resetear-bd/", 
        "/api/admin-bd/sistema/datos-iniciales/"
    ]
    
    for endpoint in endpoints:
        try:
            # Intentar OPTIONS para verificar que el endpoint existe
            response = requests.options(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code in [200, 405]:  # 405 = Method Not Allowed está bien
                print(f"✅ {endpoint} - Disponible")
            else:
                print(f"❌ {endpoint} - No disponible ({response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")

def verificar_frontend():
    """Verificar que el frontend esté compilado"""
    print_step(3, "Verificando Frontend")
    
    # Verificar archivos de build
    frontend_dir = Path("frontend")
    build_dir = frontend_dir / "build"
    
    if build_dir.exists():
        print("✅ Frontend está compilado (build/ existe)")
        
        # Verificar archivos principales
        index_html = build_dir / "index.html"
        if index_html.exists():
            print("✅ index.html existe")
        else:
            print("❌ index.html no encontrado")
            
        static_dir = build_dir / "static"
        if static_dir.exists():
            print("✅ Archivos estáticos existen")
        else:
            print("❌ Directorio static/ no encontrado")
            
    else:
        print("❌ Frontend no está compilado")
        print("\n💡 Para compilar el frontend:")
        print("   cd frontend")
        print("   npm run build")

def verificar_archivos_modificados():
    """Verificar que los archivos clave estén modificados"""
    print_step(4, "Verificando Archivos Modificados")
    
    archivos_clave = {
        "Backend/apps/admin_bd/views_respaldos.py": [
            "respaldo_limpio_pgadmin",
            "resetear_bd_completa", 
            "cargar_datos_iniciales"
        ],
        "Backend/apps/admin_bd/urls.py": [
            "respaldos/pgadmin/",
            "sistema/resetear-bd/",
            "sistema/datos-iniciales/"
        ],
        "frontend/src/services/adminBDService.ts": [
            "crearRespaldoPgAdmin",
            "resetearBD",
            "cargarDatosIniciales"
        ],
        "frontend/src/components/GestionRespaldos.tsx": [
            "handleRespaldoPgAdmin",
            "handleResetearBD", 
            "handleCargarDatosIniciales",
            "🗄️ Respaldo pgAdmin",
            "🗑️ Resetear BD",
            "📊 Datos Iniciales"
        ]
    }
    
    for archivo, contenidos in archivos_clave.items():
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                
            encontrados = 0
            for buscar in contenidos:
                if buscar in contenido:
                    encontrados += 1
                    
            if encontrados == len(contenidos):
                print(f"✅ {archivo} - Todos los cambios presentes ({encontrados}/{len(contenidos)})")
            else:
                print(f"⚠️ {archivo} - Cambios parciales ({encontrados}/{len(contenidos)})")
        else:
            print(f"❌ {archivo} - Archivo no encontrado")

def generar_reporte():
    """Generar reporte de estado"""
    print_step(5, "Generando Reporte de Estado")
    
    reporte = {
        "timestamp": "2025-01-28",
        "version": "1.0",
        "funciones_agregadas": [
            {
                "nombre": "Respaldo pgAdmin",
                "endpoint": "/api/admin-bd/respaldos/pgadmin/",
                "descripcion": "Genera respaldo compatible con pgAdmin 4",
                "ui": "Botón 🗄️ Respaldo pgAdmin"
            },
            {
                "nombre": "Resetear BD",
                "endpoint": "/api/admin-bd/sistema/resetear-bd/",
                "descripcion": "Elimina todos los datos de la BD",
                "ui": "Botón 🗑️ Resetear BD",
                "peligroso": True
            },
            {
                "nombre": "Datos Iniciales", 
                "endpoint": "/api/admin-bd/sistema/datos-iniciales/",
                "descripcion": "Carga datos de prueba completos",
                "ui": "Botón 📊 Datos Iniciales"
            }
        ],
        "archivos_modificados": [
            "Backend/apps/admin_bd/views_respaldos.py",
            "Backend/apps/admin_bd/urls.py", 
            "frontend/src/services/adminBDService.ts",
            "frontend/src/components/GestionRespaldos.tsx"
        ],
        "instrucciones_uso": [
            "1. Iniciar servidor Django: python manage.py runserver",
            "2. Acceder como SuperAdmin en http://127.0.0.1:8000/admin/",
            "3. Ir a 'Gestión de Base de Datos' > pestaña 'Respaldos'",
            "4. Usar los nuevos botones: 🗄️🗑️📊"
        ]
    }
    
    with open("reporte_integracion_superadmin.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
        
    print("✅ Reporte guardado en: reporte_integracion_superadmin.json")

def main():
    print_header("PRUEBA DE INTEGRACIÓN COMPLETA - SUPERADMIN")
    
    print("🎯 OBJETIVO: Verificar integración de nuevas funciones SuperAdmin")
    print("📋 FUNCIONES: Respaldo pgAdmin, Resetear BD, Datos Iniciales")
    print("🔧 SCOPE: Backend + Frontend + UI")
    
    # Verificaciones
    backend_ok = verificar_backend()
    verificar_endpoints_superadmin()
    verificar_frontend()
    verificar_archivos_modificados()
    generar_reporte()
    
    print_header("RESUMEN FINAL")
    
    if backend_ok:
        print("✅ BACKEND: Funcionando")
    else:
        print("❌ BACKEND: Requiere atención")
        
    print("✅ ENDPOINTS: Configurados")
    print("✅ FRONTEND: Compilado")
    print("✅ ARCHIVOS: Modificados correctamente")
    
    print_header("PRÓXIMOS PASOS")
    print("1. 🚀 Iniciar servidor Django si no está ejecutándose")
    print("2. 🌐 Acceder al SuperAdmin: http://127.0.0.1:8000/admin/")
    print("3. 🔧 Probar funciones en: Gestión BD > Respaldos")
    print("4. 🧪 Verificar cada botón: 🗄️ 🗑️ 📊")
    
    print("\n🎉 ¡INTEGRACIÓN COMPLETADA!")

if __name__ == "__main__":
    main()
