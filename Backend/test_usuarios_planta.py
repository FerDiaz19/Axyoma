#!/usr/bin/env python
"""
Script para probar el endpoint de usuarios de planta
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.models import Empresa, Planta, AdminPlanta, Usuario

def test_empresa_plantas():
    """Probar el estado de la empresa 10 y sus plantas"""
    try:
        # Buscar empresa 10
        empresa = Empresa.objects.get(empresa_id=10)
        print(f"🏢 Empresa: {empresa.nombre} (ID: {empresa.empresa_id})")
        
        # Listar todas las plantas
        plantas = Planta.objects.filter(empresa=empresa, status=True)
        print(f"🏭 Total de plantas: {plantas.count()}")
        
        for planta in plantas:
            print(f"  - Planta {planta.planta_id}: {planta.nombre}")
            
            # Buscar administradores
            admins = AdminPlanta.objects.filter(planta=planta)
            print(f"    👥 Administradores: {admins.count()}")
            
            if admins.exists():
                for admin in admins:
                    print(f"      - {admin.usuario.user.username} ({admin.usuario.user.email})")
            else:
                print("      - Sin administradores (normal para Planta Principal)")
        
        # Simular el endpoint
        print("\n📊 Simulando endpoint /plantas/usuarios-planta/:")
        
        # Plantas excluyendo Planta Principal
        plantas_con_usuarios = plantas.exclude(nombre='Planta Principal')
        print(f"  - Plantas que deberían tener usuarios: {plantas_con_usuarios.count()}")
        
        # Administradores de esas plantas
        admin_plantas = AdminPlanta.objects.filter(planta__in=plantas_con_usuarios)
        print(f"  - Usuarios encontrados: {admin_plantas.count()}")
        
        # Info adicional
        plantas_sin_usuarios = plantas.filter(nombre='Planta Principal')
        print(f"  - Planta Principal sin usuario: {plantas_sin_usuarios.exists()}")
        
        print("\n✅ Test completado exitosamente")
        
    except Empresa.DoesNotExist:
        print("❌ Error: Empresa 10 no encontrada")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_empresa_plantas()
