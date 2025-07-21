from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Empresa, Empleado
from apps.evaluaciones.models import EvaluacionCompleta
from apps.evaluaciones.serializers import EvaluacionSerializer
from django.db import models


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }
        
        # Agregar información de empresa si existe
        try:
            empresa = Empresa.objects.get(usuario=user)
            data['empresa'] = {
                'id': empresa.id,
                'nombre': empresa.nombre,
                'tipo': empresa.tipo,
                'activa': empresa.activa
            }
        except Empresa.DoesNotExist:
            data['empresa'] = None
            
        # Agregar información de empleado si existe
        try:
            empleado = Empleado.objects.get(usuario=user)
            data['empleado'] = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'email': empleado.email,
                'puesto': empleado.puesto,
                'empresa_id': empleado.empresa.id if empleado.empresa else None
            }
        except Empleado.DoesNotExist:
            data['empleado'] = None
            
        return Response(data)

    @action(detail=False, methods=['get'])
    def evaluaciones_disponibles(self, request):
        """Obtener evaluaciones disponibles para el usuario"""
        user = request.user
        
        # Primero verificar si es un empleado
        try:
            empleado = Empleado.objects.get(usuario=user)
            # Obtener evaluaciones asignadas al empleado
            from apps.evaluaciones.models import AsignacionEvaluacion
            asignaciones = AsignacionEvaluacion.objects.filter(
                empleado=empleado,
                estado__in=['pendiente', 'en_progreso']
            )
            evaluaciones = [asig.evaluacion for asig in asignaciones]
        except Empleado.DoesNotExist:
            # Si no es empleado, verificar si tiene empresa
            try:
                empresa = Empresa.objects.get(usuario=user)
                # Obtener todas las evaluaciones de la empresa
                evaluaciones = EvaluacionCompleta.objects.filter(empresa=empresa)
            except Empresa.DoesNotExist:
                # Si no tiene empresa, mostrar evaluaciones públicas
                evaluaciones = EvaluacionCompleta.objects.filter(empresa__isnull=True)
        
        serializer = EvaluacionSerializer(evaluaciones, many=True)
        return Response(serializer.data)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar empresas según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Empresa.objects.all()
        else:
            return Empresa.objects.filter(usuario=user)

    @action(detail=True, methods=['get'])
    def empleados(self, request, pk=None):
        """Obtener empleados de una empresa"""
        empresa = self.get_object()
        empleados = Empleado.objects.filter(empresa=empresa)
        data = []
        for empleado in empleados:
            data.append({
                'id': empleado.id,
                'nombre': empleado.nombre,
                'email': empleado.email,
                'puesto': empleado.puesto,
                'usuario_id': empleado.usuario.id if empleado.usuario else None
            })
        return Response(data)


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar empleados según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Empleado.objects.all()
        else:
            try:
                empresa = Empresa.objects.get(usuario=user)
                return Empleado.objects.filter(empresa=empresa)
            except Empresa.DoesNotExist:
                return Empleado.objects.filter(usuario=user)

    @action(detail=False, methods=['get'])
    def mis_evaluaciones(self, request):
        """Obtener evaluaciones asignadas al empleado actual"""
        user = request.user
        try:
            empleado = Empleado.objects.get(usuario=user)
            from apps.evaluaciones.models import AsignacionEvaluacion
            asignaciones = AsignacionEvaluacion.objects.filter(empleado=empleado)
            
            data = []
            for asignacion in asignaciones:
                data.append({
                    'id': asignacion.id,
                    'evaluacion': EvaluacionSerializer(asignacion.evaluacion).data,
                    'estado': asignacion.estado,
                    'fecha_asignacion': asignacion.fecha_asignacion,
                    'fecha_completada': asignacion.fecha_completada,
                    'duracion_dias': asignacion.duracion_dias,
                    'duracion_horas': asignacion.duracion_horas,
                    'dias_restantes': asignacion.dias_restantes,
                    'porcentaje_tiempo_usado': asignacion.porcentaje_tiempo_usado
                })
            
            return Response(data)
        except Empleado.DoesNotExist:
            return Response({'error': 'Usuario no es un empleado'}, status=status.HTTP_400_BAD_REQUEST)
