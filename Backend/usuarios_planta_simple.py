#!/usr/bin/env python
"""
Script para mostrar usuarios de planta específicamente
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import AdminPlanta

print("=== USUARIOS DE PLANTA ===")
admin_plantas = AdminPlanta.objects.all()
print(f"Total: {admin_plantas.count()}")

for ap in admin_plantas:
    u = ap.usuario.user
    p = ap.planta
    print(f"- {p.nombre}: {u.username} ({u.email})")
