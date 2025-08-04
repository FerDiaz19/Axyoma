#!/usr/bin/env python
"""
🧪 SCRIPT DE PRUEBAS PARA BACKUP OPTIMIZADO
=========================================

Script para probar todas las optimizaciones implementadas en el sistema de backup.
Verifica que funcionen correctamente los nuevos endpoints y configuraciones.
"""

import requests
import json
import time
from datetime import datetime

# Configuración del servidor de prueba
BASE_URL = "http://localhost:8000/api/admin-bd"
USERNAME = "superadmin"  # Cambiar por tu usuario SuperAdmin
PASSWORD = "tu_password"  # Cambiar por tu contraseña

class BackupTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        
    def login(self):
        """Hacer login y obtener token"""
        login_data = {
            "username": USERNAME,
            "password": PASSWORD
        }
        
        response = self.session.post(f"{BASE_URL.replace('/admin-bd', '')}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            self.token = response.json().get('token')
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            print("✅ Login exitoso")
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            return False
    
    def test_monitoreo_sistema(self):
        """Probar endpoint de monitoreo"""
        print("\n🔍 PROBANDO: Monitoreo del sistema...")
        
        response = self.session.get(f"{BASE_URL}/respaldos/monitorear/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Monitoreo funcionando correctamente")
            print(f"   📊 Tamaño BD: {data['analisis_bd_actual']['size_pretty']}")
            print(f"   ⚡ Jobs recomendados: {data['recomendaciones']['jobs_recomendados']}")
            print(f"   ⏰ Timeout recomendado: {data['recomendaciones']['timeout_recomendado']}")
            return True
        else:
            print(f"❌ Error en monitoreo: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    
    def test_backup_optimizado(self):
        """Probar backup completo optimizado"""
        print("\n🚀 PROBANDO: Backup completo optimizado...")
        
        backup_data = {
            "incluir_datos": True,
            "descripcion": "Prueba de backup optimizado - Test automatizado"
        }
        
        print("   ⏳ Iniciando backup...")
        start_time = datetime.now()
        
        response = self.session.post(f"{BASE_URL}/respaldos/bd-completa/", json=backup_data)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backup optimizado completado exitosamente")
            print(f"   ⏱️ Tiempo total: {duration}")
            print(f"   📁 Archivo: {data['archivo']}")
            print(f"   📊 Tamaño: {data['tamaño_mb']} MB")
            print(f"   ⚡ Jobs usados: {data['rendimiento']['jobs_paralelos_usados']}")
            print(f"   🛠️ Optimizaciones: {data['rendimiento']['optimizaciones_aplicadas']}")
            return True
        else:
            print(f"❌ Error en backup optimizado: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    
    def test_backup_emergencia(self):
        """Probar backup de emergencia"""
        print("\n🚨 PROBANDO: Backup de emergencia...")
        
        print("   ⏳ Iniciando backup de emergencia...")
        start_time = datetime.now()
        
        response = self.session.post(f"{BASE_URL}/respaldos/emergencia/")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backup de emergencia completado")
            print(f"   ⏱️ Tiempo: {duration}")
            print(f"   📁 Archivo: {data['archivo']}")
            print(f"   📊 Tamaño: {data['tamaño_mb']} MB")
            print(f"   🚨 Tipo: {data['tipo']}")
            print(f"   ⚡ Optimizaciones: {data['optimizaciones']}")
            return True
        else:
            print(f"❌ Error en backup de emergencia: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    
    def test_listar_backups(self):
        """Probar listado de backups"""
        print("\n📋 PROBANDO: Listado de backups...")
        
        response = self.session.get(f"{BASE_URL}/respaldos/listar/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Listado de backups funcionando")
            print(f"   📁 Total de archivos: {len(data['archivos'])}")
            if data['archivos']:
                ultimo = data['archivos'][0]
                print(f"   📄 Último backup: {ultimo['nombre']}")
                print(f"   📊 Tamaño: {ultimo['tamaño_mb']} MB")
            return True
        else:
            print(f"❌ Error en listado: {response.status_code}")
            return False
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE BACKUP OPTIMIZADO")
        print("=" * 60)
        
        if not self.login():
            print("❌ No se pudo hacer login. Verificar credenciales.")
            return False
        
        tests = [
            ("Monitoreo del Sistema", self.test_monitoreo_sistema),
            ("Listado de Backups", self.test_listar_backups), 
            ("Backup de Emergencia", self.test_backup_emergencia),
            ("Backup Completo Optimizado", self.test_backup_optimizado),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ Error en {test_name}: {str(e)}")
                results[test_name] = False
        
        # Reporte final
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE PRUEBAS")
        print("=" * 60)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
        
        if passed == total:
            print("🎉 ¡TODAS LAS OPTIMIZACIONES FUNCIONAN CORRECTAMENTE!")
        else:
            print("⚠️ Algunas pruebas fallaron. Revisar configuración.")
        
        return passed == total

if __name__ == "__main__":
    print("🚀 SISTEMA DE BACKUP OPTIMIZADO - PRUEBAS AUTOMATIZADAS")
    print("⚠️ IMPORTANTE: Asegúrate de que el servidor Django esté ejecutándose")
    print("⚠️ CREDENCIALES: Actualiza USERNAME y PASSWORD en este script")
    print()
    
    input("Presiona ENTER para continuar...")
    
    tester = BackupTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ El sistema de backup optimizado está funcionando perfectamente.")
    else:
        print("\n❌ Hay problemas con el sistema. Revisar logs del servidor.")
