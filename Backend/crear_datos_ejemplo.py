#!/usr/bin/env python
"""
Script para crear datos de ejemplo completos para Axyoma
Incluye empresas, plantas, departamentos, puestos y empleados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
from datetime import datetime, timedelta
import random

def crear_datos_ejemplo():
    """Crear datos de ejemplo completos para el sistema"""
    
    print("🚀 Iniciando creación de datos de ejemplo...")
    
    try:
        with transaction.atomic():
            # 1. EMPRESAS ADICIONALES
            empresas_data = [
                {
                    'nombre': 'Manufactura Industrial SA',
                    'rfc': 'MIS850623AB1',
                    'direccion': 'Av. Industrial 456, Zona Industrial, Guadalajara, Jalisco',
                    'email_contacto': 'contacto@manufacturaindustrial.mx',
                    'telefono_contacto': '33-1234-5678'
                },
                {
                    'nombre': 'Servicios Corporativos del Norte',
                    'rfc': 'SCN920815CD2',
                    'direccion': 'Blvd. Revolución 789, Centro, Monterrey, Nuevo León',
                    'email_contacto': 'info@servicosnorte.mx',
                    'telefono_contacto': '81-9876-5432'
                },
                {
                    'nombre': 'Consultora Técnica Avanzada',
                    'rfc': 'CTA780404EF3',
                    'direccion': 'Periférico Sur 321, Del Valle, CDMX',
                    'email_contacto': 'contacto@consultecnica.mx',
                    'telefono_contacto': '55-5555-1234'
                }
            ]
            
            # Crear empresas con administradores
            empresas_creadas = []
            for i, empresa_info in enumerate(empresas_data, 2):  # Empezar desde 2 porque ya existe una
                print(f"📊 Creando empresa: {empresa_info['nombre']}")
                
                # Crear usuario administrador
                username = f"admin_empresa_{i}"
                user = User.objects.create_user(
                    username=username,
                    email=empresa_info['email_contacto'],
                    password='1234'
                )
                
                # Crear perfil
                perfil = PerfilUsuario.objects.create(
                    user=user,
                    nombre=f"Admin {empresa_info['nombre'].split()[0]}",
                    apellido_paterno="Administrador",
                    apellido_materno="Principal",
                    correo=empresa_info['email_contacto'],
                    nivel_usuario='admin-empresa'
                )
                
                # Crear empresa
                empresa = Empresa.objects.create(
                    nombre=empresa_info['nombre'],
                    rfc=empresa_info['rfc'],
                    direccion=empresa_info['direccion'],
                    email_contacto=empresa_info['email_contacto'],
                    telefono_contacto=empresa_info['telefono_contacto'],
                    administrador=perfil
                )
                
                empresas_creadas.append(empresa)
                print(f"✅ Empresa creada: {empresa.nombre}")
            
            # 2. PLANTAS PARA CADA EMPRESA
            todas_empresas = list(Empresa.objects.all())
            plantas_creadas = []
            
            plantas_por_empresa = {
                'CodeWave Technologies': ['Oficina Central Tijuana', 'Sucursal Monterrey', 'Centro de Desarrollo CDMX'],
                'Manufactura Industrial SA': ['Planta Guadalajara', 'Planta León', 'Almacén Central'],
                'Servicios Corporativos del Norte': ['Oficina Monterrey', 'Sucursal Saltillo'],
                'Consultora Técnica Avanzada': ['Oficina Principal CDMX', 'Centro de Capacitación']
            }
            
            for empresa in todas_empresas:
                if empresa.nombre in plantas_por_empresa:
                    plantas_nombres = plantas_por_empresa[empresa.nombre]
                    for nombre_planta in plantas_nombres:
                        planta, created = Planta.objects.get_or_create(
                            nombre=nombre_planta,
                            empresa=empresa,
                            defaults={
                                'direccion': f'Dirección de {nombre_planta}',
                                'status': True
                            }
                        )
                        if created:
                            plantas_creadas.append(planta)
                            print(f"🏢 Planta creada: {planta.nombre} para {empresa.nombre}")
                            
                            # CREAR USUARIO ADMIN-PLANTA AUTOMÁTICAMENTE
                            username_planta = f"admin_planta_{planta.planta_id}"
                            email_planta = f"admin.planta.{planta.planta_id}@{empresa.nombre.lower().replace(' ', '')}.com"
                            
                            # Crear usuario Django para admin-planta
                            user_planta = User.objects.create_user(
                                username=username_planta,
                                email=email_planta,
                                password='1234'
                            )
                            
                            # Crear perfil admin-planta
                            perfil_planta = PerfilUsuario.objects.create(
                                user=user_planta,
                                nombre=f"Admin {nombre_planta.split()[0]}",
                                apellido_paterno="Planta",
                                apellido_materno=f"{empresa.nombre.split()[0]}",
                                correo=email_planta,
                                nivel_usuario='admin-planta'
                            )
                            
                            # Crear relación AdminPlanta
                            AdminPlanta.objects.create(
                                usuario=perfil_planta,
                                planta=planta,
                                status=True,
                                password_temporal='1234'
                            )
                            
                            print(f"👤 Usuario admin-planta creado: {username_planta}")
            
            # 3. DEPARTAMENTOS ESTÁNDAR PARA CADA PLANTA
            departamentos_estandar = [
                'Recursos Humanos',
                'Contabilidad',
                'Desarrollo de Software',
                'Ventas',
                'Marketing',
                'Producción',
                'Calidad',
                'Compras',
                'Almacén',
                'Mantenimiento'
            ]
            
            todas_plantas = Planta.objects.all()
            departamentos_creados = []
            
            for planta in todas_plantas:
                # Determinar departamentos según el tipo de empresa/planta
                if 'CodeWave' in planta.empresa.nombre or 'Desarrollo' in planta.nombre:
                    deptos_planta = ['Recursos Humanos', 'Contabilidad', 'Desarrollo de Software', 'Ventas', 'Marketing']
                elif 'Manufactura' in planta.empresa.nombre:
                    deptos_planta = ['Recursos Humanos', 'Contabilidad', 'Producción', 'Calidad', 'Compras', 'Almacén', 'Mantenimiento']
                elif 'Servicios' in planta.empresa.nombre:
                    deptos_planta = ['Recursos Humanos', 'Contabilidad', 'Ventas', 'Marketing', 'Compras']
                else:  # Consultora
                    deptos_planta = ['Recursos Humanos', 'Contabilidad', 'Desarrollo de Software', 'Ventas']
                
                for nombre_depto in deptos_planta:
                    depto, created = Departamento.objects.get_or_create(
                        nombre=nombre_depto,
                        planta=planta,
                        defaults={
                            'descripcion': f'Departamento de {nombre_depto} - {planta.nombre}',
                            'status': True
                        }
                    )
                    if created:
                        departamentos_creados.append(depto)
            
            print(f"🏬 Departamentos creados: {len(departamentos_creados)}")
            
            # 4. PUESTOS ESTÁNDAR PARA CADA DEPARTAMENTO
            puestos_por_departamento = {
                'Recursos Humanos': ['Gerente de RRHH', 'Especialista en RRHH', 'Asistente de RRHH', 'Coordinador de Nóminas'],
                'Contabilidad': ['Contador General', 'Auxiliar Contable', 'Analista Financiero', 'Tesorero'],
                'Desarrollo de Software': ['Líder de Proyecto', 'Desarrollador Full Stack', 'Desarrollador Frontend', 'Desarrollador Backend', 'QA Tester', 'DevOps Engineer'],
                'Ventas': ['Gerente de Ventas', 'Ejecutivo de Ventas', 'Representante de Ventas', 'Coordinador Comercial'],
                'Marketing': ['Gerente de Marketing', 'Especialista en Marketing Digital', 'Community Manager', 'Diseñador Gráfico'],
                'Producción': ['Jefe de Producción', 'Supervisor de Línea', 'Operador de Máquina', 'Técnico de Producción'],
                'Calidad': ['Jefe de Calidad', 'Inspector de Calidad', 'Técnico en Calidad', 'Auditor Interno'],
                'Compras': ['Jefe de Compras', 'Comprador', 'Analista de Proveedores', 'Coordinador de Compras'],
                'Almacén': ['Jefe de Almacén', 'Encargado de Inventarios', 'Montacarguista', 'Auxiliar de Almacén'],
                'Mantenimiento': ['Jefe de Mantenimiento', 'Técnico Mecánico', 'Técnico Eléctrico', 'Soldador']
            }
            
            todos_departamentos = Departamento.objects.all()
            puestos_creados = []
            
            for departamento in todos_departamentos:
                if departamento.nombre in puestos_por_departamento:
                    puestos_dept = puestos_por_departamento[departamento.nombre]
                    for nombre_puesto in puestos_dept:
                        puesto, created = Puesto.objects.get_or_create(
                            nombre=nombre_puesto,
                            departamento=departamento,
                            defaults={
                                'descripcion': f'{nombre_puesto} del departamento {departamento.nombre}',
                                'status': True
                            }
                        )
                        if created:
                            puestos_creados.append(puesto)
            
            print(f"💼 Puestos creados: {len(puestos_creados)}")
            
            # 5. EMPLEADOS PARA CADA PUESTO
            nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Carmen', 'José', 'Elena', 'Miguel', 'Rosa']
            apellidos_p = ['García', 'Rodríguez', 'López', 'Martínez', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Cruz', 'Torres']
            apellidos_m = ['Hernández', 'Morales', 'Jiménez', 'Ruiz', 'Díaz', 'Vargas', 'Castro', 'Ortiz', 'Ramos', 'Mendoza']
            
            todos_puestos = Puesto.objects.all()
            empleados_creados = []
            
            for puesto in todos_puestos:
                # Crear entre 1-4 empleados por puesto dependiendo del nivel
                if 'Gerente' in puesto.nombre or 'Jefe' in puesto.nombre or 'Líder' in puesto.nombre:
                    cantidad = 1  # Solo 1 gerente/jefe por puesto
                elif 'Especialista' in puesto.nombre or 'Analista' in puesto.nombre:
                    cantidad = random.randint(1, 2)  # 1-2 especialistas
                else:
                    cantidad = random.randint(2, 4)  # 2-4 empleados operativos
                
                for i in range(cantidad):
                    nombre = random.choice(nombres)
                    apellido_p = random.choice(apellidos_p)
                    apellido_m = random.choice(apellidos_m)
                    
                    # Generar email y teléfono únicos
                    email_base = f"{nombre.lower()}.{apellido_p.lower()}"
                    contador = 1
                    while Empleado.objects.filter(email=f"{email_base}@{puesto.departamento.planta.empresa.nombre.lower().replace(' ', '')}.com").exists():
                        email_base = f"{nombre.lower()}.{apellido_p.lower()}{contador}"
                        contador += 1
                    
                    empleado = Empleado.objects.create(
                        nombre=nombre,
                        apellido_paterno=apellido_p,
                        apellido_materno=apellido_m,
                        email=f"{email_base}@{puesto.departamento.planta.empresa.nombre.lower().replace(' ', '')}.com",
                        telefono=f"55-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                        fecha_ingreso=datetime.now().date() - timedelta(days=random.randint(30, 1825)),  # Entre 1 mes y 5 años
                        puesto=puesto,
                        status=True
                    )
                    empleados_creados.append(empleado)
            
            print(f"👥 Empleados creados: {len(empleados_creados)}")
            
            # 6. CREAR PLANES DE SUSCRIPCIÓN SI NO EXISTEN
            planes_data = [
                {
                    'nombre': 'Plan Básico',
                    'descripcion': 'Plan básico para pequeñas empresas',
                    'precio_mensual': 299.00,
                    'max_empleados': 50,
                    'max_plantas': 2,
                    'evaluaciones_personalizadas': False
                },
                {
                    'nombre': 'Plan Profesional', 
                    'descripcion': 'Plan profesional para medianas empresas',
                    'precio_mensual': 599.00,
                    'max_empleados': 200,
                    'max_plantas': 5,
                    'evaluaciones_personalizadas': True
                },
                {
                    'nombre': 'Plan Empresarial',
                    'descripcion': 'Plan empresarial para grandes corporaciones',
                    'precio_mensual': 1299.00,
                    'max_empleados': 1000,
                    'max_plantas': 20,
                    'evaluaciones_personalizadas': True
                }
            ]
            
            planes_creados = []
            for plan_info in planes_data:
                plan, created = PlanSuscripcion.objects.get_or_create(
                    nombre=plan_info['nombre'],
                    defaults=plan_info
                )
                if created:
                    planes_creados.append(plan)
            
            print(f"📋 Planes de suscripción creados: {len(planes_creados)}")
            
            # 7. ASIGNAR SUSCRIPCIONES A LAS EMPRESAS
            todas_empresas = Empresa.objects.all()
            todos_planes = PlanSuscripcion.objects.all()
            suscripciones_creadas = []
            
            for empresa in todas_empresas:
                # Verificar si ya tiene suscripción activa
                if not hasattr(empresa, 'suscripciones') or not empresa.suscripciones.filter(estado='Activa').exists():
                    plan = random.choice(todos_planes)
                    suscripcion = SuscripcionEmpresa.objects.create(
                        empresa=empresa,
                        plan=plan,
                        fecha_inicio=datetime.now().date(),
                        fecha_fin=datetime.now().date() + timedelta(days=365),
                        estado='Activa',
                        status=True
                    )
                    suscripciones_creadas.append(suscripcion)
                    print(f"💳 Suscripción creada: {plan.nombre} para {empresa.nombre}")
            
            print("\n🎉 ¡DATOS DE EJEMPLO CREADOS EXITOSAMENTE!")
            print("="*50)
            print(f"📊 Empresas totales: {Empresa.objects.count()}")
            print(f"🏢 Plantas totales: {Planta.objects.count()}")
            print(f"🏬 Departamentos totales: {Departamento.objects.count()}")
            print(f"💼 Puestos totales: {Puesto.objects.count()}")
            print(f"👥 Empleados totales: {Empleado.objects.count()}")
            print(f"👤 Usuarios totales: {PerfilUsuario.objects.count()}")
            print(f"📋 Planes totales: {PlanSuscripcion.objects.count()}")
            print(f"💳 Suscripciones totales: {SuscripcionEmpresa.objects.count()}")
            
    except Exception as e:
        print(f"❌ Error al crear datos: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_datos_ejemplo()
