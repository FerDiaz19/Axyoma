from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Empresa, Empleado, PerfilUsuario, Planta, 
    Departamento, Puesto, AdminPlanta
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser']


class EmpresaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='administrador.correo', read_only=True)
    
    class Meta:
        model = Empresa
        fields = ['empresa_id', 'nombre', 'rfc', 'direccion', 'status', 'administrador', 'usuario_username', 'fecha_registro']
        read_only_fields = ['empresa_id', 'fecha_registro']


class EmpleadoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='puesto.departamento.nombre', read_only=True)
    puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='puesto.departamento.planta.nombre', read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 
                 'email', 'telefono', 'status', 'puesto',
                 'departamento_nombre', 'puesto_nombre', 'planta_nombre']
        read_only_fields = ['empleado_id']


class EmpleadoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear empleados"""
    
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono', 'fecha_ingreso', 'puesto']
    
    def create(self, validated_data):
        # Si no se proporciona fecha_ingreso, usar la fecha actual
        if 'fecha_ingreso' not in validated_data or validated_data['fecha_ingreso'] is None:
            from datetime import date
            validated_data['fecha_ingreso'] = date.today()
        
        return super().create(validated_data)


# ====================== SERIALIZERS PARA TODOS LOS MODELOS ======================

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = ['id', 'user', 'username', 'email', 'tipo_usuario', 'activo', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class PlantaSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Planta
        fields = ['planta_id', 'nombre', 'direccion', 'fecha_registro', 'status', 'empresa', 'empresa_nombre']
        read_only_fields = ['planta_id', 'fecha_registro']


class DepartamentoSerializer(serializers.ModelSerializer):
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    empresa_nombre = serializers.CharField(source='planta.empresa.nombre', read_only=True)
    
    class Meta:
        model = Departamento
        fields = ['departamento_id', 'nombre', 'descripcion', 'fecha_registro', 'status', 'planta', 'planta_nombre', 'empresa_nombre']
        read_only_fields = ['departamento_id', 'fecha_registro']


class PuestoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    planta_nombre = serializers.CharField(source='departamento.planta.nombre', read_only=True)
    
    class Meta:
        model = Puesto
        fields = ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento', 
                 'departamento_nombre', 'planta_nombre']
        read_only_fields = ['puesto_id']


class AdminPlantaSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.user.username', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    
    class Meta:
        model = AdminPlanta
        fields = ['id', 'usuario', 'usuario_username', 'planta', 'planta_nombre', 
                 'fecha_asignacion', 'status', 'password_temporal']
        read_only_fields = ['id', 'fecha_asignacion']


# ====================== SERIALIZERS DE CREACIÓN ======================

class EmpresaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear empresas"""
    
    class Meta:
        model = Empresa
        fields = ['nombre', 'rfc', 'direccion']


class PlantaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear plantas con estructura automática"""
    
    class Meta:
        model = Planta
        fields = ['nombre', 'direccion', 'empresa']


class DepartamentoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear departamentos"""
    
    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion', 'planta']


class PuestoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear puestos"""
    
    class Meta:
        model = Puesto
        fields = ['nombre', 'descripcion', 'departamento']
