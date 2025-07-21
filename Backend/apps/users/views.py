from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import Empresa, Empleado, PerfilUsuario, Planta, Departamento, Puesto, AdminPlanta
from apps.evaluaciones.models import EvaluacionCompleta
from apps.evaluaciones.serializers import EvaluacionSerializer
from django.db import models


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
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 
                 'genero', 'antiguedad', 'status', 'departamento_nombre', 
                 'puesto_nombre', 'planta_nombre']


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
        
        # Obtener información del perfil de usuario
        try:
            perfil = PerfilUsuario.objects.get(correo=user.email)
            data['perfil'] = {
                'id': perfil.id,
                'nombre': perfil.nombre,
                'apellido_paterno': perfil.apellido_paterno,
                'apellido_materno': perfil.apellido_materno,
                'nivel_usuario': perfil.nivel_usuario,
                'status': perfil.status
            }
            
            # Si es admin_empresa, buscar su empresa
            if perfil.nivel_usuario == 'admin_empresa':
                try:
                    empresa = Empresa.objects.get(administrador=perfil)
                    data['empresa'] = {
                        'id': empresa.empresa_id,
                        'nombre': empresa.nombre,
                        'rfc': empresa.rfc,
                        'activa': empresa.status
                    }
                except Empresa.DoesNotExist:
                    data['empresa'] = None
            
            # Si es admin_planta, buscar su planta asignada
            elif perfil.nivel_usuario == 'admin_planta':
                try:
                    admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                    data['planta'] = {
                        'id': admin_planta.planta.planta_id,
                        'nombre': admin_planta.planta.nombre,
                        'direccion': admin_planta.planta.direccion,
                        'empresa': {
                            'id': admin_planta.planta.empresa.empresa_id,
                            'nombre': admin_planta.planta.empresa.nombre
                        }
                    }
                    data['empresa'] = data['planta']['empresa']  # Para compatibilidad
                except AdminPlanta.DoesNotExist:
                    data['planta'] = None
                    data['empresa'] = None
            else:
                data['empresa'] = None
                
        except PerfilUsuario.DoesNotExist:
            data['perfil'] = None
            data['empresa'] = None
            
        # El modelo Empleado actual no tiene relación con User
        data['empleado'] = None
            
        return Response(data)

    @action(detail=False, methods=['get'])
    def evaluaciones_disponibles(self, request):
        """Obtener evaluaciones disponibles para el usuario"""
        user = request.user
        
        # Verificar si el usuario tiene empresa a través de PerfilUsuario
        try:
            perfil = PerfilUsuario.objects.get(correo=user.email)
            empresa = Empresa.objects.get(administrador=perfil)
            # Obtener todas las evaluaciones de la empresa
            evaluaciones = EvaluacionCompleta.objects.filter(empresa=empresa)
        except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
            # Si no tiene empresa, mostrar evaluaciones públicas
            evaluaciones = EvaluacionCompleta.objects.filter(empresa__isnull=True)
        
        serializer = EvaluacionSerializer(evaluaciones, many=True)
        return Response(serializer.data)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar empresas según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Empresa.objects.all()
        else:
            try:
                # Filtrar por el perfil del usuario
                perfil = PerfilUsuario.objects.get(correo=user.email)
                return Empresa.objects.filter(administrador=perfil)
            except PerfilUsuario.DoesNotExist:
                return Empresa.objects.none()

    @action(detail=True, methods=['get'])
    def empleados(self, request, pk=None):
        """Obtener empleados de una empresa"""
        empresa = self.get_object()
        # El modelo Empleado tiene una relación con planta, no directamente con empresa
        # Buscar empleados a través de las plantas de la empresa
        empleados = Empleado.objects.filter(planta__empresa=empresa)
        data = []
        for empleado in empleados:
            data.append({
                'id': empleado.empleado_id,
                'nombre': f"{empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno or ''}".strip(),
                'departamento': empleado.departamento.nombre if empleado.departamento else None,
                'puesto': empleado.puesto.nombre if empleado.puesto else None,
                'planta': empleado.planta.nombre if empleado.planta else None,
                'status': empleado.status
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
                'suscripciones_activas': SuscripcionEmpresa.objects.filter(status=True, estado='ACTIVA').count(),
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
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar empleados según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Empleado.objects.all()
        else:
            try:
                # Filtrar empleados a través del perfil de usuario y empresa
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                return Empleado.objects.filter(planta__empresa=empresa)
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                return Empleado.objects.none()

    @action(detail=False, methods=['get'])
    def mis_evaluaciones(self, request):
        """Obtener evaluaciones asignadas al empleado actual"""
        user = request.user
        # Nota: El modelo Empleado actual no tiene relación directa con User
        # Esta funcionalidad requeriría una estructura diferente
        return Response({
            'message': 'Funcionalidad no disponible - el modelo Empleado no tiene relación con User',
            'evaluaciones': []
        })


class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar plantas según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Planta.objects.all()
        else:
            try:
                # Filtrar plantas de la empresa del usuario
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                return Planta.objects.filter(empresa=empresa)
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                return Planta.objects.none()

    def perform_create(self, serializer):
        """Asignar automáticamente la empresa del usuario actual y crear usuario de planta"""
        import secrets
        import string
        from django.contrib.auth.hashers import make_password
        
        user = self.request.user
        if user.is_superuser:
            # Si es superuser, puede especificar la empresa o crearla sin empresa
            planta = serializer.save()
        else:
            try:
                # Asignar la empresa del usuario actual
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                planta = serializer.save(empresa=empresa)
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                raise ValidationError("No se puede determinar la empresa del usuario")
        
        # Crear automáticamente un usuario de planta
        try:
            # Generar correo y contraseña automáticos
            planta_nombre_clean = ''.join(c.lower() for c in planta.nombre if c.isalnum())
            correo_planta = f"planta_{planta_nombre_clean}_{planta.planta_id}@{planta.empresa.nombre.lower().replace(' ', '')}.com"
            
            # Generar contraseña temporal
            password_temporal = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
            
            print(f"Creando usuario de planta: {correo_planta}")
            
            # Crear User de Django para el login
            user_django = User.objects.create_user(
                username=correo_planta,
                email=correo_planta,
                password=password_temporal,
                first_name=f"Admin {planta.nombre}",
                last_name="Planta"
            )
            print(f"User Django creado: ID {user_django.id}")
            
            # Crear PerfilUsuario para la planta (sin password_hash ya que va en User)
            perfil_planta = PerfilUsuario.objects.create(
                nombre=f"Admin {planta.nombre}",
                apellido_paterno="Planta",
                apellido_materno="",
                correo=correo_planta,
                nivel_usuario="admin_planta",
                status=True,
                user=user_django  # Relación con User de Django
            )
            print(f"PerfilUsuario creado: ID {perfil_planta.id}")
            
            # Crear AdminPlanta
            admin_planta = AdminPlanta.objects.create(
                usuario=perfil_planta,
                planta=planta,
                status=True,
                password_temporal=password_temporal
            )
            print(f"AdminPlanta creado: ID {admin_planta.id}")
            
            # Guardar las credenciales en el objeto planta para incluirlas en la respuesta
            planta._credenciales_usuario = {
                'usuario': correo_planta,
                'password': password_temporal,
                'admin_planta_id': admin_planta.id
            }
            
            print(f"✅ Usuario de planta creado exitosamente: {correo_planta} / {password_temporal}")
            
        except Exception as e:
            print(f"❌ Error creando usuario de planta: {e}")
            import traceback
            traceback.print_exc()
            # No fallar la creación de la planta si hay error con el usuario
    
    def create(self, request, *args, **kwargs):
        """Override create para incluir credenciales en la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Obtener la respuesta normal
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        
        # Agregar credenciales si existen
        if hasattr(serializer.instance, '_credenciales_usuario'):
            response_data['credenciales_usuario_planta'] = serializer.instance._credenciales_usuario
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def usuarios_planta(self, request):
        """Obtener usuarios asignados a plantas"""
        user = request.user
        try:
            if user.is_superuser:
                # Superuser ve todos los usuarios de planta
                admin_plantas = AdminPlanta.objects.filter(status=True).select_related('usuario', 'planta', 'planta__empresa')
            else:
                # Usuario normal ve solo los de su empresa
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                admin_plantas = AdminPlanta.objects.filter(
                    planta__empresa=empresa, 
                    status=True
                ).select_related('usuario', 'planta')
            
            data = []
            for admin_planta in admin_plantas:
                data.append({
                    'id': admin_planta.id,
                    'usuario': {
                        'id': admin_planta.usuario.id,
                        'nombre': admin_planta.usuario.nombre,
                        'apellido_paterno': admin_planta.usuario.apellido_paterno,
                        'apellido_materno': admin_planta.usuario.apellido_materno,
                        'correo': admin_planta.usuario.correo,
                        'nivel_usuario': admin_planta.usuario.nivel_usuario,
                        'status': admin_planta.usuario.status
                    },
                    'planta': {
                        'id': admin_planta.planta.planta_id,
                        'nombre': admin_planta.planta.nombre,
                        'direccion': admin_planta.planta.direccion
                    },
                    'fecha_asignacion': admin_planta.fecha_asignacion,
                    'status': admin_planta.status,
                    'tiene_password_temporal': bool(admin_planta.password_temporal),
                    'credenciales': {
                        'usuario': admin_planta.usuario.correo,
                        'password': admin_planta.password_temporal
                    } if admin_planta.password_temporal else None
                })
            
            return Response(data)
        except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
            return Response([])

    @action(detail=True, methods=['post'])
    def regenerar_password(self, request, pk=None):
        """Regenerar contraseña para un usuario de planta específico"""
        import secrets
        import string
        
        try:
            planta = self.get_object()
            user = request.user
            
            # Verificar permisos
            if not user.is_superuser:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                if planta.empresa != empresa:
                    return Response(
                        {'error': 'No tiene permisos para regenerar contraseña de esta planta'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Buscar el AdminPlanta
            admin_planta = AdminPlanta.objects.get(planta=planta, status=True)
            
            # Generar nueva contraseña
            nueva_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
            
            # Actualizar en Django User
            django_user = admin_planta.usuario.user
            django_user.set_password(nueva_password)
            django_user.save()
            
            # Actualizar password temporal en AdminPlanta
            admin_planta.password_temporal = nueva_password
            admin_planta.save()
            
            return Response({
                'message': 'Contraseña regenerada exitosamente',
                'nuevas_credenciales': {
                    'usuario': admin_planta.usuario.correo,
                    'password': nueva_password
                }
            })
            
        except Planta.DoesNotExist:
            return Response({'error': 'Planta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except AdminPlanta.DoesNotExist:
            return Response({'error': 'Usuario de planta no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
            return Response({'error': 'No se puede verificar permisos'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar departamentos según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Departamento.objects.all()
        else:
            try:
                # Filtrar departamentos de plantas de la empresa del usuario
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                return Departamento.objects.filter(planta__empresa=empresa)
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                return Departamento.objects.none()

    def perform_create(self, serializer):
        """Validar que la planta pertenezca a la empresa del usuario"""
        user = self.request.user
        if not user.is_superuser:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                # Verificar que la planta especificada pertenezca a la empresa del usuario
                planta_id = serializer.validated_data.get('planta')
                if planta_id and planta_id.empresa != empresa:
                    raise ValidationError("La planta especificada no pertenece a su empresa")
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                raise ValidationError("No se puede determinar la empresa del usuario")
        serializer.save()


class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar puestos según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Puesto.objects.all()
        else:
            try:
                # Filtrar puestos de departamentos de plantas de la empresa del usuario
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                return Puesto.objects.filter(departamento__planta__empresa=empresa)
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                return Puesto.objects.none()

    def perform_create(self, serializer):
        """Validar que el departamento pertenezca a la empresa del usuario"""
        user = self.request.user
        if not user.is_superuser:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresa = Empresa.objects.get(administrador=perfil)
                # Verificar que el departamento especificado pertenezca a la empresa del usuario
                departamento = serializer.validated_data.get('departamento')
                if departamento and departamento.planta.empresa != empresa:
                    raise ValidationError("El departamento especificado no pertenece a su empresa")
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist):
                raise ValidationError("No se puede determinar la empresa del usuario")
        serializer.save()
