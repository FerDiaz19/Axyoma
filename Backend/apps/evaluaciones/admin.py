# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
    RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion
)

@admin.register(TipoEvaluacion)
class TipoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'normativa_oficial', 'activo', 'fecha_creacion']
    list_filter = ['normativa_oficial', 'activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['tipo_evaluacion', 'texto_pregunta', 'tipo_respuesta', 'empresa', 'activa', 'orden']
    list_filter = ['tipo_evaluacion', 'tipo_respuesta', 'empresa', 'activa']
    search_fields = ['texto_pregunta']
    list_editable = ['orden', 'activa']

class EvaluacionPreguntaInline(admin.TabularInline):
    model = EvaluacionPregunta
    extra = 0

@admin.register(EvaluacionCompleta)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_evaluacion', 'empresa', 'estado', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo_evaluacion', 'estado', 'empresa']
    search_fields = ['titulo', 'descripcion']
    inlines = [EvaluacionPreguntaInline]
    filter_horizontal = ['plantas', 'departamentos', 'empleados_objetivo']

@admin.register(RespuestaEvaluacion)
class RespuestaEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['evaluacion', 'empleado', 'fecha_respuesta', 'completada']
    list_filter = ['completada', 'evaluacion__tipo_evaluacion']
    search_fields = ['evaluacion__titulo', 'empleado__nombre']

@admin.register(DetalleRespuesta)
class DetalleRespuestaAdmin(admin.ModelAdmin):
    list_display = ['respuesta_evaluacion', 'pregunta', 'respuesta_texto', 'respuesta_numerica']
    list_filter = ['pregunta__tipo_respuesta']

@admin.register(ResultadoEvaluacion)
class ResultadoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['evaluacion', 'total_respuestas', 'porcentaje_participacion', 'fecha_calculo']
    list_filter = ['evaluacion__tipo_evaluacion']
    readonly_fields = ['fecha_calculo']
