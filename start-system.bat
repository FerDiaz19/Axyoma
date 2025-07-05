@echo off
echo Iniciando Sistema Axyoma...
echo.

echo Activando entorno virtual de Django...
cd Backend
call .\env\Scripts\activate.bat

echo Aplicando migraciones...
python manage.py makemigrations users
python manage.py migrate

echo Iniciando servidor Django en segundo plano...
start "Django Server" cmd /c "python manage.py runserver"

echo Esperando 5 segundos para que Django inicie...
timeout /t 5 /nobreak > nul

echo Iniciando React en segundo plano...
cd ..\frontend
start "React App" cmd /c "npm start"

echo.
echo Sistema iniciado exitosamente!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para salir...
pause > nul
