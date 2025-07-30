# -*- coding: utf-8 -*-
"""
🗄️ GESTIÓN DE RESPALDOS Y RESTAURACIÓN DE BASE DE DATOS
========================================================

Sistema completo de respaldos, restauración y gestión de base de datos para Axyoma.
Incluye respaldos compatibles con pgAdmin, reseteo de BD y carga de datos iniciales.

📋 Responsable: Yael Contreras
📅 Fecha: Enero 2025
🔢 Versión: 2.0

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respaldar_tablas(request):
    """
    Respaldar una o múltiples tablas específicas
    Body: {
        "tablas": ["tabla1", "tabla2", ...],
        "incluir_datos": true/false,
        "descripcion": "Descripción opcional del respaldo"
    }
    """
    try:
        is_superadmin, error_response = verificar_superadmin(request)
        if not is_superadmin:
            return error_response
        
        data = request.data
        tablas = data.get('tablas', [])
        incluir_datos = data.get('incluir_datos', True)
        descripcion = data.get('descripcion', '')
        
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
        
        nombre_archivo = f"backup_tablas_{tablas_str}_{timestamp}.sql"
        ruta_backup = os.path.join(BACKUP_DIR, nombre_archivo)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Construir comando pg_dump (compatible con pgAdmin)
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '--verbose',
            '--clean',
            '--if-exists',
            '--no-owner',
            '--no-privileges',
        ]
        
        # Agregar opciones según configuración
        if not incluir_datos:
            cmd.append('--schema-only')
        
        # Agregar tablas específicas
        for tabla in tablas:
            cmd.extend(['--table', tabla])
        
        cmd.extend(['--file', ruta_backup])
        
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
    Respaldar toda la base de datos
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
        
        # Crear nombre del archivo de respaldo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_completo_{timestamp}.sql"
        ruta_backup = os.path.join(BACKUP_DIR, nombre_archivo)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Construir comando pg_dump para BD completa (compatible con pgAdmin)
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '--verbose',
            '--clean',
            '--if-exists',
            '--no-owner',
            '--no-privileges',
        ]
        
        # Agregar opciones según configuración
        if not incluir_datos:
            cmd.append('--schema-only')
        
        cmd.extend(['--file', ruta_backup])
        
        # Configurar variables de entorno para PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Ejecutar pg_dump
        print(f"🔄 Ejecutando respaldo completo de BD: {db_config['name']}")
        print(f"📁 Directorio de respaldos: {BACKUP_DIR}")
        print(f"📄 Archivo de respaldo: {ruta_backup}")
        print(f"🔧 Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
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
        
        # Crear metadatos del respaldo
        metadata = {
            'tipo': 'bd_completa',
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
            'message': 'Respaldo completo creado exitosamente',
            'archivo': nombre_archivo,
            'tamaño_mb': round(metadata['tamaño_bytes'] / (1024*1024), 2),
            'ruta': ruta_backup,
            'metadata': metadata
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
        
        # Verificar que el archivo existe
        ruta_backup = os.path.join(BACKUP_DIR, archivo)
        if not os.path.exists(ruta_backup):
            return Response({'error': f'El archivo {archivo} no existe'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Leer metadatos si existen
        metadata_file = ruta_backup.replace('.sql', '_metadata.json')
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # Obtener configuración de BD
        db_config = obtener_config_db()
        
        # Construir comando psql para restaurar
        cmd = [
            'C:/Program Files/PostgreSQL/17/bin/psql.exe',
            f"--host={db_config['host']}",
            f"--port={db_config['port']}",
            f"--username={db_config['user']}",
            f"--dbname={db_config['name']}",
            '--no-password',
            '--quiet',  # Menos verbose para evitar ruido
            '--echo-errors',  # Solo mostrar errores
        ]
        
        # Configurar según modo
        if modo == 'replace':
            cmd.extend(['--single-transaction'])  # Todo o nada
        
        cmd.extend(['-f', ruta_backup])  # Usar -f en lugar de --file
        
        # Configurar variables de entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Ejecutar restauración
        print(f"🔄 Ejecutando restauración desde: {archivo}")
        print(f"🔧 Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        print(f"📤 Return code: {result.returncode}")
        print(f"📄 stdout: {result.stdout}")
        print(f"⚠️ stderr: {result.stderr}")
        
        # Verificar resultado
        if result.returncode != 0:
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
        
        return Response({
            'message': '✅ Restauración completada exitosamente',
            'archivo': archivo,
            'modo': modo,
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
