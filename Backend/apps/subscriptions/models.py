from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from apps.users.models import Empresa

class PlanSuscripcion(models.Model):
    """
    Modelo para tabla PLANES existente
    """
    plan_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField(help_text="Duración en días")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'planes'
        verbose_name = "Plan de Suscripción"
        verbose_name_plural = "Planes de Suscripción"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class SuscripcionEmpresa(models.Model):
    """
    Modelo para tabla SUSCRIPCIONES_EMPRESA existente con ForeignKeys
    """
    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(
        'users.Empresa',
        on_delete=models.CASCADE,
        db_column='empresa_id',
        verbose_name="Empresa"
    )
    plan_suscripcion = models.ForeignKey(
        PlanSuscripcion,
        on_delete=models.CASCADE,
        db_column='plan_id',
        verbose_name="Plan de Suscripción"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='Activa')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'suscripciones_empresa'
        verbose_name = "Suscripción de Empresa"
        verbose_name_plural = "Suscripciones de Empresas"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Suscripción {self.suscripcion_id} - {self.empresa.nombre}"

    @property
    def dias_restantes(self):
        """Calcula los días restantes de la suscripción"""
        from django.utils import timezone
        hoy = timezone.now().date()
        if self.fecha_fin >= hoy:
            return (self.fecha_fin - hoy).days
        return 0

    @property
    def esta_activa(self):
        """Verifica si la suscripción está activa"""
        from django.utils import timezone
        return self.estado == 'Activa' and self.fecha_fin >= timezone.now().date() and self.status

    @property
    def esta_por_vencer(self):
        """Verifica si la suscripción está por vencer (7 días o menos)"""
        return self.esta_activa and self.dias_restantes <= 7

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