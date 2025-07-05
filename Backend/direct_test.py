#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

# Test imports
try:
    from django.contrib.auth.models import User
    from apps.users.models import PerfilUsuario
    print("✅ Imports successful")
    
    # Test creation
    print("Cleaning previous test data...")
    User.objects.filter(username='test_user').delete()
    
    print("Creating test user...")
    user = User.objects.create_user(
        username='test_user',
        email='test@example.com', 
        password='1234'
    )
    print(f"User created: {user}")
    
    print("Creating test profile...")
    perfil = PerfilUsuario.objects.create(
        user=user,
        nombre='Test',
        apellido_paterno='User',
        correo='test@example.com',
        nivel_usuario='superadmin'
    )
    print(f"Profile created: {perfil}")
    
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
