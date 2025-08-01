import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from datetime import date, timedelta
import random

print("🎯 INICIANDO CARGA DE DATOS")

# Limpiar datos
print("🧹 Limpiando...")
User.objects.filter(is_superuser=False).delete()
Empleado.objects.all().delete()
Puesto.objects.all().delete()
Departamento.objects.all().delete()
Planta.objects.all().delete()
Empresa.objects.all().delete()

# Crear superadmin
print("👑 Creando superadmin...")
User.objects.filter(username='superadmin').delete()
superuser = User.objects.create_user(
    username='superadmin',
    email='superadmin@axyoma.com',
    password='admin123',
    first_name='Super',
    last_name='Admin'
)
superuser.is_superuser = True
superuser.is_staff = True
superuser.save()

perfil = PerfilUsuario.objects.create(
    nombre='Super',
    apellido_paterno='Admin',
    correo='superadmin@axyoma.com',
    nivel_usuario='superadmin',
    status=True,
    user=superuser
)

# Crear empresas
print("🏢 Creando empresas...")
empresa1 = Empresa.objects.create(
    nombre='TechCorp Solutions',
    rfc='TCS950815MX3',
    direccion='Av. Tecnológico 1500',
    email_contacto='contacto@techcorp.mx',
    telefono_contacto='4421234567',
    administrador=None,
    status=True
)

empresa2 = Empresa.objects.create(
    nombre='InnovaSoft Industries',
    rfc='ISI980320QR1',
    direccion='Blvd. Bernardo Quintana 2000',
    email_contacto='info@innovasoft.mx',
    telefono_contacto='4427654321',
    administrador=None,
    status=True
)

# Crear plantas
print("🏭 Creando plantas...")
planta1 = Planta.objects.create(nombre='Planta Norte', direccion='Zona Norte', empresa=empresa1, status=True)
planta2 = Planta.objects.create(nombre='Planta Sur', direccion='Zona Sur', empresa=empresa1, status=True)
planta3 = Planta.objects.create(nombre='Planta Central', direccion='Zona Central', empresa=empresa2, status=True)
planta4 = Planta.objects.create(nombre='Planta Satelite', direccion='Zona Satelite', empresa=empresa2, status=True)

# Crear estructura organizacional
print("📋 Creando estructura...")
plantas = [planta1, planta2, planta3, planta4]
departamentos_nombres = ['RRHH', 'Producción', 'Mantenimiento', 'Calidad', 'Logística']
puestos_nombres = ['Director', 'Gerente', 'Supervisor', 'Operador', 'Técnico']

total_empleados = 0
for planta in plantas:
    for dept_nombre in departamentos_nombres:
        dept = Departamento.objects.create(
            nombre=dept_nombre,
            descripcion=f'Departamento de {dept_nombre}',
            planta=planta,
            status=True
        )
        
        for puesto_nombre in puestos_nombres:
            puesto = Puesto.objects.create(
                nombre=puesto_nombre,
                descripcion=f'Puesto de {puesto_nombre}',
                departamento=dept,
                status=True
            )
            
            # Crear 1-2 empleados por puesto
            num_empleados = 2 if puesto_nombre in ['Operador', 'Técnico'] else 1
            
            for i in range(num_empleados):
                emp_num = random.randint(1000, 9999)
                empleado = Empleado.objects.create(
                    nombre=f'Empleado{emp_num}',
                    apellido_paterno=f'Apellido{emp_num}',
                    apellido_materno='Test',
                    email=f'emp{emp_num}@test.com',
                    telefono=f'442{random.randint(1000000, 9999999)}',
                    fecha_ingreso=date.today() - timedelta(days=random.randint(30, 365)),
                    puesto=puesto,
                    status=True
                )
                total_empleados += 1

print("")
print("🎉 ¡DATOS CARGADOS EXITOSAMENTE!")
print("=" * 50)
print(f"✅ 1 SuperAdmin creado")
print(f"✅ 2 Empresas creadas")
print(f"✅ 4 Plantas creadas")
print(f"✅ {len(departamentos_nombres) * 4} Departamentos creados")
print(f"✅ {len(puestos_nombres) * len(departamentos_nombres) * 4} Puestos creados")
print(f"✅ {total_empleados} Empleados creados")
print("")
print("🔑 CREDENCIALES:")
print("  Usuario: superadmin")
print("  Password: admin123")
print("=" * 50)
