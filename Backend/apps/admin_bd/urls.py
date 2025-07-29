# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views, views_simple

urlpatterns = [
    # URLs originales (complejas)
    path('exportar/<str:tabla_nombre>/', views.exportar_tabla_csv, name='exportar_tabla_csv'),
    path('tablas-exportables/', views.listar_tablas_exportables, name='listar_tablas_exportables'),
    path('estadisticas-exportacion/', views.estadisticas_exportacion, name='estadisticas_exportacion'),
    path('respaldar-completo/', views.respaldar_bd_completo, name='respaldar_bd_completo'),
    path('respaldar-parcial/', views.respaldar_bd_parcial, name='respaldar_bd_parcial'),
    path('descargar-respaldo/<str:archivo_nombre>/', views.descargar_respaldo, name='descargar_respaldo'),
    path('restaurar/', views.restaurar_bd, name='restaurar_bd'),
    
    # URLs simplificadas (versión mínima funcional)
    path('simple/exportar/<str:tabla_nombre>/', views_simple.exportar_tabla_csv_simple, name='exportar_tabla_simple'),
    path('simple/tablas/', views_simple.listar_tablas_simple, name='listar_tablas_simple'),
    path('simple/respaldar-completo/', views_simple.respaldar_completo_simple, name='respaldar_completo_simple'),
    path('simple/respaldar-parcial/', views_simple.respaldar_parcial_simple, name='respaldar_parcial_simple'),
    path('simple/restaurar/', views_simple.restaurar_bd_simple, name='restaurar_simple'),
    path('simple/descargar/<str:archivo_nombre>/', views_simple.descargar_respaldo_simple, name='descargar_respaldo_simple'),
]
