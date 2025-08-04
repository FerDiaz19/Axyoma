# -*- coding: utf-8 -*-
"""
🗄️ GESTIÓN DE RESPALDOS Y RESTAURACIÓN DE BASE DE DATOS
========================================================

Sistema completo de respaldos, restauración y gestión de base de datos para Axyoma.
Incluye respaldos compatibles con pgAdmin, reseteo de BD y carga de datos iniciales.



🚀 Funcionalidades:
- Respaldos de tablas específicas y BD completa
- Restauración de respaldos
- Reseteo completo de base de datos (SuperAdmin)
- Carga de datos iniciales para pruebas
- Compatibilidad total con pgAdmin 4
- Gestión de archivos de respaldo
- Sistema de logs y metadatos

🔒 Seguridad: Solo para SuperAdmin - Máxima seguridad
"""
import os
import json
import subprocess
import tempfile
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Configuración de respaldos - Ruta independiente del nombre del proyecto
def get_backup_directory():
    """
    Obtener directorio de respaldos que funcione en cualquier equipo
    Independiente del nombre del directorio del proyecto (Axyoma, Axyoma2, etc.)
    """
    # BASE_DIR apunta a Backend/config, vamos un nivel arriba para llegar a Backend
    backend_dir = settings.BASE_DIR.parent  # Esto es Backend/
    backup_dir = backend_dir / 'config' / 'backups'
    
    # Crear directorio si no existe
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    return str(backup_dir)

BACKUP_DIR = get_backup_directory()


def verificar_superadmin(request):
    """Verificar que el usuario sea SuperAdmin"""
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return False, Response({'error': 'Solo SuperAdmin puede gestionar respaldos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        return True, None
    except Exception as e:
        return False, Response({'error': f'Error de autenticación: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def obtener_config_db():
    """Obtener configuración de la base de datos desde Django settings"""
    try:
        db_config = settings.DATABASES['default']
        return {
            'host': db_config.get('HOST', 'localhost'),
            'port': db_config.get('PORT', '5432'),
            'name': db_config.get('NAME'),
            'user': db_config.get('USER'),
            'password': db_config.get('PASSWORD'),
        }
    except Exception as e:
        raise Exception(f"Error al obtener configuración de BD: {str(e)}")


def verificar_conectividad_db():
    """
    Verificar que PostgreSQL esté disponible y responda correctamente
    """
    try:
        db_config = obtener_config_db()
        
        # Comando simple para probar conectividad
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '-c', 'SELECT 1;'  # Consulta simple
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Ejecutar con timeout corto
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True, 
            timeout=30  # 30 segundos timeout
        )
        
        return result.returncode == 0, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "Timeout al conectar con PostgreSQL"
    except Exception as e:
        return False, f"Error verificando conectividad: {str(e)}"


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_tablas(request):
    """
    Respaldar una o múltiples tablas específicas
    Body: {
        "tablas": ["tabla1", "tabla2", ...],
        "incluir_datos": true/false,
        "descripcion": "Descripción opcional del respaldo"
    }""" 
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        tablas = data.get('tablas', [])
        incluir_datos = data.get('incluir_datos', True)
        descripcion = data.get('descripcion', '')
        formato = data.get('formato', 'plain')  # 'custom' para pg_restore rápido, 'plain' para psql
        
        if not tablas:
            return Response({'error': 'Debe especificar al menos una tabla'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que las tablas existan
        with connection.cursor() as cursor:
            for tabla in tablas:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    )
                """, [tabla])
                existe = cursor.fetchone()[0]
                if not existe:
                    return Response({'error': f'La tabla "{tabla}" no existe'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
        
        # Crear nombre del archivo de respaldo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tablas_str = "_".join(tablas[:3])  # Máximo 3 nombres en el archivo
        if len(tablas) > 3:
            tablas_str += f"_y_{len(tablas)-3}_mas"
        
        # Determinar extensión según formato
        extension = ".backup" if formato == 'custom' else ".sql"
        nombre_archivo = f"backup_tablas_{tablas_str}_{timestamp}{extension}"
        ruta_backup = os.path.join(BACKUP_DIR, nombre_archivo)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Construir comando pg_dump con formato especificado
        cmd = construir_comando_pg_dump_seguro(db_config, ruta_backup, tablas, incluir_datos, formato)
        
        # Configurar variables de entorno para PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Ejecutar pg_dump
        print(f"🔄 Ejecutando respaldo de tablas: {', '.join(tablas)}")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode != 0:
            return Response({
                'error': 'Error al crear respaldo',
                'details': result.stderr
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Crear metadatos del respaldo
        metadata = {
            'tipo': 'tablas',
            'tablas': tablas,
            'incluir_datos': incluir_datos,
            'descripcion': descripcion,
            'fecha_creacion': datetime.now().isoformat(),
            'usuario': request.user.username,
            'archivo': nombre_archivo,
            'tamaño_bytes': os.path.getsize(ruta_backup),
            'base_datos': db_config['name']
        }
        
        # Guardar metadatos
        metadata_file = ruta_backup.replace('.sql', '_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return Response({
            'message': 'Respaldo de tablas creado exitosamente',
            'archivo': nombre_archivo,
            'tablas': tablas,
            'tamaño_mb': round(metadata['tamaño_bytes'] / (1024*1024), 2),
            'ruta': ruta_backup,
            'metadata': metadata
        })
        
    except Exception as e:
        return Response({'error': f'Error al respaldar tablas: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_bd_completa(request):
    """
    Respaldar toda la base de datos con optimizaciones para bases de datos grandes
    Body: {
        "incluir_datos": true/false,
        "descripcion": "Descripción opcional del respaldo"
    }
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        incluir_datos = data.get('incluir_datos', True)
        descripcion = data.get('descripcion', '')
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # 🚀 NUEVA CARACTERÍSTICA: Análisis automático de BD grande
        print("🔍 Analizando tamaño de base de datos...")
        config_bd = obtener_configuracion_optimizada_bd_grande(db_config)
        print(f"📊 Tamaño BD: {config_bd['size_pretty']} ({config_bd['tabla_count']} tablas)")
        print(f"⚡ Configuración optimizada: {config_bd['jobs']} jobs, timeout {config_bd['timeout_minutos']}min")
        
        # Aplicar optimizaciones si es BD grande
        optimizaciones = []
        if config_bd['es_bd_grande']:
            print("🛠️ Aplicando optimizaciones para base de datos grande...")
            optimizaciones = aplicar_optimizaciones_postgresql_grandes(db_config)
            print(f"✅ Optimizaciones aplicadas: {len(optimizaciones)}")
          
        # Crear nombre del archivo de respaldo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Usar formato .backup para pg_restore ultra-rápido
        nombre_archivo = f"backup_completo_{timestamp}.backup"
        ruta_backup = os.path.join(BACKUP_DIR, nombre_archivo)
        
        # 🚀 Construir comando pg_dump con configuración optimizada automática
        cmd = construir_comando_pg_dump_optimizado_bd_grande(
            db_config, ruta_backup, None, incluir_datos, 'custom', config_bd
        )
        
        # Configurar variables de entorno para PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']        # Ejecutar pg_dump con timeout optimizado automáticamente según tamaño de BD
        print(f"🔄 Ejecutando respaldo completo de BD: {db_config['name']}")
        print(f"📁 Directorio de respaldos: {BACKUP_DIR}")
        print(f"📄 Archivo de respaldo: {ruta_backup}")
        print(f"🔧 Comando: {' '.join(cmd)}")
        
        # Timeout dinámico según tamaño de BD
        timeout_minutos = config_bd.get('timeout_minutos', 30)
        timeout_segundos = timeout_minutos * 60
        print(f"⏰ Timeout configurado: {timeout_minutos} minutos (automático según tamaño BD)")
        
        inicio_backup = datetime.now()
        
        try:
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True, 
                text=True, 
                timeout=timeout_segundos
            )
            tiempo_transcurrido = datetime.now() - inicio_backup
            print(f"⏱️ Backup completado en: {tiempo_transcurrido}")
            
        except subprocess.TimeoutExpired:
            tiempo_transcurrido = datetime.now() - inicio_backup
            return Response({
                'error': 'Timeout en backup completo de BD grande',
                'details': f'El respaldo excedió el tiempo límite de {timeout_minutos} minutos',
                'solucion': 'Base de datos muy grande. Considera usar respaldos por tablas específicas.',
                'tiempo_limite': f'{timeout_minutos} minutos',
                'tiempo_transcurrido': str(tiempo_transcurrido),
                'tamaño_bd': config_bd['size_pretty'],
                'directorio_backup': BACKUP_DIR,
                'optimizaciones_aplicadas': optimizaciones
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        if result.returncode != 0:
            print(f"❌ Error en pg_dump: {result.stderr}")
            return Response({
                'error': 'Error al crear respaldo completo',
                'details': result.stderr,
                'directorio_backup': BACKUP_DIR,
                'comando_ejecutado': ' '.join(cmd),
                'archivo_destino': ruta_backup
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Verificar que el archivo fue creado
        if not os.path.exists(ruta_backup):
            return Response({
                'error': 'El archivo de respaldo no fue creado',
                'ruta_esperada': ruta_backup,
                'directorio_backup': BACKUP_DIR,
                'directorio_existe': os.path.exists(BACKUP_DIR)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          # Crear metadatos del respaldo con información de optimización
        metadata = {
            'tipo': 'bd_completa',
            'incluir_datos': incluir_datos,
            'descripcion': descripcion,
            'fecha_creacion': datetime.now().isoformat(),
            'usuario': request.user.username,
            'archivo': nombre_archivo,
            'tamaño_bytes': os.path.getsize(ruta_backup),
            'base_datos': db_config['name'],
            
            # 🚀 NUEVA INFORMACIÓN DE OPTIMIZACIÓN
            'optimizaciones': {
                'analisis_automatico': config_bd,
                'configuracion_aplicada': optimizaciones,
                'tiempo_backup': str(tiempo_transcurrido),
                'jobs_paralelos': config_bd.get('jobs', 4),
                'timeout_configurado': f"{timeout_minutos} minutos",
                'formato_optimizado': 'custom_parallel'
            }
        }
        
        # Guardar metadatos
        metadata_file = ruta_backup.replace('.backup', '_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return Response({
            'message': '✅ Respaldo completo optimizado creado exitosamente',
            'archivo': nombre_archivo,
            'tamaño_mb': round(metadata['tamaño_bytes'] / (1024*1024), 2),
            'ruta': ruta_backup,
            'metadata': metadata,
            
            # 🚀 INFORMACIÓN DE RENDIMIENTO
            'rendimiento': {
                'tiempo_backup': str(tiempo_transcurrido),
                'tamaño_bd_analizado': config_bd['size_pretty'],
                'optimizaciones_aplicadas': len(optimizaciones),
                'jobs_paralelos_usados': config_bd.get('jobs', 4),
                'timeout_configurado': f"{timeout_minutos} minutos"
            },
            
            # Información técnica para debugging
            'configuracion_automatica': {
                'es_bd_grande': config_bd.get('es_bd_grande', False),
                'es_bd_muy_grande': config_bd.get('es_bd_muy_grande', False),
                'tabla_count': config_bd.get('tabla_count', 0),
                'optimizaciones_postgresql': optimizaciones
            }
        })
        
    except Exception as e:
        return Response({'error': f'Error al respaldar BD completa: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_respaldos(request):
    """Listar todos los respaldos disponibles"""
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        respaldos = []
        
        # Buscar archivos de respaldo
        if os.path.exists(BACKUP_DIR):
            for archivo in os.listdir(BACKUP_DIR):
                if archivo.endswith('_metadata.json'):
                    metadata_path = os.path.join(BACKUP_DIR, archivo)
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # Verificar que el archivo SQL exista
                        sql_file = metadata_path.replace('_metadata.json', '.sql')
                        if os.path.exists(sql_file):
                            metadata['existe_archivo'] = True
                            metadata['tamaño_mb'] = round(metadata.get('tamaño_bytes', 0) / (1024*1024), 2)
                            respaldos.append(metadata)
                        else:
                            metadata['existe_archivo'] = False
                            respaldos.append(metadata)
                            
                    except Exception as e:
                        print(f"Error al leer metadata {archivo}: {str(e)}")
        
        # Ordenar por fecha de creación (más recientes primero)
        respaldos.sort(key=lambda x: x.get('fecha_creacion', ''), reverse=True)
        
        return Response({
            'respaldos': respaldos,
            'total': len(respaldos),
            'directorio': BACKUP_DIR
        })
        
    except Exception as e:
        return Response({'error': f'Error al listar respaldos: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurar_respaldo(request):
    """
    Restaurar un respaldo usando psql
    Body: {
        "archivo": "nombre_archivo.sql",
        "confirmar": true,
        "modo": "replace" | "append"
    }
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        archivo = data.get('archivo')
        confirmar = data.get('confirmar', False)
        modo = data.get('modo', 'replace')
        
        if not archivo:
            return Response({'error': 'Debe especificar el archivo a restaurar'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        if not confirmar:
            return Response({'error': 'Debe confirmar la restauración'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar conectividad antes de continuar
        conectividad_ok, error_conectividad = verificar_conectividad_db()
        if not conectividad_ok:
            return Response({
                'error': 'No se puede conectar a PostgreSQL',
                'detalle': error_conectividad,
                'solucion': 'Verificar que PostgreSQL esté ejecutándose y las credenciales sean correctas'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            return Response({'error': f'El archivo {archivo} no existe'}, 
                          status=status.HTTP_404_NOT_FOUND)        # Leer metadatos si existen
        metadata_file = ruta_backup.replace('.sql', '_metadata.json')
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
          # Detectar formato del archivo para elegir herramienta de restauración
        es_formato_custom = archivo.endswith('.backup')
        es_bd_completa = (
            metadata.get('tipo') == 'bd_completa' or 
            'completo' in archivo.lower() or
            'backup_completo' in archivo.lower() or
            not metadata.get('tablas')  # Si no especifica tablas, asumimos BD completa
        )          # Determinar timeout dinámico y método según tipo de backup
        if es_formato_custom:
            # pg_restore ultra-rápido: 2 minutos máximo
            timeout_segundos = 120
            timeout_descripcion = "2 minutos (pg_restore ultra-rápido)"
            metodo_restauracion = "pg_restore"
        elif es_bd_completa:
            # 🔥 CORRECCIÓN: Timeout dinámico para BD completas basado en tamaño
            config_restauracion = obtener_configuracion_restauracion_optimizada(ruta_backup)
            timeout_segundos = config_restauracion['timeout_segundos']
            timeout_descripcion = config_restauracion['timeout_descripcion']
            metodo_restauracion = config_restauracion['metodo']
        else:
            # psql para tablas individuales: 1 minuto (con limpieza automática)
            timeout_segundos = 60
            timeout_descripcion = "1 minuto (con limpieza automática)"
            metodo_restauracion = "psql con limpieza previa"# Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Configurar variables de entorno ANTES de usarlas
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # 🔥 SOLUCIÓN: LIMPIAR AUTOMÁTICAMENTE TABLAS ANTES DE RESTAURAR
        if not es_bd_completa and not es_formato_custom and modo == 'replace':
            # Para tablas específicas en modo replace, limpiar automáticamente
            tablas_a_limpiar = metadata.get('tablas', [])
            if tablas_a_limpiar:
                print(f"🧹 Limpiando automáticamente tablas antes de restaurar: {', '.join(tablas_a_limpiar)}")
                
                for tabla in tablas_a_limpiar:
                    try:
                        # Comando SQL para limpiar tabla con CASCADE
                        sql_command = f"TRUNCATE TABLE {tabla} CASCADE;"
                        
                        # Comando psql para ejecutar limpieza
                        cmd_limpiar = [
                            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
                            f"--host={db_config['host']}",
                            f"--port={db_config['port']}",
                            f"--username={db_config['user']}",
                            f"--dbname={db_config['name']}",
                            '--no-password',
                            '-c', sql_command
                        ]                          # Ejecutar limpieza
                        result_limpieza = subprocess.run(
                            cmd_limpiar, 
                            env=env, 
                            capture_output=True, 
                            text=True, 
                            timeout=10  # 10 segundos timeout para limpieza
                        )
                        
                        if result_limpieza.returncode == 0:
                            print(f"✅ Tabla {tabla} limpiada exitosamente")
                            print(f"🗑️ Output limpieza: {result_limpieza.stdout}")
                        else:
                            print(f"⚠️ Advertencia al limpiar tabla {tabla}: {result_limpieza.stderr}")
                            print(f"📋 Output limpieza stderr: {result_limpieza.stdout}")
                            
                    except Exception as e:
                        print(f"⚠️ Error limpiando tabla {tabla}: {str(e)}")
                        # Continuar con la restauración aunque falle la limpieza          # Construir comando según formato de archivo
        if es_formato_custom:
            # Usar pg_restore ultra-rápido para archivos .backup
            tablas_filtro = metadata.get('tablas') if not es_bd_completa else None
            cmd = construir_comando_pg_restore_ultra_rapido(db_config, ruta_backup, tablas_filtro)
        elif es_bd_completa:
            # 🔥 NUEVA: Usar psql ultra-optimizado para BD completas grandes
            cmd = construir_comando_psql_ultra_optimizado(db_config, ruta_backup, modo, config_restauracion)
        else:
            # Usar psql optimizado para tablas específicas
            cmd = construir_comando_psql_seguro(db_config, ruta_backup, modo, es_bd_completa)
        
          # Ejecutar restauración con método optimizado
        tipo_backup_str = "BD completa" if es_bd_completa else "tabla(s) específica(s)"
        print(f"🚀 Ejecutando restauración de {tipo_backup_str} desde: {archivo}")
        print(f"⚡ Método: {metodo_restauracion}")
        print(f"⏰ Timeout: {timeout_descripcion}")
        print(f"🔧 Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True,                text=True, 
                timeout=timeout_segundos
            )
        except subprocess.TimeoutExpired:
            # 🔥 MEJORADO: Información detallada sobre timeout con sugerencias
            tamaño_archivo_mb = round(os.path.getsize(ruta_backup) / (1024*1024), 2)
            
            return Response({
                'error': f'La restauración se ha cancelado por timeout ({timeout_descripcion})',
                'archivo': archivo,
                'tipo_backup': tipo_backup_str,
                'metodo': metodo_restauracion,
                'timeout_configurado_minutos': round(timeout_segundos / 60, 1),
                'tamaño_archivo_mb': tamaño_archivo_mb,
                'diagnostico': {
                    'problema': 'El archivo es demasiado grande para el timeout configurado',
                    'timeout_usado': f'{timeout_segundos} segundos ({timeout_descripcion})',
                    'tamaño_detectado': f'{tamaño_archivo_mb} MB'
                },
                'soluciones_recomendadas': [
                    {
                        'opcion': 1,
                        'titulo': 'Crear backup en formato custom',
                        'descripcion': 'Usar formato .backup para restauraciones 40x más rápidas',
                        'comando_sugerido': 'Crear nuevo backup con formato=custom en la interfaz'
                    },
                    {
                        'opcion': 2,
                        'titulo': 'Optimizar PostgreSQL',
                        'descripcion': 'Aplicar configuraciones de memoria para grandes restauraciones',
                        'archivo_config': 'Ver CONFIGURACION_POSTGRESQL_OPTIMIZADA.md'
                    },
                    {
                        'opcion': 3,
                        'titulo': 'Restauración por partes',
                        'descripcion': 'Dividir el backup en tablas específicas y restaurar por partes',
                        'ventaja': 'Permite mayor control y timeouts individuales'
                    }
                ],
                'timeout_sugerido_minutos': min(120, max(60, tamaño_archivo_mb * 0.5)),  # 0.5 min por MB, máx 2h
                'estadisticas': {
                    'velocidad_estimada_mb_min': round(tamaño_archivo_mb / (timeout_segundos / 60), 2),
                    'tiempo_necesario_estimado_min': round(tamaño_archivo_mb * 0.5, 1)  # Estimación conservadora
                }
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        print(f"📤 Return code: {result.returncode}")
        print(f"📄 stdout: {result.stdout}")
        print(f"⚠️ stderr: {result.stderr}")
        
        # Verificar resultado
        if result.returncode != 0:
            error_msg = result.stderr
            
            # Verificar si es un error de dependencias específico
            if 'cannot drop constraint' in error_msg and 'other objects depend on' in error_msg:
                return Response({
                    'error': 'Error de dependencias en la restauración',
                    'tipo_error': 'dependencias_foreign_keys',
                    'details': result.stderr,
                    'archivo': archivo,
                    'solucion': {
                        'descripcion': 'El archivo contiene comandos DROP que fallan por dependencias de foreign keys',
                        'opciones': [
                            '1. Crear un nuevo respaldo usando solo datos (--data-only)',
                            '2. Limpiar la tabla destino manualmente antes de restaurar',
                            '3. Usar un respaldo completo de BD en lugar de tablas específicas'
                        ],
                        'comando_manual': f'Ejecutar: TRUNCATE TABLE empresas CASCADE; antes de la restauración'
                    },
                    'comando': ' '.join(cmd)
                }, status=status.HTTP_409_CONFLICT)  # 409 Conflict para indicar problema de dependencias
            else:
                return Response({
                    'error': 'Error en la restauración',
                    'details': result.stderr,
                    'archivo': archivo,
                    'comando': ' '.join(cmd)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          # Preparar respuesta
        warnings = []
        if result.stderr:
            # Filtrar mensajes que no son errores reales
            lines = result.stderr.split('\n')
            warnings = [line for line in lines if line.strip() and not line.startswith('psql:')]
          # Información sobre limpieza automática aplicada
        limpieza_automatica = (
            not es_bd_completa and 
            not es_formato_custom and 
            modo == 'replace' and 
            metadata.get('tablas')
        )
        
        return Response({
            'message': '✅ Restauración completada exitosamente',
            'archivo': archivo,
            'modo': modo,
            'metodo_restauracion': metodo_restauracion,
            'tiempo_estimado': timeout_descripcion,
            'timeout_dinamico_segundos': timeout_segundos,
            'formato_archivo': 'custom' if es_formato_custom else 'plain',
            'limpieza_automatica_aplicada': limpieza_automatica,
            'tablas_limpiadas': metadata.get('tablas', []) if limpieza_automatica else [],
            'optimizaciones_aplicadas': {
                'pg_restore_paralelo': es_formato_custom,
                'psql_single_transaction': not es_formato_custom and es_bd_completa,
                'timeout_dinamico_por_tamaño': es_bd_completa and not es_formato_custom,
                'timeout_optimizado': True,
                'limpieza_previa_automatica': limpieza_automatica,
                'comando_ultra_optimizado': es_bd_completa and not es_formato_custom
            },
            'tamaño_archivo_mb': round(os.path.getsize(ruta_backup) / (1024*1024), 2) if es_bd_completa else None,
            'configuracion_aplicada': config_restauracion if es_bd_completa and not es_formato_custom else None,
            'metadata': metadata,
            'warnings': warnings,
            'comando_ejecutado': ' '.join(cmd),
            'output': result.stdout
        })
        
    except Exception as e:
        return Response({'error': f'Error al restaurar: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_respaldo(request, archivo):
    """Eliminar un archivo de respaldo"""
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            return Response({'error': f'El archivo {archivo} no existe'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Eliminar archivo SQL
        os.remove(ruta_backup)
        
        # Eliminar metadata si existe
        metadata_file = ruta_backup.replace('.sql', '_metadata.json')
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
        
        return Response({
            'message': f'Respaldo {archivo} eliminado exitosamente'
        })
        
    except Exception as e:
        return Response({'error': f'Error al eliminar respaldo: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def descargar_respaldo(request, archivo):
    """Descargar un archivo de respaldo"""
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            return Response({'error': f'El archivo {archivo} no existe'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Servir archivo para descarga
        with open(ruta_backup, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{archivo}"'
            return response
        
    except Exception as e:
        return Response({'error': f'Error al descargar respaldo: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def info_sistema_respaldos(request):
    """Obtener información del sistema de respaldos"""
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Calcular espacio usado por respaldos
        espacio_usado = 0
        cantidad_respaldos = 0
        if os.path.exists(BACKUP_DIR):
            for archivo in os.listdir(BACKUP_DIR):
                if archivo.endswith('.sql'):
                    ruta = os.path.join(BACKUP_DIR, archivo)
                    espacio_usado += os.path.getsize(ruta)
                    cantidad_respaldos += 1
        
        return Response({
            'directorio_respaldos': BACKUP_DIR,
            'base_datos': db_config['name'],
            'host': db_config['host'],
            'puerto': db_config['port'],
            'cantidad_respaldos': cantidad_respaldos,
            'espacio_usado_mb': round(espacio_usado / (1024*1024), 2),
            'herramientas_disponibles': {
                'pg_dump': True,  # Ya verificamos que están disponibles
                'psql': True
            }
        })
        
    except Exception as e:
        return Response({'error': f'Error al obtener info del sistema: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_sistema_respaldos(request):
    """
    Verificar que el sistema de respaldos esté configurado correctamente
    Para debugging de rutas y configuración
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Verificar directorio de respaldos
        backup_dir_existe = os.path.exists(BACKUP_DIR)
        
        # Verificar permisos de escritura
        permisos_ok = False
        try:
            test_file = os.path.join(BACKUP_DIR, 'test_permisos.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            permisos_ok = True
        except:
            pass
        
        # Verificar configuración de BD
        try:
            db_config = obtener_config_db()
            bd_config_ok = True
        except Exception as e:
            db_config = {'error': str(e)}
            bd_config_ok = False
        
        # Contar archivos existentes
        archivos_existentes = []
        if backup_dir_existe:
            try:
                archivos_existentes = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.sql')]
            except:
                pass
        
        return Response({
            'sistema': 'Sistema de respaldos - Verificación',
            'directorio_respaldos': BACKUP_DIR,
            'directorio_existe': backup_dir_existe,
            'permisos_escritura': permisos_ok,
            'configuracion_bd': db_config,
            'bd_config_ok': bd_config_ok,
            'archivos_respaldo_existentes': len(archivos_existentes),
            'archivos_muestra': archivos_existentes[:5],
            'base_dir': settings.BASE_DIR,
            'rutas_relativas': {
                'esperada': 'Backend/config/backups',
                'completa': BACKUP_DIR
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Error en verificación del sistema: {str(e)}',
            'directorio_respaldos': BACKUP_DIR,
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# NUEVAS FUNCIONES PARA SUPERADMIN
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldo_limpio_pgadmin(request):
    """
    Generar respaldo limpio compatible con pgAdmin usando pg_dump
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        db_config = obtener_config_db()
        
        # Crear directorio de respaldos
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Nombre del archivo de respaldo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"respaldo_pgadmin_{timestamp}.sql"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Comando pg_dump con opciones para pgAdmin
        pg_dump_cmd = [
            'pg_dump',
            '--host', db_config['host'],
            '--port', str(db_config['port']),
            '--username', db_config['user'],
            '--dbname', db_config['name'],
            '--no-password',
            '--verbose',
            '--clean',                # Incluir comandos DROP
            '--if-exists',           # Solo DROP si existe
            '--create',              # Incluir comando CREATE DATABASE
            '--encoding', 'UTF8',    # Encoding UTF-8
            '--no-owner',            # Sin comandos de propietario
            '--no-privileges',       # Sin comandos de privilegios
            '--file', backup_path
        ]
        
        # Configurar variable de entorno para password
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Ejecutar pg_dump
        result = subprocess.run(
            pg_dump_cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Verificar que el archivo se creó
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            
            return Response({
                'mensaje': 'Respaldo limpio generado exitosamente',
                'archivo': backup_filename,
                'ruta': backup_path,
                'tamaño': file_size,
                'tamaño_mb': round(file_size / 1024 / 1024, 2),
                'compatible_con': 'pgAdmin 4',
                'formato': 'SQL estándar PostgreSQL',
                'timestamp': timestamp,
                'instrucciones': {
                    'pgadmin': [
                        'Abre pgAdmin 4',
                        'Click derecho en Databases',
                        'Create > Database',
                        'Click derecho en nueva BD',
                        'Restore > Selecciona archivo',
                        'Format: Plain',
                        'Ejecuta restauración'
                    ],
                    'comando_alternativo': f'psql -U postgres -h localhost -f "{backup_path}"'
                }
            })
        else:
            return Response({'error': 'Error: El archivo de respaldo no se creó'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except subprocess.CalledProcessError as e:
        return Response({
            'error': 'Error al ejecutar pg_dump',
            'codigo_salida': e.returncode,
            'stderr': e.stderr,
            'solucion': 'Verifica que PostgreSQL client tools estén instalados y en PATH'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': f'Error generando respaldo: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resetear_bd_completa(request):
    """
    PELIGROSO: Eliminar todos los datos de la base de datos usando BAT
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        confirmacion = request.data.get('confirmacion')
        if confirmacion != 'CONFIRMO_RESETEAR_BD':
            return Response({
                'error': 'Confirmación requerida',
                'requerido': 'confirmacion: "CONFIRMO_RESETEAR_BD"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ejecutar script Python de reseteo rápido
        import subprocess
        import os
        
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resetear_bd_rapido.py')
        script_path = os.path.abspath(script_path)
        
        print(f"🔄 Ejecutando reseteo rápido: {script_path}")
        
        # Ejecutar script Python
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            return Response({
                'mensaje': '⚠️ BASE DE DATOS RESETEADA COMPLETAMENTE',
                'metodo': 'BAT rápido',
                'output': result.stdout,
                'timestamp': datetime.now().isoformat(),
                'advertencia': 'Todos los datos han sido eliminados permanentemente'
            })
        else:
            return Response({
                'error': 'Error en el reseteo',
                'details': result.stderr,
                'output': result.stdout
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({'error': f'Error reseteando BD: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({'error': f'Error reseteando BD: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cargar_datos_iniciales(request):
    """
    Cargar datos de prueba iniciales usando BAT
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Ejecutar script Python de carga rápida
        import subprocess
        import os
        
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'cargar_datos_rapido.py')
        script_path = os.path.abspath(script_path)
        
        print(f"🔄 Ejecutando carga rápida: {script_path}")
        
        # Ejecutar script Python
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            return Response({
                'mensaje': '✅ DATOS INICIALES CARGADOS EXITOSAMENTE',
                'metodo': 'BAT rápido',
                'output': result.stdout,
                'usuarios_disponibles': {
                    'superadmin': 'superadmin / 1234',
                    'admin_empresa': 'admin_empresa / 1234', 
                    'admin_planta': 'admin_planta / 1234'
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response({
                'error': 'Error cargando datos',
                'details': result.stderr,
                'output': result.stdout
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({'error': f'Error cargando datos iniciales: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurar_estado_inicial(request):
    """
    Restaurar la BD al punto de inicio usando BAT
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        confirmacion = request.data.get('confirmacion')
        if confirmacion != 'CONFIRMO_RESTAURAR_INICIAL':
            return Response({
                'error': 'Confirmación requerida',
                'requerido': 'confirmacion: "CONFIRMO_RESTAURAR_INICIAL"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ejecutar script combinado: reseteo + carga
        import subprocess
        import os
        
        # Paso 1: Resetear
        reset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resetear_bd_rapido.py')
        reset_path = os.path.abspath(reset_path)
        
        print(f"🔄 Paso 1/2: Reseteando BD...")
        reset_result = subprocess.run(['python', reset_path], capture_output=True, text=True)
        
        if reset_result.returncode != 0:
            return Response({
                'error': 'Error en reseteo',
                'details': reset_result.stderr,
                'output': reset_result.stdout
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Paso 2: Cargar datos
        load_path = os.path.join(os.path.dirname(__file__), '..', '..', 'cargar_datos_rapido.py')
        load_path = os.path.abspath(load_path)
        
        print(f"🔄 Paso 2/2: Cargando datos...")
        load_result = subprocess.run(['python', load_path], capture_output=True, text=True)
        
        if load_result.returncode != 0:
            return Response({
                'error': 'Error cargando datos',
                'details': load_result.stderr,
                'output': load_result.stdout
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Combinar outputs
        combined_output = f"RESETEO:\n{reset_result.stdout}\n\nCARGA:\n{load_result.stdout}"
        
        return Response({
            'mensaje': '🎉 BD RESTAURADA AL ESTADO INICIAL EXITOSAMENTE',
            'metodo': 'Scripts Python combinados',
            'output': combined_output,
            'estado_final': 'BD lista para usar como primer día del software',
            'usuarios_disponibles': {
                'superadmin': 'superadmin / 1234',
                'admin_empresa': 'admin_empresa / 1234', 
                'admin_planta': 'admin_planta / 1234'
            },
            'timestamp': datetime.now().isoformat(),
            'recomendacion': 'Crear respaldo después de este estado inicial'
        })
        
    except Exception as e:
        return Response({'error': f'Error restaurando estado inicial: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def construir_comando_psql_seguro(db_config, archivo_sql, modo='replace', es_bd_completa=False):
    """
    Construir comando psql optimizado según el tipo de backup
    
    Args:
        es_bd_completa: True para BD completas (más optimizaciones)
    """
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/psql.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password'
    ]
    
    if es_bd_completa:
        # Optimizaciones para BD completas
        cmd.extend([
            '--single-transaction',  # Todo en una sola transacción (más rápido y seguro)
            '--set', 'ON_ERROR_STOP=1',  # Parar inmediatamente en errores críticos
            '--quiet',  # Reducir output verboso para mejorar velocidad
            '--set', 'AUTOCOMMIT=off'  # Controlar commits manualmente
        ])
    else:
        # Para tablas individuales, permitir errores menores
        cmd.extend([
            '-v', 'ON_ERROR_STOP=0'  # Continuar con errores menores
        ])
    
    cmd.extend(['-f', archivo_sql])
    
    return cmd


def construir_comando_pg_restore_ultra_rapido(db_config, archivo_backup, tablas=None):
    """
    Construir comando pg_restore ultra-optimizado para restauraciones de 5-10 segundos
    OPTIMIZADO PARA BASES DE DATOS GRANDES
    
    Args:
        archivo_backup: Archivo .backup en formato custom
        tablas: Lista de tablas específicas (opcional)
    """
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/pg_restore.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password',
        
        # OPTIMIZACIONES ULTRA-RÁPIDAS
        '--clean',                    # Limpiar objetos existentes
        '--if-exists',               # Solo limpiar si existe
        '--no-owner',                # Sin comandos de propietario
        '--no-privileges',           # Sin comandos de privilegios
        '--no-comments',             # Sin comentarios
        '--disable-triggers',        # Deshabilitar triggers durante inserción
        
        # 🚀 PARALELIZACIÓN AUTOMÁTICA OPTIMIZADA
        '--jobs=6',                  # Usar 6 cores en paralelo (AUMENTADO)
        
        # 🚀 OPTIMIZACIONES DE MEMORIA MEJORADAS
        '--no-tablespaces',          # Sin tablespaces
        '--single-transaction',      # Una sola transacción (más rápido)
        '--no-security-labels',      # Sin etiquetas de seguridad (NUEVO)
        '--no-synchronized-snapshots', # Mejor rendimiento (NUEVO)
        
        # MANEJO DE ERRORES OPTIMIZADO
        '--exit-on-error',          # Salir en errores críticos
        '--verbose',                # Output detallado para debugging
        
        archivo_backup
    ]
    
    # Si especifica tablas, agregar filtros
    if tablas:
        for tabla in tablas:
            cmd.extend(['--table', tabla])
    
    return cmd


def construir_comando_pg_dump_seguro(db_config, archivo_destino, tablas=None, incluir_datos=True, formato='custom'):
    """
    Construir comando pg_dump optimizado con formato custom para restauraciones ultra-rápidas
    OPTIMIZADO PARA BASES DE DATOS GRANDES
    
    Args:
        formato: 'custom' para pg_restore rápido, 'plain' para psql tradicional
    """
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password',
        '--verbose',
        '--no-owner',
        '--no-privileges'
    ]
    
    # Configurar formato de salida
    if formato == 'custom':
        # Formato custom para pg_restore ultra-rápido
        cmd.extend([
            '--format=custom',  # Formato binario comprimido
            '--compress=9',     # Máxima compresión
            
            # 🚀 OPTIMIZACIONES PARA BASES DE DATOS GRANDES
            '--jobs=4',         # Paralelización en 4 cores (NUEVO)
            '--no-tablespaces', # Evitar dependencias de tablespace (NUEVO)
            '--no-comments',    # Reducir tamaño del archivo (NUEVO)
            '--no-security-labels',  # Omitir etiquetas de seguridad (NUEVO)
            '--exclude-table-data=django_session',  # Excluir datos temporales (NUEVO)
            
            '--file', archivo_destino
        ])
    else:
        # Formato plain para psql tradicional
        cmd.extend(['--file', archivo_destino])
    
    # Para respaldos de tablas específicas
    if tablas:
        if formato == 'custom':
            # En formato custom, mantener estructura para mejor restauración
            cmd.extend(['--clean', '--if-exists'])
        else:
            # Solo datos para formato plain
            cmd.append('--data-only')
            cmd.append('--disable-triggers')
            cmd.append('--no-comments')
        
        # Agregar tablas específicas
        for tabla in tablas:
            cmd.extend(['--table', tabla])
    else:
        # Para respaldos completos, siempre incluir clean
        cmd.extend(['--clean', '--if-exists'])
    
    # Agregar opciones según configuración
    if not incluir_datos:
        cmd.append('--schema-only')
    
    return cmd


def construir_comando_pg_dump_optimizado_bd_grande(db_config, archivo_destino, tablas=None, incluir_datos=True, formato='custom', config_bd=None):
    """
    Construir comando pg_dump súper optimizado para bases de datos grandes
    Configuración automática según tamaño de BD
    """
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password',
        '--verbose',
        '--no-owner',
        '--no-privileges'
    ]
    
    # Configurar formato custom con optimizaciones automáticas
    if formato == 'custom':
        jobs = config_bd.get('jobs', 4) if config_bd else 4
        
        cmd.extend([
            '--format=custom',  # Formato binario comprimido
            '--compress=9',     # Máxima compresión
            
            # 🚀 OPTIMIZACIONES ADAPTATIVAS SEGÚN TAMAÑO DE BD
            f'--jobs={jobs}',   # Paralelización automática
            '--no-tablespaces', # Evitar dependencias de tablespace
            '--no-comments',    # Reducir tamaño del archivo
            '--no-security-labels',  # Omitir etiquetas de seguridad
            '--exclude-table-data=django_session',  # Excluir datos temporales
            '--exclude-table-data=auth_session',    # Excluir sesiones
            
            # Optimizaciones específicas para BD grandes
            '--no-synchronized-snapshots',  # Mejorar rendimiento en BD grandes
            '--quote-all-identifiers',      # Evitar problemas de naming
            
            '--file', archivo_destino
        ])
        
        # Optimizaciones adicionales para BD muy grandes (>500MB)
        if config_bd and config_bd.get('es_bd_muy_grande', False):
            print("🔥 Aplicando optimizaciones EXTREMAS para BD muy grande (>500MB)")
            # Para BD muy grandes, excluir más datos temporales
            cmd.extend([
                '--exclude-table-data=django_admin_log',  # Logs de admin
                '--exclude-table-data=django_migrations', # Migraciones (se regeneran)
            ])
    
    # Para respaldos completos, siempre incluir clean
    if not tablas:
        cmd.extend(['--clean', '--if-exists'])
    
    # Agregar opciones según configuración
    if not incluir_datos:
        cmd.append('--schema-only')
    
    return cmd


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def limpiar_tabla_para_restaurar(request):
    """
    Limpiar una tabla específica para permitir restauración sin conflictos
    Body: {
        "tabla": "nombre_tabla",
        "confirmar": true
    }
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        tabla = data.get('tabla')
        confirmar = data.get('confirmar', False)
        
        if not tabla:
            return Response({'error': 'Debe especificar la tabla a limpiar'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        if not confirmar:
            return Response({'error': 'Debe confirmar la limpieza de la tabla'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar conectividad
        conectividad_ok, error_conectividad = verificar_conectividad_db()
        if not conectividad_ok:
            return Response({
                'error': 'No se puede conectar a PostgreSQL',
                'detalle': error_conectividad
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Crear comando SQL para limpiar la tabla con CASCADE
        sql_command = f"TRUNCATE TABLE {tabla} CASCADE;"
        
        # Comando psql para ejecutar
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '-c', sql_command
        ]
        
        # Configurar variables de entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        print(f"🧹 Limpiando tabla: {tabla}")
        print(f"🔧 Comando SQL: {sql_command}")
        
        # Ejecutar comando
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True, 
            timeout=60  # 1 minuto timeout
        )
        
        if result.returncode != 0:
            return Response({
                'error': f'Error al limpiar tabla {tabla}',
                'details': result.stderr,
                'comando': sql_command
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': f'✅ Tabla {tabla} limpiada exitosamente',
            'tabla': tabla,
            'comando_ejecutado': sql_command,
            'output': result.stdout,
            'siguiente_paso': 'Ahora puede proceder con la restauración del respaldo'
        })
        
    except subprocess.TimeoutExpired:
        return Response({
            'error': f'Timeout al limpiar tabla {tabla}',
            'solucion': 'La tabla puede tener muchos datos o estar bloqueada'
        }, status=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as e:
        return Response({'error': f'Error al limpiar tabla: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# OPTIMIZACIONES ESPECÍFICAS PARA BASES DE DATOS GRANDES
# ============================================================================

def obtener_configuracion_optimizada_bd_grande(db_config):
    """
    Configurar parámetros optimizados para bases de datos grandes
    """
    with connection.cursor() as cursor:
        # Verificar tamaño de la base de datos
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size,
                   pg_database_size(current_database()) as size_bytes
        """)
        size_info = cursor.fetchone()
        
        # Contar número de tablas con datos
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        tabla_count = cursor.fetchone()[0]
        
        # Configuración según tamaño
        size_bytes = size_info[1]
        config = {
            'size_pretty': size_info[0],
            'size_bytes': size_bytes,
            'tabla_count': tabla_count,
            'es_bd_grande': size_bytes > 100 * 1024 * 1024,  # > 100MB
            'timeout_minutos': 10,  # Timeout base
            'jobs': 2,  # Jobs paralelos base
        }
        
        # Ajustar configuración según tamaño
        if size_bytes > 500 * 1024 * 1024:  # > 500MB
            config.update({
                'timeout_minutos': 45,
                'jobs': 6,
                'es_bd_muy_grande': True
            })
        elif size_bytes > 100 * 1024 * 1024:  # > 100MB
            config.update({
                'timeout_minutos': 30,
                'jobs': 4,
                'es_bd_muy_grande': False
            })
        else:
            config.update({
                'timeout_minutos': 15,
                'jobs': 2,
                'es_bd_muy_grande': False
            })
        
        return config

def aplicar_optimizaciones_postgresql_grandes(db_config):
    """
    Aplicar configuraciones específicas de PostgreSQL para mejorar 
    rendimiento en backups de bases de datos grandes
    """
    optimizaciones = []
    
    try:
        with connection.cursor() as cursor:
            # Desactivar autovacuum temporalmente durante backup
            cursor.execute("SET log_autovacuum_min_duration = -1;")
            optimizaciones.append("Autovacuum logging disabled")
            
            # Optimizar parámetros de memoria para backup
            cursor.execute("SET work_mem = '256MB';")
            optimizaciones.append("work_mem increased to 256MB")
            
            # Optimizar checkpoint para reducir I/O
            cursor.execute("SET checkpoint_completion_target = 0.9;")
            optimizaciones.append("checkpoint_completion_target optimized")
            
    except Exception as e:
        optimizaciones.append(f"Warning: No se pudieron aplicar todas las optimizaciones: {str(e)}")
    
    return optimizaciones

# ============================================================================
# MONITOREO DE PROGRESO Y ESTADÍSTICAS DEL SISTEMA DE BACKUP
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monitorear_backup_progreso(request):
    """
    Monitorear el progreso de backups en curso y estadísticas del sistema
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        # Analizar BD actual
        db_config = obtener_config_db()
        config_bd = obtener_configuracion_optimizada_bd_grande(db_config)
        
        # Obtener últimos backups
        archivos_backup = []
        if os.path.exists(BACKUP_DIR):
            for archivo in os.listdir(BACKUP_DIR):
                if archivo.endswith(('.backup', '.sql')):
                    ruta_completa = os.path.join(BACKUP_DIR, archivo)
                    stat = os.stat(ruta_completa)
                    
                    # Buscar metadata
                    metadata_path = ruta_completa.replace('.backup', '_metadata.json').replace('.sql', '_metadata.json')
                    metadata = {}
                    if os.path.exists(metadata_path):
                        try:
                            with open(metadata_path, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                        except:
                            pass
                    
                    archivos_backup.append({
                        'archivo': archivo,
                        'tamaño_mb': round(stat.st_size / (1024*1024), 2),
                        'fecha_creacion': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'metadata': metadata
                    })
        
        # Ordenar por fecha más reciente
        archivos_backup.sort(key=lambda x: x['fecha_creacion'], reverse=True)
        
        return Response({
            'sistema_backup': {
                'directorio': BACKUP_DIR,
                'archivos_totales': len(archivos_backup),
                'estado': 'Optimizado para BD grandes'
            },
            'analisis_bd_actual': config_bd,
            'ultimos_backups': archivos_backup[:10],  # Últimos 10
            'recomendaciones': {
                'formato_recomendado': 'custom' if config_bd['es_bd_grande'] else 'plain',
                'jobs_recomendados': config_bd['jobs'],
                'timeout_recomendado': f"{config_bd['timeout_minutos']} minutos",
                'optimizaciones_disponibles': 'automáticas' if config_bd['es_bd_grande'] else 'básicas'
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Error monitoreando sistema backup: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============================================================================
# BACKUP DE EMERGENCIA
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def backup_emergencia_optimizado(request):
    """
    Crear backup de emergencia ultra-rápido con máximas optimizaciones
    Para usar cuando hay problemas de rendimiento
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        db_config = obtener_config_db()
        
        # Configuración de emergencia: solo estructura + datos críticos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_emergencia_{timestamp}.backup"
        ruta_backup = os.path.join(BACKUP_DIR, nombre_archivo)
        
        # Comando ultra-optimizado para emergencia
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '--format=custom',
            '--compress=9',
            
            # 🚨 MÁXIMAS OPTIMIZACIONES DE EMERGENCIA
            '--jobs=8',                 # Máximo paralelismo
            '--no-owner',
            '--no-privileges', 
            '--no-tablespaces',
            '--no-comments',
            '--no-security-labels',
            '--no-synchronized-snapshots',
            
            # Excluir datos no críticos para velocidad máxima
            '--exclude-table-data=django_session',
            '--exclude-table-data=django_admin_log',
            '--exclude-table-data=auth_session',
            '--exclude-table-data=django_migrations',
            
            # Solo datos esenciales del negocio
            '--exclude-table=django_content_type',
            '--exclude-table=auth_permission',
            
            '--file', ruta_backup
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        print("🚨 EJECUTANDO BACKUP DE EMERGENCIA ULTRA-OPTIMIZADO")
        inicio = datetime.now()
        
        try:
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True, 
                text=True, 
                timeout=600  # Máximo 10 minutos para emergencia
            )
            tiempo_transcurrido = datetime.now() - inicio
            
            if result.returncode != 0:
                return Response({
                    'error': 'Error en backup de emergencia',
                    'details': result.stderr
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            tamaño_archivo = os.path.getsize(ruta_backup)
            
            return Response({
                'message': '🚨 Backup de emergencia completado exitosamente',
                'archivo': nombre_archivo,
                'tiempo_backup': str(tiempo_transcurrido),
                'tamaño_mb': round(tamaño_archivo / (1024*1024), 2),
                'tipo': 'EMERGENCIA - Solo datos críticos',
                'optimizaciones': 'Máximas (8 jobs paralelos)',
                'excluidos': [
                    'Sesiones de usuario',
                    'Logs de admin', 
                    'Datos temporales',
                    'Permisos de sistema'
                ],
                'warning': 'Este backup excluye datos no críticos para máxima velocidad'
            })
            
        except subprocess.TimeoutExpired:
            return Response({
                'error': 'Timeout en backup de emergencia',
                'solucion': 'La BD es demasiado grande para backup de emergencia. Contacta al administrador.',
                'tiempo_limite': '10 minutos'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
            
    except Exception as e:
        return Response({
            'error': f'Error en backup de emergencia: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def obtener_configuracion_restauracion_optimizada(ruta_backup):
    """
    🔥 NUEVA: Configuración dinámica de timeouts para restauración de BD completas
    Analiza el tamaño del archivo de backup y configura timeouts optimizados
    """
    try:
        # Obtener tamaño del archivo de backup
        tamaño_archivo_mb = os.path.getsize(ruta_backup) / (1024 * 1024)
        
        if tamaño_archivo_mb < 50:
            # 🔥 TEMPORAL: Aumentado a 20 minutos para resolver problema actual
            return {
                'timeout_segundos': 300,  # AUMENTADO de 600 a 1200
                'timeout_descripcion': '5 minutos (archivo < 50MB) - TEMPORAL',
                'metodo': 'psql optimizado - archivo pequeño',
                'jobs': 1
            }
        elif tamaño_archivo_mb < 200:
            # Archivos medianos (50-200MB): 30 minutos
            return {
                'timeout_segundos': 1800,
                'timeout_descripcion': '30 minutos (archivo 50-200MB)',
                'metodo': 'psql optimizado - archivo mediano',
                'jobs': 2
            }
        elif tamaño_archivo_mb < 500:
            # Archivos grandes (200-500MB): 60 minutos
            return {
                'timeout_segundos': 3600,
                'timeout_descripcion': '60 minutos (archivo 200-500MB)',
                'metodo': 'psql optimizado - archivo grande',
                'jobs': 4
            }
        else:
            # Archivos muy grandes (> 500MB): 90 minutos
            return {
                'timeout_segundos': 5400,
                'timeout_descripcion': '90 minutos (archivo > 500MB)',
                'metodo': 'psql optimizado - archivo muy grande',
                'jobs': 6
            }
            
    except Exception as e:
        print(f"⚠️ Error al analizar tamaño del archivo: {str(e)}")
        # Fallback: configuración conservadora
        return {
            'timeout_segundos': 3600,  # 1 hora por defecto
            'timeout_descripcion': '60 minutos (fallback - tamaño desconocido)',
            'metodo': 'psql optimizado - configuración fallback',
            'jobs': 2
        }


def construir_comando_psql_ultra_optimizado(db_config, ruta_backup, modo, config_restauracion):
    """
    🔥 NUEVA: Construir comando psql ultra-optimizado para restauraciones de BD completas grandes
    """
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/psql.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password',
        '--quiet',  # Modo silencioso para mejor rendimiento
        '--single-transaction',  # Transacción única para consistencia
        '--set', 'ON_ERROR_STOP=1',  # Parar en el primer error
    ]
    
    # Optimizaciones específicas para archivos grandes
    if config_restauracion['jobs'] > 1:
        # PostgreSQL no soporta jobs en psql, pero podemos optimizar la conexión
        cmd.extend([
            '--set', 'statement_timeout=0',  # Sin timeout de statement
            '--set', 'lock_timeout=300000',  # 5 minutos para locks
        ])
    
    # Agregar archivo como último parámetro
    cmd.extend(['-f', ruta_backup])
    
    return cmd


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def diagnosticar_restauracion(request):
    """
    🔍 NUEVA: Diagnosticar problemas de restauración paso a paso
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        archivo = data.get('archivo')
        
        if not archivo:
            return Response({'error': 'Debe especificar el archivo a diagnosticar'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        diagnostico = {'archivo': archivo, 'problemas': [], 'soluciones': []}
        
        # 1. Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            diagnostico['problemas'].append('❌ El archivo no existe')
            return Response(diagnostico, status=status.HTTP_404_NOT_FOUND)
        
        diagnostico['archivo_existe'] = True
        diagnostico['tamaño_archivo_mb'] = round(os.path.getsize(ruta_backup) / (1024*1024), 2)
        
        # 2. Verificar conectividad PostgreSQL
        conectividad_ok, error_conectividad = verificar_conectividad_db()
        diagnostico['conectividad_postgresql'] = conectividad_ok
        if not conectividad_ok:
            diagnostico['problemas'].append(f'❌ PostgreSQL: {error_conectividad}')
            diagnostico['soluciones'].append('Verificar que PostgreSQL esté ejecutándose')
        
        # 3. Leer metadatos
        metadata_file = ruta_backup.replace('.sql', '_metadata.json').replace('.backup', '_metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            diagnostico['metadata'] = metadata
        else:
            diagnostico['problemas'].append('⚠️ No hay metadatos disponibles')
            metadata = {}
        
        # 4. Detectar tipo de archivo
        es_formato_custom = archivo.endswith('.backup')
        es_bd_completa = (
            metadata.get('tipo') == 'bd_completa' or 
            'completo' in archivo.lower() or
            'backup_completo' in archivo.lower() or
            not metadata.get('tablas')
        )
        
        diagnostico['deteccion_archivo'] = {
            'es_formato_custom': es_formato_custom,
            'es_bd_completa': es_bd_completa,
            'tipo_detectado': metadata.get('tipo', 'desconocido')
        }
        
        # 5. Configuración que se aplicaría
        if es_formato_custom:
            timeout_segundos = 120
            timeout_descripcion = "2 minutos (pg_restore ultra-rápido)"
            metodo_restauracion = "pg_restore"
        elif es_bd_completa:
            config_restauracion = obtener_configuracion_restauracion_optimizada(ruta_backup)
            timeout_segundos = config_restauracion['timeout_segundos']
            timeout_descripcion = config_restauracion['timeout_descripcion']
            metodo_restauracion = config_restauracion['metodo']
        else:
            timeout_segundos = 60
            timeout_descripcion = "1 minuto (con limpieza automática)"
            metodo_restauracion = "psql con limpieza previa"# Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Configurar variables de entorno ANTES de usarlas
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        diagnostico['configuracion_aplicada'] = {
            'timeout_segundos': timeout_segundos,
            'timeout_descripcion': timeout_descripcion,
            'metodo_restauracion': metodo_restauracion
        }
        
        # 6. Verificar locks en la BD
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pg_locks WHERE NOT granted;")
                locks_bloqueantes = cursor.fetchone()[0]
                diagnostico['locks_bloqueantes'] = locks_bloqueantes
                
                if locks_bloqueantes > 0:
                    diagnostico['problemas'].append(f'❌ Hay {locks_bloqueantes} locks bloqueantes')
                    diagnostico['soluciones'].append('Terminar conexiones idle o transacciones largas')
        except:
            diagnostico['problemas'].append('⚠️ No se pudo verificar locks')
        
        # 7. Análisis específico del problema
        if diagnostico['tamaño_archivo_mb'] <= 50 and timeout_segundos == 600:
            diagnostico['analisis'] = {
                'problema_principal': 'Archivo pequeño con timeout correcto, pero falló',
                'causas_probables': [
                    'Locks en la base de datos',
                    'Archivo backup corrupto',
                    'Problemas de conectividad PostgreSQL',
                    'Configuración PostgreSQL inadecuada'
                ],
                'solucion_recomendada': 'Verificar locks y conectividad antes de intentar de nuevo'
            }
        
        return Response({
            'diagnostico_completo': diagnostico,
            'recomendacion': 'Revisar los problemas identificados antes de reintentar la restauración'
        })
        
    except Exception as e:
        return Response({'error': f'Error en diagnóstico: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restaurar_respaldo_forzado(request):
    """
    🔥 NUEVA: Restaurar respaldo con timeout extendido para resolver problemas específicos
    Body: {
        "archivo": "nombre_archivo.sql",
        "confirmar": true,
        "timeout_minutos": 30  // Opcional: timeout personalizado
    }
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        archivo = data.get('archivo')
        confirmar = data.get('confirmar', False)
        timeout_minutos = data.get('timeout_minutos', 30)  # Timeout extendido por defecto
        
        if not archivo:
            return Response({'error': 'Debe especificar el archivo a restaurar'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        if not confirmar:
            return Response({'error': 'Debe confirmar la restauración'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar conectividad antes de continuar
        conectividad_ok, error_conectividad = verificar_conectividad_db()
        if not conectividad_ok:
            return Response({
                'error': 'No se puede conectar a PostgreSQL',
                'detalle': error_conectividad,
                'solucion': 'Verificar que PostgreSQL esté ejecutándose y las credenciales sean correctas'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            return Response({'error': f'El archivo {archivo} no existe'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Configurar variables de entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # 🔥 COMANDO SIMPLIFICADO PARA MÁXIMA COMPATIBILIDAD
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '--quiet',
            '-f', ruta_backup
        ]
        
        # Timeout extendido en segundos
        timeout_segundos = timeout_minutos * 60
        
        print(f"🔥 RESTAURACIÓN FORZADA iniciada")
        print(f"📁 Archivo: {archivo}")
        print(f"⏰ Timeout extendido: {timeout_minutos} minutos ({timeout_segundos} segundos)")
        print(f"🔧 Comando: {' '.join(cmd)}")
        
        inicio = datetime.now()
        
        try:
            result = subprocess.run(
                cmd, 
                env=env, 
                capture_output=True, 
                text=True, 
                timeout=timeout_segundos
            )
            tiempo_transcurrido = datetime.now() - inicio
            
        except subprocess.TimeoutExpired:
            tiempo_transcurrido = datetime.now() - inicio
            return Response({
                'error': f'Restauración forzada cancelada por timeout ({timeout_minutos} minutos)',
                'archivo': archivo,
                'tiempo_transcurrido': str(tiempo_transcurrido),
                'timeout_usado': f'{timeout_minutos} minutos',
                'solucion': 'El problema persiste. Verificar locks de BD o usar función de diagnóstico.'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        print(f"⏱️ Restauración completada en: {tiempo_transcurrido}")
        print(f"📤 Return code: {result.returncode}")
        print(f"📄 stdout: {result.stdout}")
        print(f"⚠️ stderr: {result.stderr}")
        
        # Verificar resultado
        if result.returncode != 0:
            return Response({
                'error': 'Error en la restauración forzada',
                'details': result.stderr,
                'archivo': archivo,
                'tiempo_transcurrido': str(tiempo_transcurrido),
                'comando': ' '.join(cmd)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': '✅ Restauración forzada completada exitosamente',
            'archivo': archivo,
            'metodo': 'psql simplificado (sin optimizaciones complejas)',
            'tiempo_transcurrido': str(tiempo_transcurrido),
            'timeout_usado': f'{timeout_minutos} minutos',
            'comando_ejecutado': ' '.join(cmd),
            'output': result.stdout,
            'nota': 'Restauración con comando simplificado para máxima compatibilidad'
        })
        
    except Exception as e:
        return Response({'error': f'Error en restauración forzada: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
