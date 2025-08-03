# # -*- coding: utf-8 -*-
# """
# Serializers para los modelos oficiales de evaluaciones NOM
# """

# from rest_framework import serializers
# from .models_oficiales import (
#     EvaluacionOficial, SeccionOficial, PreguntaOficial,
#     AsignacionEvaluacion, EmpleadoAsignado, RespuestaEmpleado
# )
# from apps.users.models import Empleado, Empresa, Planta

# class EvaluacionOficialSerializer(serializers.ModelSerializer):
#     total_secciones = serializers.SerializerMethodField()
#     total_preguntas = serializers.SerializerMethodField()

#     class Meta:
#         model = EvaluacionOficial
#         fields = '__all__'

#     def get_total_secciones(self, obj):
#         return obj.secciones.count()

#     def get_total_preguntas(self, obj):
#         return PreguntaOficial.objects.filter(seccion__evaluacion_oficial=obj).count()

# class SeccionOficialSerializer(serializers.ModelSerializer):
#     total_preguntas = serializers.SerializerMethodField()

#     class Meta:
#         model = SeccionOficial
#         fields = '__all__'

#     def get_total_preguntas(self, obj):
#         return obj.preguntas.count()

# class PreguntaOficialSerializer(serializers.ModelSerializer):
#     seccion_nombre = serializers.CharField(source='seccion.nombre', read_only=True)
#     evaluacion_tipo = serializers.CharField(source='seccion.evaluacion_oficial.tipo_norma', read_only=True)

#     class Meta:
#         model = PreguntaOficial
#         fields = '__all__'

# class PreguntaOficialCreateSerializer(serializers.ModelSerializer):
#     """Serializer para crear/editar preguntas oficiales (SuperAdmin)"""

#     class Meta:
#         model = PreguntaOficial
#         fields = [
#             'seccion', 'texto_pregunta', 'tipo_pregunta', 'opciones_respuesta',
#             'es_obligatoria', 'numero_orden', 'pregunta_padre', 'activador_padre'
#         ]

#     def validate_opciones_respuesta(self, value):
#         """Validar que opciones_respuesta tenga formato correcto"""
#         if self.initial_data.get('tipo_pregunta') == 'Múltiple' and not value:
#             raise serializers.ValidationError("Las preguntas de opción múltiple requieren opciones de respuesta")
#         return value

# class EmpleadoAsignadoSerializer(serializers.ModelSerializer):
#     empleado_nombre = serializers.CharField(source='empleado.nombre', read_only=True)
#     empleado_email = serializers.EmailField(source='empleado.email', read_only=True)
#     puesto = serializers.CharField(source='empleado.puesto.nombre', read_only=True)
#     departamento = serializers.CharField(source='empleado.puesto.departamento.nombre', read_only=True)

#     class Meta:
#         model = EmpleadoAsignado
#         fields = [
#             'id', 'token_empleado', 'estado', 'progreso_porcentaje',
#             'fecha_asignacion', 'fecha_inicio_empleado', 'fecha_finalizacion',
#             'ultimo_acceso', 'empleado_nombre', 'empleado_email', 'puesto', 'departamento'
#         ]

# class AsignacionEvaluacionSerializer(serializers.ModelSerializer):
#     evaluacion_nombre = serializers.CharField(source='evaluacion_oficial.nombre', read_only=True)
#     evaluacion_tipo = serializers.CharField(source='evaluacion_oficial.tipo_norma', read_only=True)
#     empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
#     planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
#     admin_nombre = serializers.CharField(source='admin_asignador.get_full_name', read_only=True)

#     total_empleados = serializers.SerializerMethodField()
#     empleados_completados = serializers.SerializerMethodField()
#     empleados_pendientes = serializers.SerializerMethodField()
#     progreso_general = serializers.SerializerMethodField()

#     class Meta:
#         model = AsignacionEvaluacion
#         fields = '__all__'

#     def get_total_empleados(self, obj):
#         return obj.empleados_asignados.count()

#     def get_empleados_completados(self, obj):
#         return obj.empleados_asignados.filter(estado='completada').count()

#     def get_empleados_pendientes(self, obj):
#         return obj.empleados_asignados.filter(estado='pendiente').count()

#     def get_progreso_general(self, obj):
#         total = obj.empleados_asignados.count()
#         if total == 0:
#             return 0
#         completados = obj.empleados_asignados.filter(estado='completada').count()
#         return round((completados / total) * 100, 2)

# class AsignacionEvaluacionCreateSerializer(serializers.ModelSerializer):
#     """Serializer para crear asignaciones de evaluación"""
#     empleados_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True,
#         help_text="Lista de IDs de empleados a asignar"
#     )

#     class Meta:
#         model = AsignacionEvaluacion
#         fields = [
#             'evaluacion_oficial', 'empresa', 'planta', 'fecha_inicio',
#             'fecha_fin', 'duracion_dias', 'empleados_ids'
#         ]

#     def validate(self, data):
#         """Validaciones personalizadas"""
#         if data['fecha_fin'] <= data['fecha_inicio']:
#             raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")

#         if data['duracion_dias'] <= 0:
#             raise serializers.ValidationError("La duración debe ser mayor a 0 días")

#         return data

#     def create(self, validated_data):
#         empleados_ids = validated_data.pop('empleados_ids')
#         admin_asignador = self.context['request'].user

#         # Generar token único de sesión
#         import secrets
#         import string
#         token_sesion = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(20))

#         validated_data['admin_asignador'] = admin_asignador
#         validated_data['token_sesion'] = token_sesion

#         asignacion = AsignacionEvaluacion.objects.create(**validated_data)

#         # Crear empleados asignados con tokens únicos
#         for empleado_id in empleados_ids:
#             try:
#                 empleado = Empleado.objects.get(id=empleado_id)
#                 token_empleado = f"EMP{asignacion.empresa.empresa_id}_EVAL{asignacion.evaluacion_oficial.id}_EMP{empleado.empleado_id}_{secrets.token_hex(8).upper()}"

#                 EmpleadoAsignado.objects.create(
#                     asignacion=asignacion,
#                     empleado=empleado,
#                     token_empleado=token_empleado
#                 )
#             except Empleado.DoesNotExist:
#                 continue

#         return asignacion

# class RespuestaEmpleadoSerializer(serializers.ModelSerializer):
#     pregunta_texto = serializers.CharField(source='pregunta_oficial.texto_pregunta', read_only=True)
#     empleado_nombre = serializers.CharField(source='empleado_asignado.empleado.nombre', read_only=True)

#     class Meta:
#         model = RespuestaEmpleado
#         fields = '__all__'

# class RespuestaEmpleadoCreateSerializer(serializers.ModelSerializer):
#     """Serializer para crear respuestas (usado por empleados)"""

#     class Meta:
#         model = RespuestaEmpleado
#         fields = [
#             'pregunta_oficial', 'respuesta_texto', 'respuesta_numerica',
#             'respuesta_multiple', 'respuesta_booleana', 'tiempo_respuesta_segundos'
#         ]

#     def validate(self, data):
#         """Validar que se proporcione el tipo correcto de respuesta"""
#         pregunta = data['pregunta_oficial']

#         if pregunta.tipo_pregunta == 'Múltiple' and not data.get('respuesta_multiple'):
#             raise serializers.ValidationError("Se requiere respuesta_multiple para preguntas de opción múltiple")
#         elif pregunta.tipo_pregunta == 'Abierta' and not data.get('respuesta_texto'):
#             raise serializers.ValidationError("Se requiere respuesta_texto para preguntas abiertas")
#         elif pregunta.tipo_pregunta == 'Si/No' and data.get('respuesta_booleana') is None:
#             raise serializers.ValidationError("Se requiere respuesta_booleana para preguntas Sí/No")
#         elif pregunta.tipo_pregunta == 'Escala' and not data.get('respuesta_numerica'):
#             raise serializers.ValidationError("Se requiere respuesta_numerica para preguntas de escala")

#         return data


# # ===== SERIALIZERS PARA FASE 2: ASIGNACIONES CON TOKENS =====

# from apps.users.models import Empleado

# class EmpleadoAsignadoSimpleSerializer(serializers.ModelSerializer):
#     """Serializer simple para empleados en asignaciones"""

#     departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
#     puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)
#     planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
#     empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

#     class Meta:
#         model = Empleado
#         fields = [
#             'id', 'nombre', 'apellido', 'numero_empleado',
#             'departamento_nombre', 'puesto_nombre', 'planta_nombre', 'empresa_nombre',
#             'fecha_ingreso', 'activo'
#         ]


# class AsignacionEvaluacionCreateSerializer(serializers.ModelSerializer):
#     """Serializer para crear asignaciones"""

#     empleados_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True,
#         help_text="Lista de IDs de empleados a asignar"
#     )
#     evaluacion_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         model = AsignacionEvaluacion
#         fields = [
#             'evaluacion_id', 'nombre_asignacion', 'duracion_dias',
#             'empleados_ids', 'instrucciones_adicionales'
#         ]

#     def validate_empleados_ids(self, value):
#         if not value or len(value) == 0:
#             raise serializers.ValidationError("Debe seleccionar al menos un empleado")
#         return value

#     def validate_duracion_dias(self, value):
#         if value < 1 or value > 365:
#             raise serializers.ValidationError("La duración debe estar entre 1 y 365 días")
#         return value


# class TokenValidacionSerializer(serializers.Serializer):
#     """Serializer para validar tokens de empleados"""

#     token = serializers.CharField(
#         max_length=20,
#         min_length=8,
#         help_text="Token de acceso de 8 caracteres"
#     )

#     def validate_token(self, value):
#         # Convertir a mayúsculas y limpiar espacios
#         return value.upper().strip()
