
# ---------------------------------------------------------------------------- #

from . import views
from django.urls import path

# ---------------------------------------------------------------------------- #

app_name = 'AnorLondo'

urlpatterns = [
    path('', views.AccesoEvaluacion.as_view(), name='AccesoEvaluacion'),
    path('ashen-one/', views.EvaluacionActiva.as_view(), name='EvaluacionActiva'),
    path('chosen-undead/', views.EvaluacionCompletada.as_view(), name='EvaluacionCompletada'),
]

# ---------------------------------------------------------------------------- #
