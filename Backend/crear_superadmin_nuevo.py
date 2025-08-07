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

def crear_superadmin():
    """
    Crear un superadmin nuevo con credenciales simples
    """
    print("🔧 Creando SuperAdmin nuevo...")
    
    # Credenciales del nuevo superadmin
    USERNAME = "admin"
    PASSWORD = "1234"
    EMAIL = "admin@axyoma.com"
    
    try:
        with transaction.atomic():
            # Eliminar usuario existente si existe
            if User.objects.filter(username=USERNAME).exists():
                print(f"⚠️ Usuario '{USERNAME}' ya existe. Eliminando...")
                User.objects.filter(username=USERNAME).delete()
            
            # Crear usuario Django
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
            
            # Crear perfil de usuario
            perfil = PerfilUsuario.objects.create(
                user_id=user,
                nombre="Super",
                apellido_paterno="Admin",
                apellido_materno="Sistema",
                correo=EMAIL,
                nivel_usuario="superadmin",
                status=True
            )
            
            print(f"✅ Perfil creado: {perfil.nombre_completo}")
            
            # Mostrar credenciales
            print("\n" + "="*50)
            print("🎉 SUPERADMIN CREADO EXITOSAMENTE")
            print("="*50)
            print(f"👤 Usuario: {USERNAME}")
            print(f"🔑 Contraseña: {PASSWORD}")
            print(f"📧 Email: {EMAIL}")
            print(f"🎯 Nivel: {perfil.nivel_usuario}")
            print("="*50)
            print("\n🌐 URLS DE ACCESO:")
            print("   • Admin Panel: http://127.0.0.1:8000/admin/")
            print("   • API Login: http://127.0.0.1:8000/api/auth/login/")
            print("   • Frontend: http://localhost:3000")
            print("\n🚀 ¡Ya puedes hacer login con estas credenciales!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando SuperAdmin: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT CREAR SUPERADMIN")
    print("-" * 30)
    
    success = crear_superadmin()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
        
        # Verificar login
        from django.contrib.auth import authenticate
        user = authenticate(username="admin", password="1234")
        if user:
            print("✅ Login verificado - credenciales funcionan correctamente")
        else:
            print("⚠️ Error verificando login")
    else:
        print("\n❌ Proceso falló")
