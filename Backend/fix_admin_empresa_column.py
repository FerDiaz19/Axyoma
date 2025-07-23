#!/usr/bin/env python
"""
Script para corregir el problema de la columna admin_empresa_id vs admin_empresa
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

def verificar_columna():
    """Verificar si existe el problema de la columna admin_empresa_id"""
    print("🔍 Verificando estructura de la tabla usuarios...")
    
    try:
        with connection.cursor() as cursor:
            # Obtener columnas de la tabla usuarios
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios'
            """)
            columnas = [col[0] for col in cursor.fetchall()]
            print(f"📋 Columnas encontradas: {', '.join(columnas)}")
            
            # Verificar si existe admin_empresa o admin_empresa_id
            tiene_admin_empresa = 'admin_empresa' in columnas
            tiene_admin_empresa_id = 'admin_empresa_id' in columnas
            
            if tiene_admin_empresa and not tiene_admin_empresa_id:
                print("✅ La tabla tiene la columna 'admin_empresa' (correcto)")
                return True
            elif tiene_admin_empresa_id and not tiene_admin_empresa:
                print("❌ La tabla tiene la columna 'admin_empresa_id' en lugar de 'admin_empresa'")
                return False
            elif tiene_admin_empresa and tiene_admin_empresa_id:
                print("⚠️ La tabla tiene ambas columnas: 'admin_empresa' y 'admin_empresa_id'")
                return True
            else:
                print("⚠️ La tabla no tiene ninguna de las columnas 'admin_empresa' o 'admin_empresa_id'")
                return None
    except Exception as e:
        print(f"❌ Error verificando columnas: {str(e)}")
        return None

def corregir_modelos():
    """Instrucciones para corregir los modelos de Django"""
    print("\n📝 INSTRUCCIONES PARA CORREGIR EL PROBLEMA:")
    print("1. Edite el archivo: apps/users/models.py")
    print("2. En la clase PerfilUsuario, modifique la definición del campo admin_empresa:")
    print("   admin_empresa = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='admin_empresa')")
    print("3. Reinicie el servidor Django")

def main():
    print("\n🚀 DIAGNÓSTICO DE COLUMNA ADMIN_EMPRESA")
    print("=" * 60)
    
    resultado = verificar_columna()
    
    if resultado is None:
        print("\n❓ No se pudo determinar la estructura de la columna.")
    elif resultado:
        print("\n✅ La estructura de la columna es correcta.")
        print("Si sigues teniendo problemas, verifica que el modelo en Django esté definido correctamente.")
    else:
        print("\n❌ Se detectó un problema con la columna admin_empresa_id.")
        corregir_modelos()
    
    print("\n🏁 DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    main()
