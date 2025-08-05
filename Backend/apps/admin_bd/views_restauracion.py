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
from django.utils import timezone

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
    📊 CARGAR DATOS DEMO - Solo usuario admin y planes básicos
    
    Crea únicamente:
    - Usuario admin (si no existe)
    - 3 planes de suscripción básicos
    
    Sin empresas, plantas, departamentos, empleados ni otras complejidades.
    """
    try:
        datos_creados = {}
        
        with transaction.atomic():
            print("📊 CARGANDO DATOS DEMO SIMPLIFICADOS...")
            
            # 1. VERIFICAR/CREAR USUARIO ADMIN
            print("Verificando usuario admin...")
            admin_user = None
            try:
                admin_user = User.objects.get(username='admin')
                print(f"✅ Usuario admin ya existe (ID: {admin_user.id})")
                
                # Verificar si tiene perfil
                try:
                    perfil_admin = admin_user.perfil
                    print(f"✅ Perfil admin existe: {perfil_admin.nombre_completo}")
                except:
                    print("🔧 Creando perfil para usuario admin existente...")
                    PerfilUsuario.objects.create(
                        user=admin_user,
                        nombre="Administrador",
                        apellido_paterno="Sistema",
                        correo="admin@axyoma.com",
                        nivel_usuario="superadmin",
                        status=True
                    )
                    print("✅ Perfil admin creado")
                    
            except User.DoesNotExist:
                print("🔧 Creando usuario admin...")
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@axyoma.com',
                    password='admin123',
                    first_name='Super',
                    last_name='Admin',
                    is_staff=True,
                    is_superuser=True
                )
                
                # Crear perfil asociado
                PerfilUsuario.objects.create(
                    user=admin_user,
                    nombre='Super',
                    apellido_paterno='Admin',
                    correo='admin@axyoma.com',
                    nivel_usuario='superadmin',
                    status=True
                )
                print(f"✅ Usuario admin creado con ID: {admin_user.id}")
            
            datos_creados['usuario_admin'] = 1
            
            # 2. CREAR PLANES DE SUSCRIPCIÓN
            print("Creando planes de suscripción...")
            planes_data = [
                {
                    'nombre': 'Plan Básico',
                    'descripcion': 'Plan básico para pequeñas empresas con funcionalidades esenciales',
                    'precio': 299.00,
                    'duracion': 30,
                    'status': True
                },
                {
                    'nombre': 'Plan Profesional',
                    'descripcion': 'Plan profesional para empresas medianas con funcionalidades avanzadas',
                    'precio': 599.00,
                    'duracion': 30,
                    'status': True
                },
                {
                    'nombre': 'Plan Empresarial',
                    'descripcion': 'Plan empresarial para grandes organizaciones con todas las funcionalidades',
                    'precio': 999.00,
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
                    print(f"✅ Plan creado: {plan.nombre} - ${plan.precio}")
                else:
                    print(f"⚠️ Plan ya existe: {plan.nombre} - ${plan.precio}")
            
            datos_creados['planes'] = len(planes_creados)
            
        total_creados = sum(datos_creados.values())
        
        print(f"✅ DATOS DEMO CARGADOS - {total_creados} elementos procesados")
        
        return Response({
            'message': 'Datos demo cargados exitosamente (versión simplificada)',
            'datos_creados': datos_creados,
            'total_creados': total_creados,
            'fecha_operacion': datetime.now().isoformat(),
            'usuario_operacion': request.user.username if request.user.is_authenticated else 'Anónimo',
            'admin_usuario': {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@axyoma.com',
                'mensaje': 'Usuario admin listo para acceder al sistema'
            },
            'planes_disponibles': [
                {'nombre': plan.nombre, 'precio': f'${plan.precio}', 'duracion': f'{plan.duracion} días'}
                for plan in planes_creados
            ],
            'estado': 'datos_basicos_listos'
        })
        
    except Exception as e:
        print(f"❌ ERROR cargando datos demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': f'Error cargando datos demo: {str(e)}',
            'datos_creados': datos_creados if 'datos_creados' in locals() else {},
            'tipo_error': type(e).__name__
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cargar_datos_demo_simple(request):
    """
    🌱 CARGAR DATOS DEMO SIMPLIFICADO
    
    Versión simplificada que evita validaciones complejas de usuarios y suscripciones.
    Solo crea la estructura organizacional básica usando el usuario actual como administrador.
    """
    is_superadmin, error_response = verificar_superadmin(request)
    if not is_superadmin:
        return error_response
    
    try:
        # Usar el usuario actual como administrador de empresa
        usuario_admin = request.user
        
        # Crear o obtener perfil para el usuario actual si no existe
        perfil_admin, created = PerfilUsuario.objects.get_or_create(
            user=usuario_admin,
            defaults={
                'nivel_usuario': 'superadmin',
                'activo': True,
                'fecha_creacion': timezone.now()
            }
        )
        
        # 1. Crear empresa demo
        empresa, created = Empresa.objects.get_or_create(
            nombre='Empresa Demo AXYOMA',
            defaults={
                'rfc': 'DEMO123456789',
                'razon_social': 'Empresa Demostración AXYOMA S.A. de C.V.',
                'direccion': 'Av. Demo 123, Ciudad Demo',
                'telefono': '55-1234-5678',
                'email': 'demo@axyoma.com',
                'activo': True,
                'fecha_creacion': timezone.now(),
                'admin_empresa': perfil_admin
            }
        )
        
        # 2. Crear planta demo
        planta, created = Planta.objects.get_or_create(
            nombre='Planta Principal Demo',
            empresa=empresa,
            defaults={
                'direccion': 'Zona Industrial Demo, Lote 1',
                'telefono': '55-1234-5679',
                'activo': True,
                'fecha_creacion': timezone.now()
            }
        )
        
        # 3. Crear departamentos demo
        departamentos_data = [
            {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal'},
            {'nombre': 'Producción', 'descripcion': 'Área de manufactura'},
            {'nombre': 'Calidad', 'descripcion': 'Control de calidad'},
            {'nombre': 'Mantenimiento', 'descripcion': 'Mantenimiento de equipos'},
            {'nombre': 'Administración', 'descripcion': 'Gestión administrativa'}
        ]
        
        departamentos_creados = []
        for dept_data in departamentos_data:
            dept, created = Departamento.objects.get_or_create(
                nombre=dept_data['nombre'],
                planta=planta,
                defaults={
                    'descripcion': dept_data['descripcion'],
                    'activo': True,
                    'fecha_creacion': timezone.now()
                }
            )
            departamentos_creados.append(dept)
        
        # 4. Crear puestos demo
        puestos_data = [
            {'nombre': 'Gerente de Recursos Humanos', 'departamento': 'Recursos Humanos'},
            {'nombre': 'Supervisor de Producción', 'departamento': 'Producción'},
            {'nombre': 'Operador de Máquina', 'departamento': 'Producción'},
            {'nombre': 'Inspector de Calidad', 'departamento': 'Calidad'},
            {'nombre': 'Técnico de Mantenimiento', 'departamento': 'Mantenimiento'},
            {'nombre': 'Asistente Administrativo', 'departamento': 'Administración'}
        ]
        
        puestos_creados = []
        for puesto_data in puestos_data:
            # Buscar el departamento correspondiente
            departamento = next((d for d in departamentos_creados if d.nombre == puesto_data['departamento']), None)
            if departamento:
                puesto, created = Puesto.objects.get_or_create(
                    nombre=puesto_data['nombre'],
                    departamento=departamento,
                    defaults={
                        'descripcion': f'Puesto de {puesto_data["nombre"]}',
                        'activo': True,
                        'fecha_creacion': timezone.now()
                    }
                )
                puestos_creados.append(puesto)
        
        # 5. Crear empleados demo
        empleados_data = [
            {'nombre': 'Juan', 'apellidos': 'Pérez García', 'puesto': 'Gerente de Recursos Humanos'},
            {'nombre': 'María', 'apellidos': 'López Rodríguez', 'puesto': 'Supervisor de Producción'},
            {'nombre': 'Carlos', 'apellidos': 'González Martínez', 'puesto': 'Operador de Máquina'},
            {'nombre': 'Ana', 'apellidos': 'Hernández López', 'puesto': 'Inspector de Calidad'},
            {'nombre': 'Luis', 'apellidos': 'Ramírez Torres', 'puesto': 'Técnico de Mantenimiento'},
            {'nombre': 'Elena', 'apellidos': 'Morales Sánchez', 'puesto': 'Asistente Administrativo'}
        ]
        
        empleados_creados = []
        for i, emp_data in enumerate(empleados_data, 1):
            # Buscar el puesto correspondiente
            puesto = next((p for p in puestos_creados if p.nombre == emp_data['puesto']), None)
            if puesto:
                empleado, created = Empleado.objects.get_or_create(
                    numero_empleado=f'EMP{i:03d}',
                    defaults={
                        'nombre': emp_data['nombre'],
                        'apellidos': emp_data['apellidos'],
                        'puesto': puesto,
                        'email': f'{emp_data["nombre"].lower()}.{emp_data["apellidos"].split()[0].lower()}@demo.com',
                        'telefono': f'55-1234-567{i}',
                        'activo': True,
                        'fecha_ingreso': timezone.now().date(),
                        'fecha_creacion': timezone.now()
                    }
                )
                empleados_creados.append(empleado)
        
        # Respuesta de éxito
        return Response({
            'success': True,
            'message': 'Datos demo cargados exitosamente (versión simplificada)',
            'datos_creados': {
                'empresa': {
                    'id': empresa.id,
                    'nombre': empresa.nombre,
                    'admin': usuario_admin.username
                },
                'planta': {
                    'id': planta.id,
                    'nombre': planta.nombre
                },
                'departamentos': len(departamentos_creados),
                'puestos': len(puestos_creados),
                'empleados': len(empleados_creados)
            },
            'detalles': {
                'departamentos': [d.nombre for d in departamentos_creados],
                'puestos': [p.nombre for p in puestos_creados],
                'empleados': [f'{e.nombre} {e.apellidos}' for e in empleados_creados]
            },
            'fecha_carga': timezone.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        return Response({
            'success': False,
            'error': f'Error cargando datos demo: {str(e)}',
            'traceback': traceback.format_exc(),
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












