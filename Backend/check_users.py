#!/usr/bin/env python
"""
Script to verify users and create test users if needed
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import Empresa, PerfilUsuario

def check_users():
    """Check existing users and create test user if needed"""
    print("👥 Checking Users in System")
    print("=" * 40)
    
    # Check total users
    total_users = User.objects.count()
    print(f"📊 Total users: {total_users}")
    
    # Check admin users
    admin_users = User.objects.filter(is_superuser=True)
    print(f"🔑 Superusers: {admin_users.count()}")
    for user in admin_users:
        print(f"   - {user.username} ({user.email})")
    
    # Check regular users
    regular_users = User.objects.filter(is_superuser=False)
    print(f"👤 Regular users: {regular_users.count()}")
    for user in regular_users[:5]:  # Show first 5
        profile = getattr(user, 'perfil', None)
        print(f"   - {user.username} ({user.email}) - Nivel: {profile.nivel_usuario if profile else 'N/A'}")
    
    # Check companies
    empresas = Empresa.objects.all()
    print(f"\n🏢 Empresas: {empresas.count()}")
    for empresa in empresas:
        print(f"   - {empresa.nombre}")
    
    # Create test user if no admin exists
    if not admin_users.exists():
        print("\n🚀 Creating test superuser...")
        user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        print(f"✅ Created superuser: {user.username}")
    
    # Create test empresa admin if no regular users exist
    if not regular_users.exists():
        print("\n🚀 Creating test empresa admin...")
        
        # Create empresa if doesn't exist
        empresa, created = Empresa.objects.get_or_create(
            nombre='Empresa Test',
            defaults={
                'direccion': 'Test Address',
                'telefono': '1234567890',
                'email': 'test@empresa.com'
            }
        )
        if created:
            print(f"✅ Created empresa: {empresa.nombre}")
        
        # Create user
        user = User.objects.create_user(
            username='empresa_admin',
            email='empresa@test.com',
            password='admin123'
        )
        
        # Create profile
        profile = PerfilUsuario.objects.create(
            user=user,
            nombre='Admin',
            apellido_paterno='Empresa',
            correo=user.email,
            nivel_usuario='admin-empresa'
        )
        print(f"✅ Created empresa admin: {user.username}")
        print(f"   Empresa: {empresa.nombre}")
        print(f"   Password: admin123")

if __name__ == '__main__':
    check_users()
