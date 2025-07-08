#!/bin/bash
# Script de prueba para verificar endpoints de suscripciones

echo "=== PROBANDO ENDPOINTS DE SUSCRIPCIONES ==="

# URL base del API
BASE_URL="http://localhost:8000/api"

echo "1. Probando endpoint de planes..."
curl -X GET "$BASE_URL/suscripciones/listar_planes/" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool

echo -e "\n2. Probando endpoint de suscripciones..."
curl -X GET "$BASE_URL/suscripciones/listar_suscripciones/" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool

echo -e "\n3. Probando endpoint de pagos..."
curl -X GET "$BASE_URL/suscripciones/listar_pagos/" \
  -H "Content-Type: application/json" \
  2>/dev/null | python -m json.tool

echo -e "\n=== FIN DE PRUEBAS ==="
