@echo off
echo ===============================================
echo    PROBAR FUNCIONALIDAD EMPRESA SUSPENDIDA
echo ===============================================
echo.

cd /d "%~dp0Backend"

echo 🧪 Probando funcionalidad de empresa suspendida...
python test_empresa_suspendida.py

echo.
echo ✅ PRUEBA COMPLETADA
echo.
echo 📋 CAMBIOS IMPLEMENTADOS:
echo.
echo ✅ BACKEND:
echo   - Login permite empresas suspendidas
echo   - Campo empresa_suspendida en response
echo   - Mensajes de advertencia incluidos
echo   - Informacion de suspension para admin-empresa y admin-planta
echo.
echo ✅ FRONTEND:
echo   - Banner de advertencia en dashboard
echo   - Estado SUSPENDIDA en header
echo   - Mensaje de suscripcion expirada en estadisticas
echo   - Estilos CSS para alertas de suspension
echo.
echo ✅ MODAL DE EMPLEADOS:
echo   - Campo 'salario' eliminado del formulario
echo   - Backend actualizado sin campo salario
echo   - Formulario simplificado y funcional
echo.
echo 🎯 PARA PROBAR EN NAVEGADOR:
echo   1. Ejecutar: INICIAR_SISTEMA_COMPLETO.bat
echo   2. Login como SuperAdmin y suspender una empresa
echo   3. Login con admin de esa empresa suspendida
echo   4. Verificar banner de advertencia
echo   5. Ir a seccion Reportes/Estadisticas
echo   6. Ver mensaje "Suscripcion Expirada"
echo.
pause
