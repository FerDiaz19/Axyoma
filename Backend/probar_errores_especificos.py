# -*- coding: utf-8 -*-
"""
Script para probar específicamente las operaciones que están fallando
"""
import requests
import json

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

def test_eliminar_empresa():
    """Probar eliminación de empresa"""
    print("\n🏢 === PROBANDO ELIMINAR EMPRESA ===")
    
    # Obtener empresas
    response = requests.get(f"{API_URL}listar_empresas/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empresas = data.get('empresas', [])
        
        # Buscar una empresa que no sea la principal
        empresa_test = None
        for emp in empresas:
            if emp['empresa_id'] != 1:  # No eliminar la empresa principal
                empresa_test = emp
                break
        
        if empresa_test:
            empresa_id = empresa_test['empresa_id']
            print(f"   🎯 Intentando eliminar empresa {empresa_id}: {empresa_test['nombre']}")
            
            data = {'empresa_id': empresa_id}
            response = requests.delete(f"{API_URL}eliminar_empresa/", 
                                     data=json.dumps(data), headers=headers)
            
            print(f"   📝 Status Code: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
        else:
            print("   ⚠️ No hay empresas para eliminar (solo empresa principal)")

def test_eliminar_usuario():
    """Probar eliminación de usuario"""
    print("\n👤 === PROBANDO ELIMINAR USUARIO ===")
    
    # Obtener usuarios
    response = requests.get(f"{API_URL}listar_usuarios/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('usuarios', [])
        
        # Buscar un usuario que no sea superadmin y tenga user_id
        usuario_test = None
        for user in usuarios:
            if ('superadmin' not in user.get('nivel_usuario', '').lower() and 
                user.get('user_id') is not None):
                usuario_test = user
                break
        
        if usuario_test:
            usuario_id = usuario_test['user_id']
            print(f"   🎯 Intentando eliminar usuario {usuario_id}: {usuario_test['username']}")
            
            data = {'usuario_id': usuario_id}
            response = requests.delete(f"{API_URL}eliminar_usuario/", 
                                     data=json.dumps(data), headers=headers)
            
            print(f"   📝 Status Code: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
        else:
            print("   ⚠️ No hay usuarios no-superadmin con user_id para eliminar")

def test_editar_usuario():
    """Probar edición de usuario"""
    print("\n✏️ === PROBANDO EDITAR USUARIO ===")
    
    # Obtener usuarios
    response = requests.get(f"{API_URL}listar_usuarios/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('usuarios', [])
        
        # Buscar un usuario que no sea superadmin y tenga user_id
        usuario_test = None
        for user in usuarios:
            if ('superadmin' not in user.get('nivel_usuario', '').lower() and 
                user.get('user_id') is not None):
                usuario_test = user
                break
        
        if usuario_test:
            usuario_id = usuario_test['user_id']
            print(f"   🎯 Intentando editar usuario {usuario_id}: {usuario_test['username']}")
            
            data = {
                'usuario_id': usuario_id,
                'first_name': 'EDITADO TEST'
            }
            response = requests.put(f"{API_URL}editar_usuario/", 
                                  data=json.dumps(data), headers=headers)
            
            print(f"   📝 Status Code: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
        else:
            print("   ⚠️ No hay usuarios no-superadmin con user_id para editar")

def test_suspender_empresa():
    """Probar suspensión de empresa y verificar efectos en cascada"""
    print("\n⏸️ === PROBANDO SUSPENDER EMPRESA (CASCADA) ===")
    
    # Obtener empresas
    response = requests.get(f"{API_URL}listar_empresas/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empresas = data.get('empresas', [])
        
        if empresas:
            empresa_test = empresas[0]
            empresa_id = empresa_test['empresa_id']
            print(f"   🎯 Empresa a suspender: {empresa_test['nombre']} (ID: {empresa_id})")
            
            # Verificar plantas antes
            print("\n   📊 ANTES - Verificando plantas de la empresa:")
            resp_plantas = requests.get(f"{API_URL}listar_plantas/", headers=headers)
            if resp_plantas.status_code == 200:
                plantas_data = resp_plantas.json()
                plantas_empresa = [p for p in plantas_data.get('plantas', []) 
                                 if p.get('empresa', {}).get('id') == empresa_id]
                print(f"   🏭 Plantas activas de empresa {empresa_id}: {len(plantas_empresa)}")
            
            # Suspender empresa
            print(f"\n   ⏸️ Suspendiendo empresa {empresa_id}...")
            data = {'empresa_id': empresa_id, 'accion': 'suspender'}
            response = requests.post(f"{API_URL}suspender_empresa/", 
                                   data=json.dumps(data), headers=headers)
            
            print(f"   📝 Status Code: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            
            # Verificar plantas después
            print("\n   📊 DESPUÉS - Verificando plantas de la empresa:")
            resp_plantas = requests.get(f"{API_URL}listar_plantas/", headers=headers)
            if resp_plantas.status_code == 200:
                plantas_data = resp_plantas.json()
                plantas_empresa = [p for p in plantas_data.get('plantas', []) 
                                 if p.get('empresa', {}).get('id') == empresa_id]
                print(f"   🏭 Plantas activas de empresa {empresa_id}: {len(plantas_empresa)}")

if __name__ == "__main__":
    print("🧪 === PROBANDO OPERACIONES CON PROBLEMAS ===")
    
    test_eliminar_empresa()
    test_eliminar_usuario() 
    test_editar_usuario()
    test_suspender_empresa()
