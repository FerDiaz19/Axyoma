# -*- coding: utf-8 -*-
"""
Script para verificar que la eliminación de usuario funcionó
"""
import requests

# Configuración del servidor Django
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/superadmin/"

# Token del SuperAdmin
TOKEN = "2c1787a8c17851aa39fefc7bd760ad8eb5305556"

# Headers para las peticiones
headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def verificar_usuario_eliminado():
    """Verificar que el usuario se eliminó correctamente"""
    print("🔍 === VERIFICANDO USUARIO ELIMINADO ===")
    
    response = requests.get(f"{API_URL}listar_usuarios/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('usuarios', [])
        
        print(f"   📊 Total usuarios: {len(usuarios)}")
        
        # Buscar usuario con id 2
        usuario_eliminado = None
        for usuario in usuarios:
            if usuario['id'] == 2:
                usuario_eliminado = usuario
                break
        
        if usuario_eliminado:
            print(f"   🎯 Usuario ID 2 encontrado:")
            print(f"      - Nombre: {usuario_eliminado['nombre_completo']}")
            print(f"      - Email: {usuario_eliminado['email']}")
            print(f"      - Activo: {usuario_eliminado['is_active']}")
            print(f"      - Status: {'✅ DESACTIVADO' if not usuario_eliminado['is_active'] else '❌ SIGUE ACTIVO'}")
        else:
            print(f"   ⚠️ Usuario ID 2 no encontrado en la lista")
        
        print(f"\n   📋 Resumen usuarios activos/inactivos:")
        activos = sum(1 for u in usuarios if u['is_active'])
        inactivos = len(usuarios) - activos
        print(f"      - ✅ Activos: {activos}")
        print(f"      - ❌ Inactivos: {inactivos}")

if __name__ == "__main__":
    verificar_usuario_eliminado()
