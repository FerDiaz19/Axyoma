# -*- coding: utf-8 -*-
import os
import subprocess
from datetime import datetime
from django.conf import settings


class BackupManager:
    """
    Gestor de respaldos de PostgreSQL usando pg_dump
    """
    
    def __init__(self):
        self.db_settings = settings.DATABASES['default']
        self.backup_dir = os.path.join(settings.BASE_DIR, 'respaldos')
        self._crear_directorio_respaldos()
    
    def _crear_directorio_respaldos(self):
        """Crear directorio de respaldos si no existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def crear_respaldo_completo(self, nombre_archivo=None):
        """
        Crear respaldo completo de la base de datos
        """
        if not nombre_archivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f'respaldo_completo_{timestamp}.sql'
        
        ruta_archivo = os.path.join(self.backup_dir, nombre_archivo)
        
        comando = [
            'pg_dump',
            '-h', self.db_settings['HOST'],
            '-p', str(self.db_settings['PORT']),
            '-U', self.db_settings['USER'],
            '-d', self.db_settings['NAME'],
            '-f', ruta_archivo,
            '--verbose',
            '--no-password'
        ]
        
        try:
            # Configurar variable de entorno para password
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_settings['PASSWORD']
            
            result = subprocess.run(
                comando,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                'exitoso': True,
                'archivo': nombre_archivo,
                'ruta_completa': ruta_archivo,
                'tamaño': os.path.getsize(ruta_archivo) if os.path.exists(ruta_archivo) else 0,
                'mensaje': 'Respaldo creado exitosamente'
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'exitoso': False,
                'error': f'Error en pg_dump: {e.stderr}',
                'mensaje': 'Error al crear respaldo'
            }
        except Exception as e:
            return {
                'exitoso': False,
                'error': str(e),
                'mensaje': 'Error inesperado'
            }
    
    def crear_respaldo_parcial(self, tablas, nombre_archivo=None):
        """
        Crear respaldo de tablas específicas
        """
        if not nombre_archivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f'respaldo_parcial_{timestamp}.sql'
        
        ruta_archivo = os.path.join(self.backup_dir, nombre_archivo)
        
        comando = [
            'pg_dump',
            '-h', self.db_settings['HOST'],
            '-p', str(self.db_settings['PORT']),
            '-U', self.db_settings['USER'],
            '-d', self.db_settings['NAME'],
            '-f', ruta_archivo,
            '--verbose',
            '--no-password',
            '--data-only'  # Solo datos, no estructura
        ]
        
        # Agregar tablas específicas
        for tabla in tablas:
            comando.extend(['-t', tabla])
        
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_settings['PASSWORD']
            
            result = subprocess.run(
                comando,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                'exitoso': True,
                'archivo': nombre_archivo,
                'ruta_completa': ruta_archivo,
                'tablas': tablas,
                'tamaño': os.path.getsize(ruta_archivo) if os.path.exists(ruta_archivo) else 0,
                'mensaje': f'Respaldo de {len(tablas)} tablas creado exitosamente'
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'exitoso': False,
                'error': f'Error en pg_dump: {e.stderr}',
                'mensaje': 'Error al crear respaldo parcial'
            }
        except Exception as e:
            return {
                'exitoso': False,
                'error': str(e),
                'mensaje': 'Error inesperado'
            }
    
    def listar_respaldos(self):
        """
        Listar todos los respaldos disponibles
        """
        respaldos = []
        
        if not os.path.exists(self.backup_dir):
            return respaldos
        
        for archivo in os.listdir(self.backup_dir):
            if archivo.endswith('.sql'):
                ruta_completa = os.path.join(self.backup_dir, archivo)
                stat = os.stat(ruta_completa)
                
                respaldos.append({
                    'nombre': archivo,
                    'tamaño': stat.st_size,
                    'fecha_creacion': datetime.fromtimestamp(stat.st_ctime),
                    'fecha_modificacion': datetime.fromtimestamp(stat.st_mtime)
                })
        
        return sorted(respaldos, key=lambda x: x['fecha_creacion'], reverse=True)
    
    def eliminar_respaldo(self, nombre_archivo):
        """
        Eliminar un archivo de respaldo
        """
        ruta_archivo = os.path.join(self.backup_dir, nombre_archivo)
        
        try:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                return {'exitoso': True, 'mensaje': 'Respaldo eliminado exitosamente'}
            else:
                return {'exitoso': False, 'mensaje': 'Archivo no encontrado'}
        except Exception as e:
            return {'exitoso': False, 'mensaje': f'Error al eliminar: {str(e)}'}
