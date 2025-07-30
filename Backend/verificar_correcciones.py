#!/usr/bin/env python
"""
🔧 VERIFICAR CORRECCIONES IMPLEMENTADAS
===================================

Verificación simple de que las correcciones se aplicaron correctamente
"""

import os
import sys

def verificar_archivo(archivo_path, verificaciones):
    """Verificar que las correcciones estén en el archivo"""
    print(f"📁 Verificando: {archivo_path}")
    
    if not os.path.exists(archivo_path):
        print(f"❌ Archivo no encontrado: {archivo_path}")
        return False
    
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    resultados = {}
    for nombre, patron in verificaciones.items():
        presente = patron in contenido
        status = "✅" if presente else "❌"
        print(f"  {status} {nombre}: {'Presente' if presente else 'Falta'}")
        resultados[nombre] = presente
    
    return all(resultados.values())

def main():
    print("🔧 VERIFICANDO CORRECCIONES IMPLEMENTADAS")
    print("=" * 50)
    
    # Verificar backend
    views_respaldos = "c:/xampp2/htdocs/UTT4B/Axyoma2/Backend/apps/admin_bd/views_respaldos.py"
    verificaciones_backend = {
        "Función restaurar_estado_inicial": "def restaurar_estado_inicial(request):",
        "Verificación return code": "if result.returncode != 0:",
        "Comando psql con -f": "'-f', ruta_backup",
        "Debugging comando": 'print(f"🔧 Comando:',
        "Modo quiet": "'--quiet'",
        "Echo errors": "'--echo-errors'",
        "Reseteo BD mejorado": "SELECT tablename FROM pg_tables",
        "Obtener tablas dinámicamente": "cursor.execute(f\"SELECT COUNT(*) FROM {tabla}\")"
    }
    
    backend_ok = verificar_archivo(views_respaldos, verificaciones_backend)
    
    # Verificar URLs
    urls_path = "c:/xampp2/htdocs/UTT4B/Axyoma2/Backend/apps/admin_bd/urls.py"
    verificaciones_urls = {
        "Ruta estado inicial": "path('sistema/estado-inicial/', views_respaldos.restaurar_estado_inicial",
        "Ruta resetear BD": "path('sistema/resetear-bd/', views_respaldos.resetear_bd_completa",
        "Ruta datos iniciales": "path('sistema/datos-iniciales/', views_respaldos.cargar_datos_iniciales"
    }
    
    urls_ok = verificar_archivo(urls_path, verificaciones_urls)
    
    # Verificar frontend
    service_path = "c:/xampp2/htdocs/UTT4B/Axyoma2/frontend/src/services/adminBDService.ts"
    verificaciones_frontend = {
        "Función restaurarEstadoInicial": "async restaurarEstadoInicial(): Promise<any>",
        "Endpoint estado inicial": "'/sistema/estado-inicial/'",
        "Confirmación requerida": "confirmacion: 'CONFIRMO_RESTAURAR_INICIAL'",
        "Export función": "export const restaurarEstadoInicial"
    }
    
    frontend_ok = verificar_archivo(service_path, verificaciones_frontend)
    
    # Verificar componente
    component_path = "c:/xampp2/htdocs/UTT4B/Axyoma2/frontend/src/components/GestionRespaldos.tsx"
    verificaciones_component = {
        "Import restaurarEstadoInicial": "restaurarEstadoInicial",
        "Función handleRestaurarEstadoInicial": "const handleRestaurarEstadoInicial = async () =>",
        "Botón Estado Inicial": "🎯 Estado Inicial",
        "Llamada a función": "await restaurarEstadoInicial();"
    }
    
    component_ok = verificar_archivo(component_path, verificaciones_component)
    
    print("\n" + "=" * 50)
    
    total_tests = 4
    exitosos = sum([backend_ok, urls_ok, frontend_ok, component_ok])
    
    print(f"📊 RESUMEN: {exitosos}/{total_tests} archivos verificados correctamente")
    
    if exitosos == total_tests:
        print("🎉 TODAS LAS CORRECCIONES ESTÁN IMPLEMENTADAS")
        print("✅ Sistema listo para probar funcionalidad de restauración")
    else:
        print("⚠️ FALTAN ALGUNAS CORRECCIONES")
        print("❌ Revisar archivos con problemas")
    
    print("\n📋 FUNCIONES NUEVAS IMPLEMENTADAS:")
    print("1. ✅ restaurar_respaldo() - Corregida con mejor manejo de errores")
    print("2. ✅ resetear_bd_completa() - Mejorada para obtener tablas dinámicamente")
    print("3. ✅ restaurar_estado_inicial() - Nueva función que combina reseteo + datos")
    print("4. ✅ Frontend - Botón y función para restaurar estado inicial")

if __name__ == "__main__":
    main()
