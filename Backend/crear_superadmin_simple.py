#!/usr/bin/env python
import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def crear_superadmin_simple():
    """
    Crear superadmin SOLO para login de la aplicación web
    """
    print("🚀 Creando SuperAdmin SIMPLE para login...")
    
    # Credenciales
    USERNAME = "superadmin"
    PASSWORD = "1234"
    EMAIL = "superadmin@axyoma.com"
    
    try:
        with transaction.atomic():
            # 1. Eliminar usuario existente si existe
            if User.objects.filter(username=USERNAME).exists():
                print(f"⚠️ Usuario '{USERNAME}' ya existe. Eliminando...")
                User.objects.filter(username=USERNAME).delete()
            
            # 2. Crear usuario Django
            user = User.objects.create_user(
                username=USERNAME,
                email=EMAIL,
                password=PASSWORD,
                first_name="Super",
                last_name="Admin",
                is_staff=True,
                is_superuser=True
            )
            print(f"✅ Usuario Django creado: {user.username}")
            
            # 3. Crear perfil SuperAdmin
            perfil = PerfilUsuario.objects.create(
                user_id=user,
                nombre="Super",
                apellido_paterno="Admin",
                apellido_materno="Sistema",
                correo=EMAIL,
                nivel_usuario="superadmin",
                status=True,
                admin_empresa=None  # SuperAdmin no tiene admin_empresa
            )
            print(f"✅ Perfil SuperAdmin creado: {perfil.nombre_completo}")
            
            print("\n" + "="*50)
            print("🎉 SUPERADMIN CREADO PARA LOGIN")
            print("="*50)
            print(f"👤 Usuario: {USERNAME}")
            print(f"🔑 Contraseña: {PASSWORD}")
            print(f"📧 Email: {EMAIL}")
            print(f"🎯 Nivel: {perfil.nivel_usuario}")
            print("="*50)
            print("\n🌐 PARA PROBAR:")
            print("1. Inicia servidor: python manage.py runserver")
            print("2. Ve a: http://localhost:3000/login")
            print("3. USA: superadmin / 1234")
            print("\n🚀 ¡Ya puedes hacer login!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando SuperAdmin: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT CREAR SUPERADMIN SIMPLE")
    print("-" * 30)
    
    success = crear_superadmin_simple()
    
    if success:
        print("\n✅ SuperAdmin creado exitosamente")
        
        # Verificar login
        from django.contrib.auth import authenticate
        user = authenticate(username="superadmin", password="1234")
        if user:
            print("✅ Login verificado - credenciales funcionan")
            print("✅ ¡Listo para usar en la aplicación web!")
        else:
            print("⚠️ Error verificando login")
    else:
        print("\n❌ Proceso falló")
