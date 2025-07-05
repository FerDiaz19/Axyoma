#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import authenticate
from apps.users.models import PerfilUsuario, Empresa

print("=== VERIFICANDO JUAN PEREZ ===")

# Buscar perfil
try:
    perfil = PerfilUsuario.objects.get(correo='juan.perez@codewave.com')
    print(f"✅ Perfil encontrado: {perfil.nombre} {perfil.apellido_paterno}")
    print(f"   Nivel: {perfil.nivel_usuario}")
    print(f"   ID: {perfil.id}")
    
    # Buscar empresa
    try:
        empresa = Empresa.objects.get(administrador=perfil)
        print(f"✅ Empresa encontrada: {empresa.nombre}")
        print(f"   ID: {empresa.empresa_id}")
        print(f"   RFC: {empresa.rfc}")
    except Empresa.DoesNotExist:
        print("❌ No se encontró empresa para este perfil")
        
        # Verificar si hay empresas
        empresas = Empresa.objects.all()
        print(f"Total empresas en BD: {empresas.count()}")
        for emp in empresas:
            print(f"  - {emp.nombre} (Admin: {emp.administrador.nombre})")
            
except PerfilUsuario.DoesNotExist:
    print("❌ Perfil juan.perez no encontrado")

# Probar autenticación
print("\n=== PROBANDO LOGIN ===")
user = authenticate(username='juan.perez@codewave.com', password='1234')
if user and hasattr(user, 'perfil'):
    print(f"✅ Login exitoso: {user.perfil.nivel_usuario}")
else:
    print("❌ Login falló")
