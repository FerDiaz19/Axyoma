#!/usr/bin/env python
"""
Script para verificar las rutas disponibles en el backend Django
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.urls import get_resolver, URLPattern, URLResolver

def imprimir_rutas(urlpatterns, prefix=""):
    """Imprime recursivamente todas las rutas definidas"""
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            imprimir_rutas(pattern.url_patterns, prefix=prefix + pattern.pattern.regex.pattern)
        elif isinstance(pattern, URLPattern):
            print(f"{prefix}{pattern.pattern.regex.pattern} -> {pattern.callback.__name__}")

def obtener_todas_rutas():
    """Obtiene todas las rutas definidas en el proyecto"""
    print("\n🔍 RUTAS DISPONIBLES EN LA API:")
    print("=" * 60)
    
    # Obtener el resolver de URLs
    resolver = get_resolver()
    
    # Imprimir rutas
    imprimir_rutas(resolver.url_patterns)
    
    print("\n🔍 RUTAS DE LA APLICACIÓN:")
    
    try:
        from config.urls import urlpatterns
        from apps.urls import urlpatterns as apps_urlpatterns
        
        print("\n📁 Rutas principales:")
        for pattern in urlpatterns:
            print(f" - {pattern}")
        
        print("\n📁 Rutas de apps:")
        for pattern in apps_urlpatterns:
            print(f" - {pattern}")
            
    except ImportError as e:
        print(f"❌ Error al importar módulos de URLs: {str(e)}")

def probar_rutas_superadmin():
    """Probar rutas específicas del SuperAdmin"""
    print("\n🔍 PROBANDO RUTAS DE SUPERADMIN:")
    print("=" * 60)
    
    import requests
    
    # URLs a probar
    urls = [
        "http://localhost:8000/api/superadmin/listar_empresas/",
        "http://localhost:8000/api/superadmin/listar_usuarios/",
        "http://localhost:8000/api/superadmin/estadisticas_sistema/",
        "http://localhost:8000/api/superadmin/listar_todas_plantas/",
        "http://localhost:8000/api/superadmin/listar_todos_departamentos/",
        "http://localhost:8000/api/superadmin/listar_todos_puestos/",
        "http://localhost:8000/api/superadmin/listar_todos_empleados/"
    ]
    
    # Intentar obtener un token
    from rest_framework.authtoken.models import Token
    from django.contrib.auth.models import User
    
    token = None
    try:
        superadmin = User.objects.get(username='superadmin')
        token, _ = Token.objects.get_or_create(user=superadmin)
        print(f"✅ Token obtenido: {token.key}")
    except User.DoesNotExist:
        print("❌ Usuario 'superadmin' no encontrado")
        return
    except Exception as e:
        print(f"❌ Error obteniendo token: {str(e)}")
        return
    
    # Probar cada URL
    headers = {"Authorization": f"Token {token.key}"}
    
    for url in urls:
        try:
            print(f"\nProbando {url}")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code}")
                # Mostrar primeros 500 caracteres de la respuesta
                print(f"📝 Respuesta: {response.text[:500]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 VERIFICADOR DE RUTAS DJANGO")
    print("=" * 60)
    
    obtener_todas_rutas()
    probar_rutas_superadmin()
    
    print("\n🏁 VERIFICACIÓN COMPLETADA")
