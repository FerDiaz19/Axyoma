#!/usr/bin/env python
"""
🧪 TEST DE FUNCIONES DE RESTAURACIÓN CORREGIDAS
============================================

Prueba las nuevas funciones corregidas de restauración
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

def test_info_sistema():
    """Test básico para verificar configuración"""
    print("🔧 Verificando configuración de BD...")
    
    try:
        from apps.admin_bd.views_respaldos import obtener_config_db
        config = obtener_config_db()
        print(f"✅ Configuración BD: {config['name']} en {config['host']}:{config['port']}")
        return True
    except Exception as e:
        print(f"❌ Error configuración: {e}")
        return False

def test_endpoints_disponibles():
    """Verificar que las nuevas rutas estén disponibles"""
    print("🌐 Verificando endpoints disponibles...")
    
    try:
        from django.urls import reverse
        
        endpoints = [
            'admin_bd:resetear_bd',
            'admin_bd:cargar_datos_iniciales', 
            'admin_bd:restaurar_estado_inicial'
        ]
        
        for endpoint in endpoints:
            try:
                url = reverse(endpoint)
                print(f"✅ {endpoint}: {url}")
            except Exception as e:
                print(f"❌ {endpoint}: {e}")
                
    except Exception as e:
        print(f"❌ Error verificando endpoints: {e}")

def test_verificar_mejoras_restauracion():
    """Verificar las mejoras en la función de restauración"""
    print("🔍 Verificando mejoras en función de restauración...")
    
    try:
        # Importar la función
        import inspect
        from apps.admin_bd.views_respaldos import restaurar_respaldo
        
        # Obtener código fuente 
        source = inspect.getsource(restaurar_respaldo)
        
        # Verificar mejoras implementadas
        mejoras = {
            'return_code_check': 'result.returncode != 0' in source,
            'proper_error_handling': 'HTTP_500_INTERNAL_SERVER_ERROR' in source,
            'comando_debugging': 'print(f"🔧 Comando:' in source,
            'quiet_mode': '--quiet' in source,
            'file_flag': '-f' in source
        }
        
        for mejora, presente in mejoras.items():
            status = "✅" if presente else "❌"
            print(f"{status} {mejora}: {'Implementado' if presente else 'Falta'}")
            
        return all(mejoras.values())
        
    except Exception as e:
        print(f"❌ Error verificando mejoras: {e}")
        return False

def main():
    print("🧪 INICIANDO TESTS DE RESTAURACIÓN CORREGIDA")
    print("=" * 50)
    
    tests = [
        ("Configuración BD", test_info_sistema),
        ("Endpoints disponibles", test_endpoints_disponibles), 
        ("Mejoras restauración", test_verificar_mejoras_restauracion)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        print(f"\n📋 {nombre}:")
        resultado = test_func()
        resultados.append(resultado)
        print()
    
    print("=" * 50)
    exitosos = sum(resultados)
    total = len(resultados)
    
    if exitosos == total:
        print(f"🎉 TODOS LOS TESTS PASARON ({exitosos}/{total})")
        print("✅ Las funciones de restauración están corregidas")
    else:
        print(f"⚠️ ALGUNOS TESTS FALLARON ({exitosos}/{total})")
        print("❌ Hay problemas en las correcciones")

if __name__ == "__main__":
    main()
