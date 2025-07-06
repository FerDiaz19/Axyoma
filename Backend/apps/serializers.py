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
