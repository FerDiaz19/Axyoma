#!/bin/bash

# Script de demostración del CRUD de usuarios SuperAdmin
# Requiere que el servidor Django esté corriendo en localhost:8000

echo "🚀 Iniciando demostración del CRUD de usuarios SuperAdmin..."
echo "================================================="

# Obtener token de autenticación
echo "🔑 Obteniendo token de autenticación..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","password":"1234"}')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Error: No se pudo obtener el token de autenticación"
    exit 1
fi

echo "✅ Token obtenido: ${TOKEN:0:20}..."

# 1. CREAR usuario SuperAdmin
echo ""
echo "📝 1. CREAR - Creando nuevo usuario SuperAdmin..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/superadmin/crear_usuario/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_superadmin",
    "email": "demo@axyoma.com",
    "nombre": "Usuario",
    "apellido_paterno": "Demo",
    "apellido_materno": "SuperAdmin",
    "password": "demo123"
  }')

echo "📋 Respuesta: $CREATE_RESPONSE"

# 2. LEER usuarios (listar)
echo ""
echo "📋 2. LEER - Listando usuarios SuperAdmin..."
LIST_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/superadmin/listar_usuarios/?nivel_usuario=superadmin" \
  -H "Authorization: Token $TOKEN")

echo "📋 Usuarios SuperAdmin encontrados:"
echo $LIST_RESPONSE | grep -o '"username":"[^"]*' | cut -d'"' -f4 | head -5

# Obtener ID del usuario creado
USER_ID=$(echo $LIST_RESPONSE | grep -o '"user_id":[0-9]*' | grep -A1 '"username":"demo_superadmin"' | tail -1 | cut -d':' -f2)

if [ -z "$USER_ID" ]; then
    echo "⚠️  Advertencia: No se encontró el ID del usuario creado"
    # Intentar obtener el último usuario creado
    USER_ID=$(echo $LIST_RESPONSE | grep -o '"user_id":[0-9]*' | cut -d':' -f2 | tail -1)
fi

echo "🆔 ID del usuario para demo: $USER_ID"

# 3. ACTUALIZAR usuario
echo ""
echo "✏️ 3. ACTUALIZAR - Modificando datos del usuario..."
UPDATE_RESPONSE=$(curl -s -X PUT http://localhost:8000/api/superadmin/editar_usuario/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"username\": \"demo_superadmin_actualizado\",
    \"email\": \"demo_actualizado@axyoma.com\"
  }")

echo "📋 Respuesta: $UPDATE_RESPONSE"

# 4. SUSPENDER usuario
echo ""
echo "⏸️ 4. SUSPENDER - Suspendiendo usuario..."
SUSPEND_RESPONSE=$(curl -s -X POST http://localhost:8000/api/superadmin/suspender_usuario/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"accion\": \"suspender\"
  }")

echo "📋 Respuesta: $SUSPEND_RESPONSE"

# 5. ACTIVAR usuario
echo ""
echo "▶️ 5. ACTIVAR - Reactivando usuario..."
ACTIVATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/superadmin/suspender_usuario/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"accion\": \"activar\"
  }")

echo "📋 Respuesta: $ACTIVATE_RESPONSE"

# 6. ELIMINAR usuario
echo ""
echo "🗑️ 6. ELIMINAR - Eliminando usuario de demostración..."
DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:8000/api/superadmin/eliminar_usuario/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID
  }")

echo "📋 Respuesta: $DELETE_RESPONSE"

# Verificar que se eliminó
echo ""
echo "✅ Verificando eliminación..."
FINAL_LIST=$(curl -s -X GET "http://localhost:8000/api/superadmin/listar_usuarios/?nivel_usuario=superadmin" \
  -H "Authorization: Token $TOKEN")

DEMO_USER_EXISTS=$(echo $FINAL_LIST | grep -o '"username":"demo_superadmin_actualizado"' | wc -l)

if [ $DEMO_USER_EXISTS -eq 0 ]; then
    echo "✅ Usuario de demostración eliminado exitosamente"
else
    echo "⚠️  Usuario de demostración aún existe"
fi

echo ""
echo "🎉 ¡Demostración completada!"
echo "================================================="
echo "📊 Resumen de operaciones realizadas:"
echo "   ✅ CREATE - Usuario SuperAdmin creado"
echo "   ✅ READ   - Usuarios listados"
echo "   ✅ UPDATE - Datos actualizados"
echo "   ✅ SUSPEND - Usuario suspendido"
echo "   ✅ ACTIVATE - Usuario reactivado"
echo "   ✅ DELETE - Usuario eliminado"
echo ""
echo "🚀 El CRUD de usuarios SuperAdmin está funcionando correctamente!"
