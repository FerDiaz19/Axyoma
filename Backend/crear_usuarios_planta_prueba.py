#!/usr/bin/env python
"""
Crear usuarios AdminPlanta de prueba para las plantas de la empresa axis88
"""
import os
import sys
import django

# Configurar Django
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def crear_usuarios_planta_prueba():
    """Crear usuarios AdminPlanta para las plantas de la empresa axis88"""
    print("🏭 Creando usuarios de planta de prueba...")
    
    from apps.users.models import Empresa, Planta, AdminPlanta, PerfilUsuario
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    import random
    import string
    
    try:
        # Obtener empresa axis88
        empresa = Empresa.objects.filter(empresa_id=10).first()
        if not empresa:
            print("❌ Empresa con ID 10 no encontrada")
            return
            
        print(f"✅ Empresa encontrada: {empresa.nombre}")
        
        # Obtener plantas sin usuarios (excluyendo Planta Principal)
        plantas_sin_usuarios = Planta.objects.filter(
            empresa=empresa, 
            status=True
        ).exclude(nombre='Planta Principal')
        
        plantas_ya_con_usuarios = AdminPlanta.objects.filter(
            planta__empresa=empresa
        ).values_list('planta__planta_id', flat=True)
        
        plantas_disponibles = plantas_sin_usuarios.exclude(
            planta_id__in=plantas_ya_con_usuarios
        )
        
        print(f"✅ Plantas disponibles para asignar usuarios: {plantas_disponibles.count()}")
        
        usuarios_creados = 0
        
        for i, planta in enumerate(plantas_disponibles[:3]):  # Solo crear 3 usuarios de prueba
            print(f"\n🔨 Creando usuario para planta: {planta.nombre} (ID: {planta.planta_id})")
            
            try:
                # Generar username único
                base_username = f"admin_planta_{planta.planta_id}"
                username = base_username
                contador = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}_{contador}"
                    contador += 1
                
                # Generar contraseña segura
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                
                # Crear usuario Django
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@{empresa.nombre.lower().replace(' ', '')}.com",
                    password=password,
                    first_name=f"Admin",
                    last_name=f"Planta {planta.planta_id}"
                )
                
                # Crear perfil de usuario
                perfil = PerfilUsuario.objects.create(
                    user_id=user,
                    nombre=f"Admin",
                    apellido_paterno=f"Planta",
                    apellido_materno=f"{planta.planta_id}",
                    correo=user.email,
                    nivel_usuario='admin-planta',
                    admin_empresa=empresa.administrador
                )
                
                # Crear relación AdminPlanta
                admin_planta = AdminPlanta.objects.create(
                    usuario=perfil,
                    planta=planta,
                    status=True
                )
                
                # Crear token
                token = Token.objects.create(user=user)
                
                print(f"  ✅ Usuario creado: {username}")
                print(f"  📧 Email: {user.email}")
                print(f"  🔑 Password: {password}")
                print(f"  🎯 Token: {token.key}")
                
                usuarios_creados += 1
                
            except Exception as e:
                print(f"  ❌ Error creando usuario para planta {planta.nombre}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🎉 Proceso completado: {usuarios_creados} usuarios creados")
        
        # Verificar resultado
        total_admin_plantas = AdminPlanta.objects.filter(planta__empresa=empresa).count()
        print(f"📊 Total AdminPlanta records para empresa {empresa.nombre}: {total_admin_plantas}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_usuarios_planta_prueba()
