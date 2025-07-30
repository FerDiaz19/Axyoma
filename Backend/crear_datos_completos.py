#!/usr/bin/env python
"""
Script para crear datos de prueba completos para Axyoma
Incluye: Empresa, Plantas, Departamentos, Puestos y Empleados enlazados
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import (
    PerfilUsuario, Empresa, Planta, AdminPlanta, 
    Departamento, Puesto, Empleado
)

def crear_datos_empresa_completa():
    """Crear una empresa completa con estructura organizacional"""
    print("\n🏢 CREANDO EMPRESA DEMO CON ESTRUCTURA COMPLETA")
    print("=" * 70)
    
    # Verificar que existe admin_empresa
    try:
        admin_user = User.objects.get(username='admin_empresa')
        admin_perfil = admin_user.perfil
    except User.DoesNotExist:
        print("❌ Usuario admin_empresa no encontrado. Ejecuta crear_usuarios_prueba.py primero")
        return False
    
    # 1. EMPRESA PRINCIPAL
    try:
        # Verificar si ya existe una empresa con este admin
        empresa_existente = Empresa.objects.filter(administrador=admin_perfil).first()
        if empresa_existente:
            print(f"⚠️ Actualizando empresa existente: {empresa_existente.nombre}")
            # Actualizar datos de la empresa existente
            empresa_existente.nombre = 'TechnoMex Industries'
            empresa_existente.rfc = 'TMI950815AB2'
            empresa_existente.direccion = 'Blvd. Tecnológico #2000, Parque Industrial Norte, Querétaro, Qro. 76120'
            empresa_existente.email_contacto = 'contacto@technomex.com.mx'
            empresa_existente.telefono_contacto = '4421234567'
            empresa_existente.status = True
            empresa_existente.save()
            empresa = empresa_existente
            print(f"✅ Empresa actualizada: {empresa.nombre}")
        else:
            empresa = Empresa.objects.create(
                nombre='TechnoMex Industries',
                rfc='TMI950815AB2',
                direccion='Blvd. Tecnológico #2000, Parque Industrial Norte, Querétaro, Qro. 76120',
                email_contacto='contacto@technomex.com.mx',
                telefono_contacto='4421234567',
                administrador=admin_perfil,
                status=True
            )
            print(f"✅ Empresa creada: {empresa.nombre}")
    except Exception as e:
        print(f"❌ Error creando empresa: {e}")
        return False
    
    # 2. PLANTAS DE LA EMPRESA
    plantas_data = [
        {
            'nombre': 'Planta Querétaro Centro',
            'direccion': 'Av. Constituyentes #850, Centro Histórico, Querétaro, Qro. 76000'
        },
        {
            'nombre': 'Planta El Marqués',
            'direccion': 'Carr. Querétaro-México Km. 45, El Marqués, Qro. 76240'
        },
        {
            'nombre': 'Planta San Juan del Río',
            'direccion': 'Zona Industrial La Noria, San Juan del Río, Qro. 76800'
        }
    ]
    
    plantas_creadas = []
    for planta_info in plantas_data:
        try:
            planta, created = Planta.objects.get_or_create(
                nombre=planta_info['nombre'],
                empresa=empresa,
                defaults={
                    'direccion': planta_info['direccion'],
                    'status': True
                }
            )
            plantas_creadas.append(planta)
            if created:
                print(f"✅ Planta creada: {planta.nombre}")
            else:
                print(f"⚠️ Planta ya existe: {planta.nombre}")
        except Exception as e:
            print(f"❌ Error creando planta {planta_info['nombre']}: {e}")
    
    # 3. DEPARTAMENTOS POR PLANTA
    departamentos_base = [
        {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del talento humano y desarrollo organizacional'},
        {'nombre': 'Producción', 'descripcion': 'Operaciones de manufactura y control de calidad'},
        {'nombre': 'Mantenimiento', 'descripcion': 'Mantenimiento preventivo y correctivo de equipos'},
        {'nombre': 'Calidad', 'descripcion': 'Control de calidad y sistemas de gestión'},
        {'nombre': 'Almacén', 'descripcion': 'Logística, inventarios y distribución'},
        {'nombre': 'Administración', 'descripcion': 'Finanzas, contabilidad y administración general'},
        {'nombre': 'Sistemas', 'descripcion': 'Tecnologías de información y automatización'},
    ]
    
    departamentos_creados = []
    for planta in plantas_creadas:
        print(f"\n📋 Creando departamentos para {planta.nombre}:")
        for dept_info in departamentos_base:
            try:
                departamento, created = Departamento.objects.get_or_create(
                    nombre=dept_info['nombre'],
                    planta=planta,
                    defaults={
                        'descripcion': dept_info['descripcion'],
                        'status': True
                    }
                )
                departamentos_creados.append(departamento)
                if created:
                    print(f"  ✅ {departamento.nombre}")
                else:
                    print(f"  ⚠️ {departamento.nombre} (ya existe)")
            except Exception as e:
                print(f"  ❌ Error creando departamento {dept_info['nombre']}: {e}")
    
    # 4. PUESTOS POR DEPARTAMENTO
    puestos_por_departamento = {
        'Recursos Humanos': [
            {'nombre': 'Director de RH', 'descripcion': 'Dirección estratégica de recursos humanos'},
            {'nombre': 'Gerente de RH', 'descripcion': 'Gestión operativa de recursos humanos'},
            {'nombre': 'Especialista en Reclutamiento', 'descripcion': 'Reclutamiento y selección de personal'},
            {'nombre': 'Analista de Nómina', 'descripcion': 'Procesamiento de nómina y beneficios'},
            {'nombre': 'Capacitador', 'descripcion': 'Desarrollo y capacitación del personal'},
        ],
        'Producción': [
            {'nombre': 'Gerente de Producción', 'descripcion': 'Coordinación general de producción'},
            {'nombre': 'Supervisor de Línea', 'descripcion': 'Supervisión directa de líneas productivas'},
            {'nombre': 'Operador de Máquina', 'descripcion': 'Operación de maquinaria industrial'},
            {'nombre': 'Técnico de Proceso', 'descripcion': 'Optimización de procesos productivos'},
            {'nombre': 'Inspector de Calidad', 'descripcion': 'Control de calidad en línea'},
        ],
        'Mantenimiento': [
            {'nombre': 'Jefe de Mantenimiento', 'descripcion': 'Coordinación de mantenimiento general'},
            {'nombre': 'Técnico Mecánico', 'descripcion': 'Mantenimiento mecánico de equipos'},
            {'nombre': 'Técnico Eléctrico', 'descripcion': 'Mantenimiento eléctrico e instrumentación'},
            {'nombre': 'Soldador', 'descripcion': 'Trabajos de soldadura y reparación'},
        ],
        'Calidad': [
            {'nombre': 'Gerente de Calidad', 'descripcion': 'Gestión del sistema de calidad'},
            {'nombre': 'Auditor Interno', 'descripcion': 'Auditorías internas de calidad'},
            {'nombre': 'Técnico de Laboratorio', 'descripcion': 'Análisis de laboratorio y pruebas'},
        ],
        'Almacén': [
            {'nombre': 'Jefe de Almacén', 'descripcion': 'Coordinación de almacén y logística'},
            {'nombre': 'Almacenista', 'descripcion': 'Manejo de inventarios y materiales'},
            {'nombre': 'Montacarguista', 'descripcion': 'Operación de montacargas y equipo'},
        ],
        'Administración': [
            {'nombre': 'Gerente Administrativo', 'descripcion': 'Gestión administrativa general'},
            {'nombre': 'Contador', 'descripcion': 'Contabilidad y estados financieros'},
            {'nombre': 'Auxiliar Contable', 'descripcion': 'Apoyo en procesos contables'},
            {'nombre': 'Recepcionista', 'descripcion': 'Atención al público y recepción'},
        ],
        'Sistemas': [
            {'nombre': 'Jefe de Sistemas', 'descripcion': 'Coordinación de TI y automatización'},
            {'nombre': 'Programador', 'descripcion': 'Desarrollo de software y sistemas'},
            {'nombre': 'Soporte Técnico', 'descripcion': 'Soporte técnico a usuarios'},
        ]
    }
    
    puestos_creados = []
    for departamento in departamentos_creados:
        if departamento.nombre in puestos_por_departamento:
            print(f"\n💼 Creando puestos para {departamento.nombre} - {departamento.planta.nombre}:")
            for puesto_info in puestos_por_departamento[departamento.nombre]:
                try:
                    puesto, created = Puesto.objects.get_or_create(
                        nombre=puesto_info['nombre'],
                        departamento=departamento,
                        defaults={
                            'descripcion': puesto_info['descripcion'],
                            'status': True
                        }
                    )
                    puestos_creados.append(puesto)
                    if created:
                        print(f"  ✅ {puesto.nombre}")
                    else:
                        print(f"  ⚠️ {puesto.nombre} (ya existe)")
                except Exception as e:
                    print(f"  ❌ Error creando puesto {puesto_info['nombre']}: {e}")
    
    # 5. EMPLEADOS PARA TODOS LOS PUESTOS
    nombres_masculinos = [
        'Juan Carlos', 'Miguel Ángel', 'José Luis', 'Francisco', 'Roberto', 'Ricardo', 'Alejandro',
        'Fernando', 'Eduardo', 'Raúl', 'Sergio', 'Andrés', 'Daniel', 'Carlos', 'David'
    ]
    nombres_femeninos = [
        'María Elena', 'Ana Patricia', 'Claudia', 'Patricia', 'Mónica', 'Sandra', 'Leticia',
        'Gabriela', 'Adriana', 'Silvia', 'Rosa María', 'Carmen', 'Beatriz', 'Lucía', 'Verónica'
    ]
    apellidos = [
        'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Hernández', 'Pérez', 'Sánchez',
        'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez', 'Díaz', 'Cruz', 'Morales', 'Ortiz',
        'Gutiérrez', 'Vargas', 'Castillo', 'Jiménez', 'Romero', 'Ruiz', 'Herrera', 'Medina'
    ]
    
    empleados_creados = 0
    print(f"\n👥 CREANDO EMPLEADOS:")
    print("=" * 50)
    
    for puesto in puestos_creados:
        # Determinar número de empleados por puesto
        empleados_por_puesto = 1
        if 'Operador' in puesto.nombre or 'Almacenista' in puesto.nombre:
            empleados_por_puesto = random.randint(3, 6)
        elif 'Técnico' in puesto.nombre or 'Inspector' in puesto.nombre:
            empleados_por_puesto = random.randint(2, 4)
        elif 'Auxiliar' in puesto.nombre or 'Analista' in puesto.nombre:
            empleados_por_puesto = random.randint(1, 3)
        
        for i in range(empleados_por_puesto):
            try:
                # Seleccionar nombre aleatoriamente
                es_masculino = random.choice([True, False])
                nombre = random.choice(nombres_masculinos if es_masculino else nombres_femeninos)
                apellido_paterno = random.choice(apellidos)
                apellido_materno = random.choice(apellidos)
                
                # Generar email y teléfono
                nombre_clean = nombre.lower().replace(' ', '.')
                apellido_clean = apellido_paterno.lower()
                email = f"{nombre_clean}.{apellido_clean}@technomex.com.mx"
                telefono = f"442{random.randint(1000000, 9999999)}"
                
                # Fecha de ingreso aleatoria (últimos 5 años)
                fecha_ingreso = date.today() - timedelta(days=random.randint(30, 1825))
                
                empleado, created = Empleado.objects.get_or_create(
                    email=email,
                    defaults={
                        'nombre': nombre,
                        'apellido_paterno': apellido_paterno,
                        'apellido_materno': apellido_materno,
                        'telefono': telefono,
                        'fecha_ingreso': fecha_ingreso,
                        'puesto': puesto,
                        'status': True
                    }
                )
                
                if created:
                    empleados_creados += 1
                    print(f"✅ {empleado.nombre} {empleado.apellido_paterno} - {puesto.nombre} ({puesto.departamento.nombre}, {puesto.departamento.planta.nombre})")
                
            except Exception as e:
                print(f"❌ Error creando empleado para {puesto.nombre}: {e}")
    
    # 6. ASIGNAR ADMIN DE PLANTA
    try:
        admin_planta_user = User.objects.get(username='admin_planta')
        admin_planta_perfil = admin_planta_user.perfil
        
        # Asignar a la primera planta creada
        if plantas_creadas:
            planta_principal = plantas_creadas[0]
            admin_assignment, created = AdminPlanta.objects.get_or_create(
                usuario=admin_planta_perfil,
                planta=planta_principal,
                defaults={'status': True}
            )
            if created:
                print(f"\n✅ Admin de planta asignado a: {planta_principal.nombre}")
            else:
                print(f"\n⚠️ Admin de planta ya estaba asignado a: {planta_principal.nombre}")
    except Exception as e:
        print(f"\n❌ Error asignando admin de planta: {e}")
    
    # RESUMEN FINAL
    print(f"\n🎯 RESUMEN DE DATOS CREADOS:")
    print("=" * 50)
    print(f"🏢 Empresa: {empresa.nombre}")
    print(f"🏭 Plantas creadas: {len(plantas_creadas)}")
    print(f"📋 Departamentos creados: {len(departamentos_creados)}")
    print(f"💼 Puestos creados: {len(puestos_creados)}")
    print(f"👥 Empleados creados: {empleados_creados}")
    print("=" * 50)
    
    # Mostrar estructura por planta
    for planta in plantas_creadas:
        print(f"\n🏭 {planta.nombre}:")
        departamentos_planta = [d for d in departamentos_creados if d.planta == planta]
        for dept in departamentos_planta:
            puestos_dept = [p for p in puestos_creados if p.departamento == dept]
            empleados_dept = sum([Empleado.objects.filter(puesto__departamento=dept).count() for p in puestos_dept])
            print(f"  📋 {dept.nombre}: {len(puestos_dept)} puestos, {empleados_dept} empleados")
    
    return True

if __name__ == "__main__":
    crear_datos_empresa_completa()
