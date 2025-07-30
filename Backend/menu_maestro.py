#!/usr/bin/env python
"""
MENÚ MAESTRO DEL SISTEMA AXYOMA
Gestión completa de base de datos, respaldos y exportaciones
"""

import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def ejecutar_script(script_name):
    """Ejecutar un script de Python"""
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
    except FileNotFoundError:
        print(f"❌ Script no encontrado: {script_name}")

def mostrar_banner():
    """Mostrar banner del sistema"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    SISTEMA AXYOMA                           ║")
    print("║              GESTIÓN DE BASE DE DATOS                       ║")
    print("║                                                              ║")
    print("║  🏢 Gestión Empresarial  📊 Respaldos  📋 Exportaciones    ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def mostrar_estado_sistema():
    """Mostrar estado actual del sistema"""
    try:
        from apps.users.models import Empleado, Empresa, Planta, Departamento, Puesto
        
        total_empresas = Empresa.objects.count()
        total_plantas = Planta.objects.count()
        total_departamentos = Departamento.objects.count()
        total_puestos = Puesto.objects.count()
        total_empleados = Empleado.objects.count()
        
        print("\n📊 ESTADO ACTUAL DEL SISTEMA:")
        print("=" * 40)
        print(f"🏢 Empresas:     {total_empresas}")
        print(f"🏭 Plantas:      {total_plantas}")
        print(f"📋 Departamentos: {total_departamentos}")
        print(f"💼 Puestos:      {total_puestos}")
        print(f"👥 Empleados:    {total_empleados}")
        
        if total_empleados > 0:
            print("✅ Sistema con datos")
        else:
            print("⚠️ Sistema sin datos - Considera ejecutar inicialización")
            
    except Exception as e:
        print(f"⚠️ Error verificando estado: {e}")

def menu_principal():
    """Menú principal del sistema"""
    while True:
        mostrar_banner()
        mostrar_estado_sistema()
        
        print("\n🔧 OPCIONES PRINCIPALES:")
        print("=" * 40)
        print("1.  🚀 Inicializar sistema completo (usuarios + datos)")
        print("2.  🧹 Resetear base de datos (PELIGRO: borra todo)")
        print("3.  👤 Crear/corregir superadmin")
        print("4.  👥 Crear usuarios de prueba")
        print("5.  🏢 Crear datos de empresa completos")
        print("")
        print("6.  💾 Sistema de respaldos")
        print("7.  📊 Exportar datos a CSV")
        print("8.  🔄 Restaurar respaldo")
        print("")
        print("9.  📋 Verificar enlaces de empleados")
        print("10. 🔍 Estado detallado del sistema")
        print("11. 🌐 Abrir documentación")
        print("12. 🚪 Salir")
        print("=" * 40)
        
        opcion = input("Selecciona una opción (1-12): ").strip()
        
        if opcion == '1':
            print("\n🚀 INICIALIZANDO SISTEMA COMPLETO...")
            ejecutar_script("inicializar_sistema_completo.py")
            
        elif opcion == '2':
            print("\n⚠️ RESETEO COMPLETO DE BASE DE DATOS")
            ejecutar_script("resetear_bd_completo.py")
            
        elif opcion == '3':
            print("\n👤 CREANDO/CORRIGIENDO SUPERADMIN...")
            ejecutar_script("crear_superadmin.py")
            
        elif opcion == '4':
            print("\n👥 CREANDO USUARIOS DE PRUEBA...")
            ejecutar_script("crear_usuarios_prueba.py")
            
        elif opcion == '5':
            print("\n🏢 CREANDO DATOS DE EMPRESA...")
            ejecutar_script("crear_datos_completos.py")
            
        elif opcion == '6':
            print("\n💾 SISTEMA DE RESPALDOS...")
            ejecutar_script("sistema_respaldos.py")
            
        elif opcion == '7':
            print("\n📊 EXPORTAR DATOS A CSV...")
            ejecutar_script("exportar_csv.py")
            
        elif opcion == '8':
            print("\n🔄 RESTAURAR RESPALDO...")
            mostrar_info_restauracion()
            
        elif opcion == '9':
            print("\n📋 VERIFICANDO ENLACES...")
            ejecutar_script("verificar_enlaces_empleados.py")
            
        elif opcion == '10':
            mostrar_estado_detallado()
            
        elif opcion == '11':
            mostrar_documentacion()
            
        elif opcion == '12':
            print("\n👋 ¡Gracias por usar AXYOMA!")
            print("🚀 Sistema de gestión empresarial")
            break
            
        else:
            print("❌ Opción inválida. Selecciona un número del 1 al 12.")
        
        input("\n⏎ Presiona ENTER para continuar...")

def mostrar_info_restauracion():
    """Mostrar información sobre restauración"""
    print("🔄 RESTAURACIÓN DE RESPALDOS")
    print("=" * 50)
    print("Para restaurar un respaldo:")
    print("")
    print("1. 📁 Ubicar archivo .sql en directorio backups/")
    print("2. 🔧 Usar comando psql:")
    print("   psql -U postgres -d axyoma_bd < archivo_respaldo.sql")
    print("")
    print("3. 🌐 O usar herramientas gráficas como pgAdmin")
    print("")
    print("⚠️ IMPORTANTE: La restauración sobrescribirá datos existentes")

def mostrar_estado_detallado():
    """Mostrar estado detallado del sistema"""
    try:
        from apps.users.models import Empleado, Empresa, Planta, Departamento, Puesto
        from django.contrib.auth.models import User
        
        print("\n📊 ESTADO DETALLADO DEL SISTEMA")
        print("=" * 60)
        
        # Usuarios del sistema
        total_usuarios = User.objects.count()
        usuarios_activos = User.objects.filter(is_active=True).count()
        print(f"👤 Usuarios totales: {total_usuarios}")
        print(f"✅ Usuarios activos: {usuarios_activos}")
        
        # Estructura organizacional
        empresas = Empresa.objects.all()
        print(f"\n🏢 EMPRESAS ({len(empresas)}):")
        for empresa in empresas:
            plantas = Planta.objects.filter(empresa=empresa).count()
            empleados = Empleado.objects.filter(
                puesto__departamento__planta__empresa=empresa
            ).count()
            print(f"   • {empresa.nombre}: {plantas} plantas, {empleados} empleados")
        
        # Plantas
        plantas = Planta.objects.all()
        print(f"\n🏭 PLANTAS ({len(plantas)}):")
        for planta in plantas:
            departamentos = Departamento.objects.filter(planta=planta).count()
            empleados = Empleado.objects.filter(
                puesto__departamento__planta=planta
            ).count()
            print(f"   • {planta.nombre}: {departamentos} depts, {empleados} empleados")
        
    except Exception as e:
        print(f"❌ Error obteniendo estado detallado: {e}")

def mostrar_documentacion():
    """Mostrar documentación del sistema"""
    print("\n📚 DOCUMENTACIÓN DEL SISTEMA AXYOMA")
    print("=" * 60)
    print("🔗 Enlaces importantes:")
    print("   • Frontend: http://localhost:3000")
    print("   • Backend API: http://localhost:8000/api/")
    print("   • Admin Django: http://localhost:8000/admin/")
    print("")
    print("🔑 Credenciales por defecto:")
    print("   • SuperAdmin: superadmin / 1234")
    print("   • Admin Empresa: admin_empresa / admin123")
    print("   • Admin Planta: admin_planta / admin123")
    print("")
    print("📁 Archivos importantes:")
    print("   • Respaldos: ../backups/")
    print("   • Exportaciones CSV: ./export_*.csv")
    print("   • Logs: ../logs/")
    print("")
    print("🛠️ Scripts disponibles:")
    print("   • inicializar_sistema_completo.py")
    print("   • resetear_bd_completo.py")
    print("   • sistema_respaldos.py")
    print("   • exportar_csv.py")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
