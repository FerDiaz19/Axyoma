#!/usr/bin/env python
"""
🎯 CARGADOR DE DATOS VÍA DJANGO SHELL
====================================
"""

from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from datetime import date, timedelta
import random

def limpiar_datos():
    print("🧹 Limpiando datos...")
    User.objects.filter(is_superuser=False).delete()
    Empleado.objects.all().delete()
    Puesto.objects.all().delete()
    Departamento.objects.all().delete()
    Planta.objects.all().delete()
    Empresa.objects.all().delete()
    print("✅ Datos limpiados")

def crear_superadmin():
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
    print("✅ SuperAdmin creado")

def crear_estructura():
    print("🏢 Creando estructura...")
    
    # Empresas
    techcorp = Empresa.objects.create(
        nombre='TechCorp Solutions',
        rfc='TCS950815MX3',
        direccion='Av. Tecnológico #1500',
        email_contacto='contacto@techcorp.mx',
        telefono_contacto='4421234567',
        status=True
    )
    
    innovasoft = Empresa.objects.create(
        nombre='InnovaSoft Industries', 
        rfc='ISI980320QR1',
        direccion='Blvd. Bernardo Quintana #2000',
        email_contacto='info@innovasoft.mx',
        telefono_contacto='4427654321',
        status=True
    )
    
    # Plantas
    planta1 = Planta.objects.create(
        nombre='Planta Norte TechCorp',
        direccion='Zona Industrial Norte',
        empresa=techcorp,
        status=True
    )
    
    planta2 = Planta.objects.create(
        nombre='Planta Sur TechCorp',
        direccion='Zona Industrial Sur', 
        empresa=techcorp,
        status=True
    )
    
    planta3 = Planta.objects.create(
        nombre='Planta Central InnovaSoft',
        direccion='Parque Industrial Central',
        empresa=innovasoft,
        status=True
    )
    
    planta4 = Planta.objects.create(
        nombre='Planta Satelite InnovaSoft',
        direccion='Ciudad Satelite',
        empresa=innovasoft,
        status=True
    )
    
    plantas = [planta1, planta2, planta3, planta4]
    
    # Departamentos y empleados
    departamentos_nombres = ['RRHH', 'Producción', 'Mantenimiento', 'Calidad', 'Logística']
    puestos_nombres = ['Director', 'Gerente', 'Supervisor', 'Operador', 'Técnico']
    
    total_empleados = 0
    
    for planta in plantas:
        for dept_nombre in departamentos_nombres:
            departamento = Departamento.objects.create(
                nombre=dept_nombre,
                descripcion=f"Departamento de {dept_nombre}",
                planta=planta,
                status=True
            )
            
            for puesto_nombre in puestos_nombres:
                puesto = Puesto.objects.create(
                    nombre=puesto_nombre,
                    descripcion=f"Puesto de {puesto_nombre}",
                    departamento=departamento,
                    status=True
                )
                
                # Crear 1-2 empleados por puesto
                num_empleados = 2 if puesto_nombre in ['Operador', 'Técnico'] else 1
                
                for i in range(num_empleados):
                    empleado_num = random.randint(1000, 9999)
                    empleado = Empleado.objects.create(
                        nombre=f"Empleado{empleado_num}",
                        apellido_paterno=f"Apellido{empleado_num}",
                        apellido_materno="Prueba",
                        email=f"emp{empleado_num}@empresa.com",
                        telefono=f"442{random.randint(1000000, 9999999)}",
                        fecha_ingreso=date.today() - timedelta(days=random.randint(30, 365)),
                        puesto=puesto,
                        status=True
                    )
                    total_empleados += 1
    
    print(f"✅ Estructura creada: {len(plantas)} plantas, {total_empleados} empleados")

@transaction.atomic
def main():
    print("🎯 CARGANDO DATOS DE PRUEBA")
    print("=" * 50)
    
    limpiar_datos()
    crear_superadmin()
    crear_estructura()
    
    print("\n🎉 ¡DATOS CARGADOS EXITOSAMENTE!")
    print("=" * 50)
    print("🔑 CREDENCIALES:")
    print("  Usuario: superadmin")
    print("  Password: admin123")
    print("=" * 50)

if __name__ == "__main__":
    main()
