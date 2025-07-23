#!/bin/bash

echo "===== VERIFICACIÓN DE CREDENCIALES AXYOMA ====="
echo "Verificando credenciales de acceso al sistema..."

# Cambiar según tu instalación
BACKEND_URL="http://localhost:8000/api"

echo
echo "Probando credenciales básicas:"
echo "---------------------------------"
for cred in "superadmin:1234" "admin_empresa:1234" "admin_planta:1234"; do
    username=$(echo $cred | cut -d':' -f1)
    password=$(echo $cred | cut -d':' -f2)
    
    echo -n "Probando $username/$password: "
    
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$username\",\"password\":\"$password\"}" \
        $BACKEND_URL/auth/login/)
    
    if [[ "$response" == *"token"* ]]; then
        echo "✅ OK"
    else
        echo "❌ FALLO"
        echo "   Respuesta: $response"
    fi
done

echo
echo "Si alguna credencial falló, verifica en el panel de admin:"
echo "$BACKEND_URL/admin/"
echo
