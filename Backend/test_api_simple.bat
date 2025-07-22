@echo off
echo 🧪 === PRUEBA DE CREACION DE PLANTA VIA API ===

echo 🔐 Obteniendo token de autenticacion...
curl -X POST "http://localhost:8000/api/auth/login/" ^
     -H "Content-Type: application/json" ^
     -d "{\"email\":\"admin@admin.com\",\"password\":\"admin123\"}" ^
     -s > token_response.json

if %errorlevel% neq 0 (
    echo ❌ Error obteniendo token
    exit /b 1
)

echo ✅ Token obtenido

echo.
echo 🏢 Obteniendo primera empresa...
curl -X GET "http://localhost:8000/api/empresas/" ^
     -H "Authorization: Bearer %TOKEN%" ^
     -s > empresas_response.json

echo.
echo 🏭 Creando nueva planta de prueba...
set PLANTA_NAME=Planta_API_Test_%RANDOM%

curl -X POST "http://localhost:8000/api/plantas/" ^
     -H "Content-Type: application/json" ^
     -H "Authorization: Bearer %TOKEN%" ^
     -d "{\"nombre\":\"%PLANTA_NAME%\",\"direccion\":\"Direccion de prueba via API\",\"empresa\":1,\"status\":true}" ^
     -s > planta_response.json

if %errorlevel% neq 0 (
    echo ❌ Error creando planta
    exit /b 1
)

echo ✅ Planta creada exitosamente

echo.
echo 📊 Verificando estructura automatica creada...

echo Contenido de respuesta de planta:
type planta_response.json

echo.
echo 🧹 Limpieza manual requerida - revisar base de datos

pause
