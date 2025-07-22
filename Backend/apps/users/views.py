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
from .serializers import (
    EmpresaSerializer, EmpleadoSerializer, PlantaSerializer, 
    DepartamentoSerializer, PuestoSerializer, PerfilUsuarioSerializer,
    EmpresaCreateSerializer, PlantaCreateSerializer, DepartamentoCreateSerializer, PuestoCreateSerializer,
    EmpleadoCreateSerializer
)


# ====================== AUTHENTICATION VIEWSET ======================


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
    
    def get_serializer_class(self):
        """Usar diferentes serializers para create vs otras acciones"""
        if self.action in ['create', 'registro']:
            return EmpresaCreateSerializer
        return EmpresaSerializer
    
    def get_permissions(self):
        """Permitir acceso público solo al endpoint de registro"""
        if self.action == 'registro':
            return [AllowAny()]
        return super().get_permissions()

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
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def registro(self, request):
        """Registro público de empresa con usuario administrador"""
        try:
            # Datos requeridos
            required_fields = ['nombre', 'rfc', 'usuario', 'password', 'nombre_completo']
            missing_fields = []
            
            for field in required_fields:
                if not request.data.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                return Response({
                    'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Datos de la empresa
            nombre_empresa = request.data.get('nombre').strip()
            rfc = request.data.get('rfc').strip()
            direccion = request.data.get('direccion', '').strip()
            email_contacto = request.data.get('email_contacto', '').strip()
            telefono_contacto = request.data.get('telefono_contacto', '').strip()
            
            # Datos del usuario administrador
            username = request.data.get('usuario').strip()
            password = request.data.get('password')
            nombre_completo = request.data.get('nombre_completo').strip()
            
            # Verificar que no existan duplicados
            if User.objects.filter(username=username).exists():
                return Response({
                    'error': 'El nombre de usuario ya está registrado'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if Empresa.objects.filter(rfc=rfc).exists():
                return Response({
                    'error': 'El RFC ya está registrado para otra empresa'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear usuario administrador
            nombres = nombre_completo.split(' ')
            first_name = nombres[0] if nombres else ''
            last_name = ' '.join(nombres[1:]) if len(nombres) > 1 else ''
            
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email_contacto or f"{username}@empresa.com",
                first_name=first_name,
                last_name=last_name
            )
            
            # Crear perfil del usuario
            perfil = PerfilUsuario.objects.create(
                nombre=first_name,
                apellido_paterno=last_name.split(' ')[0] if last_name else '',
                apellido_materno=' '.join(last_name.split(' ')[1:]) if len(last_name.split(' ')) > 1 else '',
                correo=user.email,
                nivel_usuario='admin-empresa',
                status=True,
                user=user
            )
            
            # Crear empresa
            empresa = Empresa.objects.create(
                nombre=nombre_empresa,
                rfc=rfc,
                direccion=direccion,
                email_contacto=email_contacto,
                telefono_contacto=telefono_contacto,
                administrador=perfil,
                status=True
            )
            
            # Crear automáticamente la Planta General para la empresa
            from .models import Planta
            planta_general = Planta.objects.create(
                nombre=f"{nombre_empresa} - Sede Principal",
                direccion=direccion or "Dirección de la sede principal",
                empresa=empresa,
                status=True
            )
            
            return Response({
                'message': 'Empresa registrada exitosamente',
                'empresa_id': empresa.empresa_id,
                'empresa': {
                    'empresa_id': empresa.empresa_id,
                    'nombre': empresa.nombre,
                    'rfc': empresa.rfc,
                    'direccion': empresa.direccion,
                    'status': empresa.status,
                    'fecha_registro': empresa.fecha_registro
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Error interno del servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        """Crear empresa asignando automáticamente el administrador"""
        try:
            # Obtener o crear perfil del usuario autenticado
            user = request.user
            
            # Buscar perfil por email
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
            except PerfilUsuario.DoesNotExist:
                # Si no existe perfil, crear uno
                perfil = PerfilUsuario.objects.create(
                    nombre=user.first_name or user.username,
                    apellido_paterno=user.last_name or '',
                    correo=user.email,
                    nivel_usuario='admin-empresa',
                    status=True,
                    user=user
                )
            
            # Crear empresa con el administrador asignado
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Asignar administrador antes de guardar
            empresa = serializer.save(administrador=perfil)
            
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Empresa registrada exitosamente',
                'empresa_id': empresa.empresa_id,
                'empresa': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            return Response({
                'error': f'Error al registrar empresa: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Usar diferentes serializers para create vs otras acciones"""
        if self.action == 'create':
            return EmpleadoCreateSerializer
        return EmpleadoSerializer

    def create(self, request, *args, **kwargs):
        """Override create para incluir empleado_id en la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data.copy()
        response_data['empleado_id'] = serializer.instance.empleado_id
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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

    def get_serializer_class(self):
        """Usar diferentes serializers para create vs otras acciones"""
        if self.action == 'create':
            return PlantaCreateSerializer
        return PlantaSerializer

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
            # Si es superuser, debe especificar la empresa en el payload
            # El serializer ya valida que la empresa existe
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
        self._crear_usuario_planta(planta)
        
        # Crear estructura base (departamentos y puestos)
        self._crear_estructura_base_planta(planta)
    
    def _crear_estructura_base_planta(self, planta):
        """Crear departamentos y puestos base para una nueva planta"""
        try:
            print(f"🏗️  Creando estructura base para planta: {planta.nombre}")
            
            # Departamentos base
            DEPARTAMENTOS_BASE = [
                {'nombre': 'Recursos Humanos', 'descripcion': 'Departamento encargado de la gestión del personal y desarrollo organizacional'},
                {'nombre': 'Administración', 'descripcion': 'Departamento de administración general y control interno'},
                {'nombre': 'Operaciones', 'descripcion': 'Departamento de operaciones y procesos productivos'},
                {'nombre': 'Finanzas', 'descripcion': 'Departamento de contabilidad y gestión financiera'},
                {'nombre': 'Ventas', 'descripcion': 'Departamento de ventas y atención al cliente'}
            ]
            
            # Puestos base por departamento
            PUESTOS_POR_DEPARTAMENTO = {
                'Recursos Humanos': [
                    {'nombre': 'Gerente de RRHH', 'descripcion': 'Responsable de la gestión integral de recursos humanos'},
                    {'nombre': 'Especialista en Reclutamiento', 'descripcion': 'Encargado del proceso de selección de personal'},
                    {'nombre': 'Analista de Nómina', 'descripcion': 'Responsable del cálculo y procesamiento de nóminas'},
                    {'nombre': 'Coordinador de Capacitación', 'descripcion': 'Encargado del desarrollo y capacitación del personal'},
                    {'nombre': 'Asistente de RRHH', 'descripcion': 'Apoyo administrativo en actividades de recursos humanos'}
                ],
                'Administración': [
                    {'nombre': 'Gerente Administrativo', 'descripcion': 'Responsable de la administración general de la empresa'},
                    {'nombre': 'Coordinador de Servicios Generales', 'descripcion': 'Encargado del mantenimiento y servicios generales'},
                    {'nombre': 'Analista Administrativo', 'descripcion': 'Apoyo en procesos administrativos y documentación'},
                    {'nombre': 'Asistente Ejecutivo', 'descripcion': 'Asistente de dirección y coordinación ejecutiva'},
                    {'nombre': 'Recepcionista', 'descripcion': 'Atención de recepción y servicios de comunicación'}
                ],
                'Operaciones': [
                    {'nombre': 'Gerente de Operaciones', 'descripcion': 'Responsable de la coordinación de operaciones productivas'},
                    {'nombre': 'Supervisor de Producción', 'descripcion': 'Supervisión directa de procesos productivos'},
                    {'nombre': 'Operario Especializado', 'descripcion': 'Operario con especialización en procesos específicos'},
                    {'nombre': 'Técnico de Calidad', 'descripcion': 'Control y aseguramiento de la calidad de productos'},
                    {'nombre': 'Auxiliar de Operaciones', 'descripcion': 'Apoyo en actividades operativas generales'}
                ],
                'Finanzas': [
                    {'nombre': 'Gerente Financiero', 'descripcion': 'Responsable de la gestión financiera y contable'},
                    {'nombre': 'Contador General', 'descripcion': 'Encargado de la contabilidad general de la empresa'},
                    {'nombre': 'Analista Financiero', 'descripcion': 'Análisis de estados financieros e indicadores'},
                    {'nombre': 'Auxiliar Contable', 'descripcion': 'Apoyo en actividades contables y registros'},
                    {'nombre': 'Tesorero', 'descripcion': 'Manejo de flujo de efectivo y operaciones bancarias'}
                ],
                'Ventas': [
                    {'nombre': 'Gerente de Ventas', 'descripcion': 'Responsable de estrategias de ventas y objetivos comerciales'},
                    {'nombre': 'Ejecutivo de Cuentas', 'descripcion': 'Gestión y desarrollo de cuentas clave'},
                    {'nombre': 'Representante de Ventas', 'descripcion': 'Venta directa y atención a clientes'},
                    {'nombre': 'Coordinador de Marketing', 'descripcion': 'Desarrollo de estrategias de marketing y promoción'},
                    {'nombre': 'Asistente Comercial', 'descripcion': 'Apoyo en actividades comerciales y ventas'}
                ]
            }
            
            departamentos_creados = 0
            puestos_creados = 0
            
            for dept_data in DEPARTAMENTOS_BASE:
                # Crear departamento
                departamento = Departamento.objects.create(
                    nombre=dept_data['nombre'],
                    descripcion=dept_data['descripcion'],
                    planta=planta,
                    status=True
                )
                departamentos_creados += 1
                
                # Crear puestos para este departamento
                puestos_dept = PUESTOS_POR_DEPARTAMENTO.get(dept_data['nombre'], [])
                for puesto_data in puestos_dept:
                    Puesto.objects.create(
                        nombre=puesto_data['nombre'],
                        descripcion=puesto_data['descripcion'],
                        departamento=departamento,
                        status=True
                    )
                    puestos_creados += 1
            
            print(f"✅ Estructura creada: {departamentos_creados} departamentos y {puestos_creados} puestos")
            
        except Exception as e:
            print(f"❌ Error creando estructura base: {e}")
            # No fallar la creación de la planta si hay error con la estructura
    
    def _crear_usuario_planta(self, planta):
        """Crear automáticamente un usuario administrador para la planta"""
        try:
            import secrets
            import string
            
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
                nivel_usuario="admin-planta",  # ← Corregido: usar guión, no guión bajo
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
        response_data = serializer.data.copy()
        
        # Asegurar que incluya el planta_id
        response_data['planta_id'] = serializer.instance.planta_id
        
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

    def get_serializer_class(self):
        """Usar diferentes serializers para create vs otras acciones"""
        if self.action == 'create':
            return DepartamentoCreateSerializer
        return DepartamentoSerializer

    def create(self, request, *args, **kwargs):
        """Override create para incluir departamento_id en la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data.copy()
        response_data['departamento_id'] = serializer.instance.departamento_id
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Filtrar departamentos según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Departamento.objects.all()
        else:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                
                # Si es admin_empresa, mostrar todos los departamentos de su empresa
                if perfil.nivel_usuario == 'admin-empresa':
                    empresa = Empresa.objects.get(administrador=perfil)
                    return Departamento.objects.filter(planta__empresa=empresa)
                
                # Si es admin_planta, mostrar solo los departamentos de su planta
                elif perfil.nivel_usuario == 'admin-planta':
                    admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                    return Departamento.objects.filter(planta=admin_planta.planta)
                
                else:
                    return Departamento.objects.none()
                    
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist, AdminPlanta.DoesNotExist):
                return Departamento.objects.none()

    def perform_create(self, serializer):
        """Validar que la planta pertenezca al contexto del usuario"""
        user = self.request.user
        if not user.is_superuser:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                planta_id = serializer.validated_data.get('planta')
                
                # Si es admin_empresa, verificar que la planta pertenezca a su empresa
                if perfil.nivel_usuario == 'admin-empresa':
                    empresa = Empresa.objects.get(administrador=perfil)
                    if planta_id and planta_id.empresa != empresa:
                        raise ValidationError("La planta especificada no pertenece a su empresa")
                
                # Si es admin_planta, solo puede crear en su propia planta
                elif perfil.nivel_usuario == 'admin-planta':
                    admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                    if planta_id and planta_id != admin_planta.planta:
                        raise ValidationError("Solo puede crear departamentos en su propia planta")
                
                else:
                    raise ValidationError("No tiene permisos para crear departamentos")
                    
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist, AdminPlanta.DoesNotExist):
                raise ValidationError("No se puede determinar la empresa del usuario")
        serializer.save()


class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Usar diferentes serializers para create vs otras acciones"""
        if self.action == 'create':
            return PuestoCreateSerializer
        return PuestoSerializer

    def create(self, request, *args, **kwargs):
        """Override create para incluir puesto_id en la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data.copy()
        response_data['puesto_id'] = serializer.instance.puesto_id
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Filtrar puestos según el usuario"""
        user = self.request.user
        if user.is_superuser:
            return Puesto.objects.all()
        else:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                
                # Si es admin_empresa, mostrar todos los puestos de su empresa
                if perfil.nivel_usuario == 'admin-empresa':
                    empresa = Empresa.objects.get(administrador=perfil)
                    return Puesto.objects.filter(departamento__planta__empresa=empresa)
                
                # Si es admin_planta, mostrar solo los puestos de su planta
                elif perfil.nivel_usuario == 'admin-planta':
                    admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                    return Puesto.objects.filter(departamento__planta=admin_planta.planta)
                
                else:
                    return Puesto.objects.none()
                    
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist, AdminPlanta.DoesNotExist):
                return Puesto.objects.none()

    def perform_create(self, serializer):
        """Validar que el departamento pertenezca al contexto del usuario"""
        user = self.request.user
        if not user.is_superuser:
            try:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                departamento = serializer.validated_data.get('departamento')
                
                # Si es admin_empresa, verificar que el departamento pertenezca a su empresa
                if perfil.nivel_usuario == 'admin-empresa':
                    empresa = Empresa.objects.get(administrador=perfil)
                    if departamento and departamento.planta.empresa != empresa:
                        raise ValidationError("El departamento especificado no pertenece a su empresa")
                
                # Si es admin_planta, solo puede crear en departamentos de su planta
                elif perfil.nivel_usuario == 'admin-planta':
                    admin_planta = AdminPlanta.objects.get(usuario=perfil, status=True)
                    if departamento and departamento.planta != admin_planta.planta:
                        raise ValidationError("Solo puede crear puestos en departamentos de su propia planta")
                
                else:
                    raise ValidationError("No tiene permisos para crear puestos")
                    
            except (PerfilUsuario.DoesNotExist, Empresa.DoesNotExist, AdminPlanta.DoesNotExist):
                raise ValidationError("No se puede determinar la empresa del usuario")
        serializer.save()
