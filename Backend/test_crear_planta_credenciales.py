#!/usr/bin/env python3
"""
Script para probar la creación de plantas con credenciales automáticas
"""
import os
import sys
import django
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.authtoken.models import Token

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.views import PlantaViewSet
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def test_crear_planta_con_credenciales():
    """Crear una planta y verificar que se generen las credenciales"""
    print("🧪 Iniciando prueba de creación de planta con credenciales...")
    
    try:
        # 1. Buscar un usuario admin-empresa
        admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
        
        if not admin_empresa:
            print("❌ No se encontró ningún admin-empresa")
            return
            
        print(f"👤 Admin empresa encontrado: {admin_empresa.nombre} (ID: {admin_empresa.id})")
        
        # 2. Obtener la empresa
        empresa = Empresa.objects.filter(administrador=admin_empresa).first()
        
        if not empresa:
            print("❌ No se encontró empresa para el admin")
            return
            
        print(f"🏢 Empresa encontrada: {empresa.nombre} (ID: {empresa.empresa_id})")
        
        # 3. Contar plantas actuales
        plantas_actuales = Planta.objects.filter(empresa=empresa).count()
        print(f"📊 Plantas actuales: {plantas_actuales}")
        
        if plantas_actuales >= 5:
            print("❌ Ya se alcanzó el límite de plantas (5)")
            return
        
        # 4. Crear factory de request
        factory = RequestFactory()
        request = factory.post('/plantas/', {
            'nombre': 'Planta Test Credenciales',
            'direccion': 'Dirección de prueba 123'
        })
        request.user = admin_empresa.user
        
        # 5. Crear instancia del ViewSet
        viewset = PlantaViewSet()
        viewset.request = request
        
        # 6. Preparar datos de la planta
        from apps.serializers import PlantaCreateSerializer
        serializer = PlantaCreateSerializer(data={
            'nombre': 'Planta Test Credenciales',
            'direccion': 'Dirección de prueba 123'
        })
        
        if serializer.is_valid():
            print("✅ Datos válidos, creando planta...")
            
            # 7. Simular perform_create
            viewset.perform_create(serializer)
            
            print("✅ Planta creada exitosamente")
            
            # 8. Verificar que se creó el usuario
            planta_creada = Planta.objects.filter(nombre='Planta Test Credenciales').first()
            if planta_creada:
                print(f"🏭 Planta ID: {planta_creada.planta_id}")
                
                # Buscar AdminPlanta relacionado
                admin_planta = AdminPlanta.objects.filter(planta=planta_creada).first()
                if admin_planta:
                    usuario = admin_planta.usuario.user
                    print(f"👤 Usuario creado: {usuario.username}")
                    print(f"📧 Email: {usuario.email}")
                    
                    # Verificar token
                    token = Token.objects.filter(user=usuario).first()
                    if token:
                        print(f"🔑 Token creado: {token.key}")
                    else:
                        print("❌ No se creó token")
                else:
                    print("❌ No se creó AdminPlanta")
            else:
                print("❌ No se encontró la planta creada")
        else:
            print(f"❌ Datos inválidos: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crear_planta_con_credenciales()
