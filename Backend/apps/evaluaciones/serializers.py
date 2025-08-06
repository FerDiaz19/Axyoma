# ---------------------------------------------------------------------------- #

''' Serializadores para las entidades relacionadas a las evaluaciones (Ed Rubio) '''


from .models import *
from apps.users.models import Empresa, PerfilUsuario

from rest_framework import serializers

# ---------------------------------------------------------------------------- #

class PosiblesRespuestasSerializer(serializers.ModelSerializer):

    class Meta:
        model = PosiblesRespuestas
        fields = [
            'opcion_conjunto_id', 'texto_opcion', 'valor_booleano',
            'valor_numerico', 'valor_decimal', 'numero_orden' ]

# ---------------------------------------------------------------------------- #

class ConjuntoRespuestasSerializer(serializers.ModelSerializer):
    opciones = PosiblesRespuestasSerializer(many=True, required=False)

    class Meta:
        model = ConjuntoRespuestas
        fields = [ 'conjunto_id', 'nombre', 'descripcion', 'predefinido', 'opciones' ]


    def create(self, validated_data):
        opciones_data = validated_data.pop('opciones', [])
        conjunto = ConjuntoRespuestas.objects.create(**validated_data)

        for opcion_data in opciones_data:
            opcion_data.pop('opcion_conjunto_id', None)
            PosiblesRespuestas.objects.create(conjunto_respuestas=conjunto, **opcion_data)
        return conjunto

    def update(self, instance, validated_data):
        opciones_data = validated_data.pop('opciones', None)
        instance = super().update(instance, validated_data)

        if opciones_data is not None:
            instance.opciones.all().delete()

            for opcion_data in opciones_data:
                opcion_data.pop('opcion_conjunto_id', None)
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
    pregunta = PreguntaSerializer()
    conjunto_respuestas = serializers.JSONField(required=False, allow_null=True, write_only=True)
    conjunto_respuestas_detail = ConjuntoRespuestasSerializer(source='conjunto_respuestas', read_only=True)
    respuesta_correcta = PosiblesRespuestasSerializer(required=False, allow_null=True)

    class Meta:
        model = SeccionPregunta
        fields = [
            'seccion_pregunta_id', 'pregunta', 'numero_orden',
            'conjunto_respuestas', 'respuesta_correcta', 'conjunto_respuestas_detail'
        ]

        read_only_fields = [ 'seccion_pregunta_id' ]

    def create(self, validated_data, seccion_instance):
        pregunta_data = validated_data.pop('pregunta')
        conjunto_respuestas_data = validated_data.pop('conjunto_respuestas', None)
        respuesta_correcta_data = validated_data.pop('respuesta_correcta', None)

        pregunta_instance = Pregunta.objects.create(**pregunta_data)

        conjunto_respuestas_instance = None
        if conjunto_respuestas_data:
            conjunto_id = conjunto_respuestas_data.get('conjunto_id')

            if conjunto_id is not None:
                try:
                    # Intentar obtener el ConjuntoRespuestas existente por ID
                    db_conjunto = ConjuntoRespuestas.objects.get(conjunto_id=conjunto_id)

                    # Si el conjunto existe y es predefinido, lo usamos directamente
                    if db_conjunto.predefinido:
                        conjunto_respuestas_instance = db_conjunto
                    else:
                        # Si tiene ID pero NO es predefinido, esto es un caso de uso no esperado
                        # o un intento de recrear un conjunto personalizado ya existente.
                        # Aquí, asumimos que si se envía un ID, debe ser para un predefinido.
                        raise serializers.ValidationError(
                            f"El conjunto de respuestas con ID {conjunto_id} no es predefinido y no puede ser asociado de esta manera."
                        )
                except ConjuntoRespuestas.DoesNotExist:
                    # Si el ID fue proporcionado pero no existe, es un error
                    raise serializers.ValidationError(
                        f"Conjunto de respuestas con ID {conjunto_id} no encontrado."
                    )
            else:
                # Si no se proporcionó un conjunto_id, se crea un nuevo ConjuntoRespuestas
                # Aseguramos que los nuevos conjuntos no sean marcados como predefinidos
                data_for_new_conjunto = conjunto_respuestas_data.copy()
                data_for_new_conjunto['predefinido'] = False

                conjunto_serializer = ConjuntoRespuestasSerializer(data=data_for_new_conjunto)
                conjunto_serializer.is_valid(raise_exception=True)
                conjunto_respuestas_instance = conjunto_serializer.save()

        respuesta_correcta_instance = None
        if respuesta_correcta_data and conjunto_respuestas_instance:
            opcion_id = respuesta_correcta_data.get('opcion_conjunto_id')
            opcion_text = respuesta_correcta_data.get('texto_opcion')

            try:
                if opcion_id:
                    respuesta_correcta_instance = PosiblesRespuestas.objects.get(
                        opcion_conjunto_id=opcion_id,
                        conjunto_respuestas=conjunto_respuestas_instance
                    )
                elif opcion_text:
                    respuesta_correcta_instance = PosiblesRespuestas.objects.get(
                        conjunto_respuestas=conjunto_respuestas_instance,
                        texto_opcion=opcion_text
                    )
                else:
                    raise serializers.ValidationError("Datos de respuesta correcta incompletos.")
            except PosiblesRespuestas.DoesNotExist:
                raise serializers.ValidationError("La respuesta correcta especificada no existe en el conjunto de respuestas.")

        seccion_pregunta = SeccionPregunta.objects.create(
            seccion=seccion_instance,
            pregunta=pregunta_instance,
            conjunto_respuestas=conjunto_respuestas_instance,
            respuesta_correcta=respuesta_correcta_instance,
            **validated_data
        )
        return seccion_pregunta

    def update(self, instance, validated_data, seccion_instance):
        pregunta_data = validated_data.pop('pregunta', None)
        conjunto_respuestas_data = validated_data.pop('conjunto_respuestas', None)
        respuesta_correcta_data = validated_data.pop('respuesta_correcta', None)

        if pregunta_data:
            # Asumiendo que al actualizar una pregunta, si se cambia, se crea una nueva instancia de Pregunta
            # Si la intención es actualizar la pregunta existente, la lógica debería ser diferente aquí.
            pregunta_instance = Pregunta.objects.create(**pregunta_data)
            instance.pregunta = pregunta_instance

        conjunto_respuestas_instance = None
        if conjunto_respuestas_data:
            conjunto_id = conjunto_respuestas_data.get('conjunto_id')

            if conjunto_id is not None:
                try:
                    db_conjunto = ConjuntoRespuestas.objects.get(conjunto_id=conjunto_id)
                    if db_conjunto.predefinido:
                        conjunto_respuestas_instance = db_conjunto
                    else:
                        raise serializers.ValidationError(
                            f"El conjunto de respuestas con ID {conjunto_id} no es predefinido y no puede ser asociado de esta manera."
                        )
                except ConjuntoRespuestas.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Conjunto de respuestas con ID {conjunto_id} no encontrado durante la actualización."
                    )
            else:
                data_for_new_conjunto = conjunto_respuestas_data.copy()
                data_for_new_conjunto['predefinido'] = False

                conjunto_serializer = ConjuntoRespuestasSerializer(data=data_for_new_conjunto)
                conjunto_serializer.is_valid(raise_exception=True)
                conjunto_respuestas_instance = conjunto_serializer.save()
        instance.conjunto_respuestas = conjunto_respuestas_instance

        respuesta_correcta_instance = None
        if respuesta_correcta_data and conjunto_respuestas_instance:
            opcion_id = respuesta_correcta_data.get('opcion_conjunto_id')
            opcion_text = respuesta_correcta_data.get('texto_opcion')

            try:
                if opcion_id:
                    respuesta_correcta_instance = PosiblesRespuestas.objects.get(
                        opcion_conjunto_id=opcion_id,
                        conjunto_respuestas=conjunto_respuestas_instance
                    )
                elif opcion_text:
                    respuesta_correcta_instance = PosiblesRespuestas.objects.get(
                        conjunto_respuestas=conjunto_respuestas_instance,
                        texto_opcion=opcion_text
                    )
                else:
                    raise serializers.ValidationError("Datos de respuesta correcta incompletos.")
            except PosiblesRespuestas.DoesNotExist:
                raise serializers.ValidationError("La respuesta correcta especificada no existe en el conjunto de respuestas durante la actualización.")

        instance.seccion = seccion_instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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

        seccion_pregunta_serializer = self.fields['preguntas_seccion'].child
        for pregunta_item_data in preguntas_data:
            seccion_pregunta_serializer.create(validated_data=pregunta_item_data, seccion_instance=seccion)

        return seccion

    def update(self, instance, validated_data):
        preguntas_data = validated_data.pop('preguntas_seccion', None)
        instance = super().update(instance, validated_data)

        if preguntas_data is not None:
            instance.preguntas_seccion.all().delete()
            seccion_pregunta_serializer = self.fields['preguntas_seccion'].child

            for pregunta_item_data in preguntas_data:
                seccion_pregunta_serializer.create(validated_data=pregunta_item_data, seccion_instance=instance)

        return instance

# ---------------------------------------------------------------------------- #

class EvaluacionSerializer(serializers.ModelSerializer):
    secciones = SeccionEvalSerializer(many=True, required=False)

    tipo_evaluacion = serializers.CharField(source='tipo_evaluacion.nombre', read_only=True)
    tipo_evaluacion_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEvaluacion.objects.all(), source='tipo_evaluacion')

    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True, allow_null=True)
    empresa_id = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(),
        source='empresa', write_only=True, allow_null=True, required=False)

    creado_por_nombre = serializers.CharField(source='creado_por.username', read_only=True, allow_null=True)
    creado_por_id = serializers.PrimaryKeyRelatedField(queryset=PerfilUsuario.objects.all(),
        source='creado_por', write_only=True, allow_null=True, required=False)


    class Meta:
        model = Evaluacion
        fields = [
            'evaluacion_id', 'titulo', 'descripcion', 'instrucciones', 'contenido_informativo', 'tiempo_limite',
            'umbral_aprobacion', 'estado', 'tipo_evaluacion', 'tipo_evaluacion_id', 'secciones',
            'empresa_nombre', 'empresa_id', 'creado_por_nombre', 'creado_por_id' ]

        read_only_fields = [ 'evaluacion_id' ]


    def create(self, validated_data):
        secciones_data = validated_data.pop('secciones', [])
        evaluacion = Evaluacion.objects.create(**validated_data)

        seccion_serializer = self.fields['secciones'].child
        for seccion_data in secciones_data:
            seccion_serializer.create(validated_data={**seccion_data, 'evaluacion': evaluacion})

        return evaluacion


    def update(self, instance, validated_data):
        secciones_data = validated_data.pop('secciones', None)
        instance = super().update(instance, validated_data)

        if secciones_data is not None:
            instance.secciones.all().delete()
            seccion_serializer = self.fields['secciones'].child
            for seccion_data in secciones_data:
                seccion_serializer.create(validated_data={**seccion_data, 'evaluacion': instance})

        return instance

# ---------------------------------------------------------------------------- #

class AsignacionEmpleadoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombre_completo', read_only=True)

    empleado_puesto = serializers.CharField(source='empleado.puesto.nombre', read_only=True)
    empleado_puesto_id = serializers.IntegerField(source='empleado.puesto.puesto_id', read_only=True)

    empleado_departamento = serializers.CharField(source='empleado.departamento.nombre', read_only=True)
    empleado_departamento_id = serializers.IntegerField(source='empleado.departamento.departamento_id', read_only=True)

    empleado_planta = serializers.CharField(source='empleado.planta.nombre', read_only=True)
    empleado_planta_id = serializers.IntegerField(source='empleado.planta.planta_id', read_only=True)

    empleado_empresa = serializers.CharField(source='empleado.empresa.nombre', read_only=True)
    empleado_empresa_id = serializers.IntegerField(source='empleado.empresa.empresa_id', read_only=True)

    class Meta:
        model = AsignacionEmpleado
        fields = [
            'asignacion_empleado_id', 'empleado', 'empleado_nombre', 'status', 'token_acceso',
            'empleado_puesto', 'empleado_puesto_id', 'empleado_departamento', 'empleado_departamento_id',
            'empleado_planta', 'empleado_planta_id', 'empleado_empresa', 'empleado_empresa_id'

        ]
        read_only_fields = [
            'token_acceso',
            'asignacion_empleado_id',
            'empleado_nombre',
            'empleado_puesto',
            'empleado_puesto_id',
            'empleado_departamento',
            'empleado_departamento_id',
            'empleado_planta',
            'empleado_planta_id',
            'empleado_empresa',
            'empleado_empresa_id',
            'status'
        ]

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