#!/usr/bin/env python3
"""
Test para encontrar usuarios planta y probar reseteo
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

def encontrar_usuarios_planta():
    """Encontrar todos los usuarios admin-planta disponibles"""
    
    print("🔍 Buscando usuarios admin-planta...")
    
    admin_plantas = AdminPlanta.objects.all()
    
    print(f"📊 Total AdminPlanta encontrados: {admin_plantas.count()}")
    
    for admin_planta in admin_plantas:
        usuario_perfil = admin_planta.usuario
        usuario_django = usuario_perfil.user_id
        planta = admin_planta.planta
        empresa = planta.empresa
        admin_empresa = empresa.administrador
        admin_empresa_user = admin_empresa.user_id
        
        print(f"\n👤 Usuario Planta: {usuario_django.username} (ID: {usuario_django.id})")
        print(f"   🏭 Planta: {planta.nombre}")
        print(f"   🏢 Empresa: {empresa.nombre}")
        print(f"   👤 Admin Empresa: {admin_empresa_user.username}")
        print(f"   📅 Fecha asignación: {admin_planta.fecha_asignacion}")
        print(f"   🟢 Status: {admin_planta.status}")
        
    # Intentar con el primero disponible
    if admin_plantas.exists():
        print(f"\n🧪 Probando reseteo con el primer usuario disponible...")
        
        admin_planta = admin_plantas.first()
        usuario_planta = admin_planta.usuario.user_id
        admin_empresa = admin_planta.planta.empresa.administrador.user_id
        
        print(f"   👤 Usuario planta: {usuario_planta.username}")
        print(f"   👤 Admin empresa: {admin_empresa.username}")
        
        # Simular request
        from django.test import RequestFactory
        from rest_framework.test import APIRequestFactory
        from apps.views import PlantaViewSet
        
        factory = APIRequestFactory()
        
        data = {'usuario_id': usuario_planta.id}
        request = factory.post('/api/plantas/resetear-password-usuario/', data, format='json')
        request.user = admin_empresa
        
        viewset = PlantaViewSet()
        viewset.request = request
        
        try:
            response = viewset.resetear_password_usuario(request)
            
            print(f"   🔄 Status: {response.status_code}")
            print(f"   📊 Response: {response.data}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    encontrar_usuarios_planta()
