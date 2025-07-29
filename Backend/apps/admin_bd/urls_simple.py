# -*- coding: utf-8 -*-
"""
URLs simplificadas para gestión de BD - Versión mínima funcional
"""
from django.urls import path
from . import views_simple

app_name = 'admin_bd_simple'

urlpatterns = [
    # Exportación CSV (Requisito 8)
    path('exportar-simple/<str:tabla_nombre>/', views_simple.exportar_tabla_csv_simple, name='exportar_tabla_simple'),
    path('tablas-simple/', views_simple.listar_tablas_simple, name='listar_tablas_simple'),
    
    # Respaldos (Requisitos 4 y 5)
    path('respaldar-completo-simple/', views_simple.respaldar_completo_simple, name='respaldar_completo_simple'),
    path('respaldar-parcial-simple/', views_simple.respaldar_parcial_simple, name='respaldar_parcial_simple'),
    
    # Restauración (Requisitos 6 y 7)
    path('restaurar-simple/', views_simple.restaurar_bd_simple, name='restaurar_simple'),
    
    # Descarga de respaldos
    path('descargar-respaldo-simple/<str:archivo_nombre>/', views_simple.descargar_respaldo_simple, name='descargar_respaldo_simple'),
]
