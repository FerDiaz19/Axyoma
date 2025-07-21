# -*- coding: utf-8 -*-
import secrets
import string
from datetime import datetime, timedelta
from django.utils import timezone
from .models import TokenEvaluacion

def generar_token_unico(longitud=32):
    """Genera un token único alfanumérico"""
    caracteres = string.ascii_letters + string.digits
    while True:
        token = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        if not TokenEvaluacion.objects.filter(token=token).exists():
            return token

def crear_token_evaluacion(asignacion, dias_expiracion=30):
    """Crea un token para una asignación específica"""
    token_string = generar_token_unico()
    fecha_expiracion = timezone.now() + timedelta(days=dias_expiracion)
    
    token = TokenEvaluacion.objects.create(
        asignacion=asignacion,
        token=token_string,
        fecha_expiracion=fecha_expiracion,
        activo=True,
        usado=False
    )
    
    return token

def validar_token(token_string):
    """Valida un token y retorna la asignación si es válido"""
    try:
        token = TokenEvaluacion.objects.get(
            token=token_string,
            activo=True,
            usado=False,
            fecha_expiracion__gt=timezone.now()
        )
        return token.asignacion
    except TokenEvaluacion.DoesNotExist:
        return None

def usar_token(token_string, ip_address=None):
    """Marca un token como usado"""
    try:
        token = TokenEvaluacion.objects.get(token=token_string)
        token.usado = True
        token.fecha_uso = timezone.now()
        if ip_address:
            token.ip_acceso = ip_address
        token.save()
        return True
    except TokenEvaluacion.DoesNotExist:
        return False
