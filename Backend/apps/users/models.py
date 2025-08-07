
# ---------------------------------------------------------------------------- #

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.subscriptions.models import SuscripcionEmpresa

# ---------------------------------------------------------------------------- #

''' Modelos de usuarios, corregidos por Ed Rubio. '''

# ---------------------------------------------------------------------------- #

class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ( 'superadmin', 'Administrador principal' ),
        ( 'admin-empresa', 'Administrador de empresa '),
        ( 'admin-planta', 'Administrador de planta' ),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name='Nombre(s)')
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido materno")
    correo = models.EmailField(max_length=255, unique=True, verbose_name="Correo electrónico")
    nivel_usuario = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nivel de Usuario")
    status = models.BooleanField(default=True, verbose_name='Estado de acceso a la plataforma')

    admin_empresa = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        db_column='admin_empresa',
        verbose_name="Usuario creador (administrador de empresa)",
        help_text="Administrador de empresa que ha creado a este usuario."
    )

    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE,
        db_column='user_id',
        related_name='perfil',
        verbose_name='ID del usaurio ligada a este perfil.'
    )

    # Metadatos:
    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = [ 'nombre', 'nivel_usuario' ]

        indexes = [
            models.Index(fields=['nivel_usuario']),
            models.Index(fields=['correo']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.nivel_usuario == 'admin-planta' and not self.admin_empresa:
            raise ValidationError("El usuario ha de tener un administrador de empresaa asignado.")
        if self.nivel_usuario == 'superadmin' and self.admin_empresa:
            raise ValidationError('Un administrador principal no puede estar lugador a un administrador de empresa.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        ''' Nombre completo formateado. '''
        nombres = [ self.nombre, self.apellido_paterno ]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} - ({self.get_nivel_usuario_display()})'

# ---------------------------------------------------------------------------- #

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=65, unique=True, verbose_name="Nombre de la empresa")
    rfc = models.CharField(max_length=16, unique=True, verbose_name="RFC de la empresa")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección física de la empresa")
    logotipo = models.URLField(max_length=255, blank=True, null=True, verbose_name="URL del Logotipo")
    email_contacto = models.EmailField(max_length=128, blank=True, null=True, verbose_name="Correo electrónico de contacto")
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de teléfono de contacto")

    # ! Olvidaste este campo.
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name='¿La empresa se encuentra activa en el sistema?')

    administrador = models.OneToOneField(
        PerfilUsuario, on_delete=models.PROTECT,
        db_column='administrador',
        verbose_name="Administrador de la empresa",
        limit_choices_to={ 'nivel_usuario': 'admin-empresa' }
    )

    class Meta:
        db_table = 'empresas'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = [ 'nombre', 'status' ]
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['rfc']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.administrador and self.administrador.nivel_usuario != 'admin-empresa':
            raise ValidationError("El administrador debe estar registrado como administrador de empresa.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def tiene_suscripcion_activa(self):
        ''' Verifica si la empresa tiene una suscripción activa. '''
        try:
            return SuscripcionEmpresa.objects.filter(
                empresa=self, estado='activa').exists()
        except ImportError:
            return False

    @property
    def suscripcion_activa(self):
        ''' Obtiene la suscripción activa más reciente. '''
        try:
            return SuscripcionEmpresa.objects.filter(
                empresa=self,
                estado='activa'
            ).order_by('-fecha_inicio').first()
        except ImportError:
            return None

    @property
    def total_plantas(self):
        ''' Número total de plantas activas. '''
        return self.plantas.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos. '''
        return sum(planta.total_empleados for planta in self.plantas.filter(status=True))

    def __str__(self):
        return f'{self.nombre} - ({self.status})'

# ---------------------------------------------------------------------------- #

class Planta(models.Model):
    planta_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre de la Planta")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    status = models.BooleanField(default=True, verbose_name="Activa")

    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE,
        db_column='empresa',
        related_name='plantas', verbose_name="Empresa"
    )

    class Meta:
        db_table = 'plantas'
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        ordering = [ 'empresa', 'nombre', 'status' ]
        unique_together = [[ 'empresa', 'nombre' ]]

        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['status'])
        ]

    @property
    def total_departamentos(self):
        ''' Número total de departamentos activos. '''
        return self.departamentos.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en la planta. '''
        return sum(depto.total_empleados for depto in self.departamentos.filter(status=True))

    def __str__(self):
        return f"{self.nombre} - ({self.empresa.nombre})"

# ---------------------------------------------------------------------------- #

class AdminPlanta(models.Model):
    id = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        PerfilUsuario, on_delete=models.CASCADE,
        db_column='usuario_id', verbose_name="Administrador de planta",
        limit_choices_to={ 'nivel_usuario': 'admin-planta' },
    )

    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE,
        db_column='planta_id', verbose_name="Planta asignada"
    )

    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de asignación")
    status = models.BooleanField(default=True, verbose_name='¿El usuario puede administrar esta planta?')

    password_temporal = models.CharField(
        max_length=128, blank=True, null=True,
        verbose_name="Contraseña temporal",
        help_text="Contraseña temporal generada automáticamente"
    )

    class Meta:
        db_table = 'admin_plantas'
        verbose_name = "Administrador de planta"
        verbose_name_plural = "Administradores de plantas"
        unique_together = [[ 'usuario', 'planta' ]]
        ordering = [ 'planta', 'usuario' ]
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['planta']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.usuario and self.usuario.nivel_usuario != 'admin-planta':
            raise ValidationError("El usuario debe estar registrado como administrador de planta.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.planta.nombre}"

# ---------------------------------------------------------------------------- #

class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, verbose_name="Nombre del departamento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    status = models.BooleanField(default=True, verbose_name="¿El departamento de esta empresa se encuentra acitvo?")

    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE,
        db_column='planta',
        related_name='departamentos', verbose_name="Planta"
    )

    class Meta:
        db_table = 'departamentos'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = [ 'planta', 'nombre' ]
        unique_together = [[ 'planta', 'nombre' ]]
        indexes = [
            models.Index(fields=['planta']),
            models.Index(fields=['status'])
        ]

    def clean(self):
        if self.nombre:
            self.nombre = self.nombre.strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_puestos(self):
        ''' Número total de puestos activos. '''
        return self.puestos.filter(status=True).count()

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en el departamento. '''
        return sum(puesto.total_empleados for puesto in self.puestos.filter(status=True))

    def __str__(self):
        return f"{self.nombre} - {self.planta.nombre}"


class Puesto(models.Model):
    puesto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, verbose_name="Nombre del puesto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del puesto")
    status = models.BooleanField(default=True, verbose_name="¿El puesto se encuentra activo?")

    # Relación con departamento
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE,
        db_column='departamento',
        related_name='puestos', verbose_name="Departamento"
    )

    class Meta:
        db_table = 'puestos'
        verbose_name = "Puesto"
        verbose_name_plural = "Puestos"
        ordering = [ 'nombre' ]
        unique_together = [[ 'nombre', 'departamento' ]]
        indexes = [
            models.Index(fields=['departamento']),
            models.Index(fields=['status'])
        ]

    @property
    def total_empleados(self):
        ''' Número total de empleados activos en el puesto. '''
        return self.empleados.filter(status=True).count()

    @property
    def empresa(self):
        ''' Empresa a la que pertenece el puesto. '''
        return self.departamento.planta.empresa

    @property
    def planta(self):
        ''' Planta a la que pertenece el puesto. '''
        return self.departamento.planta

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre}) : {self.empresa.nombre} ({self.departamento.planta.nombre})"

# ---------------------------------------------------------------------------- #

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=64, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=64, blank=True, null=True, verbose_name="Apellido materno")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de teléfono")
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de Ingreso")
    status = models.BooleanField(default=True, verbose_name="¿El empleado se encuentra activo?")

    puesto = models.ForeignKey(
        Puesto, on_delete=models.CASCADE,
        db_column='puesto',
        related_name='empleados', verbose_name="Puesto"
    )

    class Meta:
        db_table = 'empleados'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = [ 'nombre', 'puesto', 'status' ]
        indexes = [
            models.Index(fields=[ 'puesto' ]),
            models.Index(fields=[ 'email' ]),
            models.Index(fields=[ 'status' ])
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[ 'email' ],
                condition=models.Q(email__isnull=False) & ~models.Q(email=''),
                name='unique_employee_email'
            )
        ]

    @property
    def nombre_completo(self):
        ''' Nombre completo formateado. '''
        nombres = [ self.nombre, self.apellido_paterno ]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return " ".join(nombres)

    @property
    def empresa(self):
        ''' Empresa a la que pertenece el empleado. '''
        return self.puesto.empresa

    @property
    def planta(self):
        ''' Planta a la que pertenece el empleado. '''
        return self.puesto.planta

    @property
    def departamento(self):
        ''' Departamento al que pertenece el empleado. '''
        return self.puesto.departamento

    def __str__(self):
        return f"{self.nombre_completo} - {self.puesto.nombre}"

# ---------------------------------------------------------------------------- #
