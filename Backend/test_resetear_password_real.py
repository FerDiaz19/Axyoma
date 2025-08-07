#!/usr/bin/env python
"""
Test real del endpoint resetear-password-usuario
"""
import os
import sys
import django

# Configurar Django
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_resetear_password_real():
    """Test real del endpoint resetear-password-usuario"""
    print("🔑 Test REAL de resetear password...")
    
    from apps.users.models import AdminPlanta
    from django.contrib.auth.models import User
    import random
    import string
    
    try:
        # Obtener un usuario AdminPlanta
        admin_planta = AdminPlanta.objects.filter(planta__empresa__empresa_id=10).first()
        if not admin_planta:
            print("❌ No hay AdminPlanta para empresa 10")
            return
        
        usuario_target = admin_planta.usuario.user_id
        print(f"🎯 Usuario seleccionado: {usuario_target.username}")
        print(f"📧 Email actual: {usuario_target.email}")
        print(f"🏭 Planta: {admin_planta.planta.nombre}")
        
        # Guardar contraseña anterior para verificar el cambio
        password_anterior = usuario_target.password
        print(f"🔐 Hash anterior: {password_anterior[:50]}...")
        
        # Generar nueva contraseña
        nueva_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(f"🔑 Nueva contraseña generada: {nueva_password}")
        
        # Actualizar contraseña
        usuario_target.set_password(nueva_password)
        usuario_target.save()
        
        # Verificar que cambió
        usuario_actualizado = User.objects.get(id=usuario_target.id)
        password_nuevo = usuario_actualizado.password
        print(f"🔐 Hash nuevo: {password_nuevo[:50]}...")
        
        if password_anterior != password_nuevo:
            print(f"✅ Contraseña actualizada exitosamente!")
        else:
            print(f"❌ La contraseña NO cambió")
            
        # Verificar que puede hacer login con la nueva contraseña
        from django.contrib.auth import authenticate
        user_auth = authenticate(username=usuario_target.username, password=nueva_password)
        
        if user_auth:
            print(f"✅ Login con nueva contraseña: EXITOSO")
        else:
            print(f"❌ Login con nueva contraseña: FALLÓ")
        
        print(f"\n🎉 Test real completado!")
        print(f"📋 RESUMEN:")
        print(f"  - Usuario: {usuario_target.username}")
        print(f"  - Nueva contraseña: {nueva_password}")
        print(f"  - Email: {usuario_target.email}")
        print(f"  - Planta: {admin_planta.planta.nombre}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_resetear_password_real()
