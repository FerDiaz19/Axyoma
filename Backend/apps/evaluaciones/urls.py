
# ---------------------------------------------------------------------------- #

''' Endpoints para las entidades relacionadas a las evaluaciones (Ed Rubio) '''

from .views import *

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ---------------------------------------------------------------------------- #

router = DefaultRouter()

router.register(r'tipos-evaluacion', TipoEvaluacionViewSet)
router.register(r'evaluaciones', EvaluacionViewSet)
router.register(r'preguntas', PreguntaViewSet)
router.register(r'conjuntos-respuestas', ConjuntoRespuestasViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'asignaciones-empleado', AsignacionEmpleadoViewSet)
router.register(r'respuestas-empleado', RespuestaEmpleadoViewSet)
router.register(r'resultados-evaluacion', ResultadoEvaluacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# ---------------------------------------------------------------------------- #