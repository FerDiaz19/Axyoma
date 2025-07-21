#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User

print("🔧 RESTABLECIENDO CONTRASEÑA DE ADMIN_EMPRESA")
print("=" * 50)

try:
    admin_empresa = User.objects.get(username='admin_empresa')
    admin_empresa.set_password('empresa123')
    admin_empresa.save()
    print("✅ Contraseña de 'admin_empresa' cambiada a 'empresa123'")
    
    # También crear un demo_admin con contraseña conocida
    demo_admin, created = User.objects.get_or_create(username='demo_admin')
    demo_admin.set_password('demo123')
    demo_admin.save()
    print("✅ Usuario 'demo_admin' configurado con contraseña 'demo123'")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🔑 CREDENCIALES ACTUALIZADAS:")
print("   SuperAdmin: username='superadmin', password='admin123'")
print("   Admin Empresa: username='admin_empresa', password='empresa123'")
print("   Demo Admin: username='demo_admin', password='demo123'")
print("   Admin Planta: username='planta_plantaoeste_8@codewavetechnologies.com', password='tSv1OxAa'")
