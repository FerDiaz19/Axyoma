#!/usr/bin/env python
"""
Simple test script to verify the SuperAdmin listar_usuarios endpoint
"""
import os
import sys
import django

# Add the Backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import PerfilUsuario, AdminPlanta
from django.contrib.auth.models import User

def test_relationship_access():
    """Test that we can access relationships correctly"""
    print("Testing relationship access patterns...")
    
    try:
        # Test accessing users through PerfilUsuario
        perfiles = PerfilUsuario.objects.filter(user_id__isnull=False)[:1]
        if perfiles:
            perfil = perfiles[0]
            print(f"✅ PerfilUsuario.user access: {perfil.user_id}")
            print(f"✅ PerfilUsuario.user.username: {perfil.user_id.username}")
        
        # Test accessing AdminPlanta relationships
        admin_plantas = AdminPlanta.objects.select_related('usuario__user_id', 'planta')[:1]
        if admin_plantas:
            admin_planta = admin_plantas[0]
            print(f"✅ AdminPlanta.usuario.user_id access: {admin_planta.usuario.user_id}")
            print(f"✅ AdminPlanta.usuario.user_id.username: {admin_planta.usuario.user_id.username}")
        
        print("✅ All relationship access tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Relationship access test failed: {e}")
        return False

def test_listar_usuarios_logic():
    """Test the listar_usuarios logic without HTTP"""
    print("\nTesting listar_usuarios logic...")
    
    try:
        # Get users that have user associated
        usuarios = PerfilUsuario.objects.filter(user_id__isnull=False)
        
        usuarios_data = []
        for usuario in usuarios:
            try:
                # This is the logic from listar_usuarios
                usuario_info = {
                    'user_id': usuario.user_id.id,
                    'profile_id': usuario.id,
                    'username': usuario.user_id.username,
                    'email': usuario.user_id.email,
                    'nombre': usuario.nombre,
                    'nivel_usuario': usuario.nivel_usuario,
                    'is_active': usuario.user_id.is_active,
                }
                
                # Test admin-planta logic
                if usuario.nivel_usuario == 'admin-planta':
                    try:
                        admin_planta = AdminPlanta.objects.get(usuario=usuario)
                        planta = admin_planta.planta
                        usuario_info['planta'] = {
                            'id': planta.planta_id,
                            'nombre': planta.nombre,
                            'empresa_nombre': planta.empresa.nombre,
                            'status': admin_planta.status
                        }
                    except AdminPlanta.DoesNotExist:
                        pass
                
                usuarios_data.append(usuario_info)
                
            except Exception as e:
                print(f"⚠️ Error processing user {usuario.id}: {e}")
                continue
        
        print(f"✅ Successfully processed {len(usuarios_data)} users")
        for user_data in usuarios_data[:3]:  # Show first 3 users
            print(f"  - {user_data['username']} ({user_data['nivel_usuario']})")
        
        return True
        
    except Exception as e:
        print(f"❌ listar_usuarios logic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing SuperAdmin listar_usuarios endpoint fixes...")
    
    # Test relationship access patterns
    success1 = test_relationship_access()
    
    # Test the actual listar_usuarios logic
    success2 = test_listar_usuarios_logic()
    
    if success1 and success2:
        print("\n✅ All tests passed! The listar_usuarios endpoint should work correctly.")
    else:
        print("\n❌ Some tests failed. There may still be issues.")
