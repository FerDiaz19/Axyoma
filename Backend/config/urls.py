from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

schema_view = get_schema_view(
   openapi.Info(
      title="Axyoma API",
      default_version='v1',
      description="API para el sistema de gestión de empleados Axyoma",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@axyoma.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/evaluaciones/', include('apps.surveys.urls')),
    path('api/admin-bd/', include('apps.admin_bd.urls')),  # ← Nueva app para gestión BD
    path("api/health-check/", health_check),

    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
