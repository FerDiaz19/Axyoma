# insertar_datos_django.py
# Script para insertar datos de prueba en Django
# 
# INSTRUCCIONES:
# 1. Ejecuta primero: python manage.py makemigrations
# 2. Ejecuta después: python manage.py migrate
# 3. Ejecuta este script con: python manage.py shell < insertar_datos_django.py

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado

print("Insertando datos de prueba...")

# Crear usuarios
user1 = User.objects.create_user(username='ed-rubio@axyoma.com', email='ed-rubio@axyoma.com', password='1234', first_name='Ed', last_name='Rubio')
user2 = User.objects.create_user(username='juan.perez@codewave.com', email='juan.perez@codewave.com', password='1234', first_name='Juan', last_name='Perez')
user3 = User.objects.create_user(username='maria.gomez@codewave.com', email='maria.gomez@codewave.com', password='1234', first_name='Maria', last_name='Gomez')
user4 = User.objects.create_user(username='carlos.ruiz@codewave.com', email='carlos.ruiz@codewave.com', password='1234', first_name='Carlos', last_name='Ruiz')

# Crear perfiles
perfil1 = PerfilUsuario.objects.create(user=user1, nombre='Ed', apellido_paterno='Rubio', nivel_usuario='superadmin')
perfil2 = PerfilUsuario.objects.create(user=user2, nombre='Juan', apellido_paterno='Perez', nivel_usuario='admin-empresa')
perfil3 = PerfilUsuario.objects.create(user=user3, nombre='Maria', apellido_paterno='Gomez', nivel_usuario='admin-planta', admin_empresa=perfil2)
perfil4 = PerfilUsuario.objects.create(user=user4, nombre='Carlos', apellido_paterno='Ruiz', nivel_usuario='admin-planta', admin_empresa=perfil2)

# Crear empresa
empresa1 = Empresa.objects.create(
    nombre='Soluciones Industriales MX',
    rfc='SIMX920314ABC',
    direccion='Av. Revolución 123, Col. Centro, CDMX',
    logotipo='https://i.pinimg.com/736x/24/7e/85/247e85b4cdcc74b50326fb36128dbce4.jpg',
    email_contacto='contacto@solucionesmx.com',
    telefono_contacto='5551234567',
    administrador=perfil2
)

# Crear plantas
planta1 = Planta.objects.create(nombre='Oficina Central Tijuana', direccion='Av. Principal 456, Tijuana, BC', empresa=empresa1)
planta2 = Planta.objects.create(nombre='Oficina Monterrey', direccion='Blvd. Constitución 789, Monterrey, NL', empresa=empresa1)

# Crear departamentos
dept1 = Departamento.objects.create(nombre='Recursos Humanos', descripcion='Gestión de personal', planta=planta1)
dept2 = Departamento.objects.create(nombre='Desarrollo de Software', descripcion='Creación de aplicaciones', planta=planta1)
dept3 = Departamento.objects.create(nombre='Operaciones', descripcion='Gestión de operaciones', planta=planta1)
dept4 = Departamento.objects.create(nombre='Calidad', descripcion='Control de calidad', planta=planta2)
dept5 = Departamento.objects.create(nombre='Mantenimiento', descripcion='Mantenimiento de equipos', planta=planta2)

# Crear puestos
puesto1 = Puesto.objects.create(nombre='Gerente de RRHH', descripcion='Líder del equipo de RRHH', departamento=dept1)
puesto2 = Puesto.objects.create(nombre='Desarrollador Senior', descripcion='Programador experimentado', departamento=dept2)
puesto3 = Puesto.objects.create(nombre='Desarrollador Junior', descripcion='Programador en formación', departamento=dept2)
puesto4 = Puesto.objects.create(nombre='Supervisor de Operaciones', descripcion='Supervisión de procesos', departamento=dept3)
puesto5 = Puesto.objects.create(nombre='Especialista en Calidad', descripcion='Control de calidad', departamento=dept4)
puesto6 = Puesto.objects.create(nombre='Técnico de Mantenimiento', descripcion='Mantenimiento preventivo', departamento=dept5)

# Crear empleados
Empleado.objects.create(nombre='Laura', apellido_paterno='Fernández', apellido_materno='Torres', genero='Femenino', antiguedad=5, puesto=puesto1, departamento=dept1, planta=planta1)
Empleado.objects.create(nombre='José', apellido_paterno='Martínez', apellido_materno='López', genero='Masculino', antiguedad=2, puesto=puesto2, departamento=dept2, planta=planta1)
Empleado.objects.create(nombre='Ana', apellido_paterno='García', apellido_materno='Ruiz', genero='Femenino', antiguedad=3, puesto=puesto3, departamento=dept2, planta=planta1)
Empleado.objects.create(nombre='Carlos', apellido_paterno='López', apellido_materno='Hernández', genero='Masculino', antiguedad=4, puesto=puesto4, departamento=dept3, planta=planta1)
Empleado.objects.create(nombre='María', apellido_paterno='Rodríguez', apellido_materno='Sánchez', genero='Femenino', antiguedad=1, puesto=puesto5, departamento=dept4, planta=planta2)
Empleado.objects.create(nombre='Pedro', apellido_paterno='González', apellido_materno='Morales', genero='Masculino', antiguedad=6, puesto=puesto6, departamento=dept5, planta=planta2)

print("✓ Datos insertados correctamente!")
print("\nUsuarios creados:")
print("- ed-rubio@axyoma.com / 1234 (SuperAdmin)")
print("- juan.perez@codewave.com / 1234 (Admin Empresa)")
print("- maria.gomez@codewave.com / 1234 (Admin Planta)")
print("- carlos.ruiz@codewave.com / 1234 (Admin Planta)")
