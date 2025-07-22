from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Empresa, Empleado


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser']


class EmpresaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'tipo', 'activa', 'usuario', 'usuario_username', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono', 'fecha_ingreso', 'fecha_registro', 'status', 'puesto']
        read_only_fields = ['empleado_id', 'fecha_registro']


class EmpleadoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear empleados con usuario"""
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Empleado
        fields = ['nombre', 'email', 'puesto', 'empresa', 'username', 'password']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=password,
            first_name=validated_data['nombre'].split()[0] if validated_data['nombre'] else '',
            last_name=' '.join(validated_data['nombre'].split()[1:]) if len(validated_data['nombre'].split()) > 1 else ''
        )
        
        # Crear empleado
        empleado = Empleado.objects.create(
            usuario=user,
            **validated_data
        )
        
        return empleado
