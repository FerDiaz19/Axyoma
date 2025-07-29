# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminBDViewSet
from . import views_directo

router = DefaultRouter()
router.register(r'', AdminBDViewSet, basename='admin_bd')

urlpatterns = [
    path('', include(router.urls)),
    # URLs directas (consultas SQL directas) - SOLUCIÓN GARANTIZADA para tablas problemáticas
    path('directo/exportar/<str:tabla_nombre>/', views_directo.exportar_tabla_csv_directo, name='exportar_tabla_directo'),
    path('directo/tablas/', views_directo.listar_tablas_directas, name='listar_tablas_directas'),
]
