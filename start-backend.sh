#!/bin/bash

echo "=== INICIANDO SISTEMA AXYOMA ==="

# Ir al directorio Backend
cd Backend

echo "1. Verificando configuración de Django..."
python manage.py check

echo "2. Creando migraciones..."
python manage.py makemigrations

echo "3. Aplicando migraciones..."
python manage.py migrate

echo "4. Iniciando servidor Django..."
echo "Backend estará disponible en: http://localhost:8000"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python manage.py runserver 8000
