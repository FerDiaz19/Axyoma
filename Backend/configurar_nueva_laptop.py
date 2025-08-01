#!/usr/bin/env python
"""
🚀 CONFIGURADOR AUTOMÁTICO PARA NUEVA LAPTOP
===========================================
Este script configura automáticamente todo el sistema Axyoma
en una nueva instalación para que quede idéntico al sistema original.
"""

import os
import sys
import subprocess
import time

def imprimir_titulo(titulo):
    """Imprimir título con formato"""
    print("\n" + "=" * 60)
    print(f"🎯 {titulo}")
    print("=" * 60)

def imprimir_paso(numero, descripcion):
    """Imprimir paso con formato"""
    print(f"\n📋 PASO {numero}: {descripcion}")
    print("-" * 40)

def ejecutar_comando(comando, descripcion=""):
    """Ejecutar comando y mostrar resultado"""
    if descripcion:
        print(f"⚡ {descripcion}")
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ Comando ejecutado exitosamente")
            if resultado.stdout:
                print(f"📤 Salida: {resultado.stdout[:200]}...")
            return True
        else:
            print(f"❌ Error en comando: {resultado.stderr}")
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def verificar_requisitos():
    """Verificar que estén instalados los requisitos"""
    imprimir_paso(1, "VERIFICANDO REQUISITOS")
    
    requisitos = [
        ("python --version", "Python"),
        ("pg_config --version", "PostgreSQL"),
        ("git --version", "Git")
    ]
    
    todos_ok = True
    for comando, nombre in requisitos:
        print(f"🔍 Verificando {nombre}...")
        if ejecutar_comando(comando, f"Verificar {nombre}"):
            print(f"✅ {nombre} está instalado")
        else:
            print(f"❌ {nombre} NO está instalado o no está en PATH")
            todos_ok = False
    
    return todos_ok

def configurar_entorno():
    """Configurar entorno virtual y dependencias"""
    imprimir_paso(2, "CONFIGURANDO ENTORNO VIRTUAL")
    
    # Crear entorno virtual
    if not os.path.exists('.venv'):
        print("🔧 Creando entorno virtual...")
        if ejecutar_comando("python -m venv .venv", "Crear entorno virtual"):
            print("✅ Entorno virtual creado")
        else:
            print("❌ Error creando entorno virtual")
            return False
    else:
        print("✅ Entorno virtual ya existe")
    
    # Activar entorno e instalar dependencias
    print("📦 Instalando dependencias...")
    if os.name == 'nt':  # Windows
        comando_pip = ".venv\\Scripts\\pip install -r requirements.txt"
    else:  # Linux/Mac
        comando_pip = ".venv/bin/pip install -r requirements.txt"
    
    if ejecutar_comando(comando_pip, "Instalar dependencias"):
        print("✅ Dependencias instaladas")
        return True
    else:
        print("❌ Error instalando dependencias")
        return False

def configurar_base_datos():
    """Configurar base de datos"""
    imprimir_paso(3, "CONFIGURANDO BASE DE DATOS")
    
    print("🔧 Aplicando migraciones...")
    comandos_db = [
        ("python manage.py makemigrations", "Crear migraciones"),
        ("python manage.py migrate", "Aplicar migraciones")
    ]
    
    for comando, descripcion in comandos_db:
        if not ejecutar_comando(comando, descripcion):
            print(f"❌ Error en: {descripcion}")
            return False
    
    print("✅ Base de datos configurada")
    return True

def inicializar_sistema_completo():
    """Ejecutar inicialización completa del sistema"""
    imprimir_paso(4, "INICIALIZANDO SISTEMA COMPLETO")
    
    print("🎯 Ejecutando configuración automática completa...")
    print("⚠️  ATENCIÓN: Esto creará todos los datos del sistema")
    
    if ejecutar_comando("python sistema_completo_listo.py", "Inicializar sistema completo"):
        print("✅ Sistema inicializado con todos los datos")
        return True
    else:
        print("❌ Error en inicialización del sistema")
        return False

def verificar_instalacion():
    """Verificar que la instalación sea correcta"""
    imprimir_paso(5, "VERIFICANDO INSTALACIÓN")
    
    print("🔍 Verificando estado del sistema...")
    if ejecutar_comando("python verificacion_simple.py", "Verificar sistema"):
        print("✅ Verificación completada")
        return True
    else:
        print("⚠️ Problemas en verificación")
        return False

def mostrar_resultado_final():
    """Mostrar resultado final de la configuración"""
    imprimir_titulo("CONFIGURACIÓN COMPLETADA")
    
    print("🎉 ¡SISTEMA AXYOMA CONFIGURADO EXITOSAMENTE!")
    print()
    print("📊 TU SISTEMA INCLUYE:")
    print("  🏢 2 empresas completamente configuradas")
    print("  👥 41 empleados distribuidos en la estructura")
    print("  🏭 4 plantas operativas")
    print("  📋 14 departamentos activos")
    print("  💼 28 puestos definidos")
    print("  💳 Suscripciones y pagos configurados")
    print()
    print("🔑 CREDENCIALES DE ACCESO:")
    print("  👤 Usuario: superadmin")
    print("  🔒 Contraseña: admin123")
    print()
    print("🌐 PARA ACCEDER AL SISTEMA:")
    print("  1. Ejecutar: python manage.py runserver")
    print("  2. Abrir: http://localhost:8000")
    print("  3. Login con las credenciales de arriba")
    print()
    print("🔧 COMANDOS ÚTILES:")
    print("  📊 python verificacion_simple.py - Ver resumen del sistema")
    print("  🔍 python verificar_estado_bd.py - Verificar base de datos")
    print("  💾 python sistema_respaldos.py - Sistema de respaldos")
    print()
    print("=" * 60)

def main():
    """Función principal del configurador"""
    imprimir_titulo("CONFIGURADOR AUTOMÁTICO AXYOMA")
    print("Este script configurará automáticamente todo el sistema Axyoma")
    print("para que funcione exactamente igual que en la laptop original.")
    print()
    
    respuesta = input("¿Deseas continuar? (s/n): ").lower().strip()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Configuración cancelada")
        return
    
    # Ejecutar pasos de configuración
    pasos = [
        verificar_requisitos,
        configurar_entorno,
        configurar_base_datos,
        inicializar_sistema_completo,
        verificar_instalacion
    ]
    
    for i, paso in enumerate(pasos, 1):
        try:
            if not paso():
                print(f"\n❌ Error en paso {i}. Configuración detenida.")
                print("💡 Revisa los errores arriba y vuelve a intentar.")
                return
        except Exception as e:
            print(f"\n❌ Excepción en paso {i}: {e}")
            return
        
        time.sleep(1)  # Pausa breve entre pasos
    
    # Mostrar resultado final
    mostrar_resultado_final()

if __name__ == "__main__":
    main()
