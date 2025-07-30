#!/usr/bin/env python
"""
Script MAESTRO para inicializar completamente el sistema AXYOMA
Este script ejecuta todo el proceso: usuarios, empresa y datos de prueba
"""

import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def ejecutar_script(script_name, descripcion):
    """Ejecutar un script de Python y manejar errores"""
    print(f"\n🔄 {descripcion}")
    print("-" * 50)
    
    try:
        # Ejecutar el script en el mismo entorno Python
        resultado = subprocess.run([sys.executable, script_name], 
                                 capture_output=True, text=True, encoding='utf-8')
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - COMPLETADO")
            # Mostrar output importante
            lines = resultado.stdout.split('\n')
            for line in lines:
                if any(word in line for word in ['✅', '⚠️', '🎯', 'Credenciales', 'RESUMEN']):
                    print(f"   {line}")
        else:
            print(f"❌ {descripcion} - ERROR")
            print(f"   Error: {resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False
    
    return True

def inicializar_sistema_completo():
    """Ejecutar todo el proceso de inicialización"""
    print("🚀 INICIALIZACIÓN COMPLETA DEL SISTEMA AXYOMA")
    print("=" * 70)
    print("Este proceso creará:")
    print("  👤 Usuario superadmin")
    print("  👥 Usuarios de prueba (admin empresa, admin planta)")
    print("  🏢 Empresa completa con estructura organizacional")
    print("  🏭 3 Plantas")
    print("  📋 21 Departamentos")
    print("  💼 81 Puestos de trabajo")
    print("  👨‍💼 138+ Empleados distribuidos realísticamente")
    print("=" * 70)
    
    respuesta = input("¿Deseas continuar con la inicialización completa? (s/n): ")
    if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return False
    
    # Lista de scripts a ejecutar en orden
    scripts = [
        ("crear_superadmin.py", "Creando usuario superadmin"),
        ("crear_usuarios_prueba.py", "Creando usuarios de prueba"),
        ("crear_datos_completos.py", "Creando estructura completa de empresa")
    ]
    
    print(f"\n🎯 EJECUTANDO {len(scripts)} PROCESOS...")
    
    # Ejecutar cada script
    for script, descripcion in scripts:
        if not ejecutar_script(script, descripcion):
            print(f"\n❌ PROCESO INTERRUMPIDO en: {descripcion}")
            return False
    
    # Resumen final
    print(f"\n🎉 ¡INICIALIZACIÓN COMPLETA EXITOSA!")
    print("=" * 70)
    print("🔑 CREDENCIALES DE ACCESO:")
    print("   👑 SuperAdmin:    superadmin / 1234")
    print("   🏢 Admin Empresa: admin_empresa / admin123")
    print("   🏭 Admin Planta:  admin_planta / admin123")
    print("")
    print("🏢 ESTRUCTURA CREADA:")
    print("   🏢 Empresa: TechnoMex Industries")
    print("   🏭 Plantas: 3 (Querétaro Centro, El Marqués, San Juan del Río)")
    print("   📋 Departamentos: 21 (7 por planta)")
    print("   💼 Puestos: 81+ (distribuidos por departamento)")
    print("   👥 Empleados: 138+ (todos enlazados correctamente)")
    print("")
    print("🌐 ACCESO AL SISTEMA:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000/api/")
    print("   Admin Django: http://localhost:8000/admin/")
    print("=" * 70)
    
    return True

def main():
    """Función principal"""
    try:
        inicializar_sistema_completo()
    except KeyboardInterrupt:
        print("\n❌ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
