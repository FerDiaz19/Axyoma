#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

def mostrar_credenciales():
    print('=== CREDENCIALES DE ACCESO ===')
    
    # Obtener todos los usuarios activos
    users = User.objects.filter(is_active=True)
    
    for user in users:
        print(f'\n👤 Usuario: {user.username}')
        print(f'   Email: {user.email}')
        print(f'   Activo: {"✅" if user.is_active else "❌"}')
        print(f'   Superuser: {"✅" if user.is_superuser else "❌"}')
        
        if hasattr(user, 'perfil'):
            perfil = user.perfil
            print(f'   Perfil: {perfil.nombre}')
            print(f'   Nivel: {perfil.nivel_usuario}')
            
            try:
                print(f'   Empresa: {perfil.empresa.nombre}')
            except:
                print('   Empresa: Sin empresa')
        else:
            print('   ❌ Sin perfil')
        
        # Mostrar password hint para usuarios comunes
        if user.username in ['admin_empresa', 'demo_admin', 'superadmin']:
            print(f'   🔑 Password probable: {"admin123" if "admin" in user.username else "demo123"}')
    
    print('\n=== RECOMENDACIONES ===')
    print('🎯 Para admin empresa: usuario "admin_empresa" con password "admin123"')
    print('🎯 Para superadmin: usuario "superadmin" con password "admin123"')
    print('🎯 Para pruebas: usuario "demo_admin" con password "demo123"')

if __name__ == '__main__':
    mostrar_credenciales()
