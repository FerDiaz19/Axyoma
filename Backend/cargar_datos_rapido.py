#!/usr/bin/env python
"""
📊 CARGAR DATOS INICIALES - RAPIDO
=================================
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

def main():
    print('📊 CREANDO DATOS INICIALES...')
    
    from django.contrib.auth.models import User
    from apps.users.models import Empresa, Planta, Departamento, Puesto, Empleado, PerfilUsuario, AdminPlanta
    from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
    from django.db import transaction
    from datetime import date, timedelta
    
    with transaction.atomic():
        # 1. Usuarios REALES con contraseñas
        users_data = [
            {'username': 'superadmin', 'email': 'super@axyoma.com', 'password': '1234', 'staff': True, 'super': True},
            {'username': 'admin_empresa', 'email': 'admin@empresa.com', 'password': '1234', 'staff': False, 'super': False},
            {'username': 'admin_planta', 'email': 'admin@planta.com', 'password': '1234', 'staff': False, 'super': False},
        ]
        
        usuarios_creados = []
        for user_data in users_data:
            # Crear usuario directo (sin eliminar)
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
                usuarios_creados.append(user)
                print(f'✅ Usuario REAL: {user.username} / {user_data["password"]}')
            else:
                usuarios_creados.append(user)
                print(f'🔄 Usuario existente: {user.username}')
        
        # 2. PerfilUsuario para cada usuario
        perfiles_creados = []
        for user, user_data in zip(usuarios_creados, users_data):
            # Crear PerfilUsuario con correo único
            perfil, created = PerfilUsuario.objects.get_or_create(
                user=user,
                defaults={
                    'nombre': user.username.title(),
                    'apellido_paterno': 'Sistema',
                    'correo': user_data['email'],  # Usar el email del usuario
                    'nivel_usuario': user_data['username']
                }
            )
            perfiles_creados.append(perfil)
            if created:
                print(f'✅ PerfilUsuario: {perfil.nombre} {perfil.apellido_paterno}')
        
        # 3. Empresa con administrador
        admin_perfil = next(p for p in perfiles_creados if p.user.username == 'admin_empresa')
        
        empresa, created = Empresa.objects.get_or_create(
            nombre='Empresa Demo AXYOMA',
            defaults={
                'rfc': 'EDA123456789',
                'direccion': 'Av. Principal 123',
                'email_contacto': 'contacto@demo.com',
                'telefono_contacto': '555-0123',
                'status': True,
                'administrador': admin_perfil
            }
        )
        if created:
            print(f'✅ Empresa: {empresa.nombre} (Admin: {admin_perfil.user.username})')
        
        # 4. Plantas con AdminPlanta
        plantas_data = [
            {'nombre': 'Planta Norte', 'direccion': 'Zona Norte'},
            {'nombre': 'Planta Sur', 'direccion': 'Zona Sur'},
        ]
        
        plantas_creadas = []
        admin_planta_perfil = next(p for p in perfiles_creados if p.user.username == 'admin_planta')
        
        for i, planta_data in enumerate(plantas_data):
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
                
                # Crear AdminPlanta para la primera planta
                if i == 0:  # Solo para la primera planta
                    admin_planta, admin_created = AdminPlanta.objects.get_or_create(
                        admin=admin_planta_perfil,
                        planta=planta,
                        defaults={'status': True}
                    )
                    if admin_created:
                        print(f'✅ AdminPlanta: {admin_planta_perfil.user.username} administra {planta.nombre}')
        
        # 5. Departamentos
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
        
        # 6. Puestos
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
        
        # 7. Empleados COMPLETOS (más empleados para todas las áreas)
        empleados_data = [
            # RH
            {'nombre': 'Juan Carlos', 'apellido': 'Pérez', 'area': 'Recursos Humanos'},
            {'nombre': 'María Elena', 'apellido': 'García', 'area': 'Recursos Humanos'},
            {'nombre': 'Roberto', 'apellido': 'Hernández', 'area': 'Recursos Humanos'},
            # Producción
            {'nombre': 'Carlos Alberto', 'apellido': 'López', 'area': 'Producción'},
            {'nombre': 'Ana Sofía', 'apellido': 'Martínez', 'area': 'Producción'},
            {'nombre': 'Miguel Angel', 'apellido': 'Rodríguez', 'area': 'Producción'},
            {'nombre': 'Laura Patricia', 'apellido': 'González', 'area': 'Producción'},
            {'nombre': 'José Luis', 'apellido': 'Morales', 'area': 'Producción'},
            # Calidad
            {'nombre': 'Diana Cristina', 'apellido': 'Ramírez', 'area': 'Calidad'},
            {'nombre': 'Fernando', 'apellido': 'Castro', 'area': 'Calidad'},
            {'nombre': 'Sandra Milena', 'apellido': 'Vargas', 'area': 'Calidad'},
            {'nombre': 'Andrés Felipe', 'apellido': 'Torres', 'area': 'Calidad'},
        ]
        
        empleados_creados = []
        for emp_data in empleados_data:
            # Buscar puestos disponibles del área correspondiente
            puestos_area = [p for p in puestos_creados if emp_data['area'] in p.departamento.nombre]
            if puestos_area:
                # Rotar entre los puestos disponibles
                puesto = puestos_area[len(empleados_creados) % len(puestos_area)]
                
                empleado, created = Empleado.objects.get_or_create(
                    nombre=emp_data['nombre'],
                    apellido_paterno=emp_data['apellido'],
                    puesto=puesto,
                    defaults={
                        'apellido_materno': 'Demo',
                        'email': f'{emp_data["nombre"].lower().replace(" ", "")}@demo.com',
                        'telefono': f'555-{1000 + len(empleados_creados)}',
                        'status': True
                    }
                )
                if created:
                    empleados_creados.append(empleado)
                    print(f'✅ Empleado: {empleado.nombre} {empleado.apellido_paterno} - {puesto.nombre} en {puesto.departamento.nombre}')

        # 8. Planes de Suscripción
        planes_data = [
            {
                'nombre': 'Plan Básico',
                'descripcion': 'Plan ideal para empresas pequeñas',
                'precio': 999.00,
                'duracion': 30,
                'limite_empleados': 50,
                'limite_plantas': 2,
                'caracteristicas': 'Gestión básica de empleados, 2 plantas máximo, soporte por email'
            },
            {
                'nombre': 'Plan Profesional',
                'descripcion': 'Plan completo para empresas medianas',
                'precio': 1999.00,
                'duracion': 30,
                'limite_empleados': 200,
                'limite_plantas': 5,
                'caracteristicas': 'Gestión completa, hasta 5 plantas, reportes avanzados, soporte prioritario'
            },
            {
                'nombre': 'Plan Empresarial',
                'descripcion': 'Sin límites para grandes corporaciones',
                'precio': 4999.00,
                'duracion': 30,
                'limite_empleados': None,
                'limite_plantas': None,
                'caracteristicas': 'Sin límites, múltiples plantas, API completa, soporte 24/7'
            }
        ]
        
        planes_creados = []
        for plan_data in planes_data:
            plan, created = PlanSuscripcion.objects.get_or_create(
                nombre=plan_data['nombre'],
                defaults=plan_data
            )
            if created:
                planes_creados.append(plan)
                print(f'✅ Plan: {plan.nombre} - ${plan.precio}')

        # 9. Suscripción Activa para la empresa
        if planes_creados:
            plan_profesional = next((p for p in planes_creados if 'Profesional' in p.nombre), planes_creados[0])
            
            fecha_inicio = date.today()
            fecha_fin = fecha_inicio + timedelta(days=plan_profesional.duracion)
            
            suscripcion, created = SuscripcionEmpresa.objects.get_or_create(
                empresa=empresa,
                plan_suscripcion=plan_profesional,
                defaults={
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'estado': 'Activa',
                    'status': True
                }
            )
            if created:
                print(f'✅ Suscripción: {empresa.nombre} - {plan_profesional.nombre} (Activa hasta {fecha_fin})')

    print('')
    print('🎉 DATOS INICIALES COMPLETOS CREADOS EXITOSAMENTE')
    print('')
    print('� ESTADÍSTICAS:')
    print(f'• Usuarios: 3')
    print(f'• Empresa: 1 (con suscripción activa)')
    print(f'• Plantas: 2')  
    print(f'• Departamentos: 6 (3 por planta)')
    print(f'• Puestos: 24 (4 por departamento)')
    print(f'• Empleados: 12+ (distribuidos en todas las áreas)')
    print(f'• Planes de suscripción: 3')
    print('')
    print('�👤 USUARIOS DISPONIBLES:')
    print('• superadmin / 1234 (Acceso total)')
    print('• admin_empresa / 1234 (Gestión empresarial)')  
    print('• admin_planta / 1234 (Gestión de planta)')
    print('')
    print('🏢 ESTRUCTURA ORGANIZACIONAL COMPLETA:')
    print('• Empresa Demo AXYOMA')
    print('  ├── Planta Norte & Planta Sur')
    print('  ├── Departamentos: RH, Producción, Calidad')
    print('  ├── Puestos: Gerente, Supervisor, Analista, Operario')
    print('  └── Empleados distribuidos en todas las áreas')
    print('')

if __name__ == "__main__":
    main()
