# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Evaluacion, PreguntaEvaluacion, AplicacionEvaluacion, RespuestaEvaluacion
from apps.users.models import Empleado, Empresa, Planta
from django.contrib.auth.models import User

class PreguntaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaEvaluacion
        fields = '__all__'
        
class EvaluacionSerializer(serializers.ModelSerializer):
    preguntas = PreguntaEvaluacionSerializer(many=True, read_only=True)
    creado_por_nombre = serializers.ReadOnlyField()
    empresa_nombre = serializers.ReadOnlyField()
    planta_nombre = serializers.ReadOnlyField()
    tipo_display = serializers.ReadOnlyField()
    estado_display = serializers.ReadOnlyField()
    total_preguntas = serializers.ReadOnlyField()
    
    class Meta:
        model = Evaluacion
        fields = '__all__'
        
    def validate(self, data):
        """
        Validar que las evaluaciones normativas solo sean creadas por superusuarios
        y que las evaluaciones internas tengan empresa asignada
        """
        request = self.context.get('request')
        if request and request.user:
            user = request.user
            
            # Si es normativa, solo superusuarios pueden crearla
            if data.get('tipo') == 'normativa' and not user.is_superuser:
                raise serializers.ValidationError(
                    "Solo los superusuarios pueden crear evaluaciones normativas"
                )
            
            # Si es interna, debe tener empresa asignada
            if data.get('tipo') == 'interna':
                if not data.get('empresa') and hasattr(user, 'perfil'):
                    # Asignar automáticamente la empresa del usuario
                    try:
                        data['empresa'] = user.perfil.administrador_empresa
                    except:
                        pass
                
                if not data.get('empresa'):
                    raise serializers.ValidationError(
                        "Las evaluaciones internas deben tener una empresa asignada"
                    )
        
        return data

class EvaluacionListSerializer(serializers.ModelSerializer):
    """
    Serializer optimizado para listar evaluaciones
    """
    creado_por_nombre = serializers.ReadOnlyField()
    empresa_nombre = serializers.ReadOnlyField()
    planta_nombre = serializers.ReadOnlyField()
    tipo_display = serializers.ReadOnlyField()
    estado_display = serializers.ReadOnlyField()
    total_preguntas = serializers.ReadOnlyField()
    
    class Meta:
        model = Evaluacion
        fields = [
            'id', 'titulo', 'descripcion', 'tipo', 'estado', 'fecha_creacion', 
            'fecha_actualizacion', 'creado_por_nombre', 'empresa_nombre', 
            'planta_nombre', 'tipo_display', 'estado_display', 'total_preguntas',
            'instrucciones', 'tiempo_limite'
        ]

class EmpleadoSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para empleados en aplicaciones
    """
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'apellidos', 'email', 'departamento', 'puesto']

class AplicacionEvaluacionSerializer(serializers.ModelSerializer):
    evaluacion_titulo = serializers.CharField(source='evaluacion.titulo', read_only=True)
    aplicada_por_nombre = serializers.CharField(source='aplicada_por.get_full_name', read_only=True)
    empleados_info = EmpleadoSimpleSerializer(source='empleados', many=True, read_only=True)
    total_empleados = serializers.IntegerField(source='empleados.count', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = AplicacionEvaluacion
        fields = '__all__'

class RespuestaEvaluacionSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.get_full_name', read_only=True)
    pregunta_texto = serializers.CharField(source='pregunta.texto', read_only=True)
    
    class Meta:
        model = RespuestaEvaluacion
        fields = '__all__'
