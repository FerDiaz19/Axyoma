# Generated by Django 5.2.3 on 2025-07-10 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('NOM-035', 'NOM-035 - Factores de Riesgo Psicosocial'), ('NOM-030', 'NOM-030 - Servicios Preventivos de Seguridad'), ('360', 'Evaluación 360° - Competencias y Desempeño')], max_length=50, unique=True)),
                ('descripcion', models.TextField()),
                ('normativa_oficial', models.BooleanField(default=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tipo de Evaluación',
                'verbose_name_plural': 'Tipos de Evaluación',
            },
        ),
        migrations.CreateModel(
            name='EvaluacionCompleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('activa', 'Activa'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada')], default='borrador', max_length=20)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('es_anonima', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('departamentos', models.ManyToManyField(blank=True, to='users.departamento')),
                ('empleados_objetivo', models.ManyToManyField(blank=True, to='users.empleado')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones_nuevas', to='users.empresa')),
                ('plantas', models.ManyToManyField(blank=True, to='users.planta')),
            ],
            options={
                'verbose_name': 'Evaluación',
                'verbose_name_plural': 'Evaluaciones',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_pregunta', models.TextField()),
                ('tipo_respuesta', models.CharField(choices=[('multiple', 'Opción Múltiple'), ('escala', 'Escala Likert'), ('si_no', 'Sí/No'), ('texto', 'Texto Libre')], max_length=20)),
                ('opciones_respuesta', models.JSONField(blank=True, default=list)),
                ('es_obligatoria', models.BooleanField(default=True)),
                ('orden', models.IntegerField(default=1)),
                ('activa', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.empresa')),
                ('tipo_evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='evaluaciones.tipoevaluacion')),
            ],
            options={
                'verbose_name': 'Pregunta',
                'verbose_name_plural': 'Preguntas',
                'ordering': ['tipo_evaluacion', 'orden'],
            },
        ),
        migrations.CreateModel(
            name='EvaluacionPregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField()),
                ('es_obligatoria', models.BooleanField(default=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.evaluacioncompleta')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.pregunta')),
            ],
            options={
                'ordering': ['orden'],
                'unique_together': {('evaluacion', 'pregunta')},
            },
        ),
        migrations.AddField(
            model_name='evaluacioncompleta',
            name='preguntas',
            field=models.ManyToManyField(through='evaluaciones.EvaluacionPregunta', to='evaluaciones.pregunta'),
        ),
        migrations.CreateModel(
            name='RespuestaEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_respuesta', models.DateTimeField(auto_now_add=True)),
                ('completada', models.BooleanField(default=False)),
                ('tiempo_completado', models.IntegerField(blank=True, null=True)),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.empleado')),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.evaluacioncompleta')),
            ],
            options={
                'verbose_name': 'Respuesta a Evaluación',
                'verbose_name_plural': 'Respuestas a Evaluaciones',
                'unique_together': {('evaluacion', 'empleado')},
            },
        ),
        migrations.CreateModel(
            name='ResultadoEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_calculo', models.DateTimeField(auto_now_add=True)),
                ('total_respuestas', models.IntegerField()),
                ('porcentaje_participacion', models.DecimalField(decimal_places=2, max_digits=5)),
                ('puntuacion_promedio', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('resultados_detallados', models.JSONField(default=dict)),
                ('recomendaciones', models.TextField(blank=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.evaluacioncompleta')),
            ],
            options={
                'verbose_name': 'Resultado de Evaluación',
                'verbose_name_plural': 'Resultados de Evaluaciones',
            },
        ),
        migrations.AddField(
            model_name='evaluacioncompleta',
            name='tipo_evaluacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.tipoevaluacion'),
        ),
        migrations.CreateModel(
            name='DetalleRespuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta_texto', models.TextField(blank=True)),
                ('respuesta_numerica', models.IntegerField(blank=True, null=True)),
                ('respuesta_multiple', models.JSONField(blank=True, default=list)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.pregunta')),
                ('respuesta_evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='evaluaciones.respuestaevaluacion')),
            ],
            options={
                'verbose_name': 'Detalle de Respuesta',
                'verbose_name_plural': 'Detalles de Respuestas',
                'unique_together': {('respuesta_evaluacion', 'pregunta')},
            },
        ),
    ]
