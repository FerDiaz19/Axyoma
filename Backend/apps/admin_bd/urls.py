# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminBDViewSet

router = DefaultRouter()
router.register(r'', AdminBDViewSet, basename='admin_bd')

urlpatterns = [
    path('', include(router.urls)),
]
