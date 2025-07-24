#!/usr/bin/env python
"""
Script para crear la base de datos PostgreSQL para Axyoma
"""

import sys
import os
import subprocess

def create_database():
    """Crear base de datos PostgreSQL"""
    print("Creando base de datos PostgreSQL 'axyomadb'...")
    
    # Parámetros de conexión
    db_name = "axyomadb"
    db_user = "postgres"
    db_password = "12345678"
    db_host = "localhost"
    db_port = "5432"
    
    # Comando para verificar si la base de datos ya existe
    check_db_cmd = f'psql -U {db_user} -h {db_host} -p {db_port} -t -c "SELECT 1 FROM pg_database WHERE datname=\'{db_name}\'"'
    
    # Comando para crear la base de datos
    create_db_cmd = f'psql -U {db_user} -h {db_host} -p {db_port} -c "CREATE DATABASE {db_name} ENCODING \'UTF8\' LC_COLLATE \'Spanish_Spain.1252\' LC_CTYPE \'Spanish_Spain.1252\' TEMPLATE template0;"'
    
    # Comando para establecer contraseña mediante variable de entorno
    os.environ['PGPASSWORD'] = db_password
    
    try:
        # Verificar si la base de datos ya existe
        result = subprocess.run(check_db_cmd, shell=True, capture_output=True, text=True)
        if '1' in result.stdout.strip():
            print(f"Base de datos '{db_name}' ya existe.")
            return True
        
        # Crear la base de datos
        result = subprocess.run(create_db_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error al crear la base de datos: {result.stderr}")
            return False
        
        print(f"Base de datos '{db_name}' creada exitosamente.")
        return True
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return False
    finally:
        # Limpiar variable de entorno por seguridad
        if 'PGPASSWORD' in os.environ:
            del os.environ['PGPASSWORD']

if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
