from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),  # Asegúrate de que users tenga migraciones
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanSuscripcion',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duracion', models.IntegerField(help_text='Duración en días')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Plan de Suscripción',
                'verbose_name_plural': 'Planes de Suscripción',
                'db_table': 'planes',
            },
        ),
        migrations.CreateModel(
            name='SuscripcionEmpresa',
            fields=[
                ('suscripcion_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(default='Activa', max_length=20)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(db_column='empresa_id', on_delete=django.db.models.deletion.CASCADE, to='users.empresa', verbose_name='Empresa')),
                ('plan_suscripcion', models.ForeignKey(db_column='plan_id', on_delete=django.db.models.deletion.CASCADE, to='subscriptions.plansuscripcion', verbose_name='Plan de Suscripción')),
            ],
            options={
                'verbose_name': 'Suscripción de Empresa',
                'verbose_name_plural': 'Suscripciones de Empresas',
                'db_table': 'suscripciones_empresa',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('pago_id', models.AutoField(primary_key=True, serialize=False)),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Costo')),
                ('monto_pago', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Pagado')),
                ('estado_pago', models.CharField(choices=[('Completado', 'Completado'), ('Pendiente', 'Pendiente'), ('Cancelado', 'Cancelado'), ('Fallido', 'Fallido')], default='Pendiente', max_length=20, verbose_name='Estado del Pago')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Pago')),
                ('fecha_vencimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Vencimiento')),
                ('transaccion_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='ID de Transacción')),
                ('comprobante', models.CharField(blank=True, max_length=255, null=True, verbose_name='Comprobante de Pago')),
                ('suscripcion', models.ForeignKey(db_column='suscripcion_id', on_delete=django.db.models.deletion.CASCADE, to='subscriptions.suscripcionempresa', verbose_name='Suscripción')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que realizó el pago')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'db_table': 'pagos',
                'ordering': ['-fecha_pago'],
            },
        ),
    ]
