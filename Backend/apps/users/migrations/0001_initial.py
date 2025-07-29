from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('nivel_usuario', models.CharField(choices=[('superadmin', 'Super Administrador'), ('admin_empresa', 'Administrador de Empresa'), ('admin_planta', 'Administrador de Planta'), ('empleado', 'Empleado')], default='empleado', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Usuario',
                'verbose_name_plural': 'Perfiles de Usuario',
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('empresa_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=13)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('email_contacto', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono_contacto', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('administrador', models.ForeignKey(limit_choices_to={'nivel_usuario': 'admin_empresa'}, on_delete=django.db.models.deletion.CASCADE, to='users.perfilusuario')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'db_table': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('planta_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.empresa')),
            ],
            options={
                'verbose_name': 'Planta',
                'verbose_name_plural': 'Plantas',
                'db_table': 'plantas',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('departamento_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamentos',
            },
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('puesto_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.departamento')),
            ],
            options={
                'verbose_name': 'Puesto',
                'verbose_name_plural': 'Puestos',
                'db_table': 'puestos',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('empleado_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('antiguedad', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.departamento')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.puesto')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'empleados',
            },
        ),
        migrations.CreateModel(
            name='AdminPlanta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planta')),
                ('usuario', models.ForeignKey(limit_choices_to={'nivel_usuario': 'admin_planta'}, on_delete=django.db.models.deletion.CASCADE, to='users.perfilusuario')),
            ],
            options={
                'verbose_name': 'Administrador de Planta',
                'verbose_name_plural': 'Administradores de Plantas',
                'db_table': 'admin_plantas',
            },
        ),
    ]
