from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from apps.users.models import Empresa

class PlanSuscripcion(models.Model):
    """
    Modelo para PLANES según la estructura real de la tabla
    """
    plan_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Plan")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    duracion = models.IntegerField(help_text="Duración en días", verbose_name="Duración")
    fecha_registro = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Registro")
    status = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'planes'
        verbose_name = "Plan de Suscripción"
        verbose_name_plural = "Planes de Suscripción"
        ordering = ['precio']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
class SuscripcionEmpresa(models.Model):
    """
    Modelo para SUSCRIPCIONES según la estructura real de la tabla
    """
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    
    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE,
        db_column='empresa',
        verbose_name="Empresa"
    )
    plan = models.ForeignKey(
        PlanSuscripcion, 
        on_delete=models.PROTECT,
        db_column='plan',
        verbose_name="Plan"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, blank=True, null=True, verbose_name="Estado")
    fecha_registro = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Registro")

    class Meta:
        db_table = 'suscripciones'
        verbose_name = "Suscripción de Empresa"
        verbose_name_plural = "Suscripciones de Empresas"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Suscripción {self.empresa.nombre} - {self.plan.nombre}"

    @property
    def esta_activa(self):
        """Verifica si la suscripción está activa"""
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
        self.save()

class Pago(models.Model):
    """
    Modelo para PAGOS según el SQL original
    """
    ESTADO_PAGO_CHOICES = [
        ('Completado', 'Completado'),
        ('Pendiente', 'Pendiente'),
        ('Cancelado', 'Cancelado'),
        ('Fallido', 'Fallido'),
    ]
    
    pago_id = models.AutoField(primary_key=True)
    suscripcion = models.ForeignKey(
        SuscripcionEmpresa, 
        on_delete=models.CASCADE,
        db_column='suscripcion_id',
        verbose_name="Suscripción"
    )
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo")
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente', verbose_name="Estado del Pago")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    transaccion_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID de Transacción")
    comprobante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comprobante de Pago")
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario que realizó el pago"
    )

    class Meta:
        db_table = 'pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        usuario_info = f" - {self.usuario.username}" if self.usuario else ""
        return f"Pago ${self.monto_pago} - {self.suscripcion.empresa.nombre}{usuario_info}"


# ============================================================================
# MODELOS ADICIONALES PARA EXPORTACIÓN CSV (SIN AFECTAR LOS ORIGINALES)
# ============================================================================

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
        managed = False  # Django NO gestiona esta tabla
        
    def __str__(self):
        return f"Suscripción Export {self.suscripcion_id}"


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
    
    pago_id = models.AutoField(primary_key=True)
    suscripcion_id = models.IntegerField()  # FK simple como integer
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES)
    fecha_pago = models.DateTimeField()
    
    class Meta:
        db_table = 'pagos'
        managed = False  # Django NO gestiona esta tabla
        
    def __str__(self):
        return f"Pago Export ${self.monto_pago}"