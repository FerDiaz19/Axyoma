#!/usr/bin/env python
"""
Script para probar todos los endpoints corregidos
"""
import requests
import json

# Token de autenticación del usuario
TOKEN = 'a5bc8a7c3e2f8b5794d8e0c9a7b6f5e4c3d2a9b8'
BASE_URL = 'http://localhost:8000/api'
EMPRESA_ID = 3

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_endpoint(endpoint_name, url):
    """Prueba un endpoint específico"""
    try:
        print(f"\n🔍 Probando {endpoint_name}...")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ {endpoint_name} - OK")
                print(f"Registros encontrados: {len(data)}")
                if data:
                    print(f"Primer registro: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
                return True
            except json.JSONDecodeError:
                print(f"❌ {endpoint_name} - Respuesta no es JSON válido")
                print(f"Respuesta: {response.text[:200]}...")
                return False
        else:
            print(f"❌ {endpoint_name} - Error {response.status_code}")
            print(f"Respuesta: {response.text[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ {endpoint_name} - Excepción: {e}")
        return False

def main():
    """Función principal para probar todos los endpoints"""
    print("🚀 Iniciando pruebas de endpoints corregidos...")
    print(f"Empresa ID: {EMPRESA_ID}")
    print(f"Token: {TOKEN[:20]}...")
    
    endpoints = [
        ("Plantas", f"{BASE_URL}/plantas/?empresa_id={EMPRESA_ID}"),
        ("Departamentos", f"{BASE_URL}/departamentos/?empresa_id={EMPRESA_ID}"),
        ("Puestos", f"{BASE_URL}/puestos/?empresa_id={EMPRESA_ID}"),
        ("Empleados", f"{BASE_URL}/empleados/?empresa_id={EMPRESA_ID}"),
    ]
    
    resultados = []
    for name, url in endpoints:
        resultado = test_endpoint(name, url)
        resultados.append((name, resultado))
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*50)
    
    exitosos = 0
    for name, resultado in resultados:
        status = "✅ OK" if resultado else "❌ ERROR"
        print(f"{name}: {status}")
        if resultado:
            exitosos += 1
    
    print(f"\nTotal exitosos: {exitosos}/{len(resultados)}")
    
    if exitosos == len(resultados):
        print("🎉 ¡Todos los endpoints funcionan correctamente!")
    else:
        print("⚠️  Algunos endpoints tienen problemas")

if __name__ == "__main__":
    main()
