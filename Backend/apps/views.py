from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado
from .serializers import (
    LoginSerializer, EmpresaRegistroSerializer,
    PlantaSerializer, PlantaCreateSerializer,
    DepartamentoSerializer, DepartamentoCreateSerializer,
    PuestoSerializer, PuestoCreateSerializer,
    EmpleadoSerializer, EmpleadoCreateSerializer
)

@method_decorator(csrf_exempt, name='dispatch')
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user and hasattr(user, 'perfil'):
                profile = user.perfil
                
                # Obtener o crear token para el usuario
                token, created = Token.objects.get_or_create(user=user)
                
                # Respuesta base
                response_data = {
                    'message': 'Login exitoso',
                    'token': token.key,  # Agregar token a la respuesta
                    'usuario': user.username,
                    'user_id': user.id,
                    'profile_id': profile.id,
                    'nombre_completo': f"{profile.nombre} {profile.apellido_paterno}",
                    'nivel_usuario': profile.nivel_usuario,
                    'correo': profile.correo
                }
                
                # Datos específicos según el tipo de usuario
                if profile.nivel_usuario == 'superadmin':
                    # SuperAdmin: acceso a todo el sistema
                    response_data.update({
                        'tipo_dashboard': 'superadmin',
                        'permisos': ['ver_todas_empresas', 'gestionar_usuarios', 'configuracion_sistema']
                    })
                    
                elif profile.nivel_usuario == 'admin-empresa':
                    # Admin de Empresa: gestión de su empresa
                    try:
                        empresa = Empresa.objects.get(administrador=profile)
                        response_data.update({
                            'tipo_dashboard': 'admin-empresa',
                            'empresa_id': empresa.empresa_id,
                            'nombre_empresa': empresa.nombre,
                            'permisos': ['gestionar_estructura', 'gestionar_empleados', 'ver_evaluaciones']
                        })
                    except Empresa.DoesNotExist:
                        return Response({'error': 'Usuario sin empresa asignada'}, 
                                      status=status.HTTP_400_BAD_REQUEST)
                        
                elif profile.nivel_usuario == 'admin-planta':
                    # Admin de Planta: gestión de plantas específicas
                    response_data.update({
                        'tipo_dashboard': 'admin-planta',
                        'permisos': ['gestionar_empleados_planta', 'ver_evaluaciones_planta']
                    })
                    # Aquí podrías agregar lógica para obtener las plantas asignadas
                    
                return Response(response_data)
            else:
                return Response({'error': 'Credenciales inválidas'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class EmpresaViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def registro(self, request):
        serializer = EmpresaRegistroSerializer(data=request.data)
        if serializer.is_valid():
            empresa = serializer.save()
            return Response({
                'message': 'Empresa registrada exitosamente',
                'empresa_id': empresa.empresa_id,
                'nombre': empresa.nombre
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Empleado.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmpleadoCreateSerializer
        return EmpleadoSerializer
    
    @action(detail=False, methods=['get'])
    def plantas_disponibles(self, request):
        plantas = Planta.objects.all()
        serializer = PlantaSerializer(plantas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def departamentos_disponibles(self, request):
        departamentos = Departamento.objects.all()
        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def puestos_disponibles(self, request):
        puestos = Puesto.objects.all()
        serializer = PuestoSerializer(puestos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def departamentos_por_planta(self, request):
        planta_id = request.query_params.get('planta_id')
        if planta_id:
            departamentos = Departamento.objects.filter(planta_id=planta_id)
            serializer = DepartamentoSerializer(departamentos, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def puestos_por_departamento(self, request):
        departamento_id = request.query_params.get('departamento_id')
        if departamento_id:
            puestos = Puesto.objects.filter(departamento_id=departamento_id)
            serializer = PuestoSerializer(puestos, many=True)
            return Response(serializer.data)
        return Response([])

@method_decorator(csrf_exempt, name='dispatch')
class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlantaCreateSerializer
        return PlantaSerializer
    
    def get_queryset(self):
        # Filtrar plantas por empresa del usuario logueado
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    return Planta.objects.filter(empresa=empresa, status=True)
                except Empresa.DoesNotExist:
                    return Planta.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                # Superadmin puede ver todas las plantas
                return Planta.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                # Admin de planta solo ve sus plantas asignadas
                from apps.users.models import AdminPlanta
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                return Planta.objects.filter(planta_id__in=plantas_ids, status=True)
        
        return Planta.objects.none()
    
    def perform_create(self, serializer):
        # Asignar automáticamente la empresa del admin logueado
        user = self.request.user
        if not hasattr(user, 'perfil'):
            raise ValidationError("Usuario sin perfil")
            
        if user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                
                # Verificar que no se excedan las 5 plantas por empresa
                plantas_existentes = Planta.objects.filter(empresa=empresa, status=True).count()
                if plantas_existentes >= 5:
                    raise ValidationError("No se pueden crear más de 5 plantas por empresa")
                
                # Crear la planta
                planta = serializer.save(empresa=empresa)
                
                # Crear usuario automático para la planta
                self._crear_usuario_planta(planta)
                
            except Empresa.DoesNotExist:
                raise ValidationError("Usuario sin empresa asignada")
        elif user.perfil.nivel_usuario == 'superadmin':
            # Superadmin puede crear plantas para cualquier empresa
            # Por ahora, necesita especificar empresa_id en los datos
            raise ValidationError("Funcionalidad de superadmin pendiente")
        else:
            raise ValidationError("Usuario sin permisos para crear plantas")
    
    def _crear_usuario_planta(self, planta):
        """Crea automáticamente un usuario administrador para la planta"""
        from django.contrib.auth.models import User
        import random
        import string
        
        # Generar username único basado en el nombre de la planta
        base_username = f"admin_planta_{planta.planta_id}"
        username = base_username.lower().replace(' ', '_')[:30]  # Límite de 30 caracteres
        
        # Asegurar que el username sea único
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"[:30]
            counter += 1
        
        # Generar contraseña temporal
        password_chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(password_chars) for _ in range(12))
        
        try:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=f"admin.planta.{planta.planta_id}@{planta.empresa.nombre.lower().replace(' ', '')}.com",
                password=password,
                first_name=f"Admin",
                last_name=f"Planta {planta.nombre}"
            )
            
            # Crear perfil de usuario
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre="Admin",
                apellido_paterno="Planta",
                apellido_materno=planta.nombre,
                correo=user.email,
                nivel_usuario='admin-planta'
            )
            
            # Crear relación AdminPlanta
            try:
                AdminPlanta.objects.create(
                    usuario=perfil,
                    planta=planta,
                    password_temporal=password  # Guardar la contraseña temporal
                )
            except Exception:
                # Si falla por el campo password_temporal, crear sin él
                AdminPlanta.objects.create(
                    usuario=perfil,
                    planta=planta
                )
            
            # Log de credenciales (en producción esto debería enviarse por email)
            print(f"\n{'='*50}")
            print(f"NUEVO USUARIO DE PLANTA CREADO")
            print(f"{'='*50}")
            print(f"Planta: {planta.nombre}")
            print(f"Usuario: {username}")
            print(f"Contraseña: {password}")
            print(f"Email: {user.email}")
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"Error creando usuario de planta: {str(e)}")
            # No fallar la creación de la planta por esto
            pass

@method_decorator(csrf_exempt, name='dispatch')
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DepartamentoCreateSerializer
        return DepartamentoSerializer
    
    def get_queryset(self):
        # Filtrar departamentos por plantas del usuario
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    plantas = Planta.objects.filter(empresa=empresa)
                    return Departamento.objects.filter(planta__in=plantas)
                except Empresa.DoesNotExist:
                    return Departamento.objects.none()
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas = [ap.planta for ap in admin_plantas]
                return Departamento.objects.filter(planta__in=plantas)
        return Departamento.objects.all()
    
    def perform_create(self, serializer):
        # Validar que el usuario tenga acceso a la planta especificada
        user = self.request.user
        planta_id = serializer.validated_data.get('planta_id')
        
        if not planta_id:
            raise ValidationError("Debe especificar planta_id")
        
        try:
            planta = Planta.objects.get(planta_id=planta_id)
        except Planta.DoesNotExist:
            raise ValidationError("Planta no encontrada")
        
        # Verificar que el usuario tenga acceso a esta planta
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    if planta.empresa != empresa:
                        raise ValidationError("No tiene acceso a esta planta")
                except Empresa.DoesNotExist:
                    raise ValidationError("Usuario sin empresa asignada")
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil, planta=planta)
                if not admin_plantas.exists():
                    raise ValidationError("No tiene acceso a esta planta")
        
        # Crear el departamento y asegurar que se guarde correctamente
        departamento = serializer.save()
        return departamento
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        departamento = self.perform_create(serializer)
        
        # Usar el serializer de lectura para la respuesta
        response_serializer = DepartamentoSerializer(departamento)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PuestoCreateSerializer
        return PuestoSerializer
    
    def get_queryset(self):
        # Filtrar puestos por departamentos del usuario
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    plantas = Planta.objects.filter(empresa=empresa)
                    departamentos = Departamento.objects.filter(planta__in=plantas)
                    return Puesto.objects.filter(departamento__in=departamentos)
                except Empresa.DoesNotExist:
                    return Puesto.objects.none()
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas = [ap.planta for ap in admin_plantas]
                departamentos = Departamento.objects.filter(planta__in=plantas)
                return Puesto.objects.filter(departamento__in=departamentos)
        return Puesto.objects.all()
    
    def perform_create(self, serializer):
        # Validar que el usuario tenga acceso al departamento especificado
        user = self.request.user
        departamento_id = serializer.validated_data.get('departamento_id')
        
        if not departamento_id:
            raise ValidationError("Debe especificar departamento_id")
        
        try:
            departamento = Departamento.objects.get(departamento_id=departamento_id)
        except Departamento.DoesNotExist:
            raise ValidationError("Departamento no encontrado")
        
        # Verificar que el usuario tenga acceso a este departamento
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    if departamento.planta.empresa != empresa:
                        raise ValidationError("No tiene acceso a este departamento")
                except Empresa.DoesNotExist:
                    raise ValidationError("Usuario sin empresa asignada")
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil, planta=departamento.planta)
                if not admin_plantas.exists():
                    raise ValidationError("No tiene acceso a este departamento")
        
        # Crear el puesto y asegurar que se guarde correctamente
        puesto = serializer.save()
        return puesto
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        puesto = self.perform_create(serializer)
        
        # Usar el serializer de lectura para la respuesta
        response_serializer = PuestoSerializer(puesto)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')  
class EstructuraViewSet(viewsets.ViewSet):
    """ViewSet para obtener la estructura organizacional completa"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def mi_estructura(self, request):
        """Obtiene la estructura organizacional del usuario autenticado"""
        user = request.user
        if not hasattr(user, 'perfil'):
            return Response({'error': 'Usuario sin perfil'}, status=400)
        
        perfil = user.perfil
        
        if perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=perfil)
                plantas = Planta.objects.filter(empresa=empresa)
                
                estructura = {
                    'empresa': {
                        'id': empresa.empresa_id,
                        'nombre': empresa.nombre,
                        'rfc': empresa.rfc
                    },
                    'plantas': []
                }
                
                for planta in plantas:
                    departamentos = Departamento.objects.filter(planta=planta)
                    planta_data = {
                        'id': planta.planta_id,
                        'nombre': planta.nombre,
                        'direccion': planta.direccion,
                        'departamentos': []
                    }
                    
                    for depto in departamentos:
                        puestos = Puesto.objects.filter(departamento=depto)
                        empleados = Empleado.objects.filter(departamento=depto)
                        
                        depto_data = {
                            'id': depto.departamento_id,
                            'nombre': depto.nombre,
                            'descripcion': depto.descripcion,
                            'puestos': [{'id': p.puesto_id, 'nombre': p.nombre, 'descripcion': p.descripcion} for p in puestos],
                            'empleados_count': empleados.count()
                        }
                        planta_data['departamentos'].append(depto_data)
                    
                    estructura['plantas'].append(planta_data)
                
                return Response(estructura)
                
            except Empresa.DoesNotExist:
                return Response({'error': 'Usuario sin empresa asignada'}, status=400)
        
        return Response({'error': 'Tipo de usuario no soportado'}, status=400)
    
    @action(detail=False, methods=['get'])
    def usuarios_planta(self, request):
        """Obtener usuarios de planta para la empresa del admin logueado"""
        user = self.request.user
        if not hasattr(user, 'perfil'):
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                plantas = Planta.objects.filter(empresa=empresa, status=True)
                
                usuarios_planta = []
                for planta in plantas:
                    admin_planta = AdminPlanta.objects.filter(planta=planta).first()
                    if admin_planta:
                        usuario = admin_planta.usuario.user
                        usuarios_planta.append({
                            'planta_id': planta.planta_id,
                            'planta_nombre': planta.nombre,
                            'usuario_id': usuario.id,
                            'username': usuario.username,
                            'email': usuario.email,
                            'nombre_completo': f"{usuario.first_name} {usuario.last_name}",
                            'fecha_creacion': admin_planta.fecha_asignacion,
                            'status': admin_planta.status,
                            'password_temporal': getattr(admin_planta, 'password_temporal', f'temp{planta.planta_id}Pass123')  # Temporal
                        })
                    else:
                        usuarios_planta.append({
                            'planta_id': planta.planta_id,
                            'planta_nombre': planta.nombre,
                            'usuario_id': None,
                            'username': None,
                            'email': None,
                            'nombre_completo': None,
                            'fecha_creacion': None,
                            'status': False,
                            'password_temporal': None
                        })
                
                return Response(usuarios_planta, status=status.HTTP_200_OK)
                
            except Empresa.DoesNotExist:
                return Response({'error': 'Usuario sin empresa asignada'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuario sin permisos'}, 
                          status=status.HTTP_403_FORBIDDEN)