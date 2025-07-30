#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUÍA COMPLETA: CÓMO USAR EL RESPALDO EN PGADMIN
"""
import os

def guia_respaldo_pgadmin():
    print("🎯 GUÍA COMPLETA: USAR RESPALDO EN PGADMIN")
    print("=" * 50)
    
    # Buscar el archivo más reciente
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith('respaldo_limpio_') and f.endswith('.sql')]
    backup_files.sort(reverse=True)
    latest_backup = backup_files[0] if backup_files else None
    
    if not latest_backup:
        print("❌ No se encontró archivo de respaldo")
        return
    
    backup_path = os.path.join(backup_dir, latest_backup)
    backup_path = os.path.abspath(backup_path)
    
    print(f"📁 ARCHIVO DE RESPALDO:")
    print(f"   {backup_path}")
    
    file_size = os.path.getsize(backup_path)
    print(f"💾 Tamaño: {file_size / 1024 / 1024:.2f} MB")
    
    print(f"\n🎯 MÉTODO 1: USAR EN PGADMIN (RECOMENDADO)")
    print("=" * 50)
    print("1. 🖥️ Abre pgAdmin 4")
    print("2. 🌐 Conéctate a tu servidor PostgreSQL")
    print("3. 📊 Click derecho en 'Databases'")
    print("4. ➕ Selecciona 'Create' > 'Database...'")
    print("5. 📝 Nombre: 'axyomadb_test' (para probar)")
    print("6. ✅ Click 'Save'")
    print("7. 🔄 Click derecho en la nueva base de datos")
    print("8. 📥 Selecciona 'Restore...'")
    print("9. 📁 En 'Filename': Busca y selecciona:")
    print(f"     {backup_path}")
    print("10. ⚙️ En 'Format': Selecciona 'Plain'")
    print("11. 🧹 Marca 'Clean before restore'")
    print("12. ▶️ Click 'Restore'")
    
    print(f"\n⚡ MÉTODO 2: LÍNEA DE COMANDOS (ALTERNATIVO)")
    print("=" * 50)
    print("Si pgAdmin falla, usa este comando en PowerShell:")
    print(f'psql -U postgres -h localhost -f "{backup_path}"')
    
    print(f"\n🔧 MÉTODO 3: CREAR NUEVA BD DESDE CERO")
    print("=" * 50)
    print("1. 🗑️ Elimina la base de datos actual (si quieres)")
    print("2. ➕ Crea nueva base de datos llamada 'axyomadb'")
    print("3. 📥 Restaura usando el archivo de respaldo")
    
    print(f"\n📊 CONTENIDO DEL RESPALDO:")
    print("✅ Estructura completa de todas las tablas")
    print("✅ Datos de empresas, plantas, departamentos")
    print("✅ Datos de puestos y empleados") 
    print("✅ Usuarios y perfiles")
    print("✅ Configuración de Django")
    print("✅ Tokens de autenticación")
    
    print(f"\n⚠️ NOTAS IMPORTANTES:")
    print("🔸 El respaldo incluye comandos DROP/CREATE")
    print("🔸 Compatible con PostgreSQL 12+")
    print("🔸 Encoding UTF-8")
    print("🔸 Formato SQL estándar")
    
    print(f"\n🆘 SI TIENES PROBLEMAS:")
    print("❓ Error de permisos: Ejecuta pgAdmin como administrador")
    print("❓ Error de encoding: Asegúrate que la BD use UTF-8")
    print("❓ Error de conexión: Verifica que PostgreSQL esté corriendo")
    print("❓ Archivo no encontrado: Copia la ruta completa del archivo")
    
    print(f"\n✅ RESULTADO ESPERADO:")
    print("Después del restore, tu base de datos tendrá:")
    print("🏢 Empresas: Datos de prueba")
    print("🏭 Plantas: Asociadas a empresas")
    print("🏢 Departamentos: Por planta")
    print("💼 Puestos: Por departamento")
    print("👤 Empleados: Asignados a puestos")
    print("👥 Usuarios: Para login")
    
    print(f"\n🎉 ¡LISTO PARA USAR!")

if __name__ == '__main__':
    guia_respaldo_pgadmin()
