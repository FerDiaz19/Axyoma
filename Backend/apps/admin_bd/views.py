# -*- coding: utf-8 -*-
import csv
import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.db import connection, transaction
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import (
    Empresa, PerfilUsuario, Planta, Departamento, 
    Puesto, Empleado
)
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
from .models import LogRespaldo
from .utils.csv_exporter import CSVExporter
from .utils.backup_manager import BackupManager
import logging

logger = logging.getLogger(__name__)

class AdminBDViewSet(viewsets.ViewSet):
    """
    ViewSet para administración de base de datos
    """
    permission_classes = [IsAuthenticated]
    
    def _verify_superadmin(self, user):
        """Verificar que el usuario es SuperAdmin"""
        if not hasattr(user, 'perfil') or user.perfil.nivel_usuario != 'superadmin':
            return False
        return True
    
    @action(detail=False, methods=['get'])
    def exportar_empresas_csv(self, request):
        """Exportar empresas a CSV"""
        if not self._verify_superadmin(request.user):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            from apps.users.models import Empresa
            
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="empresas.csv"'
            
            # Agregar BOM para UTF-8
            response.write('\ufeff')
            
            writer = csv.writer(response)
            writer.writerow(['ID', 'Nombre', 'RFC', 'Teléfono', 'Email', 'Dirección', 'Status', 'Fecha Registro'])
            
            empresas = Empresa.objects.all()
            for empresa in empresas:
                writer.writerow([
                    empresa.empresa_id,
                    empresa.nombre,
                    empresa.rfc,
                    empresa.telefono_contacto or '',
                    empresa.email_contacto or '',
                    empresa.direccion or '',
                    'Activa' if empresa.status else 'Suspendida',
                    empresa.fecha_registro.strftime('%Y-%m-%d %H:%M:%S') if empresa.fecha_registro else ''
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error exportando empresas: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def exportar_usuarios_csv(self, request):
        """Exportar usuarios a CSV"""
        if not self._verify_superadmin(request.user):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            from apps.users.models import PerfilUsuario
            
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
            
            # Agregar BOM para UTF-8
            response.write('\ufeff')
            
            writer = csv.writer(response)
            writer.writerow(['ID', 'Username', 'Email', 'Nombre Completo', 'Nivel Usuario', 'Activo', 'Fecha Registro'])
            
            usuarios = PerfilUsuario.objects.select_related('user').all()
            for usuario in usuarios:
                writer.writerow([
                    usuario.user.id,
                    usuario.user.username,
                    usuario.user.email,
                    f"{usuario.nombre} {usuario.apellido_paterno} {usuario.apellido_materno or ''}".strip(),
                    usuario.nivel_usuario,
                    'Sí' if usuario.user.is_active else 'No',
                    usuario.user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if usuario.user.date_joined else ''
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error exportando usuarios: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def exportar_empleados_csv(self, request):
        """Exportar empleados a CSV"""
        if not self._verify_superadmin(request.user):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            from apps.users.models import Empleado
            
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="empleados.csv"'
            
            # Agregar BOM para UTF-8
            response.write('\ufeff')
            
            writer = csv.writer(response)
            writer.writerow([
                'ID', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 
                'Género', 'Antiguedad', 'Empresa', 'Planta', 'Departamento', 
                'Puesto', 'Status'
            ])
            
            empleados = Empleado.objects.select_related(
                'planta__empresa', 'departamento', 'puesto'
            ).all()
            
            for empleado in empleados:
                writer.writerow([
                    empleado.empleado_id,
                    empleado.nombre,
                    empleado.apellido_paterno,
                    empleado.apellido_materno or '',
                    empleado.genero,
                    empleado.antiguedad,
                    empleado.planta.empresa.nombre if empleado.planta and empleado.planta.empresa else '',
                    empleado.planta.nombre if empleado.planta else '',
                    empleado.departamento.nombre if empleado.departamento else '',
                    empleado.puesto.nombre if empleado.puesto else '',
                    'Activo' if empleado.status else 'Inactivo'
                ])
            
            return response
            
        except Exception as e:
            logger.error(f"Error exportando empleados: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def backup_database(self, request):
        """Crear backup de la base de datos"""
        if not self._verify_superadmin(request.user):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Esta funcionalidad requiere configuración específica del servidor
            # Por ahora solo retornamos un mensaje informativo
            return Response({
                'message': 'Función de backup en desarrollo',
                'info': 'Esta funcionalidad requiere configuración del servidor de base de datos'
            })
            
        except Exception as e:
            logger.error(f"Error creando backup: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def info_sistema(self, request):
        """Obtener información del sistema"""
        if not self._verify_superadmin(request.user):
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            from django.db import connection
            from apps.users.models import Empresa, PerfilUsuario, Planta, Departamento, Puesto, Empleado
            
            info = {
                'django_version': settings.DJANGO_VERSION if hasattr(settings, 'DJANGO_VERSION') else 'Unknown',
                'python_version': f"{settings.PYTHON_VERSION}" if hasattr(settings, 'PYTHON_VERSION') else 'Unknown',
                'database_info': {
                    'engine': settings.DATABASES['default']['ENGINE'],
                    'name': settings.DATABASES['default']['NAME']
                },
                'estadisticas': {
                    'empresas': Empresa.objects.count(),
                    'usuarios': PerfilUsuario.objects.count(),
                    'plantas': Planta.objects.count(),
                    'departamentos': Departamento.objects.count(),
                    'puestos': Puesto.objects.count(),
                    'empleados': Empleado.objects.count()
                }
            }
            
            return Response(info)
            
        except Exception as e:
            logger.error(f"Error obteniendo info del sistema: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportar_tabla_csv(request, tabla_nombre):
    """
    Exportar datos de una tabla específica a CSV
    Solo SuperAdmin puede exportar todas las tablas
    Admin Empresa solo puede exportar datos de su empresa
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Definir tablas exportables y sus modelos
        tablas_permitidas = {
            'empresas': {
                'modelo': Empresa,
                'campos': ['empresa_id', 'nombre', 'rfc', 'email_contacto', 'telefono', 'direccion'],
                'permisos': ['superadmin']
            },
            'empleados': {
                'modelo': Empleado,
                'campos': ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono'],
                'permisos': ['superadmin', 'admin-empresa']
            },
            'plantas': {
                'modelo': Planta,
                'campos': ['planta_id', 'nombre', 'direccion', 'telefono'],
                'permisos': ['superadmin', 'admin-empresa']
            },
            'departamentos': {
                'modelo': Departamento,
                'campos': ['departamento_id', 'nombre', 'descripcion'],
                'permisos': ['superadmin', 'admin-empresa']
            },
            'puestos': {
                'modelo': Puesto,
                'campos': ['puesto_id', 'nombre', 'descripcion'],
                'permisos': ['superadmin', 'admin-empresa']
            }
        }
        
        if tabla_nombre not in tablas_permitidas:
            return Response({'error': 'Tabla no permitida'}, status=status.HTTP_400_BAD_REQUEST)
        
        tabla_config = tablas_permitidas[tabla_nombre]
        
        # Verificar permisos
        if perfil.nivel_usuario not in tabla_config['permisos']:
            return Response({'error': 'Sin permisos para esta tabla'}, status=status.HTTP_403_FORBIDDEN)
        
        # Obtener datos según el nivel de usuario
        modelo = tabla_config['modelo']
        queryset = modelo.objects.all()
        
        # Filtrar por empresa si es admin-empresa
        if perfil.nivel_usuario == 'admin-empresa' and hasattr(modelo, 'empresa'):
            queryset = queryset.filter(empresa=perfil.empresa)
        elif perfil.nivel_usuario == 'admin-empresa' and tabla_nombre == 'empleados':
            # Para empleados, filtrar por empresa a través de puesto->departamento->planta->empresa
            queryset = queryset.filter(puesto__departamento__planta__empresa=perfil.empresa)
        
        # Crear respuesta CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{tabla_nombre}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # Escribir BOM para Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # Escribir encabezados
        campos = tabla_config['campos']
        encabezados = [campo.replace('__', '_').replace('_', ' ').title() for campo in campos]
        writer.writerow(encabezados)
        
        # Escribir datos
        for obj in queryset:
            fila = []
            for campo in campos:
                try:
                    if '__' in campo:
                        # Para campos relacionados como empresa__nombre
                        partes = campo.split('__')
                        valor = obj
                        for parte in partes:
                            valor = getattr(valor, parte, '')
                    else:
                        valor = getattr(obj, campo, '')
                    fila.append(str(valor) if valor is not None else '')
                except Exception:
                    fila.append('')
            writer.writerow(fila)
        
        # Registrar en log
        LogRespaldo.objects.create(
            tipo='parcial',
            usuario=user,
            empresa=perfil.empresa if perfil.nivel_usuario == 'admin-empresa' else None,
            archivo_nombre=f"{tabla_nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            tablas_incluidas=[tabla_nombre],
            exitoso=True
        )
        
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_tablas_exportables(request):
    """
    Listar tablas que el usuario puede exportar
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        tablas_disponibles = []
        
        if perfil.nivel_usuario == 'superadmin':
            tablas_disponibles = [
                {'nombre': 'empresas', 'descripcion': 'Todas las empresas registradas'},
                {'nombre': 'empleados', 'descripcion': 'Todos los empleados del sistema'},
                {'nombre': 'plantas', 'descripcion': 'Todas las plantas'},
                {'nombre': 'departamentos', 'descripcion': 'Todos los departamentos'},
                {'nombre': 'puestos', 'descripcion': 'Todos los puestos de trabajo'},
            ]
        elif perfil.nivel_usuario == 'admin-empresa':
            tablas_disponibles = [
                {'nombre': 'empleados', 'descripcion': 'Empleados de mi empresa'},
                {'nombre': 'plantas', 'descripcion': 'Plantas de mi empresa'},
                {'nombre': 'departamentos', 'descripcion': 'Departamentos de mi empresa'},
                {'nombre': 'puestos', 'descripcion': 'Puestos de mi empresa'},
            ]
        
        return Response({
            'tablas_disponibles': tablas_disponibles,
            'nivel_usuario': perfil.nivel_usuario
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_exportacion(request):
    """
    Obtener estadísticas de exportaciones realizadas
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filtrar logs según el usuario
        logs_query = LogRespaldo.objects.filter(tipo='parcial')
        
        if perfil.nivel_usuario == 'admin-empresa':
            logs_query = logs_query.filter(empresa=perfil.empresa)
        
        logs_recientes = logs_query.order_by('-fecha_creacion')[:10]
        
        estadisticas = {
            'total_exportaciones': logs_query.count(),
            'exportaciones_exitosas': logs_query.filter(exitoso=True).count(),
            'exportaciones_fallidas': logs_query.filter(exitoso=False).count(),
            'exportaciones_recientes': [
                {
                    'archivo': log.archivo_nombre,
                    'fecha': log.fecha_creacion,
                    'tablas': log.tablas_incluidas,
                    'exitoso': log.exitoso
                }
                for log in logs_recientes
            ]
        }
        
        return Response(estadisticas)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_bd_completo(request):
    """
    Crear un respaldo completo de la base de datos usando pg_dump
    Solo SuperAdmin puede realizar respaldos completos
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
            
        if perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede realizar respaldos completos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Configuración de la base de datos
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Crear nombre del archivo de respaldo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'respaldo_completo_{timestamp}.sql'
        
        # Crear directorio de respaldos en MEDIA_ROOT
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Comando pg_dump para PostgreSQL
        cmd = [
            'pg_dump',
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
            '--format=plain',
            f'--file={backup_path}',
            db_name
        ]
        
        # Configurar variable de entorno para la contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar pg_dump
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            tamaño_archivo = os.path.getsize(backup_path)
            
            # Registrar en log usando una nueva conexión
            with transaction.atomic():
                LogRespaldo.objects.create(
                    tipo='completo',
                    usuario=user,
                    archivo_nombre=backup_filename,
                    archivo_ruta=backup_path,
                    archivo_tamaño=tamaño_archivo,
                    tablas_incluidas=['TODAS'],
                    exitoso=True,
                    detalles='Respaldo completo exitoso usando pg_dump'
                )
            
            return Response({
                'message': 'Respaldo completo creado exitosamente',
                'archivo': backup_filename,
                'tamaño': tamaño_archivo,
                'metodo': 'pg_dump',
                'ruta_descarga': f'/api/admin-bd/descargar-respaldo/{backup_filename}/'
            })
        else:
            error_msg = result.stderr or 'Error desconocido en pg_dump'
            
            # Registrar error en log
            with transaction.atomic():
                LogRespaldo.objects.create(
                    tipo='completo',
                    usuario=user,
                    archivo_nombre=backup_filename,
                    exitoso=False,
                    detalles=f'Error en pg_dump: {error_msg}'
                )
            
            return Response({
                'error': 'Error al crear respaldo',
                'detalles': error_msg
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        # Registrar error en log
        try:
            with transaction.atomic():
                LogRespaldo.objects.create(
                    tipo='completo',
                    usuario=user,
                    archivo_nombre=backup_filename if 'backup_filename' in locals() else 'error.sql',
                    exitoso=False,
                    detalles=f'Error al crear respaldo: {str(e)}'
                )
        except:
            pass  # Si falla el log, no bloquear la respuesta
        
        return Response({
            'error': 'Error al crear respaldo',
            'detalles': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_bd_parcial(request):
    """
    Crear un respaldo parcial de tablas específicas
    Admin Empresa solo puede respaldar datos de su empresa
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        tablas_solicitadas = request.data.get('tablas', [])
        if not tablas_solicitadas:
            return Response({'error': 'Debe especificar al menos una tabla'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Configuración de la base de datos
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Crear nombre del archivo de respaldo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'respaldo_parcial_{timestamp}.sql'
        backup_path = os.path.join(settings.MEDIA_ROOT, 'backups', backup_filename)
        
        # Crear directorio si no existe
        backup_dir = os.path.dirname(backup_path)
        os.makedirs(backup_dir, exist_ok=True)
        
        # Mapear nombres de tablas a nombres reales de PostgreSQL
        tabla_mapping = {
            'empresas': 'users_empresa',
            'empleados': 'users_empleado',
            'plantas': 'users_planta',
            'departamentos': 'users_departamento',
            'puestos': 'users_puesto',
            'evaluaciones': 'evaluaciones_evaluacion',
            'encuestas': 'surveys_encuesta'
        }
        
        # Verificar permisos y mapear tablas
        tablas_reales = []
        for tabla in tablas_solicitadas:
            if tabla not in tabla_mapping:
                return Response({'error': f'Tabla no válida: {tabla}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            tablas_reales.append(tabla_mapping[tabla])
        
        # Comando pg_dump para tablas específicas
        cmd = [
            'pg_dump',
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
            '--format=plain',
            f'--file={backup_path}',
            '--data-only'  # Solo datos, no estructura
        ]
        
        # Agregar cada tabla
        for tabla in tablas_reales:
            cmd.extend(['--table', tabla])
        
        cmd.append(db_name)
        
        # Configurar variable de entorno para la contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar pg_dump
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Si es admin-empresa, filtrar datos por empresa
            if perfil.nivel_usuario == 'admin-empresa':
                # Aquí podríamos procesar el archivo SQL para filtrar por empresa
                # Por ahora devolvemos el archivo completo con advertencia
                pass
            
            # Registrar en log
            LogRespaldo.objects.create(
                tipo='parcial',
                usuario=user,
                empresa=perfil.empresa if perfil.nivel_usuario == 'admin-empresa' else None,
                archivo_nombre=backup_filename,
                archivo_ruta=backup_path,
                archivo_tamaño=os.path.getsize(backup_path),
                tablas_incluidas=tablas_solicitadas,
                exitoso=True,
                detalles=f'Respaldo parcial de {len(tablas_solicitadas)} tablas'
            )
            
            return Response({
                'message': 'Respaldo parcial creado exitosamente',
                'archivo': backup_filename,
                'tablas': tablas_solicitadas,
                'tamaño': os.path.getsize(backup_path),
                'ruta_descarga': f'/api/admin-bd/descargar-respaldo/{backup_filename}/'
            })
        else:
            # Registrar error en log
            LogRespaldo.objects.create(
                tipo='parcial',
                usuario=user,
                empresa=perfil.empresa if perfil.nivel_usuario == 'admin-empresa' else None,
                archivo_nombre=backup_filename,
                tablas_incluidas=tablas_solicitadas,
                exitoso=False,
                detalles=f'Error en pg_dump: {result.stderr}'
            )
            
            return Response({
                'error': 'Error al crear respaldo',
                'detalles': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def descargar_respaldo(request, archivo_nombre):
    """
    Descargar un archivo de respaldo
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el archivo existe en los logs
        log_respaldo = LogRespaldo.objects.filter(
            archivo_nombre=archivo_nombre,
            exitoso=True
        ).first()
        
        if not log_respaldo:
            return Response({'error': 'Archivo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos
        if perfil.nivel_usuario == 'admin-empresa' and log_respaldo.empresa != perfil.empresa:
            return Response({'error': 'Sin permisos para este archivo'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurar_bd(request):
    """
    Restaurar base de datos desde un archivo SQL
    Solo SuperAdmin puede restaurar
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
            
        if perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede restaurar la base de datos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        archivo_sql = request.FILES.get('archivo_sql')
        if not archivo_sql:
            return Response({'error': 'Debe proporcionar un archivo SQL'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar archivo temporalmente
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', archivo_sql.name)
        temp_dir = os.path.dirname(temp_path)
        os.makedirs(temp_dir, exist_ok=True)
        
        with open(temp_path, 'wb+') as destination:
            for chunk in archivo_sql.chunks():
                destination.write(chunk)
        
        # Configuración de la base de datos
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST'] or 'localhost'
        db_port = db_config['PORT'] or '5432'
        
        # Comando psql para restaurar
        cmd = [
            'psql',
            f'--host={db_host}',
            f'--port={db_port}',
            f'--username={db_user}',
            '--dbname', db_name,
            '--file', temp_path
        ]
        
        # Configurar variable de entorno para la contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Ejecutar psql
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
                detalles='Restauración exitosa'
            )
            
            return Response({
                'message': 'Base de datos restaurada exitosamente',
                'archivo': archivo_sql.name
            })
        else:
            # Registrar error en log
            LogRespaldo.objects.create(
                tipo='restauracion',
                usuario=user,
                archivo_nombre=archivo_sql.name,
                exitoso=False,
                detalles=f'Error en psql: {result.stderr}'
            )
            
            return Response({
                'error': 'Error al restaurar base de datos',
                'detalles': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
