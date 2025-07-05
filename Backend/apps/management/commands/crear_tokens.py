#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Crear tokens para usuarios existentes'

    def handle(self, *args, **options):
        self.stdout.write("🔑 Creando tokens para usuarios existentes...")
        
        users_without_tokens = 0
        users_with_tokens = 0
        
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                users_without_tokens += 1
                self.stdout.write(f"  ✅ Token creado para: {user.username}")
            else:
                users_with_tokens += 1
                self.stdout.write(f"  ℹ️  Token ya existe para: {user.username}")
        
        self.stdout.write("")
        self.stdout.write("📊 RESUMEN:")
        self.stdout.write(f"  • Tokens creados: {users_without_tokens}")
        self.stdout.write(f"  • Tokens existentes: {users_with_tokens}")
        self.stdout.write(f"  • Total usuarios: {users_without_tokens + users_with_tokens}")
        
        if users_without_tokens > 0:
            self.stdout.write("")
            self.stdout.write("🔍 TOKENS CREADOS:")
            for user in User.objects.all():
                token = Token.objects.get(user=user)
                self.stdout.write(f"  {user.username}: {token.key}")
