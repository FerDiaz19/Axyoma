# Generated by Django 5.2.3 on 2025-07-10 18:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
                ('apellido_paterno', models.CharField(max_length=64)),
                ('apellido_materno', models.CharField(blank=True, max_length=64, null=True)),
                ('correo', models.EmailField(max_length=255, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('nivel_usuario', models.CharField(choices=[('superadmin', 'Super Administrador'), ('admin-empresa', 'Administrador de Empresa'), ('admin-planta', 'Administrador de Planta')], max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('admin_empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.perfilusuario')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('empresa_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=65, unique=True)),
                ('rfc', models.CharField(max_length=16, unique=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('logotipo', models.CharField(blank=True, max_length=128, null=True)),
                ('email_contacto', models.CharField(blank=True, max_length=128, null=True)),
                ('telefono_contacto', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('administrador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.perfilusuario')),
            ],
            options={
                'db_table': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('planta_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(db_column='empresa_id', on_delete=django.db.models.deletion.CASCADE, to='users.empresa')),
            ],
            options={
                'db_table': 'plantas',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('departamento_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
            ],
            options={
                'db_table': 'departamentos',
                'unique_together': {('nombre', 'planta')},
            },
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('puesto_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.departamento')),
            ],
            options={
                'db_table': 'puestos',
                'unique_together': {('nombre', 'departamento')},
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('empleado_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
                ('apellido_paterno', models.CharField(max_length=64)),
                ('apellido_materno', models.CharField(blank=True, max_length=64, null=True)),
                ('genero', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=10)),
                ('antiguedad', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.departamento')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.puesto')),
            ],
            options={
                'db_table': 'empleados',
            },
        ),
        migrations.CreateModel(
            name='AdminPlanta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('password_temporal', models.CharField(blank=True, help_text='Contraseña temporal generada automáticamente', max_length=128, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.perfilusuario')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
            ],
            options={
                'db_table': 'admin_plantas',
                'unique_together': {('usuario', 'planta')},
            },
        ),
    ]
