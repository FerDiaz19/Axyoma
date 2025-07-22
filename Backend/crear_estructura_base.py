#!/usr/bin/env python3

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Planta, Departamento, Puesto

# Departamentos base que se crearán para cada planta
DEPARTAMENTOS_BASE = [
    {
        'nombre': 'Recursos Humanos',
        'descripcion': 'Departamento encargado de la gestión del personal y desarrollo organizacional'
    },
    {
        'nombre': 'Administración',
        'descripcion': 'Departamento de administración general y control interno'
    },
    {
        'nombre': 'Operaciones',
        'descripcion': 'Departamento de operaciones y procesos productivos'
    },
    {
        'nombre': 'Finanzas',
        'descripcion': 'Departamento de contabilidad y gestión financiera'
    },
    {
        'nombre': 'Ventas',
        'descripcion': 'Departamento de ventas y atención al cliente'
    }
]

# Puestos base por departamento (5 puestos por cada departamento)
PUESTOS_POR_DEPARTAMENTO = {
    'Recursos Humanos': [
        {'nombre': 'Gerente de RRHH', 'descripcion': 'Responsable de la gestión integral de recursos humanos'},
        {'nombre': 'Especialista en Reclutamiento', 'descripcion': 'Encargado del proceso de selección de personal'},
        {'nombre': 'Analista de Nómina', 'descripcion': 'Responsable del cálculo y procesamiento de nóminas'},
        {'nombre': 'Coordinador de Capacitación', 'descripcion': 'Encargado del desarrollo y capacitación del personal'},
        {'nombre': 'Asistente de RRHH', 'descripcion': 'Apoyo administrativo en actividades de recursos humanos'}
    ],
    'Administración': [
        {'nombre': 'Gerente Administrativo', 'descripcion': 'Responsable de la administración general de la empresa'},
        {'nombre': 'Coordinador de Servicios Generales', 'descripcion': 'Encargado del mantenimiento y servicios generales'},
        {'nombre': 'Analista Administrativo', 'descripcion': 'Apoyo en procesos administrativos y documentación'},
        {'nombre': 'Asistente Ejecutivo', 'descripcion': 'Asistente de dirección y coordinación ejecutiva'},
        {'nombre': 'Recepcionista', 'descripcion': 'Atención de recepción y servicios de comunicación'}
    ],
    'Operaciones': [
        {'nombre': 'Gerente de Operaciones', 'descripcion': 'Responsable de la coordinación de operaciones productivas'},
        {'nombre': 'Supervisor de Producción', 'descripcion': 'Supervisión directa de procesos productivos'},
        {'nombre': 'Operario Especializado', 'descripcion': 'Operario con especialización en procesos específicos'},
        {'nombre': 'Técnico de Calidad', 'descripcion': 'Control y aseguramiento de la calidad de productos'},
        {'nombre': 'Auxiliar de Operaciones', 'descripcion': 'Apoyo en actividades operativas generales'}
    ],
    'Finanzas': [
        {'nombre': 'Gerente Financiero', 'descripcion': 'Responsable de la gestión financiera y contable'},
        {'nombre': 'Contador General', 'descripcion': 'Encargado de la contabilidad general de la empresa'},
        {'nombre': 'Analista Financiero', 'descripcion': 'Análisis de estados financieros e indicadores'},
        {'nombre': 'Auxiliar Contable', 'descripcion': 'Apoyo en actividades contables y registros'},
        {'nombre': 'Tesorero', 'descripcion': 'Manejo de flujo de efectivo y operaciones bancarias'}
    ],
    'Ventas': [
        {'nombre': 'Gerente de Ventas', 'descripcion': 'Responsable de estrategias de ventas y objetivos comerciales'},
        {'nombre': 'Ejecutivo de Cuentas', 'descripcion': 'Gestión y desarrollo de cuentas clave'},
        {'nombre': 'Representante de Ventas', 'descripcion': 'Venta directa y atención a clientes'},
        {'nombre': 'Coordinador de Marketing', 'descripcion': 'Desarrollo de estrategias de marketing y promoción'},
        {'nombre': 'Asistente Comercial', 'descripcion': 'Apoyo en actividades comerciales y ventas'}
    ]
}

def crear_departamentos_y_puestos_para_planta(planta):
    """Crear departamentos y puestos base para una planta específica"""
    print(f"\n🏭 Creando estructura para planta: {planta.nombre}")
    
    departamentos_creados = 0
    puestos_creados = 0
    
    for dept_data in DEPARTAMENTOS_BASE:
        # Verificar si ya existe el departamento
        departamento, created = Departamento.objects.get_or_create(
            nombre=dept_data['nombre'],
            planta=planta,
            defaults={
                'descripcion': dept_data['descripcion'],
                'status': True
            }
        )
        
        if created:
            departamentos_creados += 1
            print(f"   📁 Departamento creado: {departamento.nombre}")
        else:
            print(f"   📁 Departamento ya existe: {departamento.nombre}")
        
        # Crear puestos para este departamento
        puestos_dept = PUESTOS_POR_DEPARTAMENTO.get(dept_data['nombre'], [])
        for puesto_data in puestos_dept:
            puesto, created = Puesto.objects.get_or_create(
                nombre=puesto_data['nombre'],
                departamento=departamento,
                defaults={
                    'descripcion': puesto_data['descripcion'],
                    'status': True
                }
            )
            
            if created:
                puestos_creados += 1
                print(f"      💼 Puesto creado: {puesto.nombre}")
            else:
                print(f"      💼 Puesto ya existe: {puesto.nombre}")
    
    print(f"   ✅ Resumen: {departamentos_creados} departamentos y {puestos_creados} puestos creados")
    return departamentos_creados, puestos_creados

def crear_estructura_base_todas_plantas():
    """Crear departamentos y puestos base para todas las plantas existentes"""
    print("🚀 === CREANDO ESTRUCTURA BASE PARA TODAS LAS PLANTAS ===")
    
    plantas = Planta.objects.filter(status=True)
    print(f"📊 Plantas encontradas: {plantas.count()}")
    
    total_departamentos = 0
    total_puestos = 0
    
    for planta in plantas:
        dept_creados, puestos_creados = crear_departamentos_y_puestos_para_planta(planta)
        total_departamentos += dept_creados
        total_puestos += puestos_creados
    
    print(f"\n🎉 === PROCESO COMPLETADO ===")
    print(f"📊 Total departamentos creados: {total_departamentos}")
    print(f"💼 Total puestos creados: {total_puestos}")
    print(f"🏭 Plantas procesadas: {plantas.count()}")
    
    # Mostrar estadísticas finales
    print(f"\n📈 === ESTADÍSTICAS FINALES ===")
    print(f"🏢 Total departamentos en sistema: {Departamento.objects.count()}")
    print(f"💼 Total puestos en sistema: {Puesto.objects.count()}")
    print(f"🏭 Total plantas activas: {Planta.objects.filter(status=True).count()}")

if __name__ == '__main__':
    crear_estructura_base_todas_plantas()
