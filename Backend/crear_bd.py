#!/usr/bin/env python
"""
🏗️ CREADOR DE BASE DE DATOS AXYOMA
===============================
Script auxiliar para crear la BD cuando psql falla
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def crear_bd():
    """Crear base de datos axyomadb"""
    print("🏗️ CREANDO BASE DE DATOS AXYOMADB...")
    
    # Intentar diferentes configuraciones
    configuraciones = [
        {'password': ''},
        {'password': 'postgres'},
        {'password': 'admin'},
        {'password': '123456'},
    ]
    
    for config in configuraciones:
        try:
            print(f"🔗 Intentando conexión...")
            conn = psycopg2.connect(
                host='localhost',
                user='postgres', 
                password=config['password'],
                dbname='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            cur = conn.cursor()
            
            # Eliminar BD si existe
            print("🗑️ Eliminando BD anterior si existe...")
            cur.execute("DROP DATABASE IF EXISTS axyomadb")
            
            # Crear nueva BD
            print("🏗️ Creando nueva base de datos...")
            cur.execute("CREATE DATABASE axyomadb")
            
            cur.close()
            conn.close()
            
            print("✅ Base de datos 'axyomadb' creada exitosamente")
            return True
            
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e) or "no password supplied" in str(e):
                continue  # Probar siguiente configuración
            else:
                print(f"❌ Error de conexión: {e}")
                break
                
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            break
    
    # Si llegamos aquí, ninguna configuración funcionó
    print("❌ No se pudo conectar con configuraciones comunes")
    print("💡 SOLUCIÓN MANUAL:")
    print("   1. Abre pgAdmin")
    print("   2. Conecta con tu usuario y password")
    print("   3. Crea base de datos 'axyomadb'")
    print("   4. Presiona Enter para continuar...")
    input()
    return False

if __name__ == "__main__":
    crear_bd()
