
# # Tomando en cuenta que, supuestamente, estos son los modelos compatibles.

# from django.db import models
# from django.contrib.auth.models import User
# from apps.users.models import Empresa, Empleado, Planta
# from .models import TipoEvaluacion, Pregunta

# # ---------------------------------------------------------------------------- #



# class EvaluacionOficial(models.Model):

#     nombre = models.CharField(max_length=100)
#     tipo_norma = models.CharField(max_length=10, choices=TIPOS_OFICIALES)
#     descripcion = models.TextField()
#     instrucciones = models.TextField()
#     tiempo_limite = models.IntegerField(null=True, blank=True)  # minutos
#     umbral_aprobacion = models.IntegerField(null=True, blank=True)  # porcentaje
#     activa = models.BooleanField(default=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Evaluación Oficial"
#         verbose_name_plural = "Evaluaciones Oficiales"
#         db_table = 'evaluaciones_oficiales'

#     def __str__(self):
#         return f"{self.tipo_norma} - {self.nombre}"
# # ---------------------------------------------------------------------------- #
# class SeccionOficial(models.Model):
#     """
#     Secciones de las evaluaciones oficiales
#     Equivalente a SECCIONES_EVAL de los SQL
#     """
#     evaluacion_oficial = models.ForeignKey(EvaluacionOficial, on_delete=models.CASCADE, related_name='secciones')
#     nombre = models.CharField(max_length=200)
#     descripcion = models.TextField(blank=True)
#     numero_orden = models.IntegerField()
#     es_evaluable = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = "Sección Oficial"
#         verbose_name_plural = "Secciones Oficiales"
#         ordering = ['evaluacion_oficial', 'numero_orden']
#         db_table = 'secciones_oficiales'

#     def __str__(self):
#         return f"{self.evaluacion_oficial.tipo_norma} - {self.nombre}"
# # ---------------------------------------------------------------------------- #
# class PreguntaOficial(models.Model):
#     """
#     Preguntas oficiales de las normas NOM
#     Compatible con tabla PREGUNTAS de los SQL
#     """
#     TIPOS_PREGUNTA = [
#         ('Múltiple', 'Opción Múltiple'),
#         ('Abierta', 'Respuesta Abierta'),
#         ('Si/No', 'Sí/No'),
#         ('Escala', 'Escala Likert'),
#     ]

#     seccion = models.ForeignKey(SeccionOficial, on_delete=models.CASCADE, related_name='preguntas')
#     texto_pregunta = models.TextField()
#     tipo_pregunta = models.CharField(max_length=20, choices=TIPOS_PREGUNTA)
#     opciones_respuesta = models.JSONField(default=list, blank=True)  # Para opciones múltiples
#     es_obligatoria = models.BooleanField(default=True)
#     numero_orden = models.IntegerField()

#     # Para preguntas condicionales
#     pregunta_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
#     activador_padre = models.CharField(max_length=100, blank=True)

#     activa = models.BooleanField(default=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Pregunta Oficial"
#         verbose_name_plural = "Preguntas Oficiales"
#         ordering = ['seccion__evaluacion_oficial', 'seccion__numero_orden', 'numero_orden']
#         db_table = 'preguntas_oficiales'

#     def __str__(self):
#         return f"{self.seccion.evaluacion_oficial.tipo_norma} - {self.texto_pregunta[:50]}..."
# # ---------------------------------------------------------------------------- #
# class AsignacionEvaluacion(models.Model):
#     """
#     Asignaciones de evaluaciones oficiales a empleados
#     Incluye sistema de tokens
#     """
#     ESTADOS = [
#         ('activa', 'Activa'),
#         ('finalizada', 'Finalizada'),
#         ('cancelada', 'Cancelada'),
#         ('pausada', 'Pausada'),
#     ]

#     evaluacion_oficial = models.ForeignKey(EvaluacionOficial, on_delete=models.CASCADE)
#     empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
#     planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True)

#     # Configuración de la asignación
#     fecha_inicio = models.DateTimeField()
#     fecha_fin = models.DateTimeField()
#     duracion_dias = models.IntegerField()
#     estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')

#     # Administrador que creó la asignación
#     admin_asignador = models.ForeignKey(User, on_delete=models.CASCADE)

#     # Token único para la sesión
#     token_sesion = models.CharField(max_length=100, unique=True)

#     # Metadatos
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Asignación de Evaluación"
#         verbose_name_plural = "Asignaciones de Evaluaciones"
#         db_table = 'asignaciones_evaluacion'

#     def __str__(self):
#         return f"{self.evaluacion_oficial.nombre} - {self.empresa.nombre}"
# # ---------------------------------------------------------------------------- #
# class EmpleadoAsignado(models.Model):
#     """
#     Empleados asignados a una evaluación específica
#     Incluye tokens individuales
#     """
#     ESTADOS_EMPLEADO = [
#         ('pendiente', 'Pendiente'),
#         ('en_progreso', 'En Progreso'),
#         ('completada', 'Completada'),
#         ('expirada', 'Expirada'),
#     ]

#     asignacion = models.ForeignKey(AsignacionEvaluacion, on_delete=models.CASCADE, related_name='empleados_asignados')
#     empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

#     # Token único para este empleado
#     token_empleado = models.CharField(max_length=100, unique=True)

#     # Estado y progreso
#     estado = models.CharField(max_length=20, choices=ESTADOS_EMPLEADO, default='pendiente')
#     fecha_inicio_empleado = models.DateTimeField(null=True, blank=True)
#     fecha_finalizacion = models.DateTimeField(null=True, blank=True)
#     progreso_porcentaje = models.IntegerField(default=0)

#     # Metadatos
#     fecha_asignacion = models.DateTimeField(auto_now_add=True)
#     ultimo_acceso = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         verbose_name = "Empleado Asignado"
#         verbose_name_plural = "Empleados Asignados"
#         unique_together = ['asignacion', 'empleado']
#         db_table = 'empleados_asignados'

#     def __str__(self):
#         return f"{self.empleado.nombre} - {self.asignacion.evaluacion_oficial.nombre}"
# # ---------------------------------------------------------------------------- #
# class RespuestaEmpleado(models.Model):
#     """
#     Respuestas de empleados a preguntas oficiales
#     """
#     empleado_asignado = models.ForeignKey(EmpleadoAsignado, on_delete=models.CASCADE, related_name='respuestas')
#     pregunta_oficial = models.ForeignKey(PreguntaOficial, on_delete=models.CASCADE)

#     # Diferentes tipos de respuesta
#     respuesta_texto = models.TextField(blank=True)
#     respuesta_numerica = models.IntegerField(null=True, blank=True)
#     respuesta_multiple = models.JSONField(default=list, blank=True)
#     respuesta_booleana = models.BooleanField(null=True, blank=True)

#     # Metadatos de la respuesta
#     fecha_respuesta = models.DateTimeField(auto_now_add=True)
#     tiempo_respuesta_segundos = models.IntegerField(null=True, blank=True)
#     es_respuesta_final = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = "Respuesta de Empleado"
#         verbose_name_plural = "Respuestas de Empleados"
#         unique_together = ['empleado_asignado', 'pregunta_oficial']
#         db_table = 'respuestas_empleados'

#     def __str__(self):
#         return f"{self.empleado_asignado.empleado.nombre} - Pregunta {self.pregunta_oficial.numero_orden}"
# # ---------------------------------------------------------------------------- #