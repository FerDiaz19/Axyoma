
from rest_framework.routers import DefaultRouter

from django.urls import path, include



router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]





# # -*- coding: utf-8 -*-
# from django.urls import path, include

# from .views import (
#     TipoEvaluacionViewSet, PreguntaViewSet,
#     EvaluacionViewSet, RespuestaEvaluacionViewSet, preguntas_nom035,
#     EvaluacionOficialViewSet, PreguntaOficialViewSet, preguntas_por_normativa
# )

# # Router para el sistema existente de evaluaciones
# router = DefaultRouter()
# router.register(r'tipos', TipoEvaluacionViewSet)
# router.register(r'preguntas', PreguntaViewSet, basename='pregunta')
# router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
# router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')

# # Router para evaluaciones oficiales (accesible por frontend)
# router_oficial = DefaultRouter()
# router_oficial.register(r'evaluaciones-oficiales', EvaluacionOficialViewSet, basename='evaluacion-oficial')
# router_oficial.register(r'preguntas-oficiales', PreguntaOficialViewSet, basename='pregunta-oficial')

# urlpatterns = [
#     # Sistema existente de evaluaciones

#     path('preguntas-nom035/', preguntas_nom035),

#     # Evaluaciones oficiales para frontend
#     path('oficial/', include(router_oficial.urls)),
#     path('oficial/normativa/<str:normativa>/', preguntas_por_normativa, name='preguntas-por-normativa'),

#     # Sistema oficial de evaluaciones NOM (SuperAdmin)
#     path('superadmin/', include('apps.evaluaciones.urls_oficiales')),

#     # Fase 2: Sistema de asignaciones con tokens
#     path('asignacion/', include('apps.evaluaciones.urls_asignaciones')),
# ]
