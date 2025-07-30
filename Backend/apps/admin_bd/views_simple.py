# -*- coding: utf-8 -*-
"""
Views simplificadas para gestión de BD - Versión mínima funcional
Enfocado en cumplir los requisitos específicos solicitados
"""
import csv
import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.db import connection, transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models_simple import EmpleadoSimple, EmpresaSimple, PlantaSimple, DepartamentoSimple, PuestoSimple
from apps.subscriptions.models import SuscripcionEmpresa
from .models import LogRespaldo


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportar_tabla_csv_simple(request, tabla_nombre):
    """
    Exportar datos de tablas específicas a CSV - Versión simplificada
    Cumple requisito 8: Permitir descargar información de una tabla mínimo, a un archivo CSV
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Solo SuperAdmin puede exportar todo
        if perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede exportar tablas'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Definir tablas y campos disponibles para exportación
        tablas_disponibles = {
            'empresas': {
                'modelo': EmpresaSimple,
                'campos': ['empresa_id', 'nombre', 'rfc', 'email_contacto', 'telefono']
            },
            'empleados': {
                'modelo': EmpleadoSimple,
                'campos': ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono']
            },
            'plantas': {
                'modelo': PlantaSimple,
                'campos': ['planta_id', 'nombre', 'direccion', 'telefono', 'empresa']
            },
            'departamentos': {
                'modelo': DepartamentoSimple,
                'campos': ['departamento_id', 'nombre', 'descripcion', 'planta']
            },
            'puestos': {
                'modelo': PuestoSimple,
                'campos': ['puesto_id', 'nombre', 'descripcion', 'departamento']
            }
        }
        
        if tabla_nombre not in tablas_disponibles:
            return Response({'error': f'Tabla {tabla_nombre} no disponible'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener configuración de la tabla
        config = tablas_disponibles[tabla_nombre]
        modelo = config['modelo']
        campos = config['campos']
        
        # Obtener datos
        queryset = modelo.objects.all()
        
        # Crear respuesta CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{tabla_nombre}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # BOM para Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # Escribir encabezados
        encabezados = [campo.replace('_', ' ').title() for campo in campos]
        writer.writerow(encabezados)
        
        # Escribir datos
        for obj in queryset:
            fila = []
            for campo in campos:
                valor = getattr(obj, campo, '')
                fila.append(str(valor) if valor is not None else '')
            writer.writerow(fila)
        
        # Registrar en log
        LogRespaldo.objects.create(
            tipo='parcial',
            usuario=user,
            archivo_nombre=f"{tabla_nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            tablas_incluidas=[tabla_nombre],
            exitoso=True,
            detalles=f'Exportación CSV de tabla {tabla_nombre}'
        )
        
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_completo_simple(request):
    """
    Crear respaldo completo de la BD usando pg_dump
    Cumple requisito 4: Realizar un respaldo completo de la BD cuando el usuario que tenga acceso lo solicite
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede crear respaldos completos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Configuración de la base de datos
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Crear archivo de respaldo con ruta independiente del nombre del proyecto
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'respaldo_completo_{timestamp}.sql'
        backend_dir = settings.BASE_DIR.parent  # Backend/config -> Backend/
        backup_dir = backend_dir / 'config' / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = str(backup_dir / backup_filename)
        
        # Comando pg_dump
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',  # Ruta al ejecutable de pg_dump
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--clean',
            '--no-owner',
            '--no-privileges',
            f'--file={backup_path}',
            db_name
        ]
        
        # Configurar contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar respaldo
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            tamaño = os.path.getsize(backup_path)
            
            # Registrar en log
            LogRespaldo.objects.create(
                tipo='completo',
                usuario=user,
                archivo_nombre=backup_filename,
                archivo_ruta=backup_path,
                archivo_tamaño=tamaño,
                tablas_incluidas=['TODAS'],
                exitoso=True,
                detalles='Respaldo completo usando pg_dump'
            )
            
            return Response({
                'message': 'Respaldo completo creado exitosamente',
                'archivo': backup_filename,
                'tamaño': tamaño,
                'ruta_descarga': f'/api/admin-bd/descargar-respaldo/{backup_filename}/'
            })
        else:
            return Response({
                'error': 'Error al crear respaldo',
                'detalles': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_parcial_simple(request):
    """
    Crear respaldo parcial de tablas específicas
    Cumple requisito 5: Realizar un respaldo parcial (1 o varias tablas) cuando el usuario que tenga acceso lo solicite
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede crear respaldos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        tablas = request.data.get('tablas', [])
        if not tablas:
            return Response({'error': 'Debe especificar al menos una tabla'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Mapeo de nombres a tablas reales
        tabla_mapping = {
            'empresas': 'empresas',
            'empleados': 'empleados',
            'plantas': 'plantas',
            'departamentos': 'departamentos',
            'puestos': 'puestos'
        }
        
        # Validar tablas
        tablas_reales = []
        for tabla in tablas:
            if tabla in tabla_mapping:
                tablas_reales.append(tabla_mapping[tabla])
            else:
                return Response({'error': f'Tabla {tabla} no válida'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        # Configuración de BD
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Crear archivo de respaldo con ruta independiente del nombre del proyecto
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'respaldo_parcial_{timestamp}.sql'
        backend_dir = settings.BASE_DIR.parent  # Backend/config -> Backend/
        backup_dir = backend_dir / 'config' / 'backups'
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = str(backup_dir / backup_filename)
        
        # Comando pg_dump para tablas específicas
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--clean',
            '--no-owner',
            '--no-privileges',
            f'--file={backup_path}'
        ]
        
        # Agregar tablas específicas
        for tabla in tablas_reales:
            cmd.extend(['--table', tabla])
        
        cmd.append(db_name)
        
        # Configurar contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar respaldo
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            tamaño = os.path.getsize(backup_path)
            
            # Registrar en log
            LogRespaldo.objects.create(
                tipo='parcial',
                usuario=user,
                archivo_nombre=backup_filename,
                archivo_ruta=backup_path,
                archivo_tamaño=tamaño,
                tablas_incluidas=tablas,
                exitoso=True,
                detalles=f'Respaldo parcial de {len(tablas)} tablas'
            )
            
            return Response({
                'message': 'Respaldo parcial creado exitosamente',
                'archivo': backup_filename,
                'tablas': tablas,
                'tamaño': tamaño,
                'ruta_descarga': f'/api/admin-bd/descargar-respaldo/{backup_filename}/'
            })
        else:
            return Response({
                'error': 'Error al crear respaldo parcial',
                'detalles': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurar_bd_simple(request):
    """
    Restaurar BD desde archivo SQL
    Cumple requisitos 6 y 7: Restaurar la BD al punto de inicio y restaurar respaldo parcial
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede restaurar la BD'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        archivo_sql = request.FILES.get('archivo_sql')
        if not archivo_sql:
            return Response({'error': 'Debe proporcionar un archivo SQL'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar archivo temporal
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', archivo_sql.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, 'wb+') as destination:
            for chunk in archivo_sql.chunks():
                destination.write(chunk)
        
        # Configuración de BD
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Comando psql para restaurar
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--dbname', db_name,
            '--file', temp_path
        ]
        
        # Configurar contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar restauración
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        if result.returncode == 0:
            # Registrar en log
            LogRespaldo.objects.create(
                tipo='restauracion',
                usuario=user,
                archivo_nombre=archivo_sql.name,
                exitoso=True,
                detalles='Restauración exitosa desde archivo SQL'
            )
            
            return Response({
                'message': 'Base de datos restaurada exitosamente',
                'archivo': archivo_sql.name
            })
        else:
            return Response({
                'error': 'Error al restaurar base de datos',
                'detalles': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def descargar_respaldo_simple(request, archivo_nombre):
    """
    Descargar archivo de respaldo
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede descargar respaldos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Verificar que el archivo existe en logs
        log_respaldo = LogRespaldo.objects.filter(
            archivo_nombre=archivo_nombre,
            exitoso=True
        ).first()
        
        if not log_respaldo:
            return Response({'error': 'Archivo no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Ruta del archivo
        archivo_path = log_respaldo.archivo_ruta or os.path.join(
            settings.MEDIA_ROOT, 'backups', archivo_nombre
        )
        
        if not os.path.exists(archivo_path):
            return Response({'error': 'Archivo físico no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Crear respuesta de descarga
        with open(archivo_path, 'rb') as archivo:
            response = HttpResponse(archivo.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{archivo_nombre}"'
            return response
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_tablas_simple(request):
    """
    Listar tablas disponibles para exportación
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede listar tablas'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        tablas = [
            {'nombre': 'empresas', 'descripcion': 'Información de empresas'},
            {'nombre': 'empleados', 'descripcion': 'Datos de empleados'},
            {'nombre': 'plantas', 'descripcion': 'Plantas de las empresas'},
            {'nombre': 'departamentos', 'descripcion': 'Departamentos por planta'},
            {'nombre': 'puestos', 'descripcion': 'Puestos de trabajo'}
        ]
        
        return Response({
            'tablas_disponibles': tablas,
            'nivel_usuario': perfil.nivel_usuario
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
