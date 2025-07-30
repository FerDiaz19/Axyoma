@echo off
echo ==========================================
echo 🎯 ESTADO INICIAL COMPLETO - RAPIDO
echo ==========================================

echo 🗑️ PASO 1/2: Reseteando BD...
call resetear_bd_rapido.bat

echo.
echo 📊 PASO 2/2: Cargando datos iniciales...
call cargar_datos_rapido.bat

echo.
echo 🎉 ESTADO INICIAL COMPLETADO
echo ✅ BD lista como primer día del software
echo.
echo 👤 USUARIOS DISPONIBLES:
echo • superadmin / 1234
echo • admin_empresa / 1234  
echo • admin_planta / 1234
echo.
echo ✅ LISTO - Presiona cualquier tecla para continuar...
pause > nul
