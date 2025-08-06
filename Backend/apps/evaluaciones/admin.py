
# ---------------------------------------------------------------------------- #

from .models import *
from django.contrib import admin

# -- INLINES ----------------------------------------------------------------- #

class SeccionEvalInline(admin.StackedInline):
    model = SeccionEval
    extra = 1

class PosiblesRespuestasInline(admin.TabularInline):
    model = PosiblesRespuestas
    extra = 1

class SeccionPreguntaInline(admin.TabularInline):
    model = SeccionPregunta
    extra = 1
    fields = ( 'pregunta', 'conjunto_respuestas', 'respuesta_correcta', 'numero_orden' )

class AsignacionEmpleadoInline(admin.StackedInline):
    model = AsignacionEmpleado
    extra = 1
    readonly_fields = ['token_acceso', 'fecha_inicio', 'fecha_completado']

class RespuestaEmpleadoInline(admin.TabularInline):
    model = RespuestaEmpleado
    extra = 0
    readonly_fields = [
        'seccion_pregunta', 'opcion_seleccionada', 'respuesta_texto',
        'respuesta_valor_numerico', 'respuesta_valor_decimal',
        'respuesta_valor_booleano', 'es_correcta', 'fecha_respuesta'
    ]
    can_delete = False
    max_num = 0

# -- REGISTRO DE MODELOS ----------------------------------------------------- #

@admin.register(TipoEvaluacion)
class TipoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

# ---------------------------------------------------------------------------- #

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_evaluacion', 'empresa', 'estado', 'fecha_registro', 'total_secciones']
    list_filter = ['estado', 'tipo_evaluacion', 'empresa']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_registro', 'fecha_modificacion']
    inlines = [SeccionEvalInline]
    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'descripcion', 'instrucciones', 'contenido_informativo', 'tipo_evaluacion')
        }),
        ('Configuración', {
            'fields': ('tiempo_limite', 'umbral_aprobacion', 'estado')
        }),
        ('Relaciones', {
            'fields': ('empresa', 'creado_por')
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_modificacion')
        }),
    )

# ---------------------------------------------------------------------------- #

@admin.register(SeccionEval)
class SeccionEvalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'evaluacion', 'numero_orden', 'es_evaluable', 'total_preguntas']
    list_filter = ['evaluacion', 'es_evaluable']
    search_fields = ['nombre', 'evaluacion__titulo']
    inlines = [SeccionPreguntaInline]

# ---------------------------------------------------------------------------- #

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto_corto', 'tipo_pregunta', 'es_obligatoria', 'pregunta_padre']
    list_filter = ['tipo_pregunta', 'es_obligatoria']
    search_fields = ['texto_pregunta']

    def texto_corto(self, obj):
        return obj.__str__()
    texto_corto.short_description = 'Pregunta'

# ---------------------------------------------------------------------------- #

@admin.register(ConjuntoRespuestas)
class ConjuntoRespuestasAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'predefinido', 'total_opciones']
    list_filter = ['predefinido']
    search_fields = ['nombre']
    inlines = [PosiblesRespuestasInline]

# ---------------------------------------------------------------------------- #

@admin.register(PosiblesRespuestas)
class PosiblesRespuestasAdmin(admin.ModelAdmin):
    list_display = ['texto_opcion', 'conjunto_respuestas', 'numero_orden', 'valor_numerico', 'valor_decimal']
    list_filter = ['conjunto_respuestas']
    search_fields = ['texto_opcion']

# ---------------------------------------------------------------------------- #

@admin.register(SeccionPregunta)
class SeccionPreguntaAdmin(admin.ModelAdmin):
    list_display = ['seccion', 'pregunta', 'numero_orden', 'conjunto_respuestas', 'respuesta_correcta']
    list_filter = ['seccion', 'conjunto_respuestas']
    search_fields = ['seccion__nombre', 'pregunta__texto_pregunta']

# ---------------------------------------------------------------------------- #

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ['evaluacion', 'esta_activa', 'status', 'fecha_inicio', 'fecha_fin']
    list_filter = ['status']
    search_fields = ['evaluacion__titulo', 'empleado_evaluado__nombre']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información General', {
            'fields': ('evaluacion', 'fecha_inicio', 'fecha_fin', 'status')
        }),
        ('Evaluación 360', {
            'fields': ('empleado_evaluado', 'puesto_al_momento', 'departamento_al_momento')
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion')
        }),
    )

# ---------------------------------------------------------------------------- #

@admin.register(AsignacionEmpleado)
class AsignacionEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['asignacion', 'empleado', 'status', 'progreso_porcentaje', 'fecha_inicio']
    list_filter = ['status']
    search_fields = ['empleado__nombre', 'empleado__apellido_paterno', 'asignacion__evaluacion__titulo']
    readonly_fields = ['token_acceso', 'fecha_inicio', 'fecha_completado']
    inlines = [RespuestaEmpleadoInline]

    def progreso_porcentaje(self, obj):
        return f"{obj.progreso_porcentaje}%"
    progreso_porcentaje.short_description = 'Progreso'

# ---------------------------------------------------------------------------- #

@admin.register(RespuestaEmpleado)
class RespuestaEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['asignacion_empleado', 'seccion_pregunta', 'opcion_seleccionada', 'es_correcta', 'fecha_respuesta']
    list_filter = ['asignacion_empleado', 'seccion_pregunta']
    search_fields = ['asignacion_empleado__empleado__nombre', 'seccion_pregunta__pregunta__texto_pregunta']
    readonly_fields = [
        'asignacion_empleado', 'seccion_pregunta', 'opcion_seleccionada', 'respuesta_texto',
        'respuesta_valor_numerico', 'respuesta_valor_decimal', 'respuesta_valor_booleano',
        'es_correcta', 'fecha_respuesta'
    ]

# ---------------------------------------------------------------------------- #

@admin.register(ResultadoEvaluacion)
class ResultadoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['asignacion_empleado', 'porcentaje_correctas', 'aprobado', 'puntaje_total']
    list_filter = ['aprobado']
    search_fields = ['asignacion_empleado__empleado__nombre', 'asignacion_empleado__asignacion__evaluacion__titulo']
    readonly_fields = [
        'asignacion_empleado', 'puntaje_total', 'num_respuestas_correctas',
        'num_preguntas_evaluables', 'porcentaje_correctas', 'aprobado'
    ]

# ---------------------------------------------------------------------------- #
