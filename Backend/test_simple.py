#!/usr/bin/env python
"""
Script simple para probar la creación de departamentos
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento
from rest_framework.authtoken.models import Token
from apps.serializers import DepartamentoCreateSerializer

def test_direct_creation():
    print("🔍 PRUEBA DIRECTA DE DEPARTAMENTOS")
    print("="*40)
    
    # Obtener datos de prueba
    admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
    if not admin_empresa:
        print("❌ No hay admin de empresa")
        return
        
    empresa = Empresa.objects.filter(administrador=admin_empresa).first()
    if not empresa:
        print("❌ No hay empresa")
        return
        
    planta = Planta.objects.filter(empresa=empresa).first()
    if not planta:
        print("❌ No hay planta")
        return
        
    print(f"✅ Admin: {admin_empresa.nombre}")
    print(f"✅ Empresa: {empresa.nombre}")
    print(f"✅ Planta: {planta.nombre} (ID: {planta.planta_id})")
    
    # Probar serializer directamente
    data = {
        'nombre': 'Departamento Test Directo',
        'descripcion': 'Prueba directa sin API',
        'planta_id': planta.planta_id
    }
    
    print(f"\n📝 Datos para crear: {data}")
    
    try:
        serializer = DepartamentoCreateSerializer(data=data)
        if serializer.is_valid():
            departamento = serializer.save()
            print(f"✅ Departamento creado exitosamente!")
            print(f"   ID: {departamento.departamento_id}")
            print(f"   Nombre: {departamento.nombre}")
            print(f"   Planta: {departamento.planta.nombre}")
        else:
            print(f"❌ Errores de validación: {serializer.errors}")
    except Exception as e:
        print(f"❌ Error creando departamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_creation()
