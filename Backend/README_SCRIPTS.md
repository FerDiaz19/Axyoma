📚 DOCUMENTACIÓN DE SCRIPTS ESENCIALES - AXYOMA BACKEND
================================================================

Este directorio contiene solo los scripts esenciales y útiles para el sistema Axyoma.
Todos los scripts temporales, de prueba y duplicados han sido eliminados.

🔧 SCRIPTS DE CONFIGURACIÓN
==========================

📄 manage.py
  • Script principal de Django para administración del proyecto
  • Uso: python manage.py [comando]
  • Comandos útiles: runserver, migrate, createsuperuser, shell

📄 sistema_completo_listo.py
  • 🎯 SCRIPT PRINCIPAL para inicializar todo el sistema desde cero
  • Resetea la base de datos y carga datos completos
  • Crea usuarios administrativos, empresas, empleados, planes y suscripciones
  • Uso: python sistema_completo_listo.py
  • ⚠️ ATENCIÓN: Resetea TODA la base de datos

📄 crear_superadmin.py
  • Crea usuarios superadministrador adicionales
  • Útil para agregar más administradores al sistema
  • Uso: python crear_superadmin.py

🔍 SCRIPTS DE VERIFICACIÓN
==========================

📄 verificar_estado_bd.py
  • Verifica el estado actual de la base de datos
  • Muestra estadísticas de registros en todas las tablas
  • Útil para diagnosticar problemas o verificar datos
  • Uso: python verificar_estado_bd.py

📄 verificacion_simple.py
  • Verificación rápida del estado del sistema
  • Muestra resumen de empresas, empleados y suscripciones
  • Uso: python verificacion_simple.py

💾 SCRIPTS DE RESPALDO
======================

📄 sistema_respaldos.py
  • Sistema completo de respaldos de la base de datos
  • Crea respaldos automáticos en formato SQL
  • Incluye restauración de respaldos
  • Uso: python sistema_respaldos.py

📄 respaldo_completo.py
  • Script para crear respaldos completos manuales
  • Genera archivos SQL con todos los datos
  • Uso: python respaldo_completo.py

⚡ SCRIPTS BATCH DE ACCESO RÁPIDO
================================

📄 cargar_datos_rapido.bat
  • Ejecuta carga rápida de datos desde Windows
  • Interfaz simplificada para el sistema_completo_listo.py

📄 estado_inicial_rapido.bat
  • Ejecuta verificación rápida del estado del sistema
  • Interfaz simplificada para verificar_estado_bd.py

📄 resetear_bd_rapido.bat
  • Reseteo rápido de base de datos desde Windows
  • Interfaz simplificada para reinicializar el sistema

📁 DIRECTORIOS IMPORTANTES
=========================

📁 apps/
  • Contiene todas las aplicaciones Django del proyecto
  • Modelos, vistas, serializers, etc.

📁 config/
  • Configuraciones del proyecto Django
  • Settings, URLs principales, WSGI, etc.

📁 core/
  • Funcionalidades centrales del sistema

📁 backups/
  • Almacena los respaldos automáticos de la base de datos

📁 fixtures/
  • Datos iniciales en formato JSON para carga rápida

📁 logs/
  • Archivos de log del sistema

📁 media/ y static/
  • Archivos multimedia y estáticos de Django

🎯 FLUJO DE TRABAJO RECOMENDADO
==============================

1️⃣ INSTALACIÓN INICIAL:
   python manage.py migrate
   python sistema_completo_listo.py

2️⃣ VERIFICACIÓN:
   python verificacion_simple.py

3️⃣ DESARROLLO:
   python manage.py runserver

4️⃣ RESPALDOS:
   python sistema_respaldos.py

5️⃣ MANTENIMIENTO:
   python verificar_estado_bd.py

🔑 CREDENCIALES POR DEFECTO
===========================
Usuario: superadmin
Contraseña: admin123

🌐 ACCESO AL SISTEMA
===================
Frontend: http://localhost:3000
Backend API: http://localhost:8000
Admin Django: http://localhost:8000/admin

⚠️ NOTAS IMPORTANTES
===================
• NO eliminar manage.py - Es esencial para Django
• NO eliminar las carpetas apps/, config/, core/ - Contienen el código principal
• Los scripts .bat son para Windows únicamente
• Siempre hacer respaldo antes de usar sistema_completo_listo.py
• Los archivos en fixtures/ y backups/ son importantes para restauración

================================================================
📅 Última actualización: Julio 31, 2025
🏷️ Versión del sistema: Operativo completo
================================================================
