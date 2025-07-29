#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar las exportaciones CSV mejoradas
Ahora con información completa de relaciones
"""
import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "fd60fcc7156be19d06e46f3f04f9455bc82593d5d"

# Headers para autenticación
headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_csv_export(tabla_nombre):
    """Probar exportación CSV de una tabla específica"""
    print(f"\n🔄 Probando exportación: {tabla_nombre}")
    print("-" * 50)
    
    url = f"{BASE_URL}/admin-bd/directo/exportar/{tabla_nombre}/"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            content_length = len(response.content)
            print(f"✅ Éxito: {tabla_nombre}")
            print(f"📊 Tamaño: {content_length} bytes")
            
            # Si es pequeño, mostrar las primeras líneas
            if content_length < 2000:
                lines = response.text.split('\n')[:10]  # Primeras 10 líneas
                print(f"📄 Primeras líneas del CSV:")
                for i, line in enumerate(lines):
                    if line.strip():
                        print(f"   {i+1}: {line}")
            else:
                # Solo mostrar headers
                lines = response.text.split('\n')[:3]
                print(f"📄 Headers y primeras filas:")
                for i, line in enumerate(lines):
                    if line.strip():
                        print(f"   {i+1}: {line}")
                        
        else:
            print(f"❌ Error {response.status_code}: {tabla_nombre}")
            try:
                error_data = response.json()
                print(f"🚨 Detalle: {error_data}")
            except:
                print(f"🚨 Respuesta: {response.text[:500]}")
                
    except Exception as e:
        print(f"💥 Excepción: {str(e)}")

def main():
    print("🚀 PRUEBA DE EXPORTACIONES CSV MEJORADAS")
    print("=" * 60)
    print(f"🔗 Base URL: {BASE_URL}")
    print(f"🔑 Token: {TOKEN[:20]}...")
    
    # Tablas a probar
    tablas = ['empleados', 'suscripciones']
    
    for tabla in tablas:
        test_csv_export(tabla)
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada!")

if __name__ == "__main__":
    main()
