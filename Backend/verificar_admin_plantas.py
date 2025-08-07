#!/usr/bin/env python3
"""
Script para verificar la estructura del modelo AdminPlanta vs BD
"""
import os
import sys
import django
from django.db import connection

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import AdminPlanta

def verificar_tabla_admin_plantas():
    """Verificar estructura de la tabla admin_plantas"""
    
    print("🔍 Verificando estructura de tabla admin_plantas...")
    
    with connection.cursor() as cursor:
        # Obtener información de columnas
        cursor.execute("""
            SELECT column_name, is_nullable, data_type, column_default
            FROM information_schema.columns 
            WHERE table_name = 'admin_plantas'
            ORDER BY ordinal_position;
        """)
        
        columnas = cursor.fetchall()
        
        print("📊 Columnas en la base de datos:")
        for col in columnas:
            nombre, nullable, tipo, default = col
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            default_str = f" DEFAULT {default}" if default else ""
            print(f"   • {nombre}: {tipo} {nullable_str}{default_str}")
        
        # Verificar si existe fecha_asignacion
        fecha_asignacion_exists = any(col[0] == 'fecha_asignacion' for col in columnas)
        
        if fecha_asignacion_exists:
            print("\n⚠️ La tabla tiene campo 'fecha_asignacion' que NO está en el modelo Django")
            
            # Verificar si es NOT NULL
            fecha_col = next(col for col in columnas if col[0] == 'fecha_asignacion')
            if fecha_col[1] == 'NO':  # is_nullable = 'NO'
                print("❌ PROBLEMA: 'fecha_asignacion' es NOT NULL pero no se está asignando")
                print("✅ SOLUCIÓN: Agregar fecha_asignacion al modelo o al crear AdminPlanta")
        else:
            print("✅ No existe campo 'fecha_asignacion' en la BD")

if __name__ == "__main__":
    verificar_tabla_admin_plantas()
