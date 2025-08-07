#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def verificar_estructura_tabla():
    """Verificar la estructura de la tabla suscripciones"""
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLA SUSCRIPCIONES")
    print("=" * 60)
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Obtener información de las columnas
            cursor.execute("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'suscripciones'
                ORDER BY ordinal_position;
            """)
            
            print("📋 Estructura de la tabla 'suscripciones':")
            print("-" * 60)
            print("COLUMNA".ljust(20), "TIPO".ljust(15), "NULO".ljust(8), "DEFAULT")
            print("-" * 60)
            
            for row in cursor.fetchall():
                column_name, data_type, is_nullable, column_default = row
                nullable_str = "SI" if is_nullable == "YES" else "NO"
                default_str = str(column_default) if column_default else "-"
                print(column_name.ljust(20), data_type.ljust(15), nullable_str.ljust(8), default_str)
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_estructura_tabla()
