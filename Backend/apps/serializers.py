# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import string
import random
import traceback
# Agregar import específico para evitar conflictos
try:
    from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
    from apps.subscriptions.models import PlanSuscripcion
except ImportError as e:
    print(f"Error importing models: {e}")

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
                user = User.objects.create_user(
                    username=usuario,
                    email=validated_data.get('email_contacto', ''),
                    password=password
                )
                print(f"✅ PASO 3: Usuario Django creado - ID: {user.id}")
                
                # Crear perfil de usuario
                user_profile = PerfilUsuario.objects.create(
                    user=user,
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
                planta_principal = Planta.objects.create(
                    nombre='Planta Principal',
                    empresa=empresa,
                    direccion=empresa.direccion,  # Misma dirección que la empresa
                    status=True
                )
                print(f"✅ PASO 6: Planta principal creada - ID: {planta_principal.planta_id}")
                
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
                    print(f"✅ PASO 7.{len(departamentos)}: Departamento creado - {dept.nombre}")
                
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
                
                puestos_creados = 0
                for puesto_data in puestos_data:
                    dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
                    if dept:
                        Puesto.objects.create(
                            nombre=puesto_data['nombre'],
                            departamento=dept
                        )
                        puestos_creados += 1
                
                print(f"✅ PASO 8: {puestos_creados} puestos creados")
                
                # CREAR SUSCRIPCIÓN BÁSICA AUTOMÁTICA - Opcional, no debe fallar el registro
                try:
                    from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
                    from django.utils import timezone
                    from datetime import timedelta
                    
                    print("🔄 PASO 9: Iniciando creación de suscripción automática...")
                    
                    # Buscar plan básico existente
                    plan_basico = PlanSuscripcion.objects.filter(
                        nombre__icontains="básico"
                    ).first()
                    
                    # Si no existe, crear uno básico
                    if not plan_basico:
                        plan_basico = PlanSuscripcion.objects.create(
                            nombre="Plan Básico",
                            descripcion="Plan básico para empresas nuevas - Prueba gratuita",
                            duracion=30,
                            precio=0.00,  # Plan gratuito inicial
                            status=True
                        )
                        print(f"✅ PASO 9.1: Plan básico creado - ID: {plan_basico.plan_id}")
                    else:
                        print(f"✅ PASO 9.1: Plan básico encontrado - {plan_basico.nombre}")
                    
                    # Crear suscripción automática de prueba
                    fecha_inicio = timezone.now().date()
                    fecha_fin = fecha_inicio + timedelta(days=30)  # 30 días de prueba
                    
                    suscripcion = SuscripcionEmpresa.objects.create(
                        empresa=empresa,
                        plan_suscripcion=plan_basico,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        estado='Activa',
                        status=True
                    )
                    print(f"✅ PASO 9.2: Suscripción de prueba creada - ID: {suscripcion.suscripcion_id}")
                    
                    # Crear pago automático (gratuito para prueba)
                    pago = Pago.objects.create(
                        suscripcion=suscripcion,
                        costo=0.00,
                        monto_pago=0.00,
                        estado_pago='Completado',
                        fecha_pago=timezone.now(),
                        transaccion_id=f"TRIAL-{empresa.empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                        usuario=user
                    )
                    print(f"✅ PASO 9.3: Pago de prueba creado - ID: {pago.pago_id}")
                    
                except Exception as e:
                    # La suscripción es opcional - no debe hacer fallar el registro
                    print(f"⚠️ PASO 9 ADVERTENCIA: Error creando suscripción automática: {str(e)}")
                    print("📝 La empresa se ha creado exitosamente, la suscripción se puede agregar después")
                    # No hacer raise - continuar con el registro
                
                print(f"🎉 ÉXITO TOTAL: Empresa {empresa.nombre} creada con ID {empresa.empresa_id}")
                
                # Verificar que la empresa realmente existe en la base de datos
                empresa_verificacion = Empresa.objects.get(empresa_id=empresa.empresa_id)
                print(f"🔍 VERIFICACIÓN: Empresa encontrada en BD - {empresa_verificacion.nombre}")
                
                return empresa
                
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: Error durante la creación: {str(e)}")
            traceback.print_exc()
            raise e

# Serializers para PLANTAS, DEPARTAMENTOS Y PUESTOS
class PlantaSerializer(serializers.ModelSerializer):
    empresa_id = serializers.IntegerField(source='empresa.empresa_id', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Planta
        fields = ['planta_id', 'nombre', 'direccion', 'status', 'empresa_id', 'empresa_nombre']

class DepartamentoSerializer(serializers.ModelSerializer):
    planta_id = serializers.IntegerField(source='planta.planta_id', read_only=True)
    planta_nombre = serializers.CharField(source='planta.nombre', read_only=True)
    
    class Meta:
        model = Departamento
        fields = ['departamento_id', 'nombre', 'descripcion', 'status', 'planta_id', 'planta_nombre']
        read_only_fields = ['departamento_id']

class PuestoSerializer(serializers.ModelSerializer):
    departamento_id = serializers.IntegerField(source='departamento.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Puesto
        fields = ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento_id', 'departamento_nombre']
        read_only_fields = ['puesto_id']

# Serializers para EMPLEADOS
class EmpleadoSerializer(serializers.ModelSerializer):
    # Acceso a través de la estructura real: puesto->departamento->planta->empresa
    empresa_id = serializers.IntegerField(source='puesto.departamento.planta.empresa.empresa_id', read_only=True)
    empresa_nombre = serializers.CharField(source='puesto.departamento.planta.empresa.nombre', read_only=True)
    planta_id = serializers.IntegerField(source='puesto.departamento.planta.planta_id', read_only=True)
    planta_nombre = serializers.CharField(source='puesto.departamento.planta.nombre', read_only=True)
    departamento_id = serializers.IntegerField(source='puesto.departamento.departamento_id', read_only=True)
    departamento_nombre = serializers.CharField(source='puesto.departamento.nombre', read_only=True)
    puesto_id = serializers.IntegerField(source='puesto.puesto_id', read_only=True)
    puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)
    numero_empleado = serializers.SerializerMethodField()
    
    def get_numero_empleado(self, obj):
        """Generar número de empleado basado en ID"""
        return f"EMP-{obj.empleado_id:06d}"
    
    class Meta:
        model = Empleado
        fields = [
            'empleado_id', 'numero_empleado', 'nombre', 'apellido_paterno', 'apellido_materno',
            'email', 'telefono', 'fecha_ingreso', 'status',
            'empresa_id', 'empresa_nombre',
            'planta_id', 'planta_nombre',
            'departamento_id', 'departamento_nombre',
            'puesto_id', 'puesto_nombre'
        ]

class EmpleadoCreateSerializer(serializers.ModelSerializer):
    # Campos extra que envía el frontend pero no están en el modelo
    departamento = serializers.IntegerField(required=False)
    planta = serializers.IntegerField(required=False)
    
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono', 'fecha_ingreso', 'puesto', 'departamento', 'planta']
    
    def validate_email(self, value):
        """Validar email y manejar valores vacíos"""
        if value == '' or value is None:
            return None  # Convertir string vacío a None
        return value
    
    def validate_telefono(self, value):
        """Validar teléfono y manejar valores vacíos"""
        if value == '' or value is None:
            return None  # Convertir string vacío a None
        return value
    
    def validate_puesto(self, value):
        """Validar que el puesto existe y está activo"""
        try:
            from apps.users.models import Puesto
            
            # Si ya es un objeto Puesto, validar que esté activo
            if hasattr(value, 'puesto_id'):
                if not value.status:
                    raise serializers.ValidationError("El puesto seleccionado está inactivo")
                return value
            
            # Si es un ID (int), buscar el objeto
            if isinstance(value, (int, str)):
                puesto_id = int(value) if isinstance(value, str) else value
                puesto = Puesto.objects.get(puesto_id=puesto_id, status=True)
                return puesto
                
            raise serializers.ValidationError("Valor de puesto inválido")
            
        except Puesto.DoesNotExist:
            raise serializers.ValidationError(f"El puesto con ID {value} no existe o está inactivo")
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError(f"ID de puesto inválido: {value}")
        except Exception as e:
            raise serializers.ValidationError(f"Error validando puesto: {e}")
    
    def validate_email(self, value):
        """Validar email y manejar valores vacíos"""
        if value == '' or value is None:
            return None  # Convertir string vacío a None
        
        # Para updates, permitir el mismo email del empleado actual
        if self.instance and self.instance.email == value:
            return value
            
        # Validar unicidad solo para emails nuevos
        from apps.users.models import Empleado
        if Empleado.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un empleado con este email")
        
        return value
    
    def to_internal_value(self, data):
        """Procesar datos antes de la validación de Django"""
        # Hacer una copia para no modificar el original
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # Convertir strings vacíos a None para campos opcionales
        optional_fields = ['apellido_materno', 'email', 'telefono', 'fecha_ingreso']
        for field in optional_fields:
            if field in data and data[field] == '':
                data[field] = None
        
        # Convertir campos numéricos (IDs) de string a int, solo si son strings
        numeric_fields = ['puesto', 'departamento', 'planta']
        for field in numeric_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = int(data[field]) if data[field] else None
                except (ValueError, TypeError):
                    # Si no se puede convertir, dejar el valor original
                    pass
                
        # Si fecha_ingreso es None, usar fecha actual
        if data.get('fecha_ingreso') is None:
            from datetime import date
            data['fecha_ingreso'] = date.today().isoformat()
        
        return super().to_internal_value(data)
    
    def validate(self, data):
        """Validación personalizada para empleados"""        
        # Si no se proporciona fecha_ingreso, usar la fecha actual
        if not data.get('fecha_ingreso'):
            from datetime import date
            data['fecha_ingreso'] = date.today()
            
        return data
    
    def create(self, validated_data):
        """Crear empleado eliminando campos que no están en el modelo"""
        import logging
        logger = logging.getLogger(__name__)
        
        logger.debug(f"EmpleadoCreateSerializer.create - Datos recibidos: {validated_data}")
        
        # Eliminar campos que no están en el modelo Empleado
        validated_data.pop('genero', None)
        validated_data.pop('departamento', None)
        validated_data.pop('planta', None)
        
        logger.debug(f"EmpleadoCreateSerializer.create - Datos para crear: {validated_data}")
        
        try:
            empleado = super().create(validated_data)
            logger.debug(f"EmpleadoCreateSerializer.create - Empleado creado exitosamente: {empleado}")
            return empleado
        except Exception as e:
            logger.error(f"EmpleadoCreateSerializer.create - Error creando empleado: {e}")
            raise
    
    def update(self, instance, validated_data):
        """Actualizar empleado eliminando campos que no están en el modelo"""
        import logging
        logger = logging.getLogger(__name__)
        
        logger.debug(f"EmpleadoCreateSerializer.update - Datos recibidos: {validated_data}")
        logger.debug(f"EmpleadoCreateSerializer.update - Instancia actual: {instance}")
        
        # Eliminar campos que no están en el modelo Empleado
        validated_data.pop('departamento', None)
        validated_data.pop('planta', None)
        
        logger.debug(f"EmpleadoCreateSerializer.update - Datos para actualizar: {validated_data}")
        
        try:
            empleado = super().update(instance, validated_data)
            logger.debug(f"EmpleadoCreateSerializer.update - Empleado actualizado exitosamente: {empleado}")
            return empleado
        except Exception as e:
            logger.error(f"EmpleadoCreateSerializer.update - Error actualizando empleado: {e}")
            raise

# Serializers para crear registros (sin campos read-only)
class PlantaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ['nombre', 'direccion']  # NO incluir empresa, se asigna automáticamente

class PlanSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanSuscripcion
        fields = '__all__'

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
