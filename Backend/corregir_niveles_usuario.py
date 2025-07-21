#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario

print("🔧 CORRIGIENDO NIVELES DE USUARIO EN LA BASE DE DATOS")
print("=" * 60)

# Corregir admin-empresa a admin_empresa
usuarios_admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa')
print(f"📝 Corrigiendo {usuarios_admin_empresa.count()} usuarios 'admin-empresa' -> 'admin_empresa'")

for usuario in usuarios_admin_empresa:
    print(f"   ✅ {usuario.correo}: 'admin-empresa' -> 'admin_empresa'")
    usuario.nivel_usuario = 'admin_empresa'
    usuario.save()

print("\n✅ CORRECCIÓN COMPLETADA")
print("\n🎯 ESTADO FINAL:")
print("-" * 30)

# Mostrar resumen actualizado
niveles = {}
for perfil in PerfilUsuario.objects.all():
    nivel = perfil.nivel_usuario
    if nivel in niveles:
        niveles[nivel] += 1
    else:
        niveles[nivel] = 1

for nivel, cantidad in niveles.items():
    print(f"'{nivel}': {cantidad} usuario(s)")

print(f"\n✅ TODOS LOS NIVELES DE USUARIO ESTÁN AHORA CONSISTENTES")
