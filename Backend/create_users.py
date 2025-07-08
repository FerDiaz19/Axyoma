#!/usr/bin/env python
"""
Script para recrear usuarios de prueba en Axyoma
"""
import os
import sys
import django
from pathlib import Path

# Configurar el entorno Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

def create_test_users():
    """Crea los usuarios de prueba del sistema"""
    try:
        django.setup()
        
        from django.contrib.auth.models import User
        from apps.users.models import PerfilUsuario, AdminPlanta, Empresa, Planta
        
        print("🔍 Verificando usuarios existentes...")
        existing_users = User.objects.all()
        print(f"Usuarios encontrados: {existing_users.count()}")
        for user in existing_users:
            print(f"  - {user.username}")
        
        print("\n👥 Creando usuarios de prueba...")
        
        # 1. SuperAdmin
        if not User.objects.filter(username='superadmin').exists():
            superadmin = User.objects.create_user(
                username='superadmin',
                password='admin123',
                email='superadmin@axyoma.com',
                first_name='Super',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )
            
            PerfilUsuario.objects.create(
                user=superadmin,
                role='superadmin',
                nombre='Super',
                apellido_paterno='Admin',
                apellido_materno='System'
            )
            print("✅ SuperAdmin creado: superadmin / admin123")
        else:
            print("✅ SuperAdmin ya existe: superadmin / admin123")
        
        # 2. Admin Empresa
        if not User.objects.filter(username='admin').exists():
            admin_empresa = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@empresa.com',
                first_name='Admin',
                last_name='Empresa'
            )
            
            PerfilUsuario.objects.create(
                user=admin_empresa,
                role='admin_empresa',
                nombre='Admin',
                apellido_paterno='Empresa',
                apellido_materno='Principal'
            )
            print("✅ Admin Empresa creado: admin / admin123")
        else:
            print("✅ Admin Empresa ya existe: admin / admin123")
        
        # 3. Admin Planta
        if not User.objects.filter(username='planta1').exists():
            admin_planta = User.objects.create_user(
                username='planta1',
                password='admin123',
                email='planta1@empresa.com',
                first_name='Admin',
                last_name='Planta'
            )
            
            PerfilUsuario.objects.create(
                user=admin_planta,
                role='admin_planta',
                nombre='Admin',
                apellido_paterno='Planta',
                apellido_materno='Uno'
            )
            print("✅ Admin Planta creado: planta1 / admin123")
        else:
            print("✅ Admin Planta ya existe: planta1 / admin123")
        
        # 4. Verificar empresas existentes
        print("\n🏢 Verificando empresas...")
        empresas = Empresa.objects.all()
        print(f"Empresas encontradas: {empresas.count()}")
        for empresa in empresas[:5]:  # Mostrar solo las primeras 5
            print(f"  - Empresa {empresa.id}: {empresa.nombre}")
        
        print("\n🎯 RESUMEN:")
        print("✅ Usuarios de prueba disponibles:")
        print("   SuperAdmin:     superadmin / admin123")
        print("   Admin Empresa:  admin / admin123")
        print("   Admin Planta:   planta1 / admin123")
        print(f"\n📊 Datos del sistema:")
        print(f"   - Usuarios: {User.objects.count()}")
        print(f"   - Empresas: {empresas.count()}")
        print(f"   - Perfiles: {PerfilUsuario.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if create_test_users():
        print("\n🚀 ¡Usuarios creados exitosamente!")
        print("Tu sistema debería funcionar normalmente ahora.")
    else:
        print("\n💥 Error en la creación de usuarios")
        sys.exit(1)
