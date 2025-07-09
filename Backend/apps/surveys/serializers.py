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
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = '__all__'
        read_only_fields = ['creado_por', 'fecha_creacion', 'fecha_actualizacion']
        
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
            
            # Si es interna, debe tener empresa asignada (excepto superusuarios)
            if data.get('tipo') == 'interna' and not user.is_superuser:
                if not data.get('empresa'):
                    # Buscar la empresa donde el usuario es administrador
                    from apps.users.models import Empresa
                    try:
                        if hasattr(user, 'perfil'):
                            empresa = Empresa.objects.get(administrador=user.perfil)
                            data['empresa'] = empresa
                    except Empresa.DoesNotExist:
                        pass
                
                if not data.get('empresa'):
                    raise serializers.ValidationError(
                        "Las evaluaciones internas deben tener una empresa asignada"
                    )
        
        return data

class EvaluacionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar evaluaciones
    """
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    total_preguntas = serializers.IntegerField(source='preguntas.count', read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = [
            'id', 'titulo', 'descripcion', 'tipo', 'tipo_display', 
            'estado', 'estado_display', 'fecha_creacion', 'fecha_actualizacion',
            'creado_por_nombre', 'empresa_nombre', 'planta_nombre', 'total_preguntas'
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
