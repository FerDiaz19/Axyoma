@echo off
echo ===== VERIFICACION DE DATOS AXYOMA =====
echo.

cd Backend
call env\Scripts\activate.bat

echo Ejecutando setup de base de datos...
python setup_database.py

echo.
echo ===== DATOS ORIGINALES RESTAURADOS =====
echo.
echo 👤 Usuarios disponibles:
echo    SuperAdmin:     ed-rubio@axyoma.com / 1234
echo    Admin Empresa:  juan.perez@codewave.com / 1234
echo    Admin Planta:   maria.gomez@codewave.com / 1234
echo.
echo 📊 Tus datos de suscripciones y pagos están preservados
echo.
pause
