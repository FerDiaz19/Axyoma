from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado
from apps.subscriptions.models import SuscripcionEmpresa
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
    
    def get_subscription_info(self, empresa):
        """Obtiene información de suscripción - NUEVA LÓGICA"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa
            from django.utils import timezone
            
            # Buscar suscripción activa de la empresa
            suscripcion = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                status=True
            ).first()
            
            if not suscripcion:
                return {
                    'tiene_suscripcion': False,
                    'estado': 'sin_suscripcion',
                    'mensaje': 'No tiene suscripción activa. Seleccione un plan para acceder a reportes.',
                    'requiere_pago': True,
                    'dias_restantes': 0,
                    'acceso_reportes': False
                }
            
            # Verificar si está vencida
            if suscripcion.fecha_fin < timezone.now().date():
                # Marcar como vencida
                suscripcion.estado = 'Vencida'
                suscripcion.save()
                
                return {
                    'tiene_suscripcion': False,
                    'estado': 'vencida',
                    'mensaje': 'Su suscripción ha vencido. Renueve para acceder a reportes.',
                    'requiere_pago': True,
                    'dias_restantes': 0,
                    'acceso_reportes': False
                }
            
            # Suscripción activa
            dias_restantes = (suscripcion.fecha_fin - timezone.now().date()).days
            
            return {
                'tiene_suscripcion': True,
                'estado': 'activa',
                'plan_nombre': suscripcion.plan_suscripcion.nombre,
                'fecha_inicio': suscripcion.fecha_inicio.isoformat(),
                'fecha_fin': suscripcion.fecha_fin.isoformat(),
                'dias_restantes': dias_restantes,
                'esta_por_vencer': dias_restantes <= 7,
                'precio': float(suscripcion.plan_suscripcion.precio),
                'duracion': suscripcion.plan_suscripcion.duracion,
                'requiere_pago': False,
                'acceso_reportes': True
            }
            
        except Exception as e:
            print(f"Error getting subscription info: {str(e)}")
            return {
                'tiene_suscripcion': False,
                'estado': 'error',
                'mensaje': f'Error al obtener información de suscripción: {str(e)}',
                'requiere_pago': True,
                'dias_restantes': 0,
                'acceso_reportes': False
            }
    
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
                        
                        # Obtener información de suscripción
                        suscripcion_info = self.get_subscription_info(empresa)
                        
                        response_data.update({
                            'tipo_dashboard': 'admin-empresa',
                            'empresa_id': empresa.empresa_id,
                            'nombre_empresa': empresa.nombre,
                            'empresa_suspendida': not empresa.status,
                            'suscripcion': suscripcion_info,
                            'permisos': ['gestionar_estructura', 'gestionar_empleados', 'ver_evaluaciones']
                        })
                        
                        # Configurar advertencias según el estado de suscripción
                        if not empresa.status:
                            response_data['advertencia'] = {
                                'tipo': 'empresa_suspendida',
                                'mensaje': 'Su empresa se encuentra suspendida. Las funcionalidades están limitadas.',
                                'detalles': 'Para reactivar su suscripción, contacte con soporte.'
                            }
                        elif not suscripcion_info['tiene_suscripcion']:
                            if suscripcion_info['estado'] == 'sin_suscripcion':
                                response_data['advertencia'] = {
                                    'tipo': 'sin_suscripcion',
                                    'mensaje': 'Su empresa no tiene una suscripción activa.',
                                    'detalles': 'Active una suscripción para acceder a todas las funcionalidades.',
                                    'requiere_accion': True
                                }
                            elif suscripcion_info['estado'] == 'vencida':
                                response_data['advertencia'] = {
                                    'tipo': 'suscripcion_vencida',
                                    'mensaje': suscripcion_info['mensaje'],
                                    'detalles': 'Renueve su suscripción para continuar usando el sistema.',
                                    'requiere_accion': True
                                }
                        elif suscripcion_info.get('requiere_renovacion'):
                            response_data['advertencia'] = {
                                'tipo': 'suscripcion_por_vencer',
                                'mensaje': suscripcion_info['mensaje'],
                                'detalles': 'Renueve su suscripción antes de que venza.',
                                'requiere_accion': False
                            }
                            
                    except Empresa.DoesNotExist:
                        return Response({'error': 'Usuario sin empresa asignada'}, 
                                      status=status.HTTP_400_BAD_REQUEST)
                        
                elif profile.nivel_usuario == 'admin-planta':
                    # Admin de Planta: gestión de plantas específicas
                    try:
                        admin_planta = AdminPlanta.objects.get(usuario=profile, status=True)
                        planta = admin_planta.planta
                        empresa_suspendida = not planta.empresa.status
                        
                        # Obtener información de suscripción de la empresa
                        suscripcion_info = self.get_subscription_info(planta.empresa)
                        
                        response_data.update({
                            'tipo_dashboard': 'admin-planta',
                            'planta_id': planta.planta_id,
                            'nombre_planta': planta.nombre,
                            'empresa_id': planta.empresa.empresa_id,
                            'nombre_empresa': planta.empresa.nombre,
                            'empresa_suspendida': empresa_suspendida,
                            'suscripcion': suscripcion_info,
                            'permisos': ['gestionar_empleados_planta', 'ver_evaluaciones_planta']
                        })
                        
                        # Configurar advertencias
                        if empresa_suspendida:
                            response_data['advertencia'] = {
                                'tipo': 'empresa_suspendida',
                                'mensaje': 'La empresa se encuentra suspendida. Las funcionalidades están limitadas.',
                                'detalles': 'Para reactivar su suscripción, contacte con soporte.'
                            }
                        elif not suscripcion_info['tiene_suscripcion']:
                            response_data['advertencia'] = {
                                'tipo': 'sin_suscripcion_planta',
                                'mensaje': suscripcion_info['mensaje'],
                                'detalles': 'Contacte al administrador de su empresa para activar la suscripción.'
                            }
                            
                    except AdminPlanta.DoesNotExist:
                        return Response({'error': 'Usuario sin planta asignada'}, 
                                      status=status.HTTP_400_BAD_REQUEST)
                    
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
                'nombre': empresa.nombre,
                'siguiente_paso': 'seleccionar_plan',
                'mensaje_siguiente': 'Para completar el registro, selecciona un plan de suscripción.',
                'requiere_suscripcion': True
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar empleados por empresa del usuario logueado
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    # Obtener empleados de todas las plantas de esta empresa
                    plantas_empresa = Planta.objects.filter(empresa=empresa, status=True)
                    return Empleado.objects.filter(planta__in=plantas_empresa, status=True)
                except Empresa.DoesNotExist:
                    return Empleado.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                # Superadmin puede ver todos los empleados
                return Empleado.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                # Admin de planta solo ve empleados de sus plantas asignadas
                from apps.users.models import AdminPlanta
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                return Empleado.objects.filter(planta__planta_id__in=plantas_ids, status=True)
        
        return Empleado.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmpleadoCreateSerializer
        return EmpleadoSerializer
    
    @action(detail=False, methods=['get'])
    def plantas_disponibles(self, request):
        # Filtrar plantas por empresa del usuario logueado
        user = request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    plantas = Planta.objects.filter(empresa=empresa, status=True)
                except Empresa.DoesNotExist:
                    plantas = Planta.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                plantas = Planta.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                from apps.users.models import AdminPlanta
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                plantas = Planta.objects.filter(planta_id__in=plantas_ids, status=True)
            else:
                plantas = Planta.objects.none()
        else:
            plantas = Planta.objects.none()
            
        serializer = PlantaSerializer(plantas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def departamentos_disponibles(self, request):
        # Filtrar departamentos por empresa del usuario logueado
        user = request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    plantas_empresa = Planta.objects.filter(empresa=empresa, status=True)
                    departamentos = Departamento.objects.filter(planta__in=plantas_empresa, status=True)
                except Empresa.DoesNotExist:
                    departamentos = Departamento.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                departamentos = Departamento.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                from apps.users.models import AdminPlanta
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                departamentos = Departamento.objects.filter(planta__planta_id__in=plantas_ids, status=True)
            else:
                departamentos = Departamento.objects.none()
        else:
            departamentos = Departamento.objects.none()
            
        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def puestos_disponibles(self, request):
        # Filtrar puestos por empresa del usuario logueado
        user = request.user
        if hasattr(user, 'perfil'):
            if user.perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=user.perfil)
                    plantas_empresa = Planta.objects.filter(empresa=empresa, status=True)
                    departamentos_empresa = Departamento.objects.filter(planta__in=plantas_empresa, status=True)
                    puestos = Puesto.objects.filter(departamento__in=departamentos_empresa, status=True)
                except Empresa.DoesNotExist:
                    puestos = Puesto.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                puestos = Puesto.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                from apps.users.models import AdminPlanta
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                departamentos_planta = Departamento.objects.filter(planta__planta_id__in=plantas_ids, status=True)
                puestos = Puesto.objects.filter(departamento__in=departamentos_planta, status=True)
            else:
                puestos = Puesto.objects.none()
        else:
            puestos = Puesto.objects.none()
            
        serializer = PuestoSerializer(puestos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def departamentos_por_planta(self, request):
        planta_id = request.query_params.get('planta_id')
        if planta_id:
            # Verificar que el usuario tenga acceso a esta planta
            user = request.user
            if hasattr(user, 'perfil'):
                if user.perfil.nivel_usuario == 'admin-empresa':
                    try:
                        empresa = Empresa.objects.get(administrador=user.perfil)
                        planta = Planta.objects.get(planta_id=planta_id, empresa=empresa, status=True)
                        departamentos = Departamento.objects.filter(planta=planta, status=True)
                    except (Empresa.DoesNotExist, Planta.DoesNotExist):
                        return Response([])
                elif user.perfil.nivel_usuario == 'superadmin':
                    departamentos = Departamento.objects.filter(planta_id=planta_id, status=True)
                elif user.perfil.nivel_usuario == 'admin-planta':
                    from apps.users.models import AdminPlanta
                    admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                    plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                    if int(planta_id) in plantas_ids:
                        departamentos = Departamento.objects.filter(planta_id=planta_id, status=True)
                    else:
                        return Response([])
                else:
                    return Response([])
            else:
                return Response([])
                
            serializer = DepartamentoSerializer(departamentos, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def puestos_por_departamento(self, request):
        departamento_id = request.query_params.get('departamento_id')
        if departamento_id:
            # Verificar que el usuario tenga acceso a este departamento
            user = request.user
            if hasattr(user, 'perfil'):
                if user.perfil.nivel_usuario == 'admin-empresa':
                    try:
                        empresa = Empresa.objects.get(administrador=user.perfil)
                        plantas_empresa = Planta.objects.filter(empresa=empresa, status=True)
                        departamento = Departamento.objects.get(departamento_id=departamento_id, planta__in=plantas_empresa, status=True)
                        puestos = Puesto.objects.filter(departamento=departamento, status=True)
                    except (Empresa.DoesNotExist, Departamento.DoesNotExist):
                        return Response([])
                elif user.perfil.nivel_usuario == 'superadmin':
                    puestos = Puesto.objects.filter(departamento_id=departamento_id, status=True)
                elif user.perfil.nivel_usuario == 'admin-planta':
                    from apps.users.models import AdminPlanta
                    admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                    plantas_ids = [ap.planta.planta_id for ap in admin_plantas]
                    try:
                        departamento = Departamento.objects.get(departamento_id=departamento_id, planta__planta_id__in=plantas_ids, status=True)
                        puestos = Puesto.objects.filter(departamento=departamento, status=True)
                    except Departamento.DoesNotExist:
                        return Response([])
                else:
                    return Response([])
            else:
                return Response([])
                
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
                    plantas = Planta.objects.filter(empresa=empresa, status=True)
                    return Departamento.objects.filter(planta__in=plantas, status=True)
                except Empresa.DoesNotExist:
                    return Departamento.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                return Departamento.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas = [ap.planta for ap in admin_plantas]
                return Departamento.objects.filter(planta__in=plantas, status=True)
        return Departamento.objects.none()
    
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
                    plantas_empresa = Planta.objects.filter(empresa=empresa, status=True)
                    departamentos_empresa = Departamento.objects.filter(planta__in=plantas_empresa, status=True)
                    return Puesto.objects.filter(departamento__in=departamentos_empresa, status=True)
                except Empresa.DoesNotExist:
                    return Puesto.objects.none()
            elif user.perfil.nivel_usuario == 'superadmin':
                return Puesto.objects.filter(status=True)
            elif user.perfil.nivel_usuario == 'admin-planta':
                admin_plantas = AdminPlanta.objects.filter(usuario=user.perfil)
                plantas = [ap.planta for ap in admin_plantas]
                departamentos = Departamento.objects.filter(planta__in=plantas, status=True)
                return Puesto.objects.filter(departamento__in=departamentos, status=True)
        return Puesto.objects.none()
    
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
    
    def perform_update(self, serializer):
        # Validar que el usuario tenga acceso al departamento especificado para la actualización
        user = self.request.user
        departamento_id = serializer.validated_data.get('departamento_id')
        
        if departamento_id:
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
        
        # Actualizar el puesto
        puesto = serializer.save()
        return puesto
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        puesto = self.perform_update(serializer)
        
        # Usar el serializer de lectura para la respuesta
        response_serializer = PuestoSerializer(puesto)
        return Response(response_serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

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

@method_decorator(csrf_exempt, name='dispatch')  
class SuperAdminViewSet(viewsets.ViewSet):
    """ViewSet para funcionalidades exclusivas del SuperAdmin"""
    permission_classes = [IsAuthenticated]
    
    def _verify_superadmin(self, user):
        """Verificar que el usuario es SuperAdmin"""
        if not hasattr(user, 'perfil') or user.perfil.nivel_usuario != 'superadmin':
            raise ValidationError("Usuario sin permisos de SuperAdmin")
    
    @action(detail=False, methods=['get'])
    def estadisticas_sistema(self, request):
        """Obtener estadísticas generales del sistema"""
        self._verify_superadmin(request.user)
        
        estadisticas = {
            'total_empresas': Empresa.objects.count(),
            'empresas_activas': Empresa.objects.filter(status=True).count(),
            'total_plantas': Planta.objects.count(),
            'plantas_activas': Planta.objects.filter(status=True).count(),
            'total_departamentos': Departamento.objects.count(),
            'departamentos_activos': Departamento.objects.filter(status=True).count(),
            'total_puestos': Puesto.objects.count(),
            'puestos_activos': Puesto.objects.filter(status=True).count(),
            'total_empleados': Empleado.objects.count(),
            'empleados_activos': Empleado.objects.filter(status=True).count(),
            'total_usuarios': PerfilUsuario.objects.count(),
            'usuarios_por_nivel': {
                'superadmin': PerfilUsuario.objects.filter(nivel_usuario='superadmin').count(),
                'admin-empresa': PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').count(),
                'admin-planta': PerfilUsuario.objects.filter(nivel_usuario='admin-planta').count(),
                'empleado': PerfilUsuario.objects.filter(nivel_usuario='empleado').count(),
            }
        }
        
        return Response(estadisticas)
    
    @action(detail=False, methods=['get'])
    def listar_empresas(self, request):
        """Listar todas las empresas con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        status_filter = request.query_params.get('status', '')
        
        empresas = Empresa.objects.all()
        
        if buscar:
            empresas = empresas.filter(
                nombre__icontains=buscar
            ) | empresas.filter(
                rfc__icontains=buscar
            )
        
        if status_filter:
            status_bool = status_filter.lower() == 'true'
            empresas = empresas.filter(status=status_bool)
        
        empresas_data = []
        for empresa in empresas:
            # Obtener información del administrador
            admin_info = None
            if empresa.administrador:
                admin_user = empresa.administrador.user
                admin_info = {
                    'id': admin_user.id,
                    'username': admin_user.username,
                    'email': admin_user.email,
                    'nombre_completo': f"{empresa.administrador.nombre} {empresa.administrador.apellido_paterno}",
                    'activo': admin_user.is_active
                }
            
            # Contar entidades relacionadas
            plantas_count = Planta.objects.filter(empresa=empresa).count()
            empleados_count = Empleado.objects.filter(planta__empresa=empresa).count()
            
            empresas_data.append({
                'empresa_id': empresa.empresa_id,
                'nombre': empresa.nombre,
                'rfc': empresa.rfc,
                'telefono': empresa.telefono_contacto,
                'correo': empresa.email_contacto,
                'direccion': empresa.direccion,
                'fecha_registro': empresa.fecha_registro,
                'status': empresa.status,
                'administrador': admin_info,
                'plantas_count': plantas_count,
                'empleados_count': empleados_count,
            })
        
        return Response({
            'empresas': empresas_data,
            'total': len(empresas_data)
        })
    
    @action(detail=False, methods=['post'])
    def suspender_empresa(self, request):
        """Suspender/activar una empresa y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        empresa_id = request.data.get('empresa_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not empresa_id or not accion:
            return Response({'error': 'Faltan parámetros empresa_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            nuevo_status = accion == 'activar'
            
            # Cambiar status de la empresa
            empresa.status = nuevo_status
            empresa.save()
            
            # Cambiar status de todas las plantas de la empresa
            plantas = Planta.objects.filter(empresa=empresa)
            plantas.update(status=nuevo_status)
            
            # Cambiar status de todos los departamentos de las plantas
            departamentos = Departamento.objects.filter(planta__empresa=empresa)
            departamentos.update(status=nuevo_status)
            
            # Cambiar status de todos los puestos de los departamentos
            puestos = Puesto.objects.filter(departamento__planta__empresa=empresa)
            puestos.update(status=nuevo_status)
            
            # Cambiar status de todos los empleados de las plantas
            empleados = Empleado.objects.filter(planta__empresa=empresa)
            empleados.update(status=nuevo_status)
            
            # Activar/desactivar cuenta del administrador de empresa
            if empresa.administrador:
                empresa.administrador.user.is_active = nuevo_status
                empresa.administrador.user.save()
            
            # Activar/desactivar cuentas de administradores de planta
            admin_plantas = AdminPlanta.objects.filter(planta__empresa=empresa)
            for admin_planta in admin_plantas:
                admin_planta.usuario.user.is_active = nuevo_status
                admin_planta.usuario.user.save()
                admin_planta.status = nuevo_status
                admin_planta.save()
            
            return Response({
                'message': f'Empresa {accion} exitosamente',
                'empresa_id': empresa_id,
                'nuevo_status': nuevo_status
            })
            
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['delete'])
    def eliminar_empresa(self, request):
        """Eliminar completamente una empresa y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        empresa_id = request.data.get('empresa_id')
        
        if not empresa_id:
            return Response({'error': 'Falta parámetro empresa_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            nombre_empresa = empresa.nombre
            
            # Eliminar en orden inverso para respetar las foreign keys
            
            # 1. Eliminar empleados
            empleados = Empleado.objects.filter(planta__empresa=empresa)
            empleados_count = empleados.count()
            empleados.delete()
            
            # 2. Eliminar puestos
            puestos = Puesto.objects.filter(departamento__planta__empresa=empresa)
            puestos_count = puestos.count()
            puestos.delete()
            
            # 3. Eliminar departamentos
            departamentos = Departamento.objects.filter(planta__empresa=empresa)
            departamentos_count = departamentos.count()
            departamentos.delete()
            
            # 4. Eliminar administradores de planta y sus usuarios
            admin_plantas = AdminPlanta.objects.filter(planta__empresa=empresa)
            admin_plantas_count = admin_plantas.count()
            for admin_planta in admin_plantas:
                if admin_planta.usuario.user:
                    admin_planta.usuario.user.delete()
                admin_planta.usuario.delete()
            
            # 5. Eliminar plantas
            plantas = Planta.objects.filter(empresa=empresa)
            plantas_count = plantas.count()
            plantas.delete()
            
            # 6. Eliminar administrador de empresa y su usuario
            admin_empresa = None
            if empresa.administrador:
                admin_empresa = empresa.administrador
                if admin_empresa.user:
                    admin_empresa.user.delete()
                admin_empresa.delete()
            
            # 7. Eliminar empresa
            empresa.delete()
            
            return Response({
                'message': f'Empresa "{nombre_empresa}" eliminada exitosamente',
                'entidades_eliminadas': {
                    'empresa': 1,
                    'plantas': plantas_count,
                    'departamentos': departamentos_count,
                    'puestos': puestos_count,
                    'empleados': empleados_count,
                    'admin_plantas': admin_plantas_count,
                    'admin_empresa': 1 if admin_empresa else 0
                }
            })
            
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando empresa: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def listar_usuarios(self, request):
        """Listar todos los usuarios del sistema con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        nivel_usuario = request.query_params.get('nivel_usuario', '')
        activo = request.query_params.get('activo', '')
        
        usuarios = PerfilUsuario.objects.all()
        
        if buscar:
            usuarios = usuarios.filter(
                nombre__icontains=buscar
            ) | usuarios.filter(
                apellido_paterno__icontains=buscar
            ) | usuarios.filter(
                correo__icontains=buscar
            ) | usuarios.filter(
                user__username__icontains=buscar
            )
        
        if nivel_usuario:
            usuarios = usuarios.filter(nivel_usuario=nivel_usuario)
        
        if activo:
            activo_bool = activo.lower() == 'true'
            usuarios = usuarios.filter(user__is_active=activo_bool)
        
        usuarios_data = []
        for usuario in usuarios:
            # Información de empresa/planta según el rol
            empresa_info = None
            planta_info = None
            
            if usuario.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=usuario)
                    empresa_info = {
                        'id': empresa.empresa_id,
                        'nombre': empresa.nombre,
                        'status': empresa.status
                    }
                except Empresa.DoesNotExist:
                    pass
            
            elif usuario.nivel_usuario == 'admin-planta':
                try:
                    admin_planta = AdminPlanta.objects.get(usuario=usuario)
                    planta = admin_planta.planta
                    planta_info = {
                        'id': planta.planta_id,
                        'nombre': planta.nombre,
                        'empresa_nombre': planta.empresa.nombre,
                        'status': admin_planta.status
                    }
                except AdminPlanta.DoesNotExist:
                    pass
            
            usuarios_data.append({
                'user_id': usuario.user.id,
                'profile_id': usuario.id,
                'username': usuario.user.username,
                'email': usuario.user.email,
                'nombre_completo': f"{usuario.nombre} {usuario.apellido_paterno} {usuario.apellido_materno or ''}".strip(),
                'correo': usuario.correo,
                'nivel_usuario': usuario.nivel_usuario,
                'fecha_registro': usuario.user.date_joined,
                'ultimo_login': usuario.user.last_login,
                'is_active': usuario.user.is_active,
                'empresa': empresa_info,
                'planta': planta_info,
            })
        
        return Response({
            'usuarios': usuarios_data,
            'total': len(usuarios_data)
        })
    
    @action(detail=False, methods=['post'])
    def suspender_usuario(self, request):
        """Suspender/activar un usuario específico"""
        self._verify_superadmin(request.user)
        
        user_id = request.data.get('user_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not user_id or not accion:
            return Response({'error': 'Faltan parámetros user_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            
            nuevo_status = accion == 'activar'
            user.is_active = nuevo_status
            user.save()
            
            return Response({
                'message': f'Usuario {accion} exitosamente',
                'user_id': user_id,
                'username': user.username,
                'nuevo_status': nuevo_status
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['delete'])
    def eliminar_usuario(self, request):
        """Eliminar completamente un usuario del sistema"""
        self._verify_superadmin(request.user)
        
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'Falta parámetro user_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            username = user.username;
            
            # Verificar si es admin de empresa
            try:
                perfil = PerfilUsuario.objects.get(user=user)
                if perfil.nivel_usuario == 'admin-empresa':
                    empresa = Empresa.objects.get(administrador=perfil)
                    return Response({
                        'error': f'No se puede eliminar el administrador de la empresa "{empresa.nombre}". Elimine la empresa primero.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Si es admin de planta, actualizar la relación
                if perfil.nivel_usuario == 'admin-planta':
                    AdminPlanta.objects.filter(usuario=perfil).delete()
                
                # Eliminar perfil
                perfil.delete()
                
            except PerfilUsuario.DoesNotExist:
                pass
            
            # Eliminar usuario
            user.delete()
            
            return Response({
                'message': f'Usuario "{username}" eliminado exitosamente',
                'user_id': user_id
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando usuario: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def listar_todas_plantas(self, request):
        """Listar todas las plantas del sistema con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        empresa_id = request.query_params.get('empresa_id', '')
        status_filter = request.query_params.get('status', '')
        
        plantas = Planta.objects.all()
        
        if buscar:
            plantas = plantas.filter(nombre__icontains=buscar)
        
        if empresa_id:
            plantas = plantas.filter(empresa_id=empresa_id)
        
        if status_filter:
            status_bool = status_filter.lower() == 'true'
            plantas = plantas.filter(status=status_bool)
        
        plantas_data = []
        for planta in plantas:
            # Obtener admin de planta
            admin_info = None
            try:
                admin_planta = AdminPlanta.objects.get(planta=planta)
                admin_user = admin_planta.usuario.user
                admin_info = {
                    'id': admin_user.id,
                    'username': admin_user.username,
                    'email': admin_user.email,
                    'nombre_completo': f"{admin_planta.usuario.nombre} {admin_planta.usuario.apellido_paterno}",
                    'activo': admin_user.is_active
                }
            except AdminPlanta.DoesNotExist:
                pass
            
            # Contar entidades relacionadas
            departamentos_count = Departamento.objects.filter(planta=planta).count()
            empleados_count = Empleado.objects.filter(planta=planta).count()
            
            plantas_data.append({
                'planta_id': planta.planta_id,
                'nombre': planta.nombre,
                'direccion': planta.direccion,
                'telefono': None,  # El modelo Planta no tiene campo telefono
                'status': planta.status,
                'empresa': {
                    'id': planta.empresa.empresa_id,
                    'nombre': planta.empresa.nombre,
                    'status': planta.empresa.status
                },
                'administrador': admin_info,
                'departamentos_count': departamentos_count,
                'empleados_count': empleados_count,
            })
        
        return Response({
            'plantas': plantas_data,
            'total': len(plantas_data)
        })
    
    @action(detail=False, methods=['get'])
    def listar_todos_departamentos(self, request):
        """Listar todos los departamentos del sistema con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        planta_id = request.query_params.get('planta_id', '')
        empresa_id = request.query_params.get('empresa_id', '')
        status_filter = request.query_params.get('status', '')
        
        departamentos = Departamento.objects.all()
        
        if buscar:
            departamentos = departamentos.filter(nombre__icontains=buscar)
        
        if planta_id:
            departamentos = departamentos.filter(planta_id=planta_id)
        
        if empresa_id:
            departamentos = departamentos.filter(planta__empresa_id=empresa_id)
        
        if status_filter:
            status_bool = status_filter.lower() == 'true'
            departamentos = departamentos.filter(status=status_bool)
        
        departamentos_data = []
        for depto in departamentos:
            # Contar entidades relacionadas
            puestos_count = Puesto.objects.filter(departamento=depto).count()
            empleados_count = Empleado.objects.filter(departamento=depto).count()
            
            departamentos_data.append({
                'departamento_id': depto.departamento_id,
                'nombre': depto.nombre,
                'descripcion': depto.descripcion,
                'status': depto.status,
                'planta': {
                    'id': depto.planta.planta_id,
                    'nombre': depto.planta.nombre,
                    'status': depto.planta.status
                },
                'empresa': {
                    'id': depto.planta.empresa.empresa_id,
                    'nombre': depto.planta.empresa.nombre,
                    'status': depto.planta.empresa.status
                },
                'puestos_count': puestos_count,
                'empleados_count': empleados_count,
            })
        
        return Response({
            'departamentos': departamentos_data,
            'total': len(departamentos_data)
        })
    
    @action(detail=False, methods=['get'])
    def listar_todos_puestos(self, request):
        """Listar todos los puestos del sistema con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        departamento_id = request.query_params.get('departamento_id', '')
        planta_id = request.query_params.get('planta_id', '')
        empresa_id = request.query_params.get('empresa_id', '')
        status_filter = request.query_params.get('status', '')
        
        puestos = Puesto.objects.all()
        
        if buscar:
            puestos = puestos.filter(nombre__icontains=buscar)
        
        if departamento_id:
            puestos = puestos.filter(departamento_id=departamento_id)
        
        if planta_id:
            puestos = puestos.filter(departamento__planta_id=planta_id)
        
        if empresa_id:
            puestos = puestos.filter(departamento__planta__empresa_id=empresa_id)
        
        if status_filter:
            status_bool = status_filter.lower() == 'true'
            puestos = puestos.filter(status=status_bool)
        
        puestos_data = []
        for puesto in puestos:
            # Contar empleados en este puesto
            empleados_count = Empleado.objects.filter(puesto=puesto).count()
            
            puestos_data.append({
                'puesto_id': puesto.puesto_id,
                'nombre': puesto.nombre,
                'descripcion': puesto.descripcion,
                'status': puesto.status,
                'departamento': {
                    'id': puesto.departamento.departamento_id,
                    'nombre': puesto.departamento.nombre,
                    'status': puesto.departamento.status
                },
                'planta': {
                    'id': puesto.departamento.planta.planta_id,
                    'nombre': puesto.departamento.planta.nombre,
                    'status': puesto.departamento.planta.status
                },
                'empresa': {
                    'id': puesto.departamento.planta.empresa.empresa_id,
                    'nombre': puesto.departamento.planta.empresa.nombre,
                    'status': puesto.departamento.planta.empresa.status
                },
                'empleados_count': empleados_count,
            })
        
        return Response({
            'puestos': puestos_data,
            'total': len(puestos_data)
        })
    
    @action(detail=False, methods=['get'])
    def listar_todos_empleados(self, request):
        """Listar todos los empleados del sistema con filtros"""
        self._verify_superadmin(request.user)
        
        # Filtros opcionales
        buscar = request.query_params.get('buscar', '')
        empresa_id = request.query_params.get('empresa_id', '')
        planta_id = request.query_params.get('planta_id', '')
        departamento_id = request.query_params.get('departamento_id', '')
        puesto_id = request.query_params.get('puesto_id', '')
        status_filter = request.query_params.get('status', '')
        
        empleados = Empleado.objects.all()
        
        if buscar:
            empleados = empleados.filter(
                nombre__icontains=buscar
            ) | empleados.filter(
                apellido_paterno__icontains=buscar
            ) | empleados.filter(
                apellido_materno__icontains=buscar
            )
        
        if empresa_id:
            empleados = empleados.filter(planta__empresa_id=empresa_id)
        
        if planta_id:
            empleados = empleados.filter(planta_id=planta_id)
        
        if departamento_id:
            empleados = empleados.filter(departamento_id=departamento_id)
        
        if puesto_id:
            empleados = empleados.filter(puesto_id=puesto_id)
        
        if status_filter:
            status_bool = status_filter.lower() == 'true'
            empleados = empleados.filter(status=status_bool)
        
        empleados_data = []
        for empleado in empleados:
            empleados_data.append({
                'empleado_id': empleado.empleado_id,
                'numero_empleado': f"EMP-{empleado.empleado_id:06d}",  # Generar número de empleado
                'nombre': empleado.nombre,
                'apellido_paterno': empleado.apellido_paterno,
                'apellido_materno': empleado.apellido_materno or '',
                'nombre_completo': f"{empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno or ''}".strip(),
                'correo': None,  # Campo no disponible en el modelo actual
                'telefono': None,  # Campo no disponible en el modelo actual
                'fecha_ingreso': None,  # Campo no disponible en el modelo actual
                'salario': None,  # Campo no disponible en el modelo actual
                'status': empleado.status,
                'empresa': {
                    'id': empleado.planta.empresa.empresa_id,
                    'nombre': empleado.planta.empresa.nombre,
                    'status': empleado.planta.empresa.status
                },
                'planta': {
                    'id': empleado.planta.planta_id,
                    'nombre': empleado.planta.nombre,
                    'status': empleado.planta.status
                },
                'departamento': {
                    'id': empleado.departamento.departamento_id,
                    'nombre': empleado.departamento.nombre,
                    'status': empleado.departamento.status
                },
                'puesto': {
                    'id': empleado.puesto.puesto_id,
                    'nombre': empleado.puesto.nombre,
                    'status': empleado.puesto.status
                }
            })
        
        return Response({
            'empleados': empleados_data,
            'total': len(empleados_data)
        })

    # ======== ENDPOINTS PARA PLANTAS ========
    @action(detail=False, methods=['post'])
    def suspender_planta(self, request):
        """Suspender/activar una planta y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        planta_id = request.data.get('planta_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not planta_id or not accion:
            return Response({'error': 'Faltan parámetros planta_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            planta = Planta.objects.get(planta_id=planta_id)
            nuevo_status = accion == 'activar'
            
            # Cambiar status de la planta
            planta.status = nuevo_status
            planta.save()
            
            # Cambiar status de todos los departamentos de la planta
            departamentos = Departamento.objects.filter(planta=planta)
            departamentos.update(status=nuevo_status)
            
            # Cambiar status de todos los puestos de los departamentos
            puestos = Puesto.objects.filter(departamento__planta=planta)
            puestos.update(status=nuevo_status)
            
            # Cambiar status de todos los empleados de la planta
            empleados = Empleado.objects.filter(planta=planta)
            empleados.update(status=nuevo_status)
            
            # Activar/desactivar cuenta del administrador de planta
            try:
                admin_planta = AdminPlanta.objects.get(planta=planta)
                admin_planta.usuario.user.is_active = nuevo_status
                admin_planta.usuario.user.save()
                admin_planta.status = nuevo_status
                admin_planta.save()
            except AdminPlanta.DoesNotExist:
                pass
            
            return Response({
                'message': f'Planta {accion} exitosamente',
                'planta_id': planta_id,
                'nuevo_status': nuevo_status
            })
            
        except Planta.DoesNotExist:
            return Response({'error': 'Planta no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def eliminar_planta(self, request):
        """Eliminar completamente una planta y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        planta_id = request.data.get('planta_id')
        
        if not planta_id:
            return Response({'error': 'Falta parámetro planta_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            planta = Planta.objects.get(planta_id=planta_id)
            nombre_planta = planta.nombre
            
            # Eliminar en orden inverso para respetar las foreign keys
            
            # 1. Eliminar empleados
            empleados = Empleado.objects.filter(planta=planta)
            empleados_count = empleados.count()
            empleados.delete()
            
            # 2. Eliminar puestos
            puestos = Puesto.objects.filter(departamento__planta=planta)
            puestos_count = puestos.count()
            puestos.delete()
            
            # 3. Eliminar departamentos
            departamentos = Departamento.objects.filter(planta=planta)
            departamentos_count = departamentos.count()
            departamentos.delete()
            
            # 4. Eliminar administrador de planta y su usuario
            admin_planta = None
            try:
                admin_planta = AdminPlanta.objects.get(planta=planta)
                if admin_planta.usuario.user:
                    admin_planta.usuario.user.delete()
                admin_planta.usuario.delete()
                admin_planta.delete()
            except AdminPlanta.DoesNotExist:
                pass
            
            # 5. Eliminar planta
            planta.delete()
            
            return Response({
                'message': f'Planta "{nombre_planta}" eliminada exitosamente',
                'entidades_eliminadas': {
                    'planta': 1,
                    'departamentos': departamentos_count,
                    'puestos': puestos_count,
                    'empleados': empleados_count,
                    'admin_planta': 1 if admin_planta else 0
                }
            })
            
        except Planta.DoesNotExist:
            return Response({'error': 'Planta no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando planta: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ======== ENDPOINTS PARA DEPARTAMENTOS ========
    @action(detail=False, methods=['post'])
    def suspender_departamento(self, request):
        """Suspender/activar un departamento y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        departamento_id = request.data.get('departamento_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not departamento_id or not accion:
            return Response({'error': 'Faltan parámetros departamento_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            departamento = Departamento.objects.get(departamento_id=departamento_id)
            nuevo_status = accion == 'activar'
            
            # Cambiar status del departamento
            departamento.status = nuevo_status
            departamento.save()
            
            # Cambiar status de todos los puestos del departamento
            puestos = Puesto.objects.filter(departamento=departamento)
            puestos.update(status=nuevo_status)
            
            # Cambiar status de todos los empleados del departamento
            empleados = Empleado.objects.filter(departamento=departamento)
            empleados.update(status=nuevo_status)
            
            return Response({
                'message': f'Departamento {accion} exitosamente',
                'departamento_id': departamento_id,
                'nuevo_status': nuevo_status
            })
            
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def eliminar_departamento(self, request):
        """Eliminar completamente un departamento y todas sus entidades relacionadas"""
        self._verify_superadmin(request.user)
        
        departamento_id = request.data.get('departamento_id')
        
        if not departamento_id:
            return Response({'error': 'Falta parámetro departamento_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            departamento = Departamento.objects.get(departamento_id=departamento_id)
            nombre_departamento = departamento.nombre
            
            # Eliminar en orden inverso para respetar las foreign keys
            
            # 1. Eliminar empleados
            empleados = Empleado.objects.filter(departamento=departamento)
            empleados_count = empleados.count()
            empleados.delete()
            
            # 2. Eliminar puestos
            puestos = Puesto.objects.filter(departamento=departamento)
            puestos_count = puestos.count()
            puestos.delete()
            
            # 3. Eliminar departamento
            departamento.delete()
            
            return Response({
                'message': f'Departamento "{nombre_departamento}" eliminado exitosamente',
                'entidades_eliminadas': {
                    'departamento': 1,
                    'puestos': puestos_count,
                    'empleados': empleados_count
                }
            })
            
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando departamento: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ======== ENDPOINTS PARA PUESTOS ========
    @action(detail=False, methods=['post'])
    def suspender_puesto(self, request):
        """Suspender/activar un puesto y todos sus empleados"""
        self._verify_superadmin(request.user)
        
        puesto_id = request.data.get('puesto_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not puesto_id or not accion:
            return Response({'error': 'Faltan parámetros puesto_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            puesto = Puesto.objects.get(puesto_id=puesto_id)
            nuevo_status = accion == 'activar'
            
            # Cambiar status del puesto
            puesto.status = nuevo_status
            puesto.save()
            
            # Cambiar status de todos los empleados del puesto
            empleados = Empleado.objects.filter(puesto=puesto)
            empleados.update(status=nuevo_status)
            
            return Response({
                'message': f'Puesto {accion} exitosamente',
                'puesto_id': puesto_id,
                'nuevo_status': nuevo_status
            })
            
        except Puesto.DoesNotExist:
            return Response({'error': 'Puesto no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def eliminar_puesto(self, request):
        """Eliminar completamente un puesto y todos sus empleados"""
        self._verify_superadmin(request.user)
        
        puesto_id = request.data.get('puesto_id')
        
        if not puesto_id:
            return Response({'error': 'Falta parámetro puesto_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            puesto = Puesto.objects.get(puesto_id=puesto_id)
            nombre_puesto = puesto.nombre
            
            # 1. Eliminar empleados
            empleados = Empleado.objects.filter(puesto=puesto)
            empleados_count = empleados.count()
            empleados.delete()
            
            # 2. Eliminar puesto
            puesto.delete()
            
            return Response({
                'message': f'Puesto "{nombre_puesto}" eliminado exitosamente',
                'entidades_eliminadas': {
                    'puesto': 1,
                    'empleados': empleados_count
                }
            })
            
        except Puesto.DoesNotExist:
            return Response({'error': 'Puesto no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando puesto: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ======== ENDPOINTS PARA EMPLEADOS ========
    @action(detail=False, methods=['post'])
    def suspender_empleado(self, request):
        """Suspender/activar un empleado específico"""
        self._verify_superadmin(request.user)
        
        empleado_id = request.data.get('empleado_id')
        accion = request.data.get('accion')  # 'suspender' o 'activar'
        
        if not empleado_id or not accion:
            return Response({'error': 'Faltan parámetros empleado_id o accion'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empleado = Empleado.objects.get(empleado_id=empleado_id)
            nuevo_status = accion == 'activar'
            
            # Cambiar status del empleado
            empleado.status = nuevo_status
            empleado.save()
            
            return Response({
                'message': f'Empleado {accion} exitosamente',
                'empleado_id': empleado_id,
                'nuevo_status': nuevo_status
            })
            
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def eliminar_empleado(self, request):
        """Eliminar completamente un empleado del sistema"""
        self._verify_superadmin(request.user)
        
        empleado_id = request.data.get('empleado_id')
        
        if not empleado_id:
            return Response({'error': 'Falta parámetro empleado_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empleado = Empleado.objects.get(empleado_id=empleado_id)
            nombre_empleado = f"{empleado.nombre} {empleado.apellido_paterno}"
            
            # Eliminar empleado
            empleado.delete()
            
            return Response({
                'message': f'Empleado "{nombre_empleado}" eliminado exitosamente',
                'empleado_id': empleado_id
            })
            
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error eliminando empleado: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ======== ENDPOINTS PARA EDICIÓN ========
    @action(detail=False, methods=['put'])
    def editar_empresa(self, request):
        """Editar datos de una empresa"""
        self._verify_superadmin(request.user)
        
        empresa_id = request.data.get('empresa_id')
        
        if not empresa_id:
            return Response({'error': 'Falta parámetro empresa_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            
            # Actualizar campos permitidos
            if 'nombre' in request.data:
                empresa.nombre = request.data['nombre']
            if 'rfc' in request.data:
                empresa.rfc = request.data['rfc']
            if 'telefono' in request.data:
                empresa.telefono_contacto = request.data.get('telefono', '')
            if 'correo' in request.data:
                empresa.email_contacto = request.data.get('correo', '')
            if 'direccion' in request.data:
                empresa.direccion = request.data.get('direccion', '')
            if 'status' in request.data:
                empresa.status = request.data['status']
            
            empresa.save()
            
            return Response({
                'message': f'Empresa "{empresa.nombre}" actualizada exitosamente',
                'empresa_id': empresa_id
            })
            
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error actualizando empresa: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['put'])
    def editar_usuario(self, request):
        """Editar datos de un usuario"""
        self._verify_superadmin(request.user)
        
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'Falta parámetro user_id'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            perfil = PerfilUsuario.objects.get(user=user)
            
            # Actualizar campos del usuario
            if 'username' in request.data:
                user.username = request.data['username']
            if 'email' in request.data:
                user.email = request.data['email']
                perfil.correo = request.data['email']  # Actualizar también en perfil
            if 'nombre' in request.data:
                perfil.nombre = request.data['nombre']
            if 'apellido_paterno' in request.data:
                perfil.apellido_paterno = request.data['apellido_paterno']
            if 'apellido_materno' in request.data:
                perfil.apellido_materno = request.data.get('apellido_materno', '')
            if 'nivel_usuario' in request.data:
                perfil.nivel_usuario = request.data['nivel_usuario']
            if 'is_active' in request.data:
                user.is_active = request.data['is_active']
            
            user.save()
            perfil.save()
            
            return Response({
                'message': f'Usuario "{user.username}" actualizado exitosamente',
                'user_id': user_id
            })
            
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except PerfilUsuario.DoesNotExist:
            return Response({'error': 'Perfil de usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error actualizando usuario: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def crear_usuario(self, request):
        """Crear un nuevo usuario (solo SuperAdmin)"""
        self._verify_superadmin(request.user)
        
        # Datos requeridos
        username = request.data.get('username')
        email = request.data.get('email')
        nombre = request.data.get('nombre')
        apellido_paterno = request.data.get('apellido_paterno')
        apellido_materno = request.data.get('apellido_materno', '')
        nivel_usuario = request.data.get('nivel_usuario', 'superadmin')
        password = request.data.get('password', '1234')  # Password por defecto
        
        if not all([username, email, nombre, apellido_paterno]):
            return Response({'error': 'Faltan campos requeridos: username, email, nombre, apellido_paterno'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Solo permitir crear usuarios superadmin desde SuperAdmin
        if nivel_usuario != 'superadmin':
            return Response({'error': 'Solo se pueden crear usuarios SuperAdmin desde esta interfaz'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            from django.db import transaction
            
            with transaction.atomic():
                # Verificar que no exista el username o email
                if User.objects.filter(username=username).exists():
                    return Response({'error': 'El nombre de usuario ya existe'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                if User.objects.filter(email=email).exists():
                    return Response({'error': 'El email ya está registrado'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                # Crear usuario
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=request.data.get('is_active', True)
                )
                
                # Crear perfil
                perfil = PerfilUsuario.objects.create(
                    user=user,
                    nombre=nombre,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    correo=email,
                    nivel_usuario=nivel_usuario
                )
                
                return Response({
                    'message': f'Usuario SuperAdmin "{username}" creado exitosamente',
                    'user_id': user.id,
                    'password_temporal': password
                })
                
        except Exception as e:
            return Response({'error': f'Error creando usuario: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# VISTAS PARA SUSCRIPCIONES - RF-001, RF-003
# ============================================================================

@method_decorator(csrf_exempt, name='dispatch')
class SuscripcionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def listar_planes(self, request):
        """Lista todos los planes de suscripción disponibles"""
        try:
            from apps.subscriptions.models import PlanSuscripcion
            
            planes = PlanSuscripcion.objects.filter(status=True).values(
                'plan_id', 'nombre', 'descripcion', 'precio', 'duracion', 'status'
            )
            
            return Response(list(planes))
            
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo planes: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def crear_plan(self, request):
        """Crear un nuevo plan de suscripción (Solo SuperAdmin)"""
        try:
            from apps.subscriptions.models import PlanSuscripcion
            from django.db import transaction
            

            data = request.data
            nombre = data.get('nombre')
            descripcion = data.get('descripcion', '')
            precio = data.get('precio')
            duracion = data.get('duracion')
            
            if not nombre or not precio or not duracion:
                return Response(
                    {'error': 'nombre, precio y duracion son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                plan = PlanSuscripcion.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=float(precio),
                    duracion=int(duracion),
                    status=True
                )
            
            return Response({
                'message': f'Plan "{plan.nombre}" creado exitosamente',
                'plan': {
                    'plan_id': plan.plan_id,
                    'nombre': plan.nombre,
                    'descripcion': plan.descripcion,
                    'precio': float(plan.precio),
                    'duracion': plan.duracion
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Error creando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['put'], permission_classes=[])
    def editar_plan(self, request):
        """Editar un plan de suscripción"""
        try:
            from apps.subscriptions.models import PlanSuscripcion
            
            plan_id = request.data.get('plan_id')
            if not plan_id:
                return Response(
                    {'error': 'plan_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            
            # Actualizar campos si se proporcionan
            if 'nombre' in request.data:
                plan.nombre = request.data['nombre']
            if 'descripcion' in request.data:
                plan.descripcion = request.data['descripcion']
            if 'precio' in request.data:
                plan.precio = float(request.data['precio'])
            if 'duracion' in request.data:
                plan.duracion = int(request.data['duracion'])
            if 'status' in request.data:
                plan.status = bool(request.data['status'])
            
            plan.save()
            
            return Response({
                'message': f'Plan "{plan.nombre}" actualizado exitosamente',
                'plan': {
                    'plan_id': plan.plan_id,
                    'nombre': plan.nombre,
                    'descripcion': plan.descripcion,
                    'precio': float(plan.precio),
                    'duracion': plan.duracion,
                    'status': plan.status
                }
            })
            
        except PlanSuscripcion.DoesNotExist:
            return Response(
                {'error': 'Plan no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error actualizando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def listar_suscripciones(self, request):
        """Lista todas las suscripciones de empresas"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa
            
            suscripciones = SuscripcionEmpresa.objects.select_related(
                'empresa', 'plan_suscripcion'
            ).values(
                'suscripcion_id',
                'empresa__nombre',
                'empresa__empresa_id',
                'plan_suscripcion__nombre',
                'plan_suscripcion__precio',
                'plan_suscripcion__duracion',
                'fecha_inicio',
                'fecha_fin',
                'estado',
                'status'
            )
            
            return Response(list(suscripciones))
            
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo suscripciones: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def crear_suscripcion(self, request):
        """Crear una nueva suscripción para una empresa"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa, PlanSuscripcion, Pago
            from django.db import transaction
            from datetime import timedelta
            
            data = request.data
            empresa_id = data.get('empresa_id')
            plan_id = data.get('plan_id')
            
            if not empresa_id or not plan_id:
                return Response(
                    {'error': 'empresa_id y plan_id son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                empresa = Empresa.objects.get(empresa_id=empresa_id)
            except Empresa.DoesNotExist:
                return Response(
                    {'error': f'Empresa con ID {empresa_id} no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            except PlanSuscripcion.DoesNotExist:
                return Response(
                    {'error': f'Plan con ID {plan_id} no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar si ya existe una suscripción activa
            suscripcion_existente = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                status=True
            ).first()
            
            if suscripcion_existente:
                return Response(
                    {'error': 'La empresa ya tiene una suscripción activa'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                # Crear nueva suscripción
                fecha_inicio = timezone.now().date()
                fecha_fin = fecha_inicio + timedelta(days=plan.duracion)
                
                suscripcion = SuscripcionEmpresa.objects.create(
                    empresa=empresa,
                    plan_suscripcion=plan,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    estado='Activa',
                    status=True
                )
                
                # Crear pago completado
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan.precio,
                    monto_pago=plan.precio,
                    estado_pago='Completado',
                    fecha_pago=timezone.now()
                )
            
            return Response({
                'message': f'Suscripción creada exitosamente para {empresa.nombre}',
                'suscripcion': {
                    'suscripcion_id': suscripcion.suscripcion_id,
                    'empresa': empresa.nombre,
                    'plan': plan.nombre,
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat(),
                    'precio': float(plan.precio)
                }
            })
            
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except PlanSuscripcion.DoesNotExist:
            return Response(
                {'error': 'Plan no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error creando suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def renovar_suscripcion(self, request):
        """Renovar una suscripción existente"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa, Pago
            from django.utils import timezone
            
            data = request.data
            suscripcion_id = data.get('suscripcion_id')
            meses = data.get('meses', 1)
            metodo_pago = data.get('metodo_pago', 'tarjeta_credito')
            
            suscripcion = SuscripcionEmpresa.objects.get(id=suscripcion_id)
            
            # Renovar la suscripción
            suscripcion.renovar_suscripcion(meses)
            
            # Crear el registro de pago
            monto = suscripcion.plan.precio_mensual * meses
            pago = Pago.objects.create(
                suscripcion=suscripcion,
                monto=monto,
                metodo_pago=metodo_pago,
                estado_pago='completado',
                referencia_pago=f"REN-{suscripcion.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )
            
            return Response({
                'message': f'Suscripción renovada por {meses} mes(es)',
                'nueva_fecha_fin': suscripcion.fecha_fin.strftime('%Y-%m-%d'),
                'monto_pagado': str(monto)
            })
            
        except SuscripcionEmpresa.DoesNotExist:
            return Response({'error': 'Suscripción no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error renovando suscripción: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def listar_pagos(self, request):
        """Listar todos los pagos del sistema con información de suscripción"""
        try:
            from apps.subscriptions.models import Pago
            
            pagos = Pago.objects.select_related(
                'suscripcion__empresa', 'suscripcion__plan_suscripcion'
            ).values(
                'pago_id',
                'suscripcion__empresa__nombre',
                'suscripcion__plan_suscripcion__nombre',
                'costo',
                'monto_pago',
                'estado_pago',
                'fecha_pago',
                'fecha_vencimiento'
            ).order_by('-fecha_pago')
            
            return Response(list(pagos))
            
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo pagos: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def procesar_pago(self, request):
        """Procesar un pago para una suscripción"""
        try:
            from apps.subscriptions.models import SuscripcionEmpresa, Pago
            from django.db import transaction
            
            data = request.data
            suscripcion_id = data.get('suscripcion_id')
            monto_pago = data.get('monto_pago')
            transaccion_id = data.get('transaccion_id', '')
            
            if not suscripcion_id or not monto_pago:
                return Response(
                    {'error': 'suscripcion_id y monto_pago son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                suscripcion = SuscripcionEmpresa.objects.get(suscripcion_id=suscripcion_id)
            except SuscripcionEmpresa.DoesNotExist:
                return Response(
                    {'error': f'Suscripción con ID {suscripcion_id} no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with transaction.atomic():
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=suscripcion.plan_suscripcion.precio,
                    monto_pago=float(monto_pago),
                    estado_pago='Completado',
                    transaccion_id=transaccion_id
                )
                
                # Activar suscripción si estaba suspendida
                if suscripcion.estado != 'Activa':
                    suscripcion.estado = 'Activa'
                    suscripcion.status = True
                    suscripcion.save()
            
            return Response({
                'message': 'Pago procesado exitosamente',
                'pago': {
                    'pago_id': pago.pago_id,
                    'monto': float(pago.monto_pago),
                    'fecha': pago.fecha_pago.isoformat(),
                    'estado': pago.estado_pago
                }
            })
            
        except SuscripcionEmpresa.DoesNotExist:
            return Response(
                {'error': 'Suscripción no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error procesando pago: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def info_suscripcion_empresa(self, request):
        """Obtener información de suscripción de una empresa específica"""
        try:
            empresa_id = request.GET.get('empresa_id')
            if not empresa_id:
                return Response(
                    {'error': 'empresa_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            info_suscripcion = self.get_subscription_info(empresa)
            return Response(info_suscripcion)
            
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo información de suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )