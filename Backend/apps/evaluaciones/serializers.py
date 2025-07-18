# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import (
    TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
    RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion
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
    
    class Meta:
        model = EvaluacionCompleta
        fields = '__all__'
        
    def get_total_preguntas(self, obj):
        return obj.preguntas.count()
        
    def get_total_respuestas(self, obj):
        return obj.respuestaevaluacion_set.count()

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
