# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import TipoEvaluacion, Evaluacion, Pregunta

class TipoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvaluacion
        fields = '__all__'

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'

class PreguntaEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'
