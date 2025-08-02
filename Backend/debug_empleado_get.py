import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.models import Empleado
from apps.serializers import EmpleadoSerializer

def debug_empleado_get():
    """Debuggear el error 500 en GET /api/empleados/1"""
    
    print("=== DEBUG EMPLEADO GET ===")
    
    # 1. Verificar si existe el empleado
    try:
        empleado = Empleado.objects.filter(empleado_id=1).first()
        if not empleado:
            print("❌ No se encontró empleado con ID 1")
            return
        
        print(f"✅ Empleado encontrado: {empleado.nombre} {empleado.apellido_paterno}")
        
        # 2. Verificar relaciones
        print(f"Puesto: {empleado.puesto}")
        if empleado.puesto:
            print(f"  - ID: {empleado.puesto.puesto_id}")
            print(f"  - Nombre: {empleado.puesto.nombre}")
            print(f"  - Departamento: {empleado.puesto.departamento}")
            
            if empleado.puesto.departamento:
                print(f"    - ID: {empleado.puesto.departamento.departamento_id}")
                print(f"    - Nombre: {empleado.puesto.departamento.nombre}")
                print(f"    - Planta: {empleado.puesto.departamento.planta}")
                
                if empleado.puesto.departamento.planta:
                    print(f"      - ID: {empleado.puesto.departamento.planta.planta_id}")
                    print(f"      - Nombre: {empleado.puesto.departamento.planta.nombre}")
                    print(f"      - Empresa: {empleado.puesto.departamento.planta.empresa}")
                    
                    if empleado.puesto.departamento.planta.empresa:
                        print(f"        - ID: {empleado.puesto.departamento.planta.empresa.empresa_id}")
                        print(f"        - Nombre: {empleado.puesto.departamento.planta.empresa.nombre}")
                    else:
                        print("❌ PROBLEMA: Planta sin empresa")
                else:
                    print("❌ PROBLEMA: Departamento sin planta")
            else:
                print("❌ PROBLEMA: Puesto sin departamento")
        else:
            print("❌ PROBLEMA: Empleado sin puesto")
        
        # 3. Intentar serializar
        print("\n=== PRUEBA DE SERIALIZACIÓN ===")
        try:
            serializer = EmpleadoSerializer(empleado)
            data = serializer.data
            print("✅ Serialización exitosa")
            print(f"Datos principales: {data.get('nombre')} - {data.get('puesto_nombre')}")
            
            # Verificar campos específicos que pueden fallar
            campos_criticos = [
                'empresa_id', 'empresa_nombre',
                'planta_id', 'planta_nombre', 
                'departamento_id', 'departamento_nombre',
                'puesto_id', 'puesto_nombre'
            ]
            
            for campo in campos_criticos:
                valor = data.get(campo)
                if valor is None:
                    print(f"⚠️  Campo {campo}: None")
                else:
                    print(f"✅ Campo {campo}: {valor}")
                    
        except Exception as e:
            print(f"❌ Error en serialización: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_empleado_get()
