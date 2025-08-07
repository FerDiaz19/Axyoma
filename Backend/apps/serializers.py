
# ---------------------------------------------------------------------------- #

import traceback
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from apps.users.models import *
from apps.subscriptions.models import *

# ---------------------------------------------------------------------------- #

# Serializers para LOGIN
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# ---------------------------------------------------------------------------- #

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
        import traceback

        print(f"🔄 INICIO: Creando empresa con datos: {validated_data}")

        try:
            with transaction.atomic():
                # Extraer datos del usuario
                usuario = validated_data.pop('usuario')
                password = validated_data.pop('password')
                nombre_completo = validated_data.pop('nombre_completo')

                print(f"🔄 PASO 1: Datos extraídos - Usuario: {usuario}, Nombre: {nombre_completo}")

                # Separar el nombre completo (manejar espacios múltiples)
                nombres = [n.strip() for n in nombre_completo.strip().split() if n.strip()]
                nombre = nombres[0] if nombres else 'Admin'
                apellido_paterno = nombres[1] if len(nombres) > 1 else 'Empresa'
                apellido_materno = nombres[2] if len(nombres) > 2 else ''

                print(f"🔄 PASO 2: Nombres separados - '{nombre}' '{apellido_paterno}' '{apellido_materno}'")

                # Crear usuario Django
                from django.contrib.auth.models import User
                user = User.objects.create_user(
                    username=usuario,
                    email=validated_data.get('email_contacto', ''),
                    password=password
                )
                print(f"✅ PASO 3: Usuario Django creado - ID: {user.id}")

                # Crear perfil de usuario
                from apps.users.models import PerfilUsuario
                user_profile = PerfilUsuario.objects.create(
                    user_id=user,  # Corregido: usar 'user_id' en lugar de 'user'
                    nombre=nombre,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    correo=validated_data.get('email_contacto', ''),
                    nivel_usuario='admin-empresa'
                )
                print(f"✅ PASO 4: Perfil creado - ID: {user_profile.id}")

                # Crear empresa
                empresa = Empresa.objects.create(
                    administrador=user_profile,
                    **validated_data
                )
                print(f"✅ PASO 5: Empresa creada - ID: {empresa.empresa_id}, Nombre: {empresa.nombre}")

                # CREAR AUTOMÁTICAMENTE LA PLANTA PRINCIPAL
                from apps.users.models import Planta, Departamento, Puesto  # Corregido el import
                planta_principal = Planta.objects.create(
                    nombre='Planta Principal',
                    empresa=empresa,
                    direccion=empresa.direccion or 'Sin dirección especificada',
                    status=True
                )
                print(f"✅ PASO 6: Planta principal creada - ID: {planta_principal.planta_id}")

                # CREAR DEPARTAMENTOS BÁSICOS
                departamentos_data = [
                    {'nombre': 'Administración', 'descripcion': 'Gestión administrativa general'},
                    {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal y nómina'},
                    {'nombre': 'Operaciones', 'descripcion': 'Operaciones principales de la empresa'},
                ]

                departamentos = []
                for dept_data in departamentos_data:
                    try:
                        dept = Departamento.objects.create(
                            nombre=dept_data['nombre'],
                            descripcion=dept_data['descripcion'],
                            planta=planta_principal
                        )
                        departamentos.append(dept)
                        print(f"✅ PASO 7.{len(departamentos)}: Departamento creado - {dept.nombre}")
                    except Exception as e:
                        print(f"⚠️ Error creando departamento {dept_data['nombre']}: {str(e)}")

                # CREAR PUESTOS BÁSICOS
                puestos_data = [
                    {'nombre': 'Gerente General', 'departamento': 'Administración'},
                    {'nombre': 'Asistente Administrativo', 'departamento': 'Administración'},
                    {'nombre': 'Gerente de RRHH', 'departamento': 'Recursos Humanos'},
                    {'nombre': 'Supervisor', 'departamento': 'Operaciones'},
                    {'nombre': 'Empleado General', 'departamento': 'Operaciones'},
                ]

                puestos_creados = 0
                for puesto_data in puestos_data:
                    try:
                        dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
                        if dept:
                            Puesto.objects.create(
                                nombre=puesto_data['nombre'],
                                departamento=dept
                            )
                            puestos_creados += 1
                    except Exception as e:
                        print(f"⚠️ Error creando puesto {puesto_data['nombre']}: {str(e)}")

                print(f"✅ PASO 8: {puestos_creados} puestos creados")

                print(f"🎉 ÉXITO: Empresa {empresa.nombre} creada con ID {empresa.empresa_id}")
                return empresa

        except Exception as e:
            print(f"❌ ERROR CRÍTICO: Error durante la creación: {str(e)}")
            print(f"❌ Tipo de error: {type(e)}")
            traceback.print_exc()
            raise e

# ---------------------------------------------------------------------------- #

# Serializers para PLANTAS, DEPARTAMENTOS Y PUESTOS
class PlantaSerializer(serializers.ModelSerializer):
    empresa_id = serializers.IntegerField(source='empresa.empresa_id', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Planta
        fields = ['planta_id', 'nombre', 'direccion', 'status', 'empresa_id', 'empresa_nombre']

# ---------------------------------------------------------------------------- #

class DepartamentoSerializer(serializers.ModelSerializer):
    planta_id = serializers.IntegerField(source='planta.planta_id', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)

    class Meta:
        model = Departamento
        fields = ['departamento_id', 'nombre', 'descripcion', 'status', 'planta_id', 'planta_nombre']
        read_only_fields = ['departamento_id']

# ---------------------------------------------------------------------------- #

class PuestoSerializer(serializers.ModelSerializer):
    departamento_id = serializers.IntegerField(source='departamento.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Puesto
        fields = ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento_id', 'departamento_nombre']
        read_only_fields = ['puesto_id']

# ---------------------------------------------------------------------------- #

# Serializers para crear registros (sin campos read-only)
class PlantaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ['nombre', 'direccion']  # NO incluir empresa, se asigna automáticamente

# ---------------------------------------------------------------------------- #

class PlanSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanSuscripcion
        fields = '__all__'

# ---------------------------------------------------------------------------- #

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

# ---------------------------------------------------------------------------- #

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

# ---------------------------------------------------------------------------- #

# EMPLEADOS SERIALIZERS - VERSION CORREGIDA
class EmpleadoSerializer(serializers.ModelSerializer):
    """Serializer para lectura de empleados con información completa"""
    # Campos de lectura con información relacionada
    empresa_id = serializers.SerializerMethodField()
    empresa_nombre = serializers.SerializerMethodField()
    planta_id = serializers.SerializerMethodField()
    planta_nombre = serializers.SerializerMethodField()
    departamento_id = serializers.SerializerMethodField()
    departamento_nombre = serializers.SerializerMethodField()
    puesto_id = serializers.SerializerMethodField()
    puesto_nombre = serializers.SerializerMethodField()
    numero_empleado = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = [
            'empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno',
            'email', 'telefono', 'fecha_ingreso', 'status',
            'puesto', 'empresa_id', 'empresa_nombre', 'planta_id', 'planta_nombre',
            'departamento_id', 'departamento_nombre', 'puesto_id', 'puesto_nombre',
            'numero_empleado'
        ]

    def get_empresa_id(self, obj):
        if obj.puesto and obj.puesto.departamento and obj.puesto.departamento.planta:
            return obj.puesto.departamento.planta.empresa.empresa_id
        return None

    def get_empresa_nombre(self, obj):
        if obj.puesto and obj.puesto.departamento and obj.puesto.departamento.planta:
            return obj.puesto.departamento.planta.empresa.nombre
        return None

    def get_planta_id(self, obj):
        if obj.puesto and obj.puesto.departamento and obj.puesto.departamento.planta:
            return obj.puesto.departamento.planta.planta_id
        return None

    def get_planta_nombre(self, obj):
        if obj.puesto and obj.puesto.departamento and obj.puesto.departamento.planta:
            return obj.puesto.departamento.planta.nombre
        return None

    def get_departamento_id(self, obj):
        if obj.puesto and obj.puesto.departamento:
            return obj.puesto.departamento.departamento_id
        return None

    def get_departamento_nombre(self, obj):
        if obj.puesto and obj.puesto.departamento:
            return obj.puesto.departamento.nombre
        return None

    def get_puesto_id(self, obj):
        if obj.puesto:
            return obj.puesto.puesto_id
        return None

    def get_puesto_nombre(self, obj):
        if obj.puesto:
            return obj.puesto.nombre
        return None

    def get_numero_empleado(self, obj):
        return f"EMP-{obj.empleado_id:06d}"

# ---------------------------------------------------------------------------- #

class EmpleadoCreateSerializer(serializers.ModelSerializer):
    """Serializer para creación y actualización de empleados"""
    puesto = serializers.IntegerField()

    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno',
            'email', 'telefono', 'fecha_ingreso', 'puesto'
        ]

    def validate_puesto(self, value):
        """Validar que el puesto existe"""
        try:
            Puesto.objects.get(puesto_id=value)
            return value  # Retornar el ID, no el objeto
        except Puesto.DoesNotExist:
            raise serializers.ValidationError("El puesto especificado no existe")

    def validate_email(self, value):
        """Validar formato de email"""
        if value and '@' not in value:
            raise serializers.ValidationError("Formato de email inválido")
        return value

    def create(self, validated_data):
        """Crear nuevo empleado"""
        puesto_id = validated_data.pop('puesto')
        puesto = Puesto.objects.get(puesto_id=puesto_id)
        empleado = Empleado.objects.create(puesto=puesto, **validated_data)
        return empleado

    def update(self, instance, validated_data):
        """Actualizar empleado existente"""
        if 'puesto' in validated_data:
            puesto_id = validated_data.pop('puesto')
            instance.puesto = Puesto.objects.get(puesto_id=puesto_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

# ---------------------------------------------------------------------------- #
