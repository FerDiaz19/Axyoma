#!/usr/bin/env python3
"""
Test para probar el reseteo de contraseña de usuarios planta
"""
import os
import sys
import django

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, AdminPlanta, Empresa
import json

def test_resetear_password():
    """Test de reseteo de contraseña"""
    
    print("🧪 Probando reseteo de contraseña de usuario planta...")
    
    # 1. Encontrar un admin-empresa
    admin_empresa_perfil = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
    if not admin_empresa_perfil:
        print("❌ No hay admin-empresa disponible")
        return
        
    admin_empresa_user = admin_empresa_perfil.user_id
    print(f"👤 Admin empresa: {admin_empresa_user.username} (Perfil ID: {admin_empresa_perfil.id})")
    
    # 2. Encontrar un usuario admin-planta de esa empresa
    empresa = Empresa.objects.filter(administrador=admin_empresa_perfil).first()
    if not empresa:
        print("❌ No se encontró empresa")
        return
        
    print(f"🏢 Empresa: {empresa.nombre}")
    
    # 3. Buscar admin-planta de esa empresa
    admin_planta_obj = AdminPlanta.objects.filter(planta__empresa=empresa).first()
    if not admin_planta_obj:
        print("❌ No hay usuarios admin-planta en la empresa")
        return
        
    usuario_planta_perfil = admin_planta_obj.usuario
    usuario_planta_user = usuario_planta_perfil.user_id
    
    print(f"👤 Usuario planta: {usuario_planta_user.username} (ID: {usuario_planta_user.id})")
    print(f"🏭 Planta: {admin_planta_obj.planta.nombre}")
    
    # 4. Simular el request
    from django.test import RequestFactory
    from rest_framework.test import APIRequestFactory
    from apps.views import PlantaViewSet
    
    factory = APIRequestFactory()
    
    # Simular datos del request
    data = {
        'usuario_id': usuario_planta_user.id
    }
    
    request = factory.post('/api/plantas/resetear-password-usuario/', data, format='json')
    request.user = admin_empresa_user
    
    # 5. Ejecutar el método
    viewset = PlantaViewSet()
    viewset.request = request
    
    try:
        response = viewset.resetear_password_usuario(request)
        
        print(f"🔄 Status Code: {response.status_code}")
        print(f"📊 Response Data: {response.data}")
        
        if response.status_code == 200:
            print("✅ Reseteo de contraseña exitoso")
            print(f"🔑 Nueva contraseña: {response.data.get('nueva_password')}")
        else:
            print(f"❌ Error: {response.data}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_resetear_password()
