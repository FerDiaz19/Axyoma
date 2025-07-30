#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar las nuevas funciones del SuperAdmin
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def probar_nuevas_funciones():
    print("🧪 PROBANDO NUEVAS FUNCIONES SUPERADMIN")
    print("=" * 50)
    
    print("\n📋 FUNCIONES AGREGADAS:")
    print("1. 🗄️ Respaldo Limpio pgAdmin")
    print("   • Endpoint: /api/admin-bd/respaldos/pgadmin/")
    print("   • Genera respaldo compatible con pgAdmin 4")
    print("   • Formato: SQL estándar PostgreSQL")
    
    print("\n2. 🗑️ Resetear BD Completa")
    print("   • Endpoint: /api/admin-bd/sistema/resetear-bd/")
    print("   • PELIGROSO: Elimina todos los datos")
    print("   • Requiere confirmación: 'CONFIRMO_RESETEAR_BD'")
    
    print("\n3. 📊 Cargar Datos Iniciales")
    print("   • Endpoint: /api/admin-bd/sistema/datos-iniciales/")
    print("   • Crea empresa demo con estructura completa")
    print("   • Usuarios: superadmin, admin_empresa, admin_planta")
    
    print("\n🎯 CÓMO USAR:")
    print("1. Inicia el servidor Django:")
    print("   python manage.py runserver")
    
    print("\n2. Accede al SuperAdmin:")
    print("   http://127.0.0.1:8000/admin/")
    print("   Usuario: superadmin")
    print("   Password: 1234")
    
    print("\n3. Ve a 'Gestión de Base de Datos'")
    print("   • Pestaña 'Respaldos'")
    print("   • Verás los nuevos botones:")
    print("     🗄️ Respaldo pgAdmin")
    print("     📊 Datos Iniciales") 
    print("     🗑️ Resetear BD")
    
    print("\n🔗 ENDPOINTS PARA PRUEBAS:")
    print("POST /api/admin-bd/respaldos/pgadmin/")
    print("POST /api/admin-bd/sistema/resetear-bd/")
    print("POST /api/admin-bd/sistema/datos-iniciales/")
    
    print("\n⚠️ IMPORTANTE:")
    print("✅ Solo funciona con usuario SuperAdmin")
    print("✅ Respaldo pgAdmin es compatible con restauración")
    print("❌ Resetear BD elimina TODO - usar con cuidado")
    print("📊 Datos iniciales son seguros de usar")
    
    print("\n🎉 ¡NUEVAS FUNCIONES LISTAS!")

if __name__ == '__main__':
    probar_nuevas_funciones()
