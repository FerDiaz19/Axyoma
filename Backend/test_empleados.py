#!/usr/bin/env python
"""
Script de prueba para verificar el endpoint de empleados
"""

import os
import sys
import django
import json
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empleado, AdminPlanta
from apps.views import EmpleadoViewSet
from django.test import RequestFactory
from rest_framework.authtoken.models import Token

def test_empleados_endpoint():
    print("🔍 Testing empleados endpoint...")
    
    # Crear un request factory
    factory = RequestFactory()
    
    # Buscar usuarios admin-planta y admin-empresa
    admin_planta_user = User.objects.filter(perfil__nivel_usuario='admin-planta').first()
    admin_empresa_user = User.objects.filter(perfil__nivel_usuario='admin-empresa').first()
    
    if admin_planta_user:
        print(f"\n👤 Testing admin-planta: {admin_planta_user.username}")
        
        # Crear request como admin-planta
        request = factory.get('/api/empleados/')
        request.user = admin_planta_user
        
        # Crear viewset y obtener queryset
        viewset = EmpleadoViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()
        
        print(f"📊 Empleados para admin-planta: {queryset.count()}")
        for emp in queryset[:3]:  # Solo los primeros 3
            print(f"  - {emp.nombre} {emp.apellido_paterno} (ID: {emp.empleado_id})")
            print(f"    Planta: {emp.puesto.departamento.planta.nombre} (ID: {emp.puesto.departamento.planta.planta_id})")
        
        # Probar serializer
        from apps.serializers import EmpleadoSerializer
        serializer = EmpleadoSerializer(queryset[:1], many=True)
        print(f"📄 Datos serializados (primer empleado):")
        if serializer.data:
            print(json.dumps(serializer.data[0], indent=2, default=str))
    
    if admin_empresa_user:
        print(f"\n🏢 Testing admin-empresa: {admin_empresa_user.username}")
        
        # Crear request como admin-empresa
        request = factory.get('/api/empleados/')
        request.user = admin_empresa_user
        
        # Crear viewset y obtener queryset
        viewset = EmpleadoViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()
        
        print(f"📊 Empleados para admin-empresa: {queryset.count()}")
        for emp in queryset[:3]:  # Solo los primeros 3
            print(f"  - {emp.nombre} {emp.apellido_paterno} (ID: {emp.empleado_id})")
            print(f"    Planta: {emp.puesto.departamento.planta.nombre} (ID: {emp.puesto.departamento.planta.planta_id})")

if __name__ == "__main__":
    test_empleados_endpoint()
