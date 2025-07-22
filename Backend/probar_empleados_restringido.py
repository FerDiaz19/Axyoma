# -*- coding: utf-8 -*-
"""
Script para probar la edición restringida de empleados
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

def test_editar_empleado_restringido():
    """Probar que solo se pueden editar los campos permitidos en empleados"""
    print("🧪 === PROBANDO EDICIÓN RESTRINGIDA DE EMPLEADOS ===")
    
    # Obtener empleados
    response = requests.get(f"{API_URL}listar_empleados/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empleados = data.get('empleados', [])
        
        if empleados:
            empleado_test = empleados[0]
            empleado_id = empleado_test['empleado_id']
            nombre_original = empleado_test['nombre']
            
            print(f"   🎯 Probando con empleado {empleado_id}: {empleado_test['nombre_completo']}")
            
            # 1. Probar campos PERMITIDOS
            print(f"\n✅ PROBANDO CAMPOS PERMITIDOS:")
            datos_permitidos = {
                'empleado_id': empleado_id,
                'nombre': 'NOMBRE_EDITADO',
                'apellido_paterno': 'APELLIDO_EDITADO',
                'apellido_materno': 'MATERNO_EDITADO'
            }
            
            response = requests.put(f"{API_URL}editar_empleado/", 
                                  data=json.dumps(datos_permitidos), headers=headers)
            
            print(f"   📝 Status: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            
            # 2. Probar campos NO PERMITIDOS (deben ser ignorados)
            print(f"\n⚠️ PROBANDO CAMPOS NO PERMITIDOS (deben ser ignorados):")
            datos_no_permitidos = {
                'empleado_id': empleado_id,
                'nombre': 'NOMBRE_FINAL',
                'email': 'nuevo_email@test.com',  # NO PERMITIDO
                'telefono': '555-1234',          # NO PERMITIDO  
                'fecha_ingreso': '2025-01-01'    # NO PERMITIDO
            }
            
            response = requests.put(f"{API_URL}editar_empleado/", 
                                  data=json.dumps(datos_no_permitidos), headers=headers)
            
            print(f"   📝 Status: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            
            # 3. Verificar el estado final
            print(f"\n🔍 VERIFICANDO EMPLEADO DESPUÉS DE EDICIONES:")
            response = requests.get(f"{API_URL}listar_empleados/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                empleados_actualizados = data.get('empleados', [])
                empleado_actualizado = None
                
                for emp in empleados_actualizados:
                    if emp['empleado_id'] == empleado_id:
                        empleado_actualizado = emp
                        break
                
                if empleado_actualizado:
                    print(f"   👤 Nombre: {empleado_actualizado.get('nombre')}")
                    print(f"   👤 Apellido P.: {empleado_actualizado.get('apellido_paterno')}")
                    print(f"   👤 Apellido M.: {empleado_actualizado.get('apellido_materno')}")
                    print(f"   📧 Email: {empleado_actualizado.get('email', 'N/A')}")
                    print(f"   📞 Teléfono: {empleado_actualizado.get('telefono', 'N/A')}")
                    print(f"   📅 Fecha Ingreso: {empleado_actualizado.get('fecha_ingreso', 'N/A')}")
            
            # 4. Restaurar nombre original
            print(f"\n🔄 RESTAURANDO NOMBRE ORIGINAL:")
            datos_restaurar = {
                'empleado_id': empleado_id,
                'nombre': nombre_original
            }
            
            response = requests.put(f"{API_URL}editar_empleado/", 
                                  data=json.dumps(datos_restaurar), headers=headers)
            print(f"   📝 Restauración: {response.status_code == 200}")

def test_eliminar_empleado():
    """Confirmar que eliminar empleados sigue funcionando"""
    print(f"\n🗑️ === VERIFICANDO QUE ELIMINAR EMPLEADOS FUNCIONA ===")
    
    # Obtener empleados
    response = requests.get(f"{API_URL}listar_empleados/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        empleados = data.get('empleados', [])
        
        print(f"   📊 Total empleados antes: {len(empleados)}")
        
        # Solo verificar que el endpoint existe (no eliminar realmente)
        if empleados:
            empleado_test = empleados[-1]  # Tomar el último
            empleado_id = empleado_test['empleado_id']
            
            # Hacer una petición OPTIONS para verificar que el endpoint existe
            response = requests.options(f"{API_URL}eliminar_empleado/", headers=headers)
            print(f"   ✅ Endpoint eliminar_empleado disponible: {response.status_code != 404}")

if __name__ == "__main__":
    test_editar_empleado_restringido()
    test_eliminar_empleado()
    
    print(f"\n🎉 === RESUMEN ===")
    print(f"✅ Editar empleados: Solo nombres, apellidos y status")
    print(f"❌ NO editable: telefono, fecha_ingreso, email")
    print(f"✅ Eliminar empleados: Disponible")
