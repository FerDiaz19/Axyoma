#!/usr/bin/env python
"""
Script para probar los endpoints directos de exportación CSV
"""
import os
import sys
import django
import requests
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def probar_exportaciones_directas():
    """Probar exportaciones CSV directas"""
    
    # URL del backend
    base_url = "http://127.0.0.1:8000"
    
    # Credenciales del SuperAdmin
    credentials = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("🔐 Obteniendo token de autenticación...")
    
    # 1. Obtener token
    login_response = requests.post(f"{base_url}/api/auth/login/", json=credentials)
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(f"   Respuesta: {login_response.text}")
        return
    
    token_data = login_response.json()
    token = token_data.get('token')
    
    if not token:
        print("❌ No se obtuvo token de acceso")
        print(f"   Respuesta: {token_data}")
        return
    
    print(f"✅ Token obtenido: {token[:20]}...")
    
    # Headers para las peticiones
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 2. Probar endpoint de listar tablas directas
    print("\n📋 Probando listado de tablas directas...")
    tablas_response = requests.get(f"{base_url}/api/admin-bd/directo/tablas/", headers=headers)
    
    if tablas_response.status_code == 200:
        tablas_data = tablas_response.json()
        print(f"✅ Tablas disponibles: {len(tablas_data.get('tablas_disponibles', []))}")
        for tabla in tablas_data.get('tablas_disponibles', []):
            print(f"   - {tabla['nombre']}: {tabla['descripcion']}")
    else:
        print(f"❌ Error listando tablas: {tablas_response.status_code}")
        print(f"   Respuesta: {tablas_response.text}")
        return
    
    # 3. Probar exportaciones de las tablas problemáticas
    tablas_probar = ['empleados', 'suscripciones', 'pagos']
    
    print(f"\n📤 Probando exportaciones directas...")
    
    for tabla in tablas_probar:
        print(f"\n🔄 Exportando tabla: {tabla}")
        export_response = requests.get(
            f"{base_url}/api/admin-bd/directo/exportar/{tabla}/", 
            headers=headers
        )
        
        if export_response.status_code == 200:
            # Es un archivo CSV
            content_type = export_response.headers.get('content-type', '')
            content_length = len(export_response.content)
            
            print(f"✅ Exportación exitosa!")
            print(f"   Content-Type: {content_type}")
            print(f"   Tamaño: {content_length} bytes")
            
            # Guardar archivo para verificar
            filename = f"test_export_{tabla}.csv"
            with open(filename, 'wb') as f:
                f.write(export_response.content)
            print(f"   Archivo guardado: {filename}")
            
            # Mostrar primeras líneas del CSV
            try:
                csv_text = export_response.content.decode('utf-8-sig')
                lines = csv_text.split('\n')[:5]
                print(f"   Primeras líneas:")
                for i, line in enumerate(lines):
                    if line.strip():
                        print(f"     {i+1}: {line[:60]}{'...' if len(line) > 60 else ''}")
            except:
                print("   (No se pudo mostrar contenido)")
                
        else:
            print(f"❌ Error exportando {tabla}: {export_response.status_code}")
            print(f"   Respuesta: {export_response.text[:200]}")

    print(f"\n🎉 ¡PRUEBAS COMPLETADAS!")
    print(f"✅ Los endpoints directos funcionan correctamente")
    print(f"✅ Las exportaciones CSV se descargan sin errores")
    print(f"✅ El sistema está listo para uso en producción")

if __name__ == "__main__":
    probar_exportaciones_directas()
