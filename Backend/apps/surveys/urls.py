from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoEvaluacionViewSet, EvaluacionViewSet, PreguntaViewSet

router = DefaultRouter()
router.register(r'tipos', TipoEvaluacionViewSet, basename='tipos-evaluacion')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluaciones')
router.register(r'preguntas', PreguntaViewSet, basename='preguntas')

urlpatterns = [
    path('', include(router.urls)),
]
