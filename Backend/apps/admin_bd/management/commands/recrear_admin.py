#!/usr/bin/env python
"""
🧪 MANAGEMENT COMMAND - RECREAR USUARIO ADMIN
=============================================

Command para recrear el usuario admin después de un reinicio de BD.
Útil cuando el sistema queda sin acceso después de limpiar la base de datos.

Uso:
    python manage.py recrear_admin

📋 Responsable: Yael Contreras  
📅 Fecha: Agosto 2025
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Recrear usuario admin después de reinicio de BD'

    def handle(self, *args, **options):
        """
        Recrear el usuario admin con credenciales por defecto
        """
        try:
            with transaction.atomic():
                # Verificar si ya existe un usuario admin
                if User.objects.filter(username='admin').exists():
                    self.stdout.write(
                        self.style.WARNING('⚠️ Usuario admin ya existe. Eliminándolo para recrear...')
                    )
                    User.objects.filter(username='admin').delete()
                
                # Crear usuario admin
                self.stdout.write('🔧 Creando usuario admin...')
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@axyoma.com',
                    password='admin123',  # Password temporal
                    first_name='Super',
                    last_name='Admin',
                    is_staff=True,
                    is_superuser=True
                )
                
                # Crear perfil de usuario asociado
                self.stdout.write('🔧 Creando perfil de superadmin...')
                perfil = PerfilUsuario.objects.create(
                    user=admin_user,
                    nivel_usuario='superadmin'
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Usuario admin recreado exitosamente!')
                )
                self.stdout.write(f'   - ID: {admin_user.id}')
                self.stdout.write(f'   - Username: {admin_user.username}')
                self.stdout.write(f'   - Email: {admin_user.email}')
                self.stdout.write(f'   - Perfil ID: {perfil.id}')
                self.stdout.write(f'   - Nivel: {perfil.nivel_usuario}')
                self.stdout.write('')
                self.stdout.write(
                    self.style.WARNING('🔐 CREDENCIALES TEMPORALES:')
                )
                self.stdout.write(f'   Username: admin')
                self.stdout.write(f'   Password: admin123')
                self.stdout.write('')
                self.stdout.write(
                    self.style.WARNING('⚠️ IMPORTANTE: Cambiar password después del primer login')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error recreando usuario admin: {str(e)}')
            )
            import traceback
            traceback.print_exc()
            return
            
        # Verificar que el login funcione
        from django.contrib.auth import authenticate
        
        self.stdout.write('🧪 Verificando login...')
        user = authenticate(username='admin', password='admin123')
        
        if user is not None:
            self.stdout.write(
                self.style.SUCCESS('✅ Login verificado correctamente!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Error: No se pudo verificar el login')
            )
