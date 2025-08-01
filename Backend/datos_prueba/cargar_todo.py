#!/usr/bin/env python
"""
🎯 CARGADOR MAESTRO DE DATOS DE PRUEBA
===================================
Script que ejecuta todos los cargadores en secuencia
"""

import os
import sys
import subprocess

def ejecutar_script(nombre_script):
    """Ejecuta un script de Python"""
    print(f"\n🚀 Ejecutando {nombre_script}...")
    print("-" * 50)
    
    try:
        # Ejecutar script
        resultado = subprocess.run(
            [sys.executable, nombre_script],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )
        
        if resultado.returncode == 0:
            print(f"✅ {nombre_script} completado exitosamente")
            return True
        else:
            print(f"❌ {nombre_script} falló con código {resultado.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {nombre_script}: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 CARGADOR MAESTRO DE DATOS DE PRUEBA")
    print("=" * 60)
    print("Este script ejecuta todos los cargadores en secuencia:")
    print("1. Datos organizacionales completos")
    print("2. Evaluaciones NOM-035")
    print()
    
    respuesta = input("¿Continuar con la carga completa? (s/n): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    scripts = [
        "cargar_datos_completos.py",
        "cargar_evaluaciones_nom035.py"
    ]
    
    resultados = []
    
    for script in scripts:
        if os.path.exists(script):
            resultado = ejecutar_script(script)
            resultados.append((script, resultado))
        else:
            print(f"⚠️  Script {script} no encontrado")
            resultados.append((script, False))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for script, resultado in resultados:
        if resultado:
            print(f"✅ {script}")
            exitosos += 1
        else:
            print(f"❌ {script}")
            fallidos += 1
    
    print("-" * 60)
    print(f"🎯 Scripts exitosos: {exitosos}")
    print(f"❌ Scripts fallidos: {fallidos}")
    print("=" * 60)
    
    if fallidos == 0:
        print("🎉 ¡TODOS LOS DATOS CARGADOS EXITOSAMENTE!")
    else:
        print("⚠️  Algunos scripts fallaron. Revisa los errores arriba.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
