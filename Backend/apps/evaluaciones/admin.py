
# ---------------------------------------------------------------------------- #

from django.contrib import admin
from .models import *

# -- INLINES ----------------------------------------------------------------- #

''' Gestiona las opciones de respuesta en un conjunto de respuestas. '''
class PosiblesRespuestasInline(admin.TabularInline):
    model = PosiblesRespuestas
    extra = 0
    fields = [ 'texto_opcion', 'numero_orden', 'valor_booleano', 'valor_int', 'valor_decimal' ]

# ---------------------------------------------------------------------------- #

''' Gestiona las preguntas dentro de una sección. '''
class SeccionPreguntaInline(admin.TabularInline):
    model = SeccionPregunta
    extra = 0
    raw_id_fields = ( 'pregunta', 'conjunto_respuestas', 'respuesta_correcta' )
    fields = [ 'pregunta', 'conjunto_respuestas', 'respuesta_correcta', 'numero_orden' ]

# ---------------------------------------------------------------------------- #

''' Gestiona las secciones de una evaluación. '''
class SeccionEvalInline(admin.TabularInline):
    model = SeccionEval
    extra = 1
    fields = [ 'nombre', 'descripcion', 'numero_orden', 'es_evaluable' ]

# ---------------------------------------------------------------------------- #

''' Gestiona los empleados dentro de una asignación de evaluación. '''
class AsignacionEmpleadoInline(admin.TabularInline):
    model = AsignacionEmpleado
    extra = 0
    raw_id_fields = ['empleado']
    fields = [ 'empleado', 'status', 'fecha_asignacion', 'fecha_completado' ]
    readonly_fields = [ 'fecha_asignacion', 'fecha_completado' ]

# ---------------------------------------------------------------------------- #

''' Gestiona las respuestas de un empleado en una asignación. '''
class RespuestaEmpleadoInline(admin.TabularInline):
    model = RespuestaEmpleado
    extra = 0
    raw_id_fields = ( 'seccion_pregunta', 'opcion_seleccionada' )
    fields = [ 'seccion_pregunta', 'opcion_seleccionada', 'respuesta_texto', 'es_correcta' ]
    readonly_fields = fields

# -- REGISTER ---------------------------------------------------------------- #

@admin.register(TipoEvaluacion)
class TipoEvaluacionAdmin(admin.ModelAdmin):
    list_display = [ 'nombre', 'descripcion', 'activo', 'fecha_creacion' ]
    list_filter = [ 'activo', 'fecha_creacion' ]
    search_fields = [ 'nombre', 'descripcion' ]

# ---------------------------------------------------------------------------- #

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = [ 'titulo', 'tipo_evaluacion', 'estado', 'creado_por', 'empresa' ]
    list_filter = [ 'tipo_evaluacion', 'estado', 'empresa' ]
    search_fields = [ 'titulo', 'descripcion' ]
    inlines = [ SeccionEvalInline ]
    fieldsets = (
        ( None, { 'fields': ( 'titulo', 'descripcion', 'instrucciones', 'contenido_informativo' )}),
        ( 'Relaciones y configuración', {
            'fields': ( 'tipo_evaluacion', 'empresa', 'creado_por', 'estado', 'tiempo_limite', 'umbral_aprobacion')
        }),
    )
    # raw_id_fields = ( 'empresa', 'creado_por' )
    list_select_related = [ 'tipo_evaluacion', 'empresa', 'creado_por' ]

# ---------------------------------------------------------------------------- #

@admin.register(SeccionEval)
class SeccionEvalAdmin(admin.ModelAdmin):
    list_display = [ 'nombre', 'evaluacion', 'numero_orden', 'es_evaluable' ]
    list_filter = [ 'evaluacion__titulo', 'es_evaluable' ]
    search_fields = [ 'nombre', 'descripcion', 'evaluacion__titulo' ]
    inlines = [ SeccionPreguntaInline ]
    # raw_id_fields = ( 'evaluacion', )
    list_select_related = [ 'evaluacion' ]

# ---------------------------------------------------------------------------- #

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = [ 'texto_pregunta', 'tipo_pregunta', 'es_obligatoria', 'pregunta_padre' ]
    list_filter = [ 'tipo_pregunta', 'es_obligatoria' ]
    search_fields = [ 'texto_pregunta' ]
    # raw_id_fields = ( 'pregunta_padre', )
    list_select_related = [ 'pregunta_padre' ]

# ---------------------------------------------------------------------------- #

@admin.register(ConjuntoRespuestas)
class ConjuntoRespuestasAdmin(admin.ModelAdmin):
    list_display = [ 'nombre', 'descripcion', 'predefinido' ]
    list_filter = [ 'predefinido' ]
    search_fields = [ 'nombre', 'descripcion' ]
    inlines = [ PosiblesRespuestasInline ]

# ---------------------------------------------------------------------------- #

@admin.register(PosiblesRespuestas)
class PosiblesRespuestasAdmin(admin.ModelAdmin):
    list_display = [ 'texto_opcion', 'conjunto_respuestas', 'numero_orden', 'valor_booleano', 'valor_int', 'valor_decimal' ]
    list_filter = [ 'conjunto_respuestas__nombre' ]
    search_fields = [ 'texto_opcion' ]
    # raw_id_fields = ( 'conjunto_respuestas', )
    list_select_related = [ 'conjunto_respuestas' ]

# ---------------------------------------------------------------------------- #

@admin.register(SeccionPregunta)
class SeccionPreguntaAdmin(admin.ModelAdmin):
    list_display = [ 'seccion', 'pregunta', 'numero_orden', 'respuesta_correcta' ]
    list_filter = [ 'seccion__evaluacion', 'seccion' ]
    search_fields = [ 'seccion__nombre', 'pregunta__texto_pregunta' ]
    # raw_id_fields = ( 'seccion', 'pregunta', 'conjunto_respuestas', 'respuesta_correcta' )
    list_select_related = [ 'seccion__evaluacion', 'pregunta', 'conjunto_respuestas', 'respuesta_correcta' ]

# ---------------------------------------------------------------------------- #

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = [ 'evaluacion', 'fecha_inicio', 'fecha_fin', 'status', 'empleado_evaluado' ]
    list_filter = [ 'evaluacion__titulo', 'status' ]
    search_fields = [ 'evaluacion__titulo', 'empleado_evaluado__nombre' ]
    inlines = [ AsignacionEmpleadoInline ]
    # raw_id_fields = ( 'evaluacion', 'empleado_evaluado' )
    list_select_related = [ 'evaluacion', 'empleado_evaluado' ]

# ---------------------------------------------------------------------------- #

@admin.register(AsignacionEmpleado)
class AsignacionEmpleadoAdmin(admin.ModelAdmin):
    list_display = [ 'empleado', 'asignacion', 'status', 'fecha_asignacion', 'fecha_completado' ]
    list_filter = [ 'asignacion__evaluacion__titulo', 'status' ]
    search_fields = [ 'empleado__nombre', 'asignacion__evaluacion__titulo' ]
    inlines = [ RespuestaEmpleadoInline ]
    # raw_id_fields = ( 'asignacion', 'empleado' )
    readonly_fields = [ 'token_acceso', 'fecha_asignacion', 'fecha_completado' ]
    list_select_related = [ 'asignacion__evaluacion', 'empleado' ]

# ---------------------------------------------------------------------------- #

@admin.register(RespuestaEmpleado)
class RespuestaEmpleadoAdmin(admin.ModelAdmin):
    list_display = [ 'asignacion_empleado', 'seccion_pregunta', 'opcion_seleccionada', 'es_correcta' ]
    list_filter = [ 'asignacion_empleado__empleado', 'seccion_pregunta__seccion__evaluacion' ]
    search_fields = [ 'asignacion_empleado__empleado__nombre', 'seccion_pregunta__pregunta__texto_pregunta' ]
    readonly_fields = [ 'asignacion_empleado', 'seccion_pregunta', 'opcion_seleccionada', 'respuesta_texto',
        'respuesta_valor_numerico', 'respuesta_valor_decimal', 'respuesta_valor_booleano', 'es_correcta', 'fecha_respuesta' ]
    # raw_id_fields = ( 'asignacion_empleado', 'seccion_pregunta', 'opcion_seleccionada' )
    list_select_related = [ 'asignacion_empleado__empleado', 'seccion_pregunta__pregunta', 'opcion_seleccionada' ]

# ---------------------------------------------------------------------------- #

@admin.register(ResultadoEvaluacion)
class ResultadoEvaluacionAdmin(admin.ModelAdmin):
    list_display = [ 'asignacion_empleado', 'evaluacion', 'aprobado', 'porcentaje_correctas', 'fecha_calculo' ]
    list_filter = [ 'evaluacion__titulo', 'aprobado' ]
    search_fields = [ 'asignacion_empleado__empleado__nombre', 'evaluacion__titulo' ]
    readonly_fields = [ 'evaluacion', 'asignacion_empleado', 'puntaje_total', 'num_respuestas_correctas',
        'num_preguntas_evaluables', 'porcentaje_correctas', 'fecha_calculo', 'aprobado' ]
    list_select_related = [ 'evaluacion', 'asignacion_empleado__empleado' ]

# ---------------------------------------------------------------------------- #
