@echo off
echo ====================================
echo      INICIANDO FRONTEND REACT
echo ====================================
echo.

cd frontend

echo Verificando dependencias de Node.js...
if not exist "node_modules" (
    echo Instalando dependencias...
    npm install
)

echo.
echo Iniciando servidor React en puerto 3000...
echo Aplicacion disponible en: http://localhost:3000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

npm start
