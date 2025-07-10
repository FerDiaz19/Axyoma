#!/usr/bin/env python3
"""
Script para limpiar la base de datos y crear usuarios base
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario
from apps.models import Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta
from django.db import transaction

def limpiar_base_datos():
    """Limpiar todos los datos de la base de datos"""
    print("🧹 Limpiando base de datos...")
    
    try:
        with transaction.atomic():
            # Eliminar en orden para respetar foreign keys
            print("   - Eliminando empleados...")
            Empleado.objects.all().delete()
            
            print("   - Eliminando puestos...")
            Puesto.objects.all().delete()
            
            print("   - Eliminando departamentos...")
            Departamento.objects.all().delete()
            
            print("   - Eliminando plantas...")
            Planta.objects.all().delete()
            
            print("   - Eliminando empresas...")
            Empresa.objects.all().delete()
            
            print("   - Eliminando perfiles de usuario...")
            PerfilUsuario.objects.all().delete()
            
            print("   - Eliminando usuarios...")
            User.objects.all().delete()
            
        print("✅ Base de datos limpiada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando base de datos: {e}")
        return False

def crear_usuarios_base():
    """Crear usuarios base del sistema"""
    print("👥 Creando usuarios base...")
    
    try:
        with transaction.atomic():
            # 1. Usuario SuperAdmin
            print("   - Creando SuperAdmin...")
            superadmin_user = User.objects.create_user(
                username='superadmin@axyoma.com',
                email='superadmin@axyoma.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            PerfilUsuario.objects.create(
                user=superadmin_user,
                nombre='Super',
                apellido_paterno='Admin',
                apellido_materno='Sistema',
                correo='superadmin@axyoma.com',
                nivel_usuario='superadmin'
            )
            
            # 2. Usuario Admin Empresa de prueba
            print("   - Creando Admin Empresa de prueba...")
            admin_empresa_user = User.objects.create_user(
                username='admin@empresa.com',
                email='admin@empresa.com',
                password='admin123',
                is_active=True
            )
            
            perfil_admin_empresa = PerfilUsuario.objects.create(
                user=admin_empresa_user,
                nombre='Admin',
                apellido_paterno='Empresa',
                apellido_materno='Prueba',
                correo='admin@empresa.com',
                nivel_usuario='admin-empresa'
            )
            
            # 3. Crear empresa de prueba
            print("   - Creando empresa de prueba...")
            empresa_prueba = Empresa.objects.create(
                nombre='Empresa de Prueba',
                rfc='EPR240101XXX',
                telefono_contacto='555-0123',
                email_contacto='contacto@empresa.com',
                direccion='Calle Principal #123, Ciudad, Estado',
                administrador=perfil_admin_empresa,
                status=True
            )
            
            # 4. Usuario Admin Planta de prueba
            print("   - Creando Admin Planta de prueba...")
            admin_planta_user = User.objects.create_user(
                username='planta@empresa.com',
                email='planta@empresa.com',
                password='admin123',
                is_active=True
            )
            
            perfil_admin_planta = PerfilUsuario.objects.create(
                user=admin_planta_user,
                nombre='Admin',
                apellido_paterno='Planta',
                apellido_materno='Uno',
                correo='planta@empresa.com',
                nivel_usuario='admin-planta'
            )
            
            # 5. Crear planta de prueba
            print("   - Creando planta de prueba...")
            planta_prueba = Planta.objects.create(
                nombre='Planta Principal',
                direccion='Zona Industrial #456, Ciudad, Estado',
                empresa=empresa_prueba,
                status=True
            )
            
            # 6. Crear AdminPlanta
            AdminPlanta.objects.create(
                usuario=perfil_admin_planta,
                planta=planta_prueba,
                status=True
            )
            
            # 7. Crear departamento de prueba
            print("   - Creando departamento de prueba...")
            departamento_prueba = Departamento.objects.create(
                nombre='Recursos Humanos',
                descripcion='Departamento encargado de la gestión del personal',
                planta=planta_prueba,
                status=True
            )
            
            # 8. Crear puesto de prueba
            print("   - Creando puesto de prueba...")
            puesto_prueba = Puesto.objects.create(
                nombre='Analista de RH',
                descripcion='Encargado del análisis y gestión de recursos humanos',
                departamento=departamento_prueba,
                status=True
            )
            
            # 9. Crear empleado de prueba
            print("   - Creando empleado de prueba...")
            Empleado.objects.create(
                nombre='Juan',
                apellido_paterno='Pérez',
                apellido_materno='García',
                planta=planta_prueba,
                departamento=departamento_prueba,
                puesto=puesto_prueba,
                status=True
            )
            
        print("✅ Usuarios base creados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios base: {e}")
        return False

def mostrar_usuarios_creados():
    """Mostrar usuarios creados"""
    print("\n📋 Usuarios creados:")
    print("=" * 50)
    
    usuarios = User.objects.all()
    for user in usuarios:
        try:
            perfil = PerfilUsuario.objects.get(user=user)
            print(f"👤 {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Nivel: {perfil.nivel_usuario}")
            print(f"   Activo: {'✅' if user.is_active else '❌'}")
            print(f"   Contraseña: admin123")
            print()
        except PerfilUsuario.DoesNotExist:
            print(f"👤 {user.username} (sin perfil)")
            print()

def main():
    """Función principal"""
    print("🚀 Iniciando limpieza y configuración de usuarios base...")
    print("=" * 60)
    
    # 1. Limpiar base de datos
    if not limpiar_base_datos():
        print("❌ Error en la limpieza. Abortando...")
        return
    
    print()
    
    # 2. Crear usuarios base
    if not crear_usuarios_base():
        print("❌ Error creando usuarios base. Abortando...")
        return
    
    print()
    
    # 3. Mostrar usuarios creados
    mostrar_usuarios_creados()
    
    print("=" * 60)
    print("🎉 ¡Configuración completada exitosamente!")
    print()
    print("📝 Credenciales para login:")
    print("   SuperAdmin:")
    print("     Usuario: superadmin@axyoma.com")
    print("     Contraseña: admin123")
    print()
    print("   Admin Empresa:")
    print("     Usuario: admin@empresa.com")
    print("     Contraseña: admin123")
    print()
    print("   Admin Planta:")
    print("     Usuario: planta@empresa.com")
    print("     Contraseña: admin123")

if __name__ == "__main__":
    main()
