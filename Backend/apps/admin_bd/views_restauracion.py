# -*- coding: utf-8 -*-
"""
🔄 VIEWS DE RESTAURACIÓN - SISTEMA AXYOMA
==========================================

Endpoints específicos para la pestaña de restauración en gestión de BD.
Incluye funciones para reiniciar BD y cargar datos demo.

📋 Responsable: Yael Contreras  
📅 Fecha: Agosto 2025
🔢 Versión: 1.0

🚀 Funcionalidades:
- Reiniciar BD (borrar datos, mantener estructura)
- Cargar datos demo mínimos para funcionamiento
- Sistema de confirmación de seguridad
- Logs detallados de operaciones

🔒 Seguridad: Solo SuperAdmin
"""

import os
import json
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import (
    PerfilUsuario, Empresa, Planta, Departamento, 
    Puesto, Empleado, AdminPlanta
)
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from .models import LogRespaldo


def verificar_superadmin(request):
    """Verificar que el usuario es SuperAdmin"""
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return False, Response({'error': 'Solo SuperAdmin puede gestionar restauración'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return True, None
    except Exception as e:
        return False, Response({'error': f'Error de autenticación: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reiniciar_bd_cero(request):
    """
    🗑️ REINICIAR BASE DE DATOS - Borrar todos los datos, mantener estructura
    
    Elimina todos los datos pero mantiene:
    - Estructura de tablas
    - Migraciones de Django
    - Superusuario admin
    """
    is_superadmin, error_response = verificar_superadmin(request)
    if not is_superadmin:
        return error_response
    
    confirmacion = request.data.get('confirmacion', '')
    if confirmacion != 'CONFIRMO_REINICIAR_BD':
        return Response({'error': 'Confirmación requerida'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        registros_eliminados = {}
        
        with transaction.atomic():
            print("🔥 INICIANDO REINICIO DE BASE DE DATOS...")
            
            # 1. Eliminar datos en orden inverso (respetando FK)
            
            # Logs y configuraciones admin_bd
            print("Eliminando logs de respaldos...")
            count = LogRespaldo.objects.count()
            LogRespaldo.objects.all().delete()
            registros_eliminados['logs_respaldos'] = count
            
            # Suscripciones y pagos
            print("Eliminando pagos...")
            count = Pago.objects.count()
            Pago.objects.all().delete()
            registros_eliminados['pagos'] = count
            
            print("Eliminando suscripciones...")
            count = SuscripcionEmpresa.objects.count()
            SuscripcionEmpresa.objects.all().delete()
            registros_eliminados['suscripciones'] = count
            
            print("Eliminando planes...")
            count = PlanSuscripcion.objects.count()
            PlanSuscripcion.objects.all().delete()
            registros_eliminados['planes'] = count
            
            # Empleados y estructura organizacional
            print("Eliminando empleados...")
            count = Empleado.objects.count()
            Empleado.objects.all().delete()
            registros_eliminados['empleados'] = count
            
            print("Eliminando admins de planta...")
            count = AdminPlanta.objects.count()
            AdminPlanta.objects.all().delete()
            registros_eliminados['admins_planta'] = count
            
            print("Eliminando puestos...")
            count = Puesto.objects.count()
            Puesto.objects.all().delete()
            registros_eliminados['puestos'] = count
            
            print("Eliminando departamentos...")
            count = Departamento.objects.count()
            Departamento.objects.all().delete()
            registros_eliminados['departamentos'] = count
            
            print("Eliminando plantas...")
            count = Planta.objects.count()
            Planta.objects.all().delete()
            registros_eliminados['plantas'] = count
            
            print("Eliminando empresas...")
            count = Empresa.objects.count()
            Empresa.objects.all().delete()
            registros_eliminados['empresas'] = count
            
            # Usuarios (excepto superuser admin)
            print("Eliminando usuarios (excepto admin)...")
            usuarios_a_eliminar = User.objects.exclude(username='admin')
            count = usuarios_a_eliminar.count()
            usuarios_a_eliminar.delete()
            registros_eliminados['usuarios'] = count
            
            # Perfiles (excepto admin)
            print("Eliminando perfiles (excepto admin)...")
            perfiles_a_eliminar = PerfilUsuario.objects.exclude(user__username='admin')
            count = perfiles_a_eliminar.count()
            perfiles_a_eliminar.delete()
            registros_eliminados['perfiles'] = count
            
            # 2. Resetear secuencias de PostgreSQL
            print("Reseteando secuencias de PostgreSQL...")
            with connection.cursor() as cursor:
                # Lista de secuencias a resetear
                secuencias = [
                    'empresas_empresa_id_seq',
                    'plantas_planta_id_seq',
                    'departamentos_departamento_id_seq',
                    'puestos_puesto_id_seq',
                    'empleados_empleado_id_seq',
                    'planes_plan_id_seq',
                    'suscripciones_empresa_suscripcion_id_seq',
                    'pagos_pago_id_seq'
                ]
                
                for secuencia in secuencias:
                    try:
                        cursor.execute(f"ALTER SEQUENCE {secuencia} RESTART WITH 1;")
                        print(f"✅ Secuencia {secuencia} reseteada")
                    except Exception as e:
                        print(f"⚠️ No se pudo resetear {secuencia}: {e}")
        
        total_eliminados = sum(registros_eliminados.values())
        
        print(f"✅ REINICIO COMPLETADO - {total_eliminados} registros eliminados")
        
        return Response({
            'message': 'Base de datos reiniciada exitosamente',
            'registros_eliminados': registros_eliminados,
            'total_eliminados': total_eliminados,
            'fecha_operacion': datetime.now().isoformat(),
            'usuario_operacion': request.user.username,
            'estado': 'reiniciada',
            'nota': 'BD lista para datos demo o producción'
        })
        
    except Exception as e:
        print(f"❌ ERROR en reinicio: {str(e)}")
        return Response({
            'error': f'Error al reiniciar BD: {str(e)}',
            'registros_eliminados': registros_eliminados
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cargar_datos_demo(request):
    """
    📊 CARGAR DATOS DEMO - Datos mínimos para funcionalidad del sistema
    
    Crea:
    - 3 usuarios (superadmin, admin_empresa, admin_planta)  
    - 1 empresa demo
    - 1 planta demo
    - 3 departamentos básicos
    - 3 puestos esenciales
    - 3 planes de suscripción
    - 1 suscripción activa    """
    is_superadmin, error_response = verificar_superadmin(request)
    if not is_superadmin:
        return error_response
    
    try:
        datos_creados = {}
        
        with transaction.atomic():
            print("📊 CARGANDO DATOS DEMO...")
            
            # 1. CREAR PLANES DE SUSCRIPCIÓN
            print("Creando planes de suscripción...")
            planes_data = [
                {
                    'nombre': 'Plan Básico Demo',
                    'descripcion': 'Plan básico para demostración con funcionalidades esenciales',
                    'precio': 499.00,
                    'duracion': 30,
                    'status': True
                },
                {
                    'nombre': 'Plan Profesional Demo',
                    'descripcion': 'Plan profesional con todas las funcionalidades',
                    'precio': 999.00,
                    'duracion': 30,
                    'status': True
                },
                {
                    'nombre': 'Plan Empresarial Demo',
                    'descripcion': 'Plan empresarial para grandes organizaciones',
                    'precio': 1999.00,
                    'duracion': 30,
                    'status': True
                }
            ]
            
            planes_creados = []
            for plan_data in planes_data:
                plan = PlanSuscripcion.objects.create(**plan_data)
                planes_creados.append(plan)
                print(f"✅ Plan creado: {plan.nombre}")
            
            datos_creados['planes'] = len(planes_creados)
            
            # 2. CREAR USUARIOS DEMO
            print("Creando usuarios demo...")
            
            # Usuario Admin Empresa
            try:
                user_empresa = User.objects.create_user(
                    username='admin_empresa',
                    email='admin_empresa@demo.com',
                    password='1234',
                    first_name='Admin',
                    last_name='Empresa'
                )
                perfil_empresa = PerfilUsuario.objects.create(
                    user=user_empresa,
                    nombre='Admin',
                    apellido_paterno='Empresa',
                    apellido_materno='Demo',
                    correo='admin_empresa@demo.com',
                    nivel_usuario='admin-empresa',
                    status=True
                )
                print(f"✅ Usuario admin_empresa creado")
            except Exception as e:
                print(f"⚠️ Usuario admin_empresa ya existe o error: {e}")
                user_empresa = User.objects.get(username='admin_empresa')
                perfil_empresa = user_empresa.perfil
            
            # Usuario Admin Planta
            try:
                user_planta = User.objects.create_user(
                    username='admin_planta',
                    email='admin_planta@demo.com',
                    password='1234',
                    first_name='Admin',
                    last_name='Planta'
                )
                perfil_planta = PerfilUsuario.objects.create(
                    user=user_planta,
                    nombre='Admin',
                    apellido_paterno='Planta',
                    apellido_materno='Demo',
                    correo='admin_planta@demo.com',
                    nivel_usuario='admin-planta',
                    status=True
                )
                print(f"✅ Usuario admin_planta creado")
            except Exception as e:
                print(f"⚠️ Usuario admin_planta ya existe o error: {e}")
                user_planta = User.objects.get(username='admin_planta')
                perfil_planta = user_planta.perfil
            
            datos_creados['usuarios'] = 2  # admin ya existe
            
            # 3. CREAR EMPRESA DEMO
            print("Creando empresa demo...")
            empresa = Empresa.objects.create(
                nombre='Empresa Demo AXYOMA',
                rfc='DEMO123456789',
                direccion='Av. Demostración #123, Ciudad Demo',
                email_contacto='contacto@empresademo.com',
                telefono_contacto='555-DEMO-123',
                status=True,
                administrador=perfil_empresa
            )
            print(f"✅ Empresa creada: {empresa.nombre}")
            datos_creados['empresas'] = 1
            
            # 4. CREAR PLANTA DEMO
            print("Creando planta demo...")
            planta = Planta.objects.create(
                nombre='Planta Principal Demo',
                direccion='Zona Industrial Demo, Sector A',
                empresa=empresa,
                status=True
            )
            print(f"✅ Planta creada: {planta.nombre}")
            datos_creados['plantas'] = 1
            
            # 5. CREAR ADMIN PLANTA
            admin_planta = AdminPlanta.objects.create(
                usuario=perfil_planta,
                planta=planta,
                status=True
            )
            print(f"✅ Admin de planta asignado")
            
            # 6. CREAR DEPARTAMENTOS DEMO
            print("Creando departamentos demo...")
            departamentos_data = [
                {
                    'nombre': 'Recursos Humanos',
                    'descripcion': 'Gestión de personal y administración de RRHH',
                    'planta': planta
                },
                {
                    'nombre': 'Producción',
                    'descripcion': 'Operaciones de manufactura y producción',
                    'planta': planta
                },
                {
                    'nombre': 'Administración',
                    'descripcion': 'Gestión administrativa y financiera',
                    'planta': planta
                }
            ]
            
            departamentos_creados = []
            for dept_data in departamentos_data:
                dept = Departamento.objects.create(**dept_data, status=True)
                departamentos_creados.append(dept)
                print(f"✅ Departamento creado: {dept.nombre}")
            
            datos_creados['departamentos'] = len(departamentos_creados)
            
            # 7. CREAR PUESTOS DEMO
            print("Creando puestos demo...")
            puestos_data = [
                {
                    'nombre': 'Analista de RRHH',
                    'descripcion': 'Responsable de análisis y gestión de recursos humanos',
                    'departamento': departamentos_creados[0]  # RRHH
                },
                {
                    'nombre': 'Operador de Producción',
                    'descripcion': 'Operador de línea de producción y maquinaria',
                    'departamento': departamentos_creados[1]  # Producción
                },
                {
                    'nombre': 'Asistente Administrativo',
                    'descripcion': 'Apoyo en gestión administrativa y documentación',
                    'departamento': departamentos_creados[2]  # Administración
                }
            ]
            
            puestos_creados = []
            for puesto_data in puestos_data:
                puesto = Puesto.objects.create(**puesto_data, status=True)
                puestos_creados.append(puesto)
                print(f"✅ Puesto creado: {puesto.nombre}")
            
            datos_creados['puestos'] = len(puestos_creados)
            
            # 8. CREAR SUSCRIPCIÓN DEMO
            print("Creando suscripción demo...")
            from datetime import date, timedelta
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan=planes_creados[1],  # Plan Profesional
                fecha_inicio=date.today(),
                fecha_fin=date.today() + timedelta(days=30),
                estado='activa',
                auto_renovacion=True
            )
            print(f"✅ Suscripción creada: {suscripcion.plan.nombre}")
            datos_creados['suscripciones'] = 1
            
            # 9. CREAR EMPLEADO DEMO (Opcional)
            print("Creando empleado demo...")
            empleado = Empleado.objects.create(
                nombre='Juan Carlos',
                apellido_paterno='Empleado',
                status=True,
                puesto=puestos_creados[0]  # Analista RRHH
            )
            print(f"✅ Empleado creado: {empleado.nombre} {empleado.apellido_paterno}")
            datos_creados['empleados'] = 1
            
        total_creados = sum(datos_creados.values())
        
        print(f"✅ DATOS DEMO CARGADOS - {total_creados} registros creados")
        
        return Response({
            'message': 'Datos demo cargados exitosamente',
            'datos_creados': datos_creados,
            'total_creados': total_creados,
            'fecha_operacion': datetime.now().isoformat(),
            'usuario_operacion': request.user.username,
            'usuarios_disponibles': {
                'superadmin': 'admin / admin (ya existía)',
                'admin_empresa': 'admin_empresa / 1234',
                'admin_planta': 'admin_planta / 1234'
            },
            'empresa_demo': {
                'nombre': empresa.nombre,
                'plantas': 1,
                'departamentos': len(departamentos_creados),
                'puestos': len(puestos_creados),
                'empleados': 1
            },
            'suscripcion': {
                'plan': suscripcion.plan.nombre,
                'estado': suscripcion.estado,
                'vigencia_dias': 30
            },
            'estado': 'datos_demo_listos'
        })
        
    except Exception as e:
        print(f"❌ ERROR cargando datos demo: {str(e)}")
        return Response({
            'error': f'Error cargando datos demo: {str(e)}',
            'datos_creados': datos_creados if 'datos_creados' in locals() else {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_bd_restauracion(request):
    """
    📊 OBTENER ESTADO ACTUAL DE LA BD para restauración
    
    Información útil para decidir qué operación realizar    """
    is_superadmin, error_response = verificar_superadmin(request)
    if not is_superadmin:
        return error_response
    
    try:
        # Contar registros actuales
        estado = {
            'empresas': Empresa.objects.count(),
            'plantas': Planta.objects.count(),
            'departamentos': Departamento.objects.count(),
            'puestos': Puesto.objects.count(),
            'empleados': Empleado.objects.count(),
            'usuarios': User.objects.count(),
            'perfiles': PerfilUsuario.objects.count(),
            'planes': PlanSuscripcion.objects.count(),
            'suscripciones': SuscripcionEmpresa.objects.count(),
            'pagos': Pago.objects.count(),
            'logs_respaldos': LogRespaldo.objects.count()
        }
        
        total_registros = sum(estado.values())
        
        # Determinar estado de la BD
        if total_registros <= 5:  # Solo datos esenciales (admin, etc.)
            estado_bd = 'vacia'
            recomendacion = 'Cargar datos demo para empezar'
        elif estado['empresas'] == 0:
            estado_bd = 'sin_empresas'
            recomendacion = 'Cargar datos demo o crear empresa manualmente'
        elif estado['empresas'] <= 2 and 'demo' in str(Empresa.objects.first().nombre).lower():
            estado_bd = 'datos_demo'
            recomendacion = 'Listo para pruebas o cargar datos reales'
        else:
            estado_bd = 'datos_reales'
            recomendacion = 'BD con datos reales - usar con precaución'
        
        return Response({
            'estado_bd': estado_bd,
            'recomendacion': recomendacion,
            'total_registros': total_registros,
            'bd_vacia': total_registros <= 5,
            'fecha_consulta': datetime.now().isoformat(),
            'tiene_datos_demo': 'demo' in str(Empresa.objects.first().nombre).lower() if estado['empresas'] > 0 else False,
            'usuarios_actuales': list(User.objects.values_list('username', flat=True)),
            'empresas_actuales': list(Empresa.objects.values_list('nombre', flat=True)),
            # Contadores individuales directamente en el objeto raíz
            'empresas': estado['empresas'],
            'plantas': estado['plantas'],
            'departamentos': estado['departamentos'],
            'puestos': estado['puestos'],
            'empleados': estado['empleados'],
            'usuarios': estado['usuarios'],
            'perfiles': estado['perfiles'],
            'planes': estado['planes'],
            'suscripciones': estado['suscripciones'],
            'pagos': estado['pagos'],
            'logs_respaldos': estado['logs_respaldos'],
            # Mantener también el objeto contadores para compatibilidad
            'contadores': estado
        })
        
    except Exception as e:
        return Response({
            'error': f'Error obteniendo estado BD: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def debug_reiniciar_bd(request):
    """Endpoint temporal para debugging - identificar error específico"""
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        confirmacion = request.data.get('confirmacion', '')
        if confirmacion != 'CONFIRMO_REINICIAR_BD':
            return Response({'error': 'Confirmación requerida'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        debug_info = {}
        
        # Test 1: Verificar acceso a modelos
        try:
            debug_info['test_modelos'] = {
                'LogRespaldo': LogRespaldo.objects.count(),
                'Pago': Pago.objects.count(),
                'SuscripcionEmpresa': SuscripcionEmpresa.objects.count(),
                'PlanSuscripcion': PlanSuscripcion.objects.count(),
                'Empleado': Empleado.objects.count(),
                'AdminPlanta': AdminPlanta.objects.count(),
                'Puesto': Puesto.objects.count(),
                'Departamento': Departamento.objects.count(),
                'Planta': Planta.objects.count(),
                'Empresa': Empresa.objects.count(),
                'User': User.objects.count(),
                'PerfilUsuario': PerfilUsuario.objects.count(),
            }
        except Exception as e:
            debug_info['error_modelos'] = str(e)
            return Response({'debug': debug_info, 'error': f'Error accediendo modelos: {str(e)}'}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Test 2: Verificar transacciones
        try:
            with transaction.atomic():
                debug_info['test_transaction'] = 'OK'
        except Exception as e:
            debug_info['error_transaction'] = str(e)
            return Response({'debug': debug_info, 'error': f'Error en transacción: {str(e)}'}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Test 3: Verificar conexión de BD
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                debug_info['test_connection'] = f'BD conectada: {result[0]}'
        except Exception as e:
            debug_info['error_connection'] = str(e)
            return Response({'debug': debug_info, 'error': f'Error de conexión BD: {str(e)}'}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': 'Debug completado exitosamente',
            'debug_info': debug_info,
            'usuario': request.user.username
        })
        
    except Exception as e:
        return Response({
            'error': f'Error general en debug: {str(e)}',
            'tipo_error': type(e).__name__
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
