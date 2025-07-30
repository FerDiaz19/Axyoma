@echo off
echo ========================================
echo 🔄 RESET RAPIDO - ESTADO INICIAL
echo ========================================
echo.

cd /d "c:\xampp2\htdocs\UTT4B\Axyoma2\Backend"

echo 📦 Activando entorno virtual...
call env\Scripts\activate.bat

echo 🔄 RESETEANDO BD COMPLETA...
python resetear_bd_rapido.py

echo 📊 CARGANDO DATOS INICIALES COMPLETOS...
python cargar_datos_rapido.py

echo.
echo ✅ ¡RESET COMPLETADO EXITOSAMENTE!
echo.
echo 👤 USUARIOS DISPONIBLES:
echo • superadmin / 1234
echo • admin_empresa / 1234
echo • admin_planta / 1234
echo.
echo 🚀 Para levantar el servidor ejecuta: start.bat
echo.
pause
