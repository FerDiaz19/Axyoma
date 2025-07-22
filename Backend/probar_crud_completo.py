# -*- coding: utf-8 -*-
"""
Script para probar CRUD completo del SuperAdmin con datos reales
"""
import os
import requests
import json
import sys

# Configuración del servidor Django
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/superadmin/"

# Token del SuperAdmin (obtenido del login)
TOKEN = "2c1787a8c17851aa39fefc7bd760ad8eb5305556"

# Headers para las peticiones
headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def probar_crud_empresa():
    """Probar CRUD completo de empresas"""
    print("\n🏢 === PROBANDO CRUD DE EMPRESAS ===")
    
    # 1. Obtener lista actual
    print("\n📋 1. Obteniendo lista de empresas...")
    response = requests.get(f"{API_URL}listar_empresas/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empresas = data.get('empresas', [])
        print(f"   ✅ {len(empresas)} empresas encontradas")
        
        if empresas:
            empresa_id = int(empresas[0]['empresa_id'])
            nombre_original = empresas[0]['nombre']
            
            # 2. Editar empresa
            print(f"\n✏️ 2. Editando empresa {empresa_id}...")
            data = {
                'empresa_id': empresa_id,
                'nombre': f"{nombre_original} - EDITADA",
                'direccion': "Dirección actualizada por prueba CRUD"
            }
            response = requests.put(f"{API_URL}editar_empresa/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empresa editada exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al editar: {response.text}")
            
            # 3. Suspender empresa
            print(f"\n⏸️ 3. Suspendiendo empresa {empresa_id}...")
            data = {'empresa_id': empresa_id, 'accion': 'suspender'}
            response = requests.post(f"{API_URL}suspender_empresa/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empresa suspendida exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al suspender: {response.text}")
            
            # 4. Reactivar empresa
            print(f"\n▶️ 4. Reactivando empresa {empresa_id}...")
            data = {'empresa_id': empresa_id, 'accion': 'activar'}
            response = requests.post(f"{API_URL}suspender_empresa/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empresa reactivada exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al reactivar: {response.text}")
                
            # 5. Restaurar nombre original
            print(f"\n🔄 5. Restaurando nombre original...")
            data = {
                'empresa_id': empresa_id,
                'nombre': nombre_original
            }
            response = requests.put(f"{API_URL}editar_empresa/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Nombre restaurado exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
    else:
        print(f"   ❌ Error al obtener empresas: {response.text}")

def probar_crud_empleado():
    """Probar CRUD completo de empleados"""
    print("\n👨‍💼 === PROBANDO CRUD DE EMPLEADOS ===")
    
    # 1. Obtener lista actual
    print("\n📋 1. Obteniendo lista de empleados...")
    response = requests.get(f"{API_URL}listar_empleados/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empleados = data.get('empleados', [])
        print(f"   ✅ {len(empleados)} empleados encontrados")
        
        if empleados:
            empleado_id = int(empleados[0]['empleado_id'])
            nombre_original = empleados[0]['nombre_completo']
            
            # 2. Editar empleado
            print(f"\n✏️ 2. Editando empleado {empleado_id}...")
            data = {
                'empleado_id': empleado_id,
                'nombres': "Juan Carlos EDITADO",
            }
            response = requests.put(f"{API_URL}editar_empleado/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empleado editado exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al editar: {response.text}")
            
            # 3. Suspender empleado
            print(f"\n⏸️ 3. Suspendiendo empleado {empleado_id}...")
            data = {'empleado_id': empleado_id, 'accion': 'suspender'}
            response = requests.post(f"{API_URL}suspender_empleado/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empleado suspendido exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al suspender: {response.text}")
            
            # 4. Reactivar empleado
            print(f"\n▶️ 4. Reactivando empleado {empleado_id}...")
            data = {'empleado_id': empleado_id, 'accion': 'activar'}
            response = requests.post(f"{API_URL}suspender_empleado/", 
                                  data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("   ✅ Empleado reactivado exitosamente")
                print(f"   📝 Respuesta: {response.json()}")
            else:
                print(f"   ❌ Error al reactivar: {response.text}")
    else:
        print(f"   ❌ Error al obtener empleados: {response.text}")

def probar_crud_usuario():
    """Probar CRUD completo de usuarios (sin eliminar)"""
    print("\n👤 === PROBANDO CRUD DE USUARIOS ===")
    
    # 1. Obtener lista actual
    print("\n📋 1. Obteniendo lista de usuarios...")
    response = requests.get(f"{API_URL}listar_usuarios/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('usuarios', [])
        print(f"   ✅ {len(usuarios)} usuarios encontrados")
        
        # Encontrar un usuario que no sea superadmin y tenga user_id
        usuario_test = None
        for user in usuarios:
            if ('superadmin' not in user.get('nivel_usuario', '').lower() and 
                user.get('user_id') is not None):
                usuario_test = user
                break
        
        if usuario_test:
            # Verificar si el usuario tiene user_id (usuario Django)
            if usuario_test.get('user_id'):
                usuario_id = int(usuario_test['user_id'])
                nombre_original = usuario_test.get('nombre', '')
                
                print(f"   🎯 Probando con usuario ID {usuario_id} ({usuario_test.get('username', 'sin username')})")
                
                # 2. Editar usuario
                print(f"\n✏️ 2. Editando usuario {usuario_id}...")
                data = {
                    'usuario_id': usuario_id,
                    'first_name': f"{nombre_original} EDITADO",
                }
                response = requests.put(f"{API_URL}editar_usuario/", 
                                      data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    print("   ✅ Usuario editado exitosamente")
                    print(f"   📝 Respuesta: {response.json()}")
                else:
                    print(f"   ❌ Error al editar: {response.text}")
                
                # 3. Suspender usuario
                print(f"\n⏸️ 3. Suspendiendo usuario {usuario_id}...")
                data = {'usuario_id': usuario_id, 'accion': 'suspender'}
                response = requests.put(f"{API_URL}suspender_usuario/", 
                                      data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    print("   ✅ Usuario suspendido exitosamente")
                    print(f"   📝 Respuesta: {response.json()}")
                else:
                    print(f"   ❌ Error al suspender: {response.text}")
                
                # 4. Reactivar usuario
                print(f"\n▶️ 4. Reactivando usuario {usuario_id}...")
                data = {'usuario_id': usuario_id, 'accion': 'activar'}
                response = requests.put(f"{API_URL}suspender_usuario/", 
                                      data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    print("   ✅ Usuario reactivado exitosamente")
                    print(f"   📝 Respuesta: {response.json()}")
                else:
                    print(f"   ❌ Error al reactivar: {response.text}")
                    
                # 5. Restaurar nombre original
                print(f"\n🔄 5. Restaurando nombre original...")
                data = {
                    'usuario_id': usuario_id,
                    'first_name': nombre_original
                }
                response = requests.put(f"{API_URL}editar_usuario/", 
                                      data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    print("   ✅ Nombre restaurado exitosamente")
                    print(f"   📝 Respuesta: {response.json()}")
            else:
                print("   ⚠️ Usuario no tiene user_id de Django, saltando prueba")
        else:
            print("   ⚠️ No se encontró usuario no-superadmin con user_id para probar")
    else:
        print(f"   ❌ Error al obtener usuarios: {response.text}")

if __name__ == "__main__":
    print("🧪 === PRUEBA COMPLETA DE CRUD SUPERADMIN ===")
    print(f"🔗 Servidor: {BASE_URL}")
    print(f"🔑 Token: {TOKEN[:20]}...")
    
    try:
        # Probar CRUD de diferentes secciones
        probar_crud_empresa()
        probar_crud_empleado()
        probar_crud_usuario()
        
        print("\n🎉 === PRUEBA CRUD COMPLETADA ===")
        print("✅ Se probaron las operaciones:")
        print("   • Editar información")
        print("   • Suspender registro")
        print("   • Reactivar registro")
        print("   • Restaurar datos originales")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
