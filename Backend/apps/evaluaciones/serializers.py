# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import (
    TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
    RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion,
    AsignacionEvaluacion, TokenEvaluacion
)
from apps.users.models import Empresa, Empleado, Departamento, Planta

class TipoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvaluacion
        fields = '__all__'

class PreguntaSerializer(serializers.ModelSerializer):
    tipo_evaluacion_nombre = serializers.CharField(source='tipo_evaluacion.nombre', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    creada_por_nombre = serializers.CharField(source='creada_por.get_full_name', read_only=True)
    
    class Meta:
        model = Pregunta
        fields = '__all__'
        
    def validate_opciones_respuesta(self, value):
        """Validar que las opciones sean requeridas para ciertos tipos"""
        tipo_respuesta = self.initial_data.get('tipo_respuesta')
        if tipo_respuesta in ['multiple', 'escala'] and not value:
            raise serializers.ValidationError("Las opciones de respuesta son requeridas para este tipo de pregunta")
        return value

class PreguntaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear preguntas"""
    class Meta:
        model = Pregunta
        fields = [
            'tipo_evaluacion', 'empresa', 'texto_pregunta', 'tipo_respuesta',
            'opciones_respuesta', 'es_obligatoria', 'orden'
        ]
        
    def create(self, validated_data):
        validated_data['creada_por'] = self.context['request'].user
        return super().create(validated_data)

class EvaluacionPreguntaSerializer(serializers.ModelSerializer):
    pregunta_texto = serializers.CharField(source='pregunta.texto_pregunta', read_only=True)
    tipo_respuesta = serializers.CharField(source='pregunta.tipo_respuesta', read_only=True)
    opciones_respuesta = serializers.JSONField(source='pregunta.opciones_respuesta', read_only=True)
    
    class Meta:
        model = EvaluacionPregunta
        fields = ['pregunta', 'orden', 'es_obligatoria', 'pregunta_texto', 'tipo_respuesta', 'opciones_respuesta']

class EvaluacionSerializer(serializers.ModelSerializer):
    tipo_evaluacion_nombre = serializers.CharField(source='tipo_evaluacion.nombre', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    creada_por_nombre = serializers.CharField(source='creada_por.get_full_name', read_only=True)
    preguntas_evaluacion = EvaluacionPreguntaSerializer(source='evaluacionpregunta_set', many=True, read_only=True)
    total_preguntas = serializers.SerializerMethodField()
    total_respuestas = serializers.SerializerMethodField()
    es_normativa = serializers.SerializerMethodField()
    empleados_asignados = serializers.SerializerMethodField()
    total_empleados_asignados = serializers.SerializerMethodField()
    asignaciones_por_estado = serializers.SerializerMethodField()
    identificador_unico = serializers.SerializerMethodField()
    
    class Meta:
        model = EvaluacionCompleta
        fields = '__all__'
        
    def get_total_preguntas(self, obj):
        return obj.preguntas.count()
        
    def get_total_respuestas(self, obj):
        return obj.respuestaevaluacion_set.count()
        
    def get_es_normativa(self, obj):
        """Determina si es una evaluación normativa (sin empresa)"""
        return obj.empresa is None
    
    def get_empleados_asignados(self, obj):
        """Obtiene lista de empleados asignados a esta evaluación"""
        asignaciones = obj.asignaciones.all()
        empleados = []
        for asignacion in asignaciones:
            empleados.append({
                'id': asignacion.empleado.empleado_id,
                'nombre': f"{asignacion.empleado.nombre} {asignacion.empleado.apellido_paterno} {asignacion.empleado.apellido_materno or ''}".strip(),
                'departamento': asignacion.empleado.departamento.nombre if asignacion.empleado.departamento else None,
                'puesto': asignacion.empleado.puesto.nombre if asignacion.empleado.puesto else None,
                'estado_asignacion': asignacion.estado,
                'fecha_asignacion': asignacion.fecha_asignacion,
                'fecha_inicio': asignacion.fecha_inicio,
                'fecha_fin': asignacion.fecha_fin,
                'fecha_completado': asignacion.fecha_completado,
            })
        return empleados
    
    def get_total_empleados_asignados(self, obj):
        """Total de empleados asignados"""
        return obj.asignaciones.count()
    
    def get_asignaciones_por_estado(self, obj):
        """Resumen de asignaciones por estado"""
        from django.db.models import Count
        resumen = obj.asignaciones.values('estado').annotate(count=Count('estado'))
        return {item['estado']: item['count'] for item in resumen}
    
    def get_identificador_unico(self, obj):
        """Genera un identificador único más descriptivo"""
        return f"{obj.tipo_evaluacion.nombre}-{obj.id}-{obj.fecha_creacion.strftime('%Y%m%d')}"

class EvaluacionCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear evaluaciones"""
    preguntas_seleccionadas = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = EvaluacionCompleta
        fields = [
            'titulo', 'descripcion', 'tipo_evaluacion', 'plantas', 'departamentos',
            'empleados_objetivo', 'fecha_inicio', 'fecha_fin', 'es_anonima',
            'preguntas_seleccionadas'
        ]
        
    def create(self, validated_data):
        preguntas_data = validated_data.pop('preguntas_seleccionadas', [])
        plantas = validated_data.pop('plantas', [])
        departamentos = validated_data.pop('departamentos', [])
        empleados = validated_data.pop('empleados_objetivo', [])
        
        # Obtener empresa del usuario
        user = self.context['request'].user
        if hasattr(user, 'perfil') and user.perfil.empresa:
            validated_data['empresa'] = user.perfil.empresa
        
        validated_data['creada_por'] = user
        
        evaluacion = EvaluacionCompleta.objects.create(**validated_data)
        
        # Agregar relaciones ManyToMany
        evaluacion.plantas.set(plantas)
        evaluacion.departamentos.set(departamentos)
        evaluacion.empleados_objetivo.set(empleados)
        
        # Agregar preguntas
        for pregunta_data in preguntas_data:
            EvaluacionPregunta.objects.create(
                evaluacion=evaluacion,
                pregunta_id=pregunta_data['pregunta_id'],
                orden=pregunta_data.get('orden', 1),
                es_obligatoria=pregunta_data.get('es_obligatoria', True)
            )
        
        return evaluacion

class DetalleRespuestaSerializer(serializers.ModelSerializer):
    pregunta_texto = serializers.CharField(source='pregunta.texto_pregunta', read_only=True)
    tipo_respuesta = serializers.CharField(source='pregunta.tipo_respuesta', read_only=True)
    
    class Meta:
        model = DetalleRespuesta
        fields = '__all__'

class RespuestaEvaluacionSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre_completo', read_only=True)
    evaluacion_titulo = serializers.CharField(source='evaluacion.titulo', read_only=True)
    detalles = DetalleRespuestaSerializer(many=True, read_only=True)
    
    class Meta:
        model = RespuestaEvaluacion
        fields = '__all__'

class RespuestaEvaluacionCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear respuestas a evaluaciones"""
    respuestas = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = RespuestaEvaluacion
        fields = ['evaluacion', 'empleado', 'respuestas']
        
    def create(self, validated_data):
        respuestas_data = validated_data.pop('respuestas')
        
        respuesta_evaluacion = RespuestaEvaluacion.objects.create(**validated_data)
        
        # Crear detalles de respuesta
        for respuesta_data in respuestas_data:
            DetalleRespuesta.objects.create(
                respuesta_evaluacion=respuesta_evaluacion,
                pregunta_id=respuesta_data['pregunta_id'],
                respuesta_texto=respuesta_data.get('respuesta_texto', ''),
                respuesta_numerica=respuesta_data.get('respuesta_numerica'),
                respuesta_multiple=respuesta_data.get('respuesta_multiple', [])
            )
        
        # Marcar como completada
        respuesta_evaluacion.completada = True
        respuesta_evaluacion.save()
        
        return respuesta_evaluacion

class ResultadoEvaluacionSerializer(serializers.ModelSerializer):
    evaluacion_titulo = serializers.CharField(source='evaluacion.titulo', read_only=True)
    
    class Meta:
        model = ResultadoEvaluacion
        fields = '__all__'

class AsignacionEvaluacionSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre', read_only=True)
    empleado_apellido = serializers.CharField(source='empleado.apellido', read_only=True)
    empleado_numero_empleado = serializers.CharField(source='empleado.numero_empleado', read_only=True)
    empleado_departamento = serializers.CharField(source='empleado.departamento.nombre', read_only=True)
    evaluacion_titulo = serializers.CharField(source='evaluacion.titulo', read_only=True)
    asignado_por_nombre = serializers.CharField(source='asignado_por.get_full_name', read_only=True)
    token_generado = serializers.SerializerMethodField()
    
    class Meta:
        model = AsignacionEvaluacion
        fields = '__all__'
        
    def get_token_generado(self, obj):
        """Obtener el token si existe"""
        try:
            return obj.token.token
        except:
            return None

class TokenEvaluacionSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='asignacion.empleado.nombre', read_only=True)
    empleado_apellido = serializers.CharField(source='asignacion.empleado.apellido', read_only=True)
    empleado_email = serializers.CharField(source='asignacion.empleado.email', read_only=True)
    empleado_numero_empleado = serializers.CharField(source='asignacion.empleado.numero_empleado', read_only=True)
    empleado_puesto = serializers.CharField(source='asignacion.empleado.puesto', read_only=True)
    empleado_departamento = serializers.CharField(source='asignacion.empleado.departamento.nombre', read_only=True)
    empleado_planta = serializers.CharField(source='asignacion.empleado.planta.nombre', read_only=True)
    evaluacion_titulo = serializers.CharField(source='asignacion.evaluacion.titulo', read_only=True)
    evaluacion_tipo = serializers.CharField(source='asignacion.evaluacion.tipo_evaluacion.nombre', read_only=True)
    evaluacion_id = serializers.IntegerField(source='asignacion.evaluacion.id', read_only=True)
    estado_asignacion = serializers.CharField(source='asignacion.estado', read_only=True)
    fecha_inicio_evaluacion = serializers.DateTimeField(source='asignacion.fecha_inicio', read_only=True)
    fecha_fin_evaluacion = serializers.DateTimeField(source='asignacion.fecha_fin', read_only=True)
    duracion_dias = serializers.IntegerField(source='asignacion.duracion_dias', read_only=True)
    duracion_horas = serializers.IntegerField(source='asignacion.duracion_horas', read_only=True)
    dias_restantes = serializers.SerializerMethodField()
    tiempo_restante_texto = serializers.SerializerMethodField()
    
    class Meta:
        model = TokenEvaluacion
        fields = '__all__'
    
    def get_dias_restantes(self, obj):
        """Calcular días restantes"""
        return obj.asignacion.dias_restantes
    
    def get_tiempo_restante_texto(self, obj):
        """Texto descriptivo del tiempo restante"""
        dias = obj.asignacion.dias_restantes
        if dias <= 0:
            return "Expirado"
        elif dias == 1:
            return "1 día restante"
        else:
            return f"{dias} días restantes"

class AsignacionMasivaSerializer(serializers.Serializer):
    """Serializer para asignación masiva de evaluaciones"""
    evaluacion_id = serializers.IntegerField()
    empleados_ids = serializers.ListField(child=serializers.IntegerField())
    fecha_inicio = serializers.DateTimeField()
    fecha_fin = serializers.DateTimeField()
    duracion_dias = serializers.IntegerField(required=False, help_text="Duración en días para completar la evaluación")
    duracion_horas = serializers.IntegerField(required=False, help_text="Duración estimada en horas para responder")
    instrucciones_especiales = serializers.CharField(required=False, max_length=500, help_text="Instrucciones adicionales para los empleados")
    
    def validate(self, data):
        """Validar que la fecha de fin sea posterior a la de inicio"""
        if data['fecha_fin'] <= data['fecha_inicio']:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        # Si se proporciona duración en días, validar que sea coherente
        if 'duracion_dias' in data:
            duracion = data['fecha_fin'] - data['fecha_inicio']
            if duracion.days > data['duracion_dias']:
                raise serializers.ValidationError(
                    f"La duración especificada ({data['duracion_dias']} días) es menor que el período de evaluación ({duracion.days} días)"
                )
        
        return data

class FiltroEmpleadosSerializer(serializers.Serializer):
    """Serializer para filtrar empleados para asignación"""
    planta_id = serializers.IntegerField(required=False)
    departamento_id = serializers.IntegerField(required=False)
    empleados_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
class EmpleadoEvaluacionSerializer(serializers.ModelSerializer):
    """Serializer simplificado para empleados en evaluaciones"""
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'apellido', 'numero_empleado', 'email', 'puesto', 
                 'departamento_nombre', 'planta_nombre']
