#!/usr/bin/env python3
"""
Test directo para verificar el fix de PerfilUsuario
"""
import os
import sys
import django

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, AdminPlanta

def test_perfil_usuario_lookup():
    """Test de búsqueda de PerfilUsuario usando user_id"""
    
    print("🔍 Probando búsqueda de PerfilUsuario con user_id...")
    
    # Obtener un usuario cualquiera
    user = User.objects.first()
    if not user:
        print("❌ No hay usuarios en el sistema")
        return
        
    print(f"👤 Usuario: {user.username} (ID: {user.id})")
    
    # Intentar encontrar el perfil usando user_id
    try:
        perfil = PerfilUsuario.objects.get(user_id=user)
        print(f"✅ Perfil encontrado: {perfil.nombre} (Nivel: {perfil.nivel_usuario})")
        
        # Si es admin-planta, ver su AdminPlanta
        if perfil.nivel_usuario == 'admin-planta':
            try:
                admin_planta = AdminPlanta.objects.get(usuario=perfil)
                print(f"✅ AdminPlanta encontrado: {admin_planta.planta.nombre}")
                print(f"   📅 Fecha asignación: {admin_planta.fecha_asignacion}")
            except AdminPlanta.DoesNotExist:
                print("❌ No se encontró AdminPlanta para este perfil")
        
    except PerfilUsuario.DoesNotExist:
        print(f"❌ No se encontró perfil para usuario {user.username}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_admin_planta_users():
    """Test específico para usuarios admin-planta"""
    
    print("\n🔍 Verificando usuarios admin-planta...")
    
    admin_plantas = AdminPlanta.objects.all()
    
    for admin_planta in admin_plantas:
        perfil = admin_planta.usuario
        user = perfil.user_id
        
        print(f"\n👤 Usuario: {user.username} (ID: {user.id})")
        print(f"   📧 Email: {user.email}")
        print(f"   🏭 Planta: {admin_planta.planta.nombre}")
        print(f"   🏢 Empresa: {admin_planta.planta.empresa.nombre}")
        
        # Verificar que se puede encontrar el perfil usando user_id
        try:
            perfil_test = PerfilUsuario.objects.get(user_id=user)
            print(f"   ✅ Búsqueda por user_id exitosa")
        except Exception as e:
            print(f"   ❌ Error en búsqueda: {str(e)}")

if __name__ == "__main__":
    test_perfil_usuario_lookup()
    test_admin_planta_users()
