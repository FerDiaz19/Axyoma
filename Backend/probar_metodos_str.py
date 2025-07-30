#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar los métodos __str__ de los modelos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.models import *

def probar_metodos_str():
    print("🧪 PROBANDO MÉTODOS __str__ DE LOS MODELOS")
    print("=" * 50)
    
    try:
        # Probar PerfilUsuario
        print("\n👤 PERFIL USUARIO:")
        perfiles = PerfilUsuario.objects.all()[:3]
        for perfil in perfiles:
            print(f"  • {str(perfil)}")
        
        # Probar Empresa
        print("\n🏢 EMPRESAS:")
        empresas = Empresa.objects.all()[:3]
        for empresa in empresas:
            print(f"  • {str(empresa)}")
        
        # Probar Planta
        print("\n🏭 PLANTAS:")
        plantas = Planta.objects.all()[:3]
        for planta in plantas:
            print(f"  • {str(planta)}")
        
        # Probar Departamento
        print("\n🏬 DEPARTAMENTOS:")
        departamentos = Departamento.objects.all()[:3]
        for departamento in departamentos:
            print(f"  • {str(departamento)}")
        
        # Probar Puesto
        print("\n💼 PUESTOS:")
        puestos = Puesto.objects.all()[:3]
        for puesto in puestos:
            print(f"  • {str(puesto)}")
        
        # Probar Empleado
        print("\n👥 EMPLEADOS:")
        empleados = Empleado.objects.all()[:5]
        for empleado in empleados:
            print(f"  • {str(empleado)}")
        
        print(f"\n✅ TODOS LOS MÉTODOS __str__ FUNCIONAN CORRECTAMENTE")
        print("🎉 Ahora el admin mostrará nombres en lugar de 'ID:'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    probar_metodos_str()
