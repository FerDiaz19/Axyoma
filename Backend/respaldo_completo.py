#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

def crear_respaldo_completo():
    """Crea un respaldo completo de la base de datos Axyoma"""
    
    # Configuración de conexión
    host = "localhost"
    port = "5432"
    database = "axyoma"
    username = "postgres"
    password = "12345678"
    
    # Nombre del archivo de respaldo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"respaldo_axyoma_completo_{timestamp}.sql"
    backup_path = os.path.join(os.getcwd(), backup_file)
    
    print(f"🔄 CREANDO RESPALDO COMPLETO DE LA BASE DE DATOS")
    print("=" * 55)
    print(f"📁 Archivo: {backup_file}")
    print(f"📍 Ubicación: {backup_path}")
    
    try:
        # Comando pg_dump
        cmd = [
            "pg_dump",
            "--host", host,
            "--port", port,
            "--username", username,
            "--dbname", database,
            "--verbose",
            "--clean",
            "--create",
            "--format", "plain",
            "--file", backup_path
        ]
        
        # Configurar variable de entorno para la contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        print("🚀 Ejecutando pg_dump...")
        
        # Ejecutar el comando
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Verificar que el archivo se creó
            if os.path.exists(backup_path):
                file_size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
                print(f"✅ ¡RESPALDO CREADO EXITOSAMENTE!")
                print(f"📊 Tamaño: {file_size:.2f} MB")
                print(f"📁 Archivo: {backup_file}")
                
                # Mostrar contenido resumido
                print("\n📋 CONTENIDO DEL RESPALDO:")
                print("   ✅ Todas las tablas del sistema")
                print("   ✅ Usuarios y perfiles")
                print("   ✅ Empresas y estructura organizacional")
                print("   ✅ Empleados y puestos")
                print("   ✅ Planes y suscripciones")
                print("   ✅ Sistema de evaluaciones (NOM-030/035)")
                print("   ✅ Índices y constraints")
                
                print(f"\n💡 Para restaurar usar:")
                print(f"   psql -h {host} -U {username} -d postgres < {backup_file}")
                
            else:
                print("❌ ERROR: El archivo de respaldo no se creó")
        else:
            print(f"❌ ERROR en pg_dump:")
            print(f"   Salida: {result.stdout}")
            print(f"   Error: {result.stderr}")
            
    except FileNotFoundError:
        print("❌ ERROR: pg_dump no encontrado")
        print("💡 Asegúrate de que PostgreSQL esté instalado y pg_dump esté en el PATH")
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")

def crear_script_restauracion():
    """Crea un script .bat para restaurar fácilmente"""
    
    script_content = '''@echo off
echo 🔄 RESTAURANDO BASE DE DATOS AXYOMA
echo ===================================

set /p backup_file="📁 Nombre del archivo de respaldo (ej: respaldo_axyoma_completo_20250731_143000.sql): "

if not exist "%backup_file%" (
    echo ❌ ERROR: El archivo %backup_file% no existe
    pause
    exit /b 1
)

echo.
echo ⚠️  ADVERTENCIA: Esto borrará la base de datos actual
set /p confirm="¿Continuar? (S/N): "

if /i not "%confirm%"=="S" (
    echo ❌ Operación cancelada
    pause
    exit /b 0
)

echo.
echo 🗑️  Borrando base de datos actual...
set PGPASSWORD=12345678
psql -h localhost -U postgres -d postgres -c "DROP DATABASE IF EXISTS axyoma;"

echo 📂 Restaurando desde %backup_file%...
psql -h localhost -U postgres -d postgres < "%backup_file%"

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ ¡BASE DE DATOS RESTAURADA EXITOSAMENTE!
    echo 🎉 El sistema Axyoma está listo para usar
) else (
    echo.
    echo ❌ ERROR durante la restauración
)

echo.
pause
'''
    
    with open("restaurar_axyoma.bat", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("📝 Script de restauración creado: restaurar_axyoma.bat")

if __name__ == "__main__":
    crear_respaldo_completo()
    print("\n" + "="*55)
    crear_script_restauracion()
    print("\n🎯 SISTEMA LISTO PARA RESPALDOS Y RESTAURACIONES")
