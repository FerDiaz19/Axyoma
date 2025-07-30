#!/usr/bin/env python
"""
📊 CARGAR DATOS SUPER SIMPLE
=================================
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

def main():
    print('📊 CREANDO DATOS SUPER SIMPLES...')
    
    from django.contrib.auth.models import User
    
    try:
        # Solo crear usuarios básicos
        user, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'super@axyoma.com',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('1234')
            user.save()
            print(f'✅ Usuario creado: {user.username}')
        else:
            print(f'🔄 Usuario ya existe: {user.username}')
            
        print('🎉 DATOS SIMPLES CREADOS')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    main()
