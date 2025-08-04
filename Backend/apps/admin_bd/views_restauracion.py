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
        print(f"🔍 DEBUG - Usuario: {user.username}")
        print(f"🔍 DEBUG - Usuario ID: {user.id}")
        print(f"🔍 DEBUG - ¿Es autenticado?: {user.is_authenticated}")
          # Verificar perfil
        perfil = getattr(user, 'perfil', None)
        print(f"🔍 DEBUG - Perfil encontrado: {perfil}")
        
        if perfil:
            print(f"🔍 DEBUG - Nivel usuario: {perfil.nivel_usuario}")
            if perfil.nivel_usuario != 'superadmin':
                print(f"🔍 DEBUG - FALLO: No es superadmin, es: {perfil.nivel_usuario}")
                return False, Response({'error': f'Usuario {user.username} no es SuperAdmin (es {perfil.nivel_usuario})'}, 
                              status=status.HTTP_403_FORBIDDEN)
        else:
            # Intentar buscar por relación reversa
            from apps.users.models import PerfilUsuario
            try:
                perfil_directo = PerfilUsuario.objects.get(user=user)
                print(f"🔍 DEBUG - Perfil encontrado por búsqueda directa: {perfil_directo}")
                print(f"🔍 DEBUG - Nivel: {perfil_directo.nivel_usuario}")
                if perfil_directo.nivel_usuario != 'superadmin':
                    print(f"🔍 DEBUG - FALLO: No es superadmin, es: {perfil_directo.nivel_usuario}")
                    return False, Response({'error': f'Usuario {user.username} no es SuperAdmin (es {perfil_directo.nivel_usuario})'}, 
                                  status=status.HTTP_403_FORBIDDEN)
                # Si encontramos el perfil directamente, lo usamos
                perfil = perfil_directo
            except PerfilUsuario.DoesNotExist:
                print("🔍 DEBUG - No existe PerfilUsuario para este usuario")
                # Auto-crear perfil para usuario admin
                if user.username == 'admin':
                    print("🔧 DEBUG - Creando perfil automáticamente para usuario admin...")
                    try:
                        perfil_directo = PerfilUsuario.objects.create(
                            user=user,
                            nombre="Administrador",
                            apellido_paterno="Sistema",
                            correo=user.email or "admin@axyoma.com",
                            nivel_usuario="superadmin",
                            status=True
                        )
                        print(f"🔧 DEBUG - ✅ Perfil creado: {perfil_directo.nombre_completo} ({perfil_directo.nivel_usuario})")
                        perfil = perfil_directo
                    except Exception as create_error:
                        print(f"🔧 DEBUG - ❌ Error al crear perfil: {create_error}")
                        return False, Response({'error': f'No se pudo crear perfil para usuario admin: {create_error}'}, 
                                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    print("🔍 DEBUG - FALLO CRÍTICO: Usuario no es admin y no tiene perfil")
                    return False, Response({'error': f'Usuario {user.username} no tiene perfil asociado'}, 
                                  status=status.HTTP_403_FORBIDDEN)
            else:
                    print("🔍 DEBUG - FALLO CRÍTICO: Usuario no es admin y no tiene perfil")
                    return False, Response({'error': f'Usuario {user.username} no tiene perfil asociado'}, 
                                  status=status.HTTP_403_FORBIDDEN)
        
        print("🔍 DEBUG - ✅ VERIFICACIÓN EXITOSA: Usuario es superadmin")
        return True, None
    except Exception as e:
        print(f"🔍 DEBUG - ERROR en verificar_superadmin: {str(e)}")
        import traceback
        traceback.print_exc()
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
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        confirmacion = request.data.get('confirmacion', '')
        if confirmacion != 'CONFIRMO_REINICIAR_BD':
            return Response({'error': 'Confirmación requerida'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        registros_eliminados = {}
        
        with transaction.atomic():
            print("🔥 INICIANDO REINICIO DE BASE DE DATOS...")            # Usar SQL directo para evitar problemas de integridad referencial
            try:
                with connection.cursor() as cursor:
                    print("Obteniendo nombres reales de tablas...")
                      # Obtener TODAS las tablas de la BD (sin filtros previos)
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name;
                    """)
                    
                    todas_las_tablas = [row[0] for row in cursor.fetchall()]
                    print(f"Todas las tablas encontradas: {todas_las_tablas}")                    # Filtrar tablas: limpiar TODAS excepto las del sistema Django
                    tablas_a_limpiar = []
                    patrones_excluir = [
                        'django_',          # Tablas del sistema Django
                        'auth_group',       # Grupos de Django (mantener)
                        'auth_permission',  # Permisos de Django (mantener)
                        'django_content_type',  # Content types (mantener)
                        'django_migrations',    # Migraciones (mantener)
                        'django_session',       # Sesiones (mantener)
                        'django_admin_log',     # Log del admin (mantener)
                    ]
                    
                    # Incluir todas las tablas que NO son del sistema Django
                    for tabla in todas_las_tablas:
                        # Excluir tablas del sistema Django
                        if not any(tabla.startswith(patron) or tabla == patron for patron in patrones_excluir):
                            tablas_a_limpiar.append(tabla)
                      # Ordenar las tablas para eliminar dependientes antes que principales
                    # Las tablas con FKs deben eliminarse antes que las principales
                    orden_preferido = [
                        # Tablas dependientes primero
                        'respuestas_empleados',
                        'evaluaciones_oficiales', 
                        'empleados',
                        'puestos',
                        'departamentos',
                        'plantas',
                        'suscripciones',
                        'admin_bd_logrespaldo',
                        'authtoken_token',
                        'usuarios',  # PerfilUsuario - debe ir antes que auth_user
                        'auth_user'  # Django User - al final
                    ]
                    
                    tablas_ordenadas = []
                    
                    # Agregar tablas en orden preferido si existen
                    for tabla_pref in orden_preferido:
                        if tabla_pref in tablas_a_limpiar:
                            tablas_ordenadas.append(tabla_pref)
                    
                    # Agregar el resto de tablas que no están en el orden preferido
                    for tabla in tablas_a_limpiar:
                        if tabla not in tablas_ordenadas:
                            tablas_ordenadas.append(tabla)
                    
                    tablas_a_limpiar = tablas_ordenadas
                    print(f"Tablas que se van a limpiar (en orden): {tablas_a_limpiar}")
                    
                    # Contar registros antes de eliminar (en transacciones separadas para evitar errores)
                    for tabla in tablas_a_limpiar:
                        try:
                            cursor.execute(f'SELECT COUNT(*) FROM "{tabla}";')
                            count = cursor.fetchone()[0]
                            registros_eliminados[tabla] = count
                            print(f"📊 {tabla}: {count} registros")
                        except Exception as e:
                            print(f"⚠️ No se pudo contar {tabla}: {e}")
                            registros_eliminados[tabla] = 0
                    
                    # Deshabilitar restricciones de FK temporalmente (PostgreSQL)
                    print("Deshabilitando restricciones de integridad...")
                    cursor.execute("SET session_replication_role = replica;")                    # Eliminar datos de todas las tablas identificadas
                    print("Eliminando datos de tablas de usuario...")
                    for tabla in tablas_a_limpiar:
                        try:
                            cursor.execute(f'DELETE FROM "{tabla}";')
                            print(f"✅ Tabla {tabla} limpiada")
                        except Exception as e:
                            print(f"⚠️ Error limpiando {tabla}: {e}")
                      # Restaurar restricciones de FK
                    print("Restaurando restricciones de integridad...")
                    cursor.execute("SET session_replication_role = DEFAULT;")  # PostgreSQL
                    
                    # Verificar que las tablas críticas estén limpias
                    cursor.execute('SELECT COUNT(*) FROM "auth_user";')
                    users_count = cursor.fetchone()[0]
                    cursor.execute('SELECT COUNT(*) FROM "usuarios";')
                    usuarios_count = cursor.fetchone()[0]
                    print(f"✅ Verificación post-limpieza: {users_count} auth_user, {usuarios_count} usuarios")
                      # Recrear usuario admin con Django User.objects.create_user
                    print("Recreando usuario admin...")
                    admin_user = User.objects.create_user(
                        username='admin',
                        email='admin@axyoma.com',
                        password='admin123',  # Password temporal - cambiar después del primer login
                        first_name='Super',
                        last_name='Admin',
                        is_staff=True,
                        is_superuser=True
                    )
                    
                    # Crear perfil de usuario asociado
                    try:
                        perfil_admin = PerfilUsuario.objects.create(
                            user=admin_user,
                            nombre='Super',
                            apellido_paterno='Admin',
                            correo='admin@axyoma.com',
                            nivel_usuario='superadmin'
                        )
                        print(f"✅ Perfil admin creado con ID: {perfil_admin.id}")
                    except Exception as e:
                        print(f"❌ ERROR creando perfil admin: {str(e)}")
                        # Si hay error al crear perfil, verificar estado de la tabla usuarios
                        cursor.execute('SELECT COUNT(*) FROM "usuarios";')
                        usuarios_count = cursor.fetchone()[0]
                        print(f"Debug: usuarios en BD: {usuarios_count}")
                        raise  # Re-lanzar para que se maneje en el bloque catch superior
                    
                    print(f"✅ Usuario admin recreado con ID: {admin_user.id}")
                    print(f"✅ Perfil admin creado con ID: {perfil_admin.id}")
                    
                    # Verificación final: contar usuarios restantes
                    usuarios_finales = User.objects.count()
                    perfiles_finales = PerfilUsuario.objects.count()
                    print(f"📊 Verificación final: {usuarios_finales} usuarios, {perfiles_finales} perfiles")
                    
                    print("✅ Limpieza con SQL directo completada")
                    
            except Exception as e:
                print(f"❌ ERROR en limpieza SQL: {str(e)}")
                # Fallback: intentar con Django ORM solo para tablas que sabemos que existen
                print("Intentando método alternativo...")
                
                # Solo eliminar de tablas que sabemos que existen
                tablas_seguras = [
                    (LogRespaldo, 'logs_respaldos'),
                    (User.objects.exclude(username='admin'), 'usuarios'),
                    (PerfilUsuario.objects.exclude(user__username='admin'), 'perfiles'),
                ]
                
                for queryset, nombre in tablas_seguras:
                    try:
                        if hasattr(queryset, 'count'):
                            count = queryset.count()
                            queryset.delete()
                        else:
                            count = queryset.objects.count()
                            queryset.objects.all().delete()
                        registros_eliminados[nombre] = count
                        print(f"✅ {nombre}: {count} registros eliminados")
                    except Exception as e2:
                        print(f"⚠️ Error con {nombre}: {e2}")
                        registros_eliminados[nombre] = 0
                    total_eliminados = sum(registros_eliminados.values())
        
        # Verificación final del estado de la BD
        usuarios_finales = User.objects.count()
        perfiles_finales = PerfilUsuario.objects.count()
        empresas_finales = Empresa.objects.count()
        
        print(f"✅ REINICIO COMPLETADO - {total_eliminados} registros eliminados")
        print(f"📊 Estado final: {usuarios_finales} usuarios, {perfiles_finales} perfiles, {empresas_finales} empresas")
        
        return Response({
            'message': 'Base de datos reiniciada exitosamente',
            'registros_eliminados': registros_eliminados,
            'total_eliminados': total_eliminados,
            'fecha_operacion': datetime.now().isoformat(),
            'usuario_operacion': request.user.username,
            'estado': 'reiniciada',
            'nota': 'BD lista para datos demo o producción (sin reseteo de secuencias)',
            'verificacion_final': {
                'usuarios_restantes': usuarios_finales,
                'perfiles_restantes': perfiles_finales,
                'empresas_restantes': empresas_finales,
                'solo_admin': usuarios_finales == 1 and perfiles_finales == 1
            },
            'admin_recreado': {
                'username': 'admin',
                'password': 'admin123',
                'mensaje': 'Usuario admin recreado - Usar estas credenciales para acceder al sistema'
            }
        })
        
    except Exception as e:
        print(f"❌ ERROR en reinicio: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': f'Error al reiniciar BD: {str(e)}',
            'tipo_error': type(e).__name__,
            'detalle': str(e)
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
    - 3 departamentos básicos    - 3 puestos esenciales
    - 3 planes de suscripción
    - 1 suscripción activa
    """
    # Auto-crear perfil para usuario admin si no existe
    if request.user.username == 'admin':
        try:
            perfil = request.user.perfil
            print(f"🔍 Perfil admin existe: {perfil.nombre_completo}")
        except:
            print("🔧 Creando perfil para usuario admin...")
            PerfilUsuario.objects.create(
                user=request.user,
                nombre="Administrador",
                apellido_paterno="Sistema", 
                correo="admin@axyoma.com",
                nivel_usuario="superadmin",
                status=True
            )
            print("✅ Perfil admin creado exitosamente")
    
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
                },                {
                    'nombre': 'Plan Empresarial Demo',
                    'descripcion': 'Plan empresarial para grandes organizaciones',
                    'precio': 1999.00,
                    'duracion': 30,
                    'status': True
                }
            ]
            
            planes_creados = []
            for plan_data in planes_data:
                plan, created = PlanSuscripcion.objects.get_or_create(
                    nombre=plan_data['nombre'],
                    defaults=plan_data
                )
                planes_creados.append(plan)
                if created:
                    print(f"✅ Plan creado: {plan.nombre}")
                else:
                    print(f"⚠️ Plan ya existe: {plan.nombre}")
            
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
                try:
                    user_empresa = User.objects.get(username='admin_empresa')
                    perfil_empresa = user_empresa.perfil
                except:
                    # Si no existe el perfil, crearlo
                    user_empresa = User.objects.get(username='admin_empresa')
                    perfil_empresa = PerfilUsuario.objects.create(
                        user=user_empresa,
                        nombre='Admin',
                        apellido_paterno='Empresa',
                        apellido_materno='Demo', 
                        correo='admin_empresa@demo.com',
                        nivel_usuario='admin-empresa',
                        status=True
                    )
            
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
                    status=True                )
                print(f"✅ Usuario admin_planta creado")
            except Exception as e:
                print(f"⚠️ Usuario admin_planta ya existe o error: {e}")
                user_planta = User.objects.get(username='admin_planta')
                perfil_planta = user_planta.perfil
            
            datos_creados['usuarios'] = 2  # admin ya existe
            
            # 3. CREAR EMPRESA DEMO
            print("Creando empresa demo...")
            empresa, created = Empresa.objects.get_or_create(
                rfc='DEMO123456789',
                defaults={
                    'nombre': 'Empresa Demo AXYOMA',
                    'direccion': 'Av. Demostración #123, Ciudad Demo',
                    'email_contacto': 'contacto@empresademo.com',
                    'telefono_contacto': '555-DEMO-123',
                    'status': True,
                    'administrador': perfil_empresa
                }
            )
            if created:
                print(f"✅ Empresa creada: {empresa.nombre}")
            else:
                print(f"⚠️ Empresa ya existe: {empresa.nombre}")
            datos_creados['empresas'] = 1
            
            # 4. CREAR PLANTA DEMO
            print("Creando planta demo...")
            planta, created = Planta.objects.get_or_create(
                nombre='Planta Principal Demo',
                empresa=empresa,
                defaults={
                    'direccion': 'Zona Industrial Demo, Sector A',
                    'status': True
                }
            )
            if created:
                print(f"✅ Planta creada: {planta.nombre}")
            else:
                print(f"⚠️ Planta ya existe: {planta.nombre}")
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
                },                {
                    'nombre': 'Administración',
                    'descripcion': 'Gestión administrativa y financiera',
                    'planta': planta
                }
            ]
            
            departamentos_creados = []
            for dept_data in departamentos_data:
                dept, created = Departamento.objects.get_or_create(
                    nombre=dept_data['nombre'],
                    planta=dept_data['planta'],
                    defaults={
                        'descripcion': dept_data['descripcion'],
                        'status': True
                    }
                )
                departamentos_creados.append(dept)
                if created:
                    print(f"✅ Departamento creado: {dept.nombre}")
                else:
                    print(f"⚠️ Departamento ya existe: {dept.nombre}")
            
            datos_creados['departamentos'] = len(departamentos_creados)
            
            # 7. CREAR PUESTOS DEMO
            print("Creando puestos demo...")
            puestos_data = [
                {
                    'nombre': 'Analista de RRHH',
                    'descripcion': 'Responsable de análisis y gestión de recursos humanos',
                    'departamento': departamentos_creados[0]  # RRHH
                },                {
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
                puesto, created = Puesto.objects.get_or_create(
                    nombre=puesto_data['nombre'],
                    departamento=puesto_data['departamento'],
                    defaults={
                        'descripcion': puesto_data['descripcion'],
                        'status': True
                    }
                )
                puestos_creados.append(puesto)
                if created:
                    print(f"✅ Puesto creado: {puesto.nombre}")
                else:
                    print(f"⚠️ Puesto ya existe: {puesto.nombre}")
            
            datos_creados['puestos'] = len(puestos_creados)
              # 8. CREAR SUSCRIPCIÓN DEMO
            print("Creando suscripción demo...")
            from datetime import date, timedelta
            
            suscripcion, created = SuscripcionEmpresa.objects.get_or_create(
                empresa=empresa,
                plan=planes_creados[1],  # Plan Profesional
                defaults={
                    'fecha_inicio': date.today(),
                    'fecha_fin': date.today() + timedelta(days=30),
                    'estado': 'activa',
                    'auto_renovacion': True
                }
            )
            if created:
                print(f"✅ Suscripción creada: {suscripcion.plan.nombre}")
            else:
                print(f"⚠️ Suscripción ya existe: {suscripcion.plan.nombre}")
            datos_creados['suscripciones'] = 1
            
            # 9. CREAR EMPLEADO DEMO (Opcional)
            print("Creando empleado demo...")
            empleado, created = Empleado.objects.get_or_create(
                nombre='Juan Carlos',
                apellido_paterno='Empleado',
                puesto=puestos_creados[0],  # Analista RRHH
                defaults={
                    'status': True
                }
            )
            if created:
                print(f"✅ Empleado creado: {empleado.nombre} {empleado.apellido_paterno}")
            else:
                print(f"⚠️ Empleado ya existe: {empleado.nombre} {empleado.apellido_paterno}")
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
def debug_cargar_datos_simple(request):
    """
    🧪 DEBUG - Cargar datos demo paso a paso para diagnosticar errores
    """
    is_superadmin, error_response = verificar_superadmin(request)
    if not is_superadmin:
        return error_response
    
    debug_info = {
        'pasos_completados': [],
        'errores': [],
        'datos_creados': {}
    }
    
    try:
        # PASO 1: Verificar modelos básicos
        debug_info['pasos_completados'].append('1. Verificando modelos...')
        try:
            planes_count = PlanSuscripcion.objects.count()
            users_count = User.objects.count()
            debug_info['pasos_completados'].append(f'1.1 Planes existentes: {planes_count}')
            debug_info['pasos_completados'].append(f'1.2 Usuarios existentes: {users_count}')
        except Exception as e:
            debug_info['errores'].append(f'Error verificando modelos: {str(e)}')
            return Response(debug_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # PASO 2: Crear plan básico
        debug_info['pasos_completados'].append('2. Creando plan de prueba...')
        try:
            plan_test = PlanSuscripcion.objects.create(
                nombre='Plan Debug Test',
                descripcion='Plan para debugging',
                precio=100.00,
                duracion=30,
                status=True
            )
            debug_info['datos_creados']['plan'] = plan_test.nombre
            debug_info['pasos_completados'].append(f'2.1 Plan creado: {plan_test.nombre}')
        except Exception as e:
            debug_info['errores'].append(f'Error creando plan: {str(e)}')
            return Response(debug_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # PASO 3: Crear usuario simple
        debug_info['pasos_completados'].append('3. Creando usuario de prueba...')
        try:
            # Limpiar usuario de test previo
            User.objects.filter(username='debug_test_user').delete()
            
            user_test = User.objects.create_user(
                username='debug_test_user',
                email='debug@test.com',
                password='1234',
                first_name='Debug',
                last_name='User'
            )
            debug_info['datos_creados']['user'] = user_test.username
            debug_info['pasos_completados'].append(f'3.1 Usuario creado: {user_test.username}')
        except Exception as e:
            debug_info['errores'].append(f'Error creando usuario: {str(e)}')
            return Response(debug_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # PASO 4: Crear perfil de usuario
        debug_info['pasos_completados'].append('4. Creando perfil de usuario...')
        try:
            perfil_test = PerfilUsuario.objects.create(
                user=user_test,
                nombre='Debug',
                apellido_paterno='User',
                correo='debug@test.com',
                nivel_usuario='admin-empresa',
                status=True
            )
            debug_info['datos_creados']['perfil'] = f'{perfil_test.nombre} {perfil_test.apellido_paterno}'
            debug_info['pasos_completados'].append(f'4.1 Perfil creado: {perfil_test.nombre}')
        except Exception as e:
            debug_info['errores'].append(f'Error creando perfil: {str(e)}')
            return Response(debug_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # PASO 5: Crear empresa simple
        debug_info['pasos_completados'].append('5. Creando empresa de prueba...')
        try:
            empresa_test = Empresa.objects.create(
                nombre='Empresa Debug Test',
                rfc='DEBUG123456789',
                direccion='Dirección Debug',
                email_contacto='contacto@debug.com',
                telefono_contacto='555-DEBUG',
                status=True,
                administrador=perfil_test
            )
            debug_info['datos_creados']['empresa'] = empresa_test.nombre
            debug_info['pasos_completados'].append(f'5.1 Empresa creada: {empresa_test.nombre}')
        except Exception as e:
            debug_info['errores'].append(f'Error creando empresa: {str(e)}')
            return Response(debug_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': '✅ Debug completado exitosamente - Los datos demo deberían funcionar',
            'debug_info': debug_info,
            'conclusion': 'Si este endpoint funciona, el problema está en la función cargar_datos_demo'
        })
        
    except Exception as e:
        debug_info['errores'].append(f'Error general: {str(e)}')
        return Response({
            'error': 'Error en debug',
            'debug_info': debug_info
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












