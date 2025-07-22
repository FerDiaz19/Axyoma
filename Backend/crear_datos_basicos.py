#!/usr/bin/env python
"""
Script simplificado para crear datos de ejemplo para el dashboard SuperAdmin
Solo incluye: empresas, plantas, departamentos, puestos y empleados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from datetime import datetime, timedelta
import random

def crear_datos_basicos():
    """Crear datos básicos para pruebas del dashboard"""
    
    print("🚀 Creando datos básicos para SuperAdmin dashboard...")
    
    try:
        with transaction.atomic():
            # 1. VERIFICAR EMPRESAS EXISTENTES
            empresas_existentes = Empresa.objects.count()
            print(f"📊 Empresas existentes: {empresas_existentes}")
            
            # 2. AGREGAR MÁS EMPLEADOS A LA EMPRESA EXISTENTE
            empresa_actual = Empresa.objects.first()
            if empresa_actual:
                print(f"🏢 Trabajando con empresa: {empresa_actual.nombre}")
                
                # Obtener plantas de la empresa actual
                plantas = Planta.objects.filter(empresa=empresa_actual)
                print(f"🏭 Plantas encontradas: {plantas.count()}")
                
                nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Carmen', 'José', 'Elena', 'Miguel', 'Rosa', 
                          'Pedro', 'Lucia', 'Fernando', 'Sofia', 'Diego', 'Patricia', 'Ricardo', 'Valeria', 'Andrés', 'Isabel']
                apellidos_p = ['García', 'Rodríguez', 'López', 'Martínez', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Cruz', 'Torres',
                              'Flores', 'Morales', 'Jiménez', 'Ruiz', 'Díaz', 'Vargas', 'Castro', 'Ortiz', 'Ramos', 'Mendoza']
                apellidos_m = ['Hernández', 'Morales', 'Jiménez', 'Ruiz', 'Díaz', 'Vargas', 'Castro', 'Ortiz', 'Ramos', 'Mendoza',
                              'Silva', 'Herrera', 'Medina', 'Aguilar', 'Gutiérrez', 'Rojas', 'Vega', 'Peña', 'Muñoz', 'Campos']
                
                empleados_agregados = 0
                
                for planta in plantas:
                    departamentos = Departamento.objects.filter(planta=planta)
                    print(f"  📁 Departamentos en {planta.nombre}: {departamentos.count()}")
                    
                    for departamento in departamentos:
                        puestos = Puesto.objects.filter(departamento=departamento)
                        print(f"    💼 Puestos en {departamento.nombre}: {puestos.count()}")
                        
                        for puesto in puestos:
                            empleados_actuales = Empleado.objects.filter(puesto=puesto).count()
                            
                            # Agregar más empleados si hay pocos
                            if empleados_actuales < 2:
                                empleados_a_agregar = random.randint(2, 5)  # Entre 2-5 empleados por puesto
                                
                                for i in range(empleados_a_agregar):
                                    nombre = random.choice(nombres)
                                    apellido_p = random.choice(apellidos_p)
                                    apellido_m = random.choice(apellidos_m)
                                    
                                    # Generar email único
                                    email_base = f"{nombre.lower()}.{apellido_p.lower()}"
                                    contador = 1
                                    email = f"{email_base}@codewave.com"
                                    while Empleado.objects.filter(email=email).exists():
                                        email = f"{email_base}{contador}@codewave.com"
                                        contador += 1
                                    
                                    empleado = Empleado.objects.create(
                                        nombre=nombre,
                                        apellido_paterno=apellido_p,
                                        apellido_materno=apellido_m,
                                        email=email,
                                        telefono=f"66-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                                        fecha_ingreso=datetime.now().date() - timedelta(days=random.randint(30, 1095)),  # Entre 1 mes y 3 años
                                        puesto=puesto,
                                        status=True
                                    )
                                    empleados_agregados += 1
                                    
                                print(f"      👥 Empleados agregados al puesto {puesto.nombre}: {empleados_a_agregar}")
                
                print(f"✅ Total empleados agregados: {empleados_agregados}")
                
                # 3. AGREGAR DEPARTAMENTOS FALTANTES SI ES NECESARIO
                departamentos_sugeridos = ['IT Support', 'Seguridad', 'Limpieza', 'Recepción']
                
                for planta in plantas:
                    for nombre_dept in departamentos_sugeridos:
                        dept, created = Departamento.objects.get_or_create(
                            nombre=nombre_dept,
                            planta=planta,
                            defaults={
                                'descripcion': f'Departamento de {nombre_dept} - {planta.nombre}',
                                'status': True
                            }
                        )
                        
                        if created:
                            print(f"🏬 Departamento creado: {nombre_dept} en {planta.nombre}")
                            
                            # Crear puestos para el nuevo departamento
                            if nombre_dept == 'IT Support':
                                puestos_nuevos = ['Técnico de Soporte', 'Administrador de Sistemas']
                            elif nombre_dept == 'Seguridad':
                                puestos_nuevos = ['Guardia de Seguridad', 'Supervisor de Seguridad']
                            elif nombre_dept == 'Limpieza':
                                puestos_nuevos = ['Personal de Limpieza', 'Supervisor de Limpieza']
                            else:  # Recepción
                                puestos_nuevos = ['Recepcionista', 'Asistente Administrativo']
                            
                            for nombre_puesto in puestos_nuevos:
                                puesto = Puesto.objects.create(
                                    nombre=nombre_puesto,
                                    departamento=dept,
                                    descripcion=f'{nombre_puesto} del departamento {nombre_dept}',
                                    status=True
                                )
                                
                                # Agregar empleados al nuevo puesto
                                for j in range(random.randint(1, 3)):
                                    nombre = random.choice(nombres)
                                    apellido_p = random.choice(apellidos_p)
                                    apellido_m = random.choice(apellidos_m)
                                    
                                    email_base = f"{nombre.lower()}.{apellido_p.lower()}"
                                    contador = 1
                                    email = f"{email_base}@codewave.com"
                                    while Empleado.objects.filter(email=email).exists():
                                        email = f"{email_base}{contador}@codewave.com"
                                        contador += 1
                                    
                                    Empleado.objects.create(
                                        nombre=nombre,
                                        apellido_paterno=apellido_p,
                                        apellido_materno=apellido_m,
                                        email=email,
                                        telefono=f"66-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                                        fecha_ingreso=datetime.now().date() - timedelta(days=random.randint(30, 730)),
                                        puesto=puesto,
                                        status=True
                                    )
                                    empleados_agregados += 1
            
            print("\n🎉 ¡DATOS BÁSICOS CREADOS EXITOSAMENTE!")
            print("="*50)
            print(f"📊 Empresas totales: {Empresa.objects.count()}")
            print(f"🏢 Plantas totales: {Planta.objects.count()}")
            print(f"🏬 Departamentos totales: {Departamento.objects.count()}")
            print(f"💼 Puestos totales: {Puesto.objects.count()}")
            print(f"👥 Empleados totales: {Empleado.objects.count()}")
            print(f"👤 Usuarios totales: {PerfilUsuario.objects.count()}")
            
            # Mostrar desglose detallado
            print("\n📋 DESGLOSE POR EMPRESA:")
            for empresa in Empresa.objects.all():
                plantas_count = Planta.objects.filter(empresa=empresa).count()
                departamentos_count = Departamento.objects.filter(planta__empresa=empresa).count()
                puestos_count = Puesto.objects.filter(departamento__planta__empresa=empresa).count()
                empleados_count = Empleado.objects.filter(puesto__departamento__planta__empresa=empresa).count()
                
                print(f"🏢 {empresa.nombre}:")
                print(f"   Plantas: {plantas_count}")
                print(f"   Departamentos: {departamentos_count}")
                print(f"   Puestos: {puestos_count}")
                print(f"   Empleados: {empleados_count}")
                
                for planta in Planta.objects.filter(empresa=empresa):
                    empleados_planta = Empleado.objects.filter(puesto__departamento__planta=planta).count()
                    print(f"     🏭 {planta.nombre}: {empleados_planta} empleados")
            
    except Exception as e:
        print(f"❌ Error al crear datos: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_datos_basicos()
