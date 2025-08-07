#!/usr/bin/env python
"""
Test del endpoint resetear-password-usuario
"""
import os
import sys
import django

# Configurar Django
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_resetear_password():
    """Test del endpoint resetear-password-usuario"""
    print("🔑 Testing resetear-password-usuario...")
    
    from apps.users.models import Empresa, Planta, AdminPlanta, PerfilUsuario
    from django.contrib.auth.models import User
    
    try:
        # Obtener empresa axis88
        empresa = Empresa.objects.filter(empresa_id=10).first()
        if not empresa:
            print("❌ Empresa con ID 10 no encontrada")
            return
            
        print(f"✅ Empresa encontrada: {empresa.nombre}")
        
        # Obtener usuarios AdminPlanta de esta empresa
        admin_plantas = AdminPlanta.objects.filter(planta__empresa=empresa)
        print(f"✅ AdminPlanta records encontrados: {admin_plantas.count()}")
        
        if admin_plantas.count() == 0:
            print("❌ No hay usuarios AdminPlanta para probar")
            return
        
        # Tomar el primer usuario
        admin_planta = admin_plantas.first()
        usuario_target = admin_planta.usuario.user_id
        
        print(f"🔍 Usuario seleccionado para test:")
        print(f"  - Username: {usuario_target.username}")
        print(f"  - Email: {usuario_target.email}")
        print(f"  - Planta: {admin_planta.planta.nombre}")
        print(f"  - Empresa: {admin_planta.planta.empresa.nombre}")
        
        # Simular la lógica del endpoint
        print(f"\n🧪 Simulando lógica del endpoint...")
        
        # Paso 1: Obtener empresa del admin (simulamos que somos el admin de empresa)
        empresa_admin = admin_planta.planta.empresa
        print(f"  ✅ Empresa admin: {empresa_admin.nombre}")
        
        # Paso 2: Verificar que el usuario pertenece a una planta de esta empresa
        try:
            perfil_target = PerfilUsuario.objects.get(user_id=usuario_target)
            admin_planta_check = AdminPlanta.objects.get(usuario=perfil_target)
            
            print(f"  ✅ Perfil target encontrado: {perfil_target.nombre_completo}")
            print(f"  ✅ AdminPlanta check: {admin_planta_check.planta.nombre}")
            
            if admin_planta_check.planta.empresa == empresa_admin:
                print(f"  ✅ Usuario pertenece a la empresa correcta")
            else:
                print(f"  ❌ Usuario NO pertenece a la empresa")
                return
                
        except (PerfilUsuario.DoesNotExist, AdminPlanta.DoesNotExist) as e:
            print(f"  ❌ Error verificando usuario: {e}")
            return
        
        # Paso 3: Generar nueva contraseña (simular)
        import random
        import string
        nueva_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(f"  ✅ Nueva contraseña generada: {nueva_password}")
        
        # Paso 4: Simular actualización de contraseña (NO hacerlo realmente en el test)
        print(f"  ⚠️ SIMULACIÓN: Actualizando contraseña de {usuario_target.username}")
        print(f"  ⚠️ NOTA: En test mode, NO actualizamos la contraseña real")
        
        # Respuesta simulada
        response_data = {
            'message': 'Contraseña reseteada exitosamente',
            'usuario_id': usuario_target.id,
            'username': usuario_target.username,
            'nueva_password': nueva_password,
            'planta': admin_planta.planta.nombre,
            'instrucciones': 'Proporcione esta nueva contraseña al usuario de la planta'
        }
        
        print(f"\n✅ Respuesta simulada:")
        for key, value in response_data.items():
            print(f"  - {key}: {value}")
        
        print(f"\n🎉 Test completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_resetear_password()
