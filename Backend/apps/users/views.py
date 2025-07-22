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


<<<<<<< HEAD
# Serializers simples para los endpoints
class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuarios con información básica"""
    perfil = serializers.SerializerMethodField()
    empresa = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'is_staff', 'is_superuser', 'date_joined', 'last_login', 
                 'is_active', 'perfil', 'empresa']
    
    def get_perfil(self, obj):
        try:
            perfil = PerfilUsuario.objects.get(correo=obj.email)
            return {
                'id': perfil.id,
                'nombre': perfil.nombre,
                'apellido_paterno': perfil.apellido_paterno,
                'apellido_materno': perfil.apellido_materno,
                'nivel_usuario': perfil.nivel_usuario,
                'status': perfil.status
            }
        except PerfilUsuario.DoesNotExist:
            return None
    
    def get_empresa(self, obj):
        try:
            perfil = PerfilUsuario.objects.get(correo=obj.email)
            if perfil.nivel_usuario == 'admin_empresa':
                empresa = Empresa.objects.get(administrador=perfil)
                return {
                    'id': empresa.empresa_id,
                    'nombre': empresa.nombre,
                    'rfc': empresa.rfc
                }
            elif perfil.nivel_usuario == 'admin_planta':
                admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                return {
                    'id': admin_planta.planta.empresa.empresa_id,
                    'nombre': admin_planta.planta.empresa.nombre,
                    'rfc': admin_planta.planta.empresa.rfc
                }
        except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist, AdminPlanta.DoesNotExist):
            pass
        return None


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['empresa_id', 'nombre', 'rfc', 'direccion', 'status', 'fecha_registro']


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 
                 'email', 'telefono', 'fecha_ingreso', 'fecha_registro', 'status', 'puesto']


class PlantaSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    empresa = serializers.PrimaryKeyRelatedField(read_only=True)  # Hacer read_only para que no sea requerido
    
    class Meta:
        model = Planta
        fields = ['planta_id', 'nombre', 'direccion', 'fecha_registro', 'status', 'empresa', 'empresa_nombre']


class DepartamentoSerializer(serializers.ModelSerializer):
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    empresa_nombre = serializers.CharField(source='planta.empresa.nombre', read_only=True)
    
    class Meta:
        model = Departamento
        fields = ['departamento_id', 'nombre', 'descripcion', 'fecha_registro', 'status', 'planta', 'planta_nombre', 'empresa_nombre']


class PuestoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='departamento.planta.nombre', read_only=True)
    empresa_nombre = serializers.CharField(source='departamento.planta.empresa.nombre', read_only=True)
    
    class Meta:
        model = Puesto
        fields = ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento', 'departamento_nombre', 'planta_nombre', 'empresa_nombre']


class AuthViewSet(viewsets.ViewSet):
    """ViewSet para manejar autenticación"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Endpoint de login"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username y password son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            
            # Obtener información adicional del usuario
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'token': token.key
            }
            
            # Intentar agregar información de empresa si existe
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                user_data['empresa'] = {
                    'id': empresa.empresa_id,
                    'nombre': empresa.nombre,
                    'rfc': empresa.rfc,
                    'activa': empresa.status
                }
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                user_data['empresa'] = None
                
            # Nota: El modelo Empleado actual no tiene relación con User
            # Por ahora no incluimos información de empleado
            user_data['empleado'] = None
            
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Endpoint de logout"""
        try:
            if request.user.is_authenticated:
                # Eliminar el token del usuario
                Token.objects.filter(user=request.user).delete()
                return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Endpoint de registro"""
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not username or not password:
            return Response(
                {'error': 'Username y password son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'El usuario ya existe'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Crear token
        token = Token.objects.create(user=user)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


=======
>>>>>>> parent of f78dc52 (solucion de errores de login y usuarios de planta)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Solo superadmin puede ver todos los usuarios"""
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        else:
            # Usuario normal solo se puede ver a sí mismo
            return User.objects.filter(id=user.id)

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

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas generales del sistema (Solo SuperAdmin)"""
        try:
            if not request.user.is_superuser:
                return Response(
                    {'error': 'Acceso denegado'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            from apps.subscriptions.models import SuscripcionEmpresa, PlanSuscripcion
            from apps.evaluaciones.models import EvaluacionCompleta
            
            # Estadísticas básicas
            estadisticas = {
                'total_empresas': Empresa.objects.count(),
                'empresas_activas': Empresa.objects.filter(status=True).count(),
                'total_usuarios': User.objects.count(),
                'usuarios_activos': User.objects.filter(is_active=True).count(),
                'total_empleados': Empleado.objects.count(),
                'empleados_activos': Empleado.objects.filter(status=True).count(),
                'total_plantas': Planta.objects.count(),
                'plantas_activas': Planta.objects.filter(status=True).count(),
                'total_departamentos': Departamento.objects.count(),
                'departamentos_activos': Departamento.objects.filter(status=True).count(),
                'total_puestos': Puesto.objects.count(),
                'puestos_activos': Puesto.objects.filter(status=True).count(),
                'total_evaluaciones': EvaluacionCompleta.objects.count(),
                'total_suscripciones': SuscripcionEmpresa.objects.count(),
                'suscripciones_activas': SuscripcionEmpresa.objects.filter(estado='Activa').count(),
                'planes_disponibles': PlanSuscripcion.objects.filter(status=True).count()
            }
            
            return Response(estadisticas)
            
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo estadísticas: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
