
# ---------------------------------------------------------------------------- #

''' Serializadores para las entidades relacionadas a las evaluaciones (Ed Rubio) '''


from .models import *
from rest_framework import serializers

# ---------------------------------------------------------------------------- #

class PosiblesRespuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosiblesRespuestas
        fields = [
            'opcion_conjunto_id', 'texto_opcion', 'valor_booleano',
            'valor_numerico', 'valor_decimal', 'numero_orden' ]

        read_only_fields = [ 'opcion_conjunto_id' ]

# ---------------------------------------------------------------------------- #

class ConjuntoRespuestasSerializer(serializers.ModelSerializer):
    opciones = PosiblesRespuestasSerializer(many=True, required=False)

    class Meta:
        model = ConjuntoRespuestas
        fields = [ 'conjunto_id', 'nombre', 'descripcion', 'predefinido', 'opciones' ]
        read_only_fields = [ 'conjunto_id', 'predefinido' ]

    def create(self, validated_data):
        opciones_data = validated_data.pop('opciones', [])
        conjunto = ConjuntoRespuestas.objects.create(**validated_data)

        for opcion_data in opciones_data:
            PosiblesRespuestas.objects.create(conjunto_respuestas=conjunto, **opcion_data)
        return conjunto

    def update(self, instance, validated_data):
        opciones_data = validated_data.pop('opciones', None)
        instance = super().update(instance, validated_data)

        if opciones_data is not None:
            instance.opciones.all().delete()

            for opcion_data in opciones_data:
                PosiblesRespuestas.objects.create(conjunto_respuestas=instance, **opcion_data)
        return instance

# ---------------------------------------------------------------------------- #

class PreguntaSerializer(serializers.ModelSerializer):
    conjunto_respuestas = ConjuntoRespuestasSerializer(read_only=True)

    class Meta:
        model = Pregunta
        fields = [ 'pregunta_id', 'texto_pregunta', 'tipo_pregunta', 'es_obligatoria',
            'pregunta_padre', 'activador_padre', 'conjunto_respuestas' ]

        read_only_fields = [ 'pregunta_id' ]

# ---------------------------------------------------------------------------- #

class SeccionPreguntaSerializer(serializers.ModelSerializer):
    pregunta = PreguntaSerializer(read_only=True)
    conjunto_respuestas = ConjuntoRespuestasSerializer(read_only=True)
    pregunta_id = serializers.PrimaryKeyRelatedField(
        queryset=Pregunta.objects.all(), source='pregunta')
    conjunto_respuestas_id = serializers.PrimaryKeyRelatedField(
        queryset=ConjuntoRespuestas.objects.all(), source='conjunto_respuestas', required=False, allow_null=True)

    class Meta:
        model = SeccionPregunta
        fields = [ 'seccion_pregunta_id', 'pregunta', 'pregunta_id', 'numero_orden',
            'conjunto_respuestas', 'conjunto_respuestas_id', 'respuesta_correcta' ]

        read_only_fields = [ 'seccion_pregunta_id' ]

# ---------------------------------------------------------------------------- #

class SeccionEvalSerializer(serializers.ModelSerializer):
    preguntas_seccion = SeccionPreguntaSerializer(many=True, required=False)

    class Meta:
        model = SeccionEval
        fields = [ 'seccion_id', 'nombre', 'descripcion',
            'numero_orden', 'es_evaluable', 'preguntas_seccion' ]

        read_only_fields = [ 'seccion_id' ]

    def create(self, validated_data):
        preguntas_data = validated_data.pop('preguntas_seccion', [])
        seccion = SeccionEval.objects.create(**validated_data)

        for pregunta_data in preguntas_data:
            SeccionPregunta.objects.create(seccion=seccion, **pregunta_data)
        return seccion

# ---------------------------------------------------------------------------- #

class EvaluacionSerializer(serializers.ModelSerializer):
    secciones = SeccionEvalSerializer(many=True, required=False)
    tipo_evaluacion = serializers.CharField(source='tipo_evaluacion.nombre', read_only=True)
    tipo_evaluacion_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEvaluacion.objects.all(), source='tipo_evaluacion'
    )

    class Meta:
        model = Evaluacion
        fields = [ 'evaluacion_id', 'titulo', 'descripcion', 'instrucciones', 'tiempo_limite',
            'umbral_aprobacion', 'estado', 'tipo_evaluacion', 'tipo_evaluacion_id', 'secciones' ]

        read_only_fields = [ 'evaluacion_id' ]

    def create(self, validated_data):
        secciones_data = validated_data.pop('secciones', [])
        evaluacion = Evaluacion.objects.create(**validated_data)

        for seccion_data in secciones_data:
            preguntas_data = seccion_data.pop('preguntas_seccion', [])
            seccion = SeccionEval.objects.create(evaluacion=evaluacion, **seccion_data)

            for pregunta_data in preguntas_data:
                pregunta_id = pregunta_data.pop('pregunta').id

                SeccionPregunta.objects.create(
                    seccion=seccion,
                    pregunta_id=pregunta_id,
                    numero_orden=pregunta_data['numero_orden'],
                    conjunto_respuestas_id=pregunta_data.get('conjunto_respuestas_id')
                )

        return evaluacion

    def update(self, instance, validated_data):
        secciones_data = validated_data.pop('secciones', None)
        instance = super().update(instance, validated_data)

        if secciones_data is not None:
            instance.secciones.all().delete()

            for seccion_data in secciones_data:
                preguntas_data = seccion_data.pop('preguntas_seccion', [])
                seccion = SeccionEval.objects.create(evaluacion=instance, **seccion_data)

                for pregunta_data in preguntas_data:
                    pregunta_id = pregunta_data.pop('pregunta').id

                    SeccionPregunta.objects.create(
                        seccion=seccion,
                        pregunta_id=pregunta_id,
                        numero_orden=pregunta_data['numero_orden'],
                        conjunto_respuestas_id=pregunta_data.get('conjunto_respuestas_id')
                    )

        return instance

# ---------------------------------------------------------------------------- #

class AsignacionEmpleadoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre_completo', read_only=True)

    class Meta:
        model = AsignacionEmpleado
        fields = [ 'asignacion_empleado_id', 'empleado', 'empleado_nombre', 'status' ]
        read_only_fields = [ 'asignacion_empleado_id', 'status', 'empleado_nombre' ]

# ---------------------------------------------------------------------------- #

class AsignacionSerializer(serializers.ModelSerializer):
    asignaciones_empleado = AsignacionEmpleadoSerializer(many=True, required=False)

    class Meta:
        model = Asignacion
        fields = [
            'asignacion_id', 'evaluacion', 'fecha_inicio', 'fecha_fin',
            'status', 'empleado_evaluado', 'asignaciones_empleado' ]

        read_only_fields = [ 'asignacion_id' ]

# ---------------------------------------------------------------------------- #

class TipoEvaluacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEvaluacion
        fields = [ 'tipo_evaluacion_id', 'nombre', 'descripcion' ]

# ---------------------------------------------------------------------------- #

class RespuestaEmpleadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RespuestaEmpleado
        fields = '__all__'

# ---------------------------------------------------------------------------- #

class ResultadoEvaluacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultadoEvaluacion
        fields = '__all__'

# ---------------------------------------------------------------------------- #
