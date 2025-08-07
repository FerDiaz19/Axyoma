#!/usr/bin/env python3
"""
Script para listar todas las rutas disponibles en Django
"""
import os
import sys
import django

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

def listar_rutas():
    """Listar todas las rutas disponibles"""
    
    print("🔍 Rutas disponibles en el sistema:")
    print("="*50)
    
    resolver = get_resolver()
    
    def print_urls(urlpatterns, prefix=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                # Es un include
                new_prefix = prefix + str(pattern.pattern)
                print_urls(pattern.url_patterns, new_prefix)
            else:
                # Es una URL individual
                full_url = prefix + str(pattern.pattern)
                if hasattr(pattern, 'callback') and pattern.callback:
                    view_name = pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)
                    print(f"  {full_url:<50} -> {view_name}")
                else:
                    print(f"  {full_url}")
    
    print_urls(resolver.url_patterns, '/')
    
    print("\n🔍 Buscando rutas de evaluaciones específicamente:")
    print("="*50)
    
    # Buscar rutas que contengan 'evaluacion'
    def find_evaluation_urls(urlpatterns, prefix=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                new_prefix = prefix + str(pattern.pattern)
                find_evaluation_urls(pattern.url_patterns, new_prefix)
            else:
                full_url = prefix + str(pattern.pattern)
                if 'evaluacion' in full_url.lower() or 'oficial' in full_url.lower():
                    if hasattr(pattern, 'callback') and pattern.callback:
                        view_name = pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)
                        print(f"  ✅ {full_url:<50} -> {view_name}")
                    else:
                        print(f"  ✅ {full_url}")
    
    find_evaluation_urls(resolver.url_patterns, '/')

if __name__ == "__main__":
    listar_rutas()
