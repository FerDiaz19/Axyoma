@echo off
echo ========================================
echo   INICIANDO SISTEMA AXYOMA COMPLETO
echo ========================================
echo.

echo [1/3] Activando entorno virtual Python...
cd Backend
call env\Scripts\activate.bat

echo [2/3] Iniciando servidor Django en puerto 8000...
start "Django Backend" cmd /k "python manage.py runserver"

echo [3/3] Esperando 5 segundos y luego iniciando frontend React...
timeout /t 5 /nobreak > nul
cd ..\frontend
start "React Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ========================================
echo Backend: http://localhost:8000/api/
echo Frontend: http://localhost:3000/
echo.
echo Para probar el SuperAdmin:
echo 1. Ve a http://localhost:3000/
echo 2. Login: superadmin / superadmin123
echo 3. Accede al Dashboard SuperAdmin
echo.
echo PresIONA CUALQUIER TECLA PARA SALIR...
pause > nul
