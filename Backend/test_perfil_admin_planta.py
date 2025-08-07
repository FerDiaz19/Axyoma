#!/usr/bin/env python3
"""
Test simple para crear PerfilUsuario admin-planta
"""
import os
import sys
import django

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

def test_crear_perfil_admin_planta():
    """Test de creación de perfil admin-planta"""
    
    # 1. Buscar un admin-empresa existente
    admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
    
    if not admin_empresa:
        print("❌ No hay admin-empresa disponible")
        return
        
    print(f"✅ Admin empresa: {admin_empresa.nombre} (ID: {admin_empresa.id})")
    
    # 2. Crear usuario Django temporal
    user = User.objects.create_user(
        username='test_admin_planta',
        email='test@test.com',
        password='test123'
    )
    print(f"✅ Usuario Django creado: {user.username}")
    
    try:
        # 3. Intentar crear PerfilUsuario
        perfil = PerfilUsuario.objects.create(
            user_id=user,  # Usar user_id en lugar de user
            nombre="Test Admin",
            apellido_paterno="Planta", 
            apellido_materno="Manager",
            correo="test@test.com",
            nivel_usuario='admin-planta',
            admin_empresa=admin_empresa  # El PerfilUsuario del admin-empresa
        )
        print(f"✅ Perfil creado exitosamente: {perfil.id}")
        
        # Limpiar
        perfil.delete()
        user.delete()
        print("✅ Test completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando perfil: {str(e)}")
        # Limpiar usuario en caso de error
        user.delete()
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crear_perfil_admin_planta()
