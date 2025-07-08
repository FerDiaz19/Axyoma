@echo off
echo ===============================================
echo   PROBANDO PANEL SUPERADMIN COMPLETO
echo ===============================================
echo.

echo [1/2] Ejecutando pruebas de backend...
cd Backend
python test_superadmin_completo.py

echo.
echo [2/2] Iniciando servidores para prueba manual...
echo.
echo Backend iniciando en http://localhost:8000/api/
start "Django Backend" cmd /k "python manage.py runserver"

echo Esperando 5 segundos...
timeout /t 5 /nobreak > nul

echo Frontend iniciando en http://localhost:3000/
cd ..\frontend
start "React Frontend" cmd /k "npm start"

echo.
echo ===============================================
echo   PRUEBAS DEL PANEL SUPERADMIN
echo ===============================================
echo.
echo ✅ Backend: Tests automaticos ejecutados
echo ✅ Frontend: Servidor iniciado
echo.
echo 🔗 Abrir: http://localhost:3000/
echo 🔑 Login: superadmin / superadmin123
echo.
echo 📋 VERIFICAR EN EL DASHBOARD:
echo    ✅ Estadisticas generales
echo    ✅ Empresas (listar, suspender, eliminar)
echo    ✅ Usuarios (listar, suspender, eliminar)
echo    ✅ Plantas (listar, suspender, eliminar)
echo    ✅ Departamentos (listar, suspender, eliminar)
echo    ✅ Puestos (listar, suspender, eliminar)
echo    ✅ Empleados (listar, suspender, eliminar)
echo.
echo Presiona CUALQUIER TECLA para cerrar...
pause > nul
