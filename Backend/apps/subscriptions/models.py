
# ---------------------------------------------------------------------------- #

from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

# ---------------------------------------------------------------------------- #

''' Modelos de usuarios, corregidos por Ed Rubio. '''

# ---------------------------------------------------------------------------- #

class PlanSuscripcion(models.Model):
    plan_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Plan")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    duracion = models.IntegerField(help_text="Duración en días", verbose_name="Duración")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    status = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'planes'
        verbose_name = "Plan de Suscripción"
        verbose_name_plural = "Planes de Suscripción"
        ordering = ['precio']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# ---------------------------------------------------------------------------- #

class SuscripcionEmpresa(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(
        'users.Empresa', on_delete=models.CASCADE,
        verbose_name="Empresa", db_column='empresa'
    )
    plan = models.ForeignKey(
        PlanSuscripcion, on_delete=models.PROTECT,
        verbose_name="Plan de suscripción"
    )

    fecha_inicio = models.DateField(auto_now_add=True, verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(null=True,  blank=True, verbose_name="Fecha de fin")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, blank=True, null=True, verbose_name="Estado")
    status = models.BooleanField(default=True, verbose_name="Activa")  # Campo agregado para coincidir con BD
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        db_table = 'suscripciones'
        verbose_name = "Suscripción de empresa"
        verbose_name_plural = "Suscripciones de empresas"
        ordering = [ '-fecha_inicio', 'empresa' ]

    def __str__(self):
        return f"Suscripción {self.empresa.nombre} - {self.plan.nombre}"

    @property
    def esta_activa(self):
        """Verifica si la suscripción está activa"""
        if not self.status:  # Campo status debe ser True
            return False
        if self.estado != 'activa':
            return False
        if self.fecha_fin and self.fecha_fin < timezone.now().date():
            return False
        return True

    @property
    def dias_restantes(self):
        """Calcula los días restantes de la suscripción"""
        if not self.fecha_fin:
            return 0
        delta = self.fecha_fin - timezone.now().date()
        return max(0, delta.days)

    @property
    def esta_por_vencer(self):
        """Verifica si la suscripción está por vencer (7 días o menos)"""
        return 0 < self.dias_restantes <= 7

    def renovar_suscripcion(self):
        """Renueva la suscripción por la duración del plan"""
        if self.fecha_fin:
            nueva_fecha = self.fecha_fin + timedelta(days=self.plan.duracion)
        else:
            nueva_fecha = timezone.now().date() + timedelta(days=self.plan.duracion)

        self.fecha_fin = nueva_fecha
        self.estado = 'activa'
        self.status = True
        self.save()

    def save(self, *args, **kwargs):
        if self.fecha_inicio and self.plan and self.plan.duracion is not None:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.plan.duracion)

        self.full_clean()
        super().save(*args, **kwargs)

# ---------------------------------------------------------------------------- #

class Pago(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('Completado', 'Completado'),
        ('Pendiente', 'Pendiente'),
        ('Cancelado', 'Cancelado'),
        ('Fallido', 'Fallido'),
    ]
    METODO_PAGO_CHOICES = [
        ('Crédito', 'Crédito'),
        ('Débito', 'Débito'),
        ('Transferencia', 'Transferencia'),
        ('Pago online', 'Pago online'),
    ]

    pago_id = models.AutoField(primary_key=True)
    suscripcion = models.ForeignKey(
        SuscripcionEmpresa, on_delete=models.SET_NULL, null=True,
        db_column='suscripcion_id', verbose_name="Suscripción"
    )

    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente', verbose_name="Estado del Pago")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")

    transaccion_id = models.CharField(max_length=100, blank=True, null=True,
        verbose_name="ID de Transacción", db_column='referencia_pago')

    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Usuario que realizó el pago"
    )

    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='Pago online', verbose_name="Método usado en el pago")

    class Meta:
        db_table = 'pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        usuario_info = f" - {self.usuario.username}" if self.usuario else ""
        return f"Pago ${self.monto_pago} - {self.suscripcion.empresa.nombre}{usuario_info}"

# ---------------------------------------------------------------------------- #

# MODELOS ADICIONALES PARA EXPORTACIÓN CSV (SIN AFECTAR LOS ORIGINALES) ------ #

class SuscripcionEmpresaExport(models.Model):
    """
        Modelo SOLO para exportación CSV - SIN relaciones complejas
        NO AFECTA los modelos originales usados por empresas
    """
    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.IntegerField()  # FK simple como integer
    plan = models.IntegerField()     # FK simple como integer
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suscripciones_empresa'
        managed = False # Django NO gestiona esta tabla

    def __str__(self):
        return f"Exportación de suscripción: {self.suscripcion_id} ({self.empresa.nombre} - {self.plan.nombre})"

# ---------------------------------------------------------------------------- #

class PagoExport(models.Model):
    """
        Modelo SOLO para exportación CSV - SIN relaciones complejas
        NO AFECTA los modelos originales usados por empresas
    """
    ESTADO_PAGO_CHOICES = [
        ('Completado', 'Completado'),
        ('Pendiente', 'Pendiente'),
        ('Cancelado', 'Cancelado'),
        ('Fallido', 'Fallido'),
    ]
    METODO_PAGO_CHOICES = [
        ('Crédito', 'Crédito'),
        ('Débito', 'Débito'),
        ('Transferencia', 'Transferencia'),
        ('Pago online', 'Pago online'),
    ]

    pago_id = models.AutoField(primary_key=True)
    suscripcion = models.IntegerField()  # FK simple como integer
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES)
    fecha_pago = models.DateTimeField()

    transaccion_id = models.CharField(max_length=100)
    usuario = models.IntegerField()
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)


    class Meta:
        db_table = 'pagos'
        managed = False # Django NO gestiona esta tabla

    def __str__(self):
        return f"Exportación de pago: {self.pago_id} - ${self.monto_pago}"

# ---------------------------------------------------------------------------- #
