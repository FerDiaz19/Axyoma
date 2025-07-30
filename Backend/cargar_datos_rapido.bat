@echo off
echo ==========================================
echo 📊 CARGAR DATOS INICIALES - RAPIDO
echo ==========================================

cd /d "c:\xampp2\htdocs\UTT4B\Axyoma2\Backend"

echo 📊 Creando datos iniciales...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import Empresa, Planta, Departamento, Puesto, Empleado
from django.db import transaction

print('🔄 Creando datos iniciales...')

with transaction.atomic():
    # 1. Usuarios
    users_data = [
        {'username': 'superadmin', 'email': 'super@axyoma.com', 'password': '1234', 'staff': True, 'super': True},
        {'username': 'admin_empresa', 'email': 'admin@empresa.com', 'password': '1234', 'staff': False, 'super': False},
        {'username': 'admin_planta', 'email': 'admin@planta.com', 'password': '1234', 'staff': False, 'super': False},
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_active': True,
                'is_staff': user_data['staff'],
                'is_superuser': user_data['super']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f'✅ Usuario: {user.username}')
    
    # 2. Empresa
    empresa, created = Empresa.objects.get_or_create(
        nombre='Empresa Demo AXYOMA',
        defaults={
            'rfc': 'EDA123456789',
            'direccion': 'Av. Principal 123',
            'email_contacto': 'contacto@demo.com',
            'telefono_contacto': '555-0123',
            'status': True
        }
    )
    if created:
        print(f'✅ Empresa: {empresa.nombre}')
    
    # 3. Plantas
    plantas_data = [
        {'nombre': 'Planta Norte', 'direccion': 'Zona Norte'},
        {'nombre': 'Planta Sur', 'direccion': 'Zona Sur'},
    ]
    
    plantas_creadas = []
    for planta_data in plantas_data:
        planta, created = Planta.objects.get_or_create(
            nombre=planta_data['nombre'],
            empresa=empresa,
            defaults={
                'direccion': planta_data['direccion'],
                'status': True
            }
        )
        if created:
            plantas_creadas.append(planta)
            print(f'✅ Planta: {planta.nombre}')
    
    # 4. Departamentos
    deptos = ['Recursos Humanos', 'Producción', 'Calidad']
    deptos_creados = []
    
    for planta in plantas_creadas:
        for dept_nombre in deptos:
            dept, created = Departamento.objects.get_or_create(
                nombre=dept_nombre,
                planta=planta,
                defaults={
                    'descripcion': f'Depto de {dept_nombre}',
                    'status': True
                }
            )
            if created:
                deptos_creados.append(dept)
                print(f'✅ Departamento: {dept.nombre} en {planta.nombre}')
    
    # 5. Puestos
    puestos_nombres = ['Gerente', 'Supervisor', 'Analista', 'Operario']
    puestos_creados = []
    
    for dept in deptos_creados:
        for puesto_nombre in puestos_nombres:
            puesto, created = Puesto.objects.get_or_create(
                nombre=puesto_nombre,
                departamento=dept,
                defaults={
                    'descripcion': f'{puesto_nombre} de {dept.nombre}',
                    'status': True
                }
            )
            if created:
                puestos_creados.append(puesto)
                print(f'✅ Puesto: {puesto.nombre} en {dept.nombre}')
    
    # 6. Empleados de ejemplo
    empleados_data = [
        {'nombre': 'Juan', 'apellido': 'Pérez'},
        {'nombre': 'María', 'apellido': 'García'},
        {'nombre': 'Carlos', 'apellido': 'López'},
        {'nombre': 'Ana', 'apellido': 'Martínez'},
    ]
    
    for i, emp_data in enumerate(empleados_data):
        if i < len(puestos_creados):
            puesto = puestos_creados[i]
            empleado, created = Empleado.objects.get_or_create(
                nombre=emp_data['nombre'],
                apellido_paterno=emp_data['apellido'],
                puesto=puesto,
                defaults={
                    'apellido_materno': 'Demo',
                    'email': f'{emp_data[\"nombre\"].lower()}@demo.com',
                    'telefono': f'555-{1000 + i}',
                    'status': True
                }
            )
            if created:
                print(f'✅ Empleado: {empleado.nombre} {empleado.apellido_paterno}')

print('')
print('🎉 DATOS INICIALES CREADOS EXITOSAMENTE')
print('')
print('👤 USUARIOS DISPONIBLES:')
print('• superadmin / 1234')
print('• admin_empresa / 1234')  
print('• admin_planta / 1234')
print('')
"

echo.
echo ✅ DATOS CARGADOS - Presiona cualquier tecla para continuar...
pause > nul
