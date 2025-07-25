# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado

# Serializers para LOGIN
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# Serializers para REGISTRO DE EMPRESA
class EmpresaRegistroSerializer(serializers.ModelSerializer):
    # Datos del usuario administrador
    usuario = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    nombre_completo = serializers.CharField(required=True)
    
    class Meta:
        model = Empresa
        fields = ['nombre', 'rfc', 'direccion', 'email_contacto', 'telefono_contacto', 
                 'usuario', 'password', 'nombre_completo']
        extra_kwargs = {
            'nombre': {'required': True},
            'rfc': {'required': True},
            'email_contacto': {'required': True}
        }
    
    def validate(self, data):
        # Validaciones adicionales
        if not data.get('nombre', '').strip():
            raise serializers.ValidationError("El nombre de la empresa es requerido")
        if not data.get('rfc', '').strip():
            raise serializers.ValidationError("El RFC es requerido")
        if not data.get('usuario', '').strip():
            raise serializers.ValidationError("El nombre de usuario es requerido")
        if not data.get('password', '').strip():
            raise serializers.ValidationError("La contraseña es requerida")
        if not data.get('nombre_completo', '').strip():
            raise serializers.ValidationError("El nombre completo del administrador es requerido")
        
        # Verificar que el usuario no exista
        from django.contrib.auth.models import User
        if User.objects.filter(username=data['usuario']).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
            
        return data
    
    def create(self, validated_data):
        from django.db import transaction
        
        with transaction.atomic():
            # Extraer datos del usuario
            usuario = validated_data.pop('usuario')
            password = validated_data.pop('password')
            nombre_completo = validated_data.pop('nombre_completo')
            
            # Separar el nombre completo
            nombres = nombre_completo.strip().split(' ')
            nombre = nombres[0] if nombres else ''
            apellido_paterno = nombres[1] if len(nombres) > 1 else ''
            apellido_materno = nombres[2] if len(nombres) > 2 else ''
            
            # Crear usuario Django
            user = User.objects.create(
                username=usuario,
                email=validated_data.get('email_contacto', ''),
                password=make_password(password)
            )
            
            # Crear perfil de usuario
            user_profile = PerfilUsuario.objects.create(
                user=user,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                correo=validated_data.get('email_contacto', ''),
                nivel_usuario='admin-empresa'
            )
            
            # Crear empresa
            empresa = Empresa.objects.create(
                administrador=user_profile,
                **validated_data
            )
            
            # CREAR AUTOMÁTICAMENTE LA PLANTA PRINCIPAL
            planta_principal = Planta.objects.create(
                nombre='Planta Principal',
                empresa=empresa,
                direccion=empresa.direccion,  # Misma dirección que la empresa
                status=True
            )
            
            # CREAR DEPARTAMENTOS BÁSICOS
            departamentos_data = [
                {'nombre': 'Administración', 'descripcion': 'Gestión administrativa general'},
                {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal y nómina'},
                {'nombre': 'Finanzas', 'descripcion': 'Gestión financiera y contable'},
                {'nombre': 'Producción', 'descripcion': 'Operaciones de manufactura'},
                {'nombre': 'Calidad', 'descripcion': 'Control y aseguramiento de calidad'},
                {'nombre': 'Mantenimiento', 'descripcion': 'Mantenimiento de equipos e instalaciones'},
                {'nombre': 'Logística', 'descripcion': 'Almacén y distribución'},
            ]
            
            departamentos = []
            for dept_data in departamentos_data:
                dept = Departamento.objects.create(
                    nombre=dept_data['nombre'],
                    descripcion=dept_data['descripcion'],
                    planta=planta_principal
                )
                departamentos.append(dept)
            
            # CREAR PUESTOS BÁSICOS
            puestos_data = [
                # Administración
                {'nombre': 'Gerente General', 'departamento': 'Administración'},
                {'nombre': 'Asistente Administrativo', 'departamento': 'Administración'},
                
                # Recursos Humanos
                {'nombre': 'Gerente de RRHH', 'departamento': 'Recursos Humanos'},
                {'nombre': 'Especialista en Nómina', 'departamento': 'Recursos Humanos'},
                {'nombre': 'Reclutador', 'departamento': 'Recursos Humanos'},
                
                # Finanzas
                {'nombre': 'Contador', 'departamento': 'Finanzas'},
                {'nombre': 'Analista Financiero', 'departamento': 'Finanzas'},
                
                # Producción
                {'nombre': 'Supervisor de Producción', 'departamento': 'Producción'},
                {'nombre': 'Operador de Máquina', 'departamento': 'Producción'},
                {'nombre': 'Técnico de Proceso', 'departamento': 'Producción'},
                
                # Calidad
                {'nombre': 'Inspector de Calidad', 'departamento': 'Calidad'},
                {'nombre': 'Auditor Interno', 'departamento': 'Calidad'},
                
                # Mantenimiento
                {'nombre': 'Técnico de Mantenimiento', 'departamento': 'Mantenimiento'},
                {'nombre': 'Electricista Industrial', 'departamento': 'Mantenimiento'},
                
                # Logística
                {'nombre': 'Coordinador de Almacén', 'departamento': 'Logística'},
                {'nombre': 'Montacarguista', 'departamento': 'Logística'},
            ]
            
            for puesto_data in puestos_data:
                dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
                if dept:
                    Puesto.objects.create(
                        nombre=puesto_data['nombre'],
                        departamento=dept
                    )
            
            # CREAR SUSCRIPCIÓN BÁSICA AUTOMÁTICA
            try:
                from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
                from django.utils import timezone
                from datetime import timedelta
                
                # Buscar un plan básico o crear uno por defecto
                plan_basico = PlanSuscripcion.objects.filter(
                    nombre__icontains='básico',
                    status=True
                ).first()
                
                if not plan_basico:
                    plan_basico = PlanSuscripcion.objects.filter(
                        status=True
                    ).first()
                
                if not plan_basico:
                    # Crear plan básico por defecto
                    plan_basico = PlanSuscripcion.objects.create(
                        nombre="Básico",
                        descripcion="Plan básico para empresas nuevas",
                        duracion=30,
                        precio=499.00,
                        status=True
                    )
                
                # Crear suscripción automática
                fecha_inicio = timezone.now().date()
                fecha_fin = fecha_inicio + timedelta(days=plan_basico.duracion)
                
                suscripcion = SuscripcionEmpresa.objects.create(
                    empresa=empresa,
                    plan_suscripcion=plan_basico,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    estado='Activa',
                    status=True
                )
                
                # Crear pago automático como completado
                Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan_basico.precio,
                    monto_pago=plan_basico.precio,
                    estado_pago='Completado',
                    fecha_pago=timezone.now(),
                    transaccion_id=f"AUTO-{empresa.empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    usuario=user  # Vincular el pago con el usuario que registró la empresa
                )
                
            except Exception as e:
                # Si falla la creación de la suscripción, solo logear el error
                # pero no fallar la creación de la empresa
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error creando suscripción automática: {str(e)}")
            
            return empresa

# Serializers para PLANTAS, DEPARTAMENTOS Y PUESTOS
class PlantaSerializer(serializers.ModelSerializer):
    empresa_id = serializers.IntegerField(source='empresa.empresa_id', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Planta
        fields = ['planta_id', 'nombre', 'direccion', 'fecha_registro', 'status', 'empresa_id', 'empresa_nombre']

class DepartamentoSerializer(serializers.ModelSerializer):
    planta_id = serializers.IntegerField(source='planta.planta_id', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    
    class Meta:
        model = Departamento
        fields = ['departamento_id', 'nombre', 'descripcion', 'fecha_registro', 'status', 'planta_id', 'planta_nombre']
        read_only_fields = ['departamento_id', 'fecha_registro']

class PuestoSerializer(serializers.ModelSerializer):
    departamento_id = serializers.IntegerField(source='departamento.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Puesto
        fields = ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento_id', 'departamento_nombre']
        read_only_fields = ['puesto_id']

# Serializers para EMPLEADOS
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 
                 'genero', 'antiguedad', 'status', 'puesto', 'departamento', 'planta']

class EmpleadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 
                 'genero', 'antiguedad', 'puesto', 'departamento', 'planta']

# Serializers para crear registros (sin campos read-only)
class PlantaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ['nombre', 'direccion']  # NO incluir empresa, se asigna automáticamente

class DepartamentoCreateSerializer(serializers.ModelSerializer):
    planta_id = serializers.IntegerField()
    
    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion', 'planta_id']
    
    def validate_nombre(self, value):
        """Validar y normalizar el nombre del departamento"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del departamento es requerido")
        
        # Normalizar espacios y asegurar UTF-8
        nombre_limpio = value.strip()
        if len(nombre_limpio) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        if len(nombre_limpio) > 64:
            raise serializers.ValidationError("El nombre no puede exceder 64 caracteres")
        
        return nombre_limpio
    
    def validate_planta_id(self, value):
        """Validar que la planta existe"""
        try:
            planta = Planta.objects.get(planta_id=value)
            return value
        except Planta.DoesNotExist:
            raise serializers.ValidationError("La planta especificada no existe")
    
    def validate(self, data):
        """Validar que no exista un departamento con el mismo nombre en la misma planta"""
        nombre = data.get('nombre')
        planta_id = data.get('planta_id')
        
        if nombre and planta_id:
            try:
                planta = Planta.objects.get(planta_id=planta_id)
                if Departamento.objects.filter(nombre=nombre, planta=planta).exists():
                    raise serializers.ValidationError({
                        'nombre': 'Ya existe un departamento con este nombre en la planta seleccionada'
                    })
            except Planta.DoesNotExist:
                pass  # El error se maneja en validate_planta_id
        
        return data
    
    def create(self, validated_data):
        planta_id = validated_data.pop('planta_id')
        planta = Planta.objects.get(planta_id=planta_id)
        return Departamento.objects.create(planta=planta, **validated_data)

class PuestoCreateSerializer(serializers.ModelSerializer):
    departamento_id = serializers.IntegerField()
    
    class Meta:
        model = Puesto
        fields = ['nombre', 'descripcion', 'departamento_id']
    
    def validate_departamento_id(self, value):
        """Validar que el departamento existe"""
        try:
            departamento = Departamento.objects.get(departamento_id=value)
            return value
        except Departamento.DoesNotExist:
            raise serializers.ValidationError("El departamento especificado no existe")
    
    def validate(self, data):
        """Validar que no exista un puesto con el mismo nombre en el mismo departamento"""
        nombre = data.get('nombre')
        departamento_id = data.get('departamento_id')
        
        if nombre and departamento_id:
            try:
                departamento = Departamento.objects.get(departamento_id=departamento_id)
                if Puesto.objects.filter(nombre=nombre, departamento=departamento).exists():
                    raise serializers.ValidationError({
                        'nombre': 'Ya existe un puesto con este nombre en el departamento seleccionado'
                    })
            except Departamento.DoesNotExist:
                pass  # El error se maneja en validate_departamento_id
        
        return data
    
    def create(self, validated_data):
        departamento_id = validated_data.pop('departamento_id')
        departamento = Departamento.objects.get(departamento_id=departamento_id)
        return Puesto.objects.create(departamento=departamento, **validated_data)
