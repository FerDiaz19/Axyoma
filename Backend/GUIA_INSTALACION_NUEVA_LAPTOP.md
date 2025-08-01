📋 GUÍA DE CONFIGURACIÓN PARA NUEVA LAPTOP - AXYOMA
================================================================

Esta guía te permitirá configurar exactamente el mismo sistema Axyoma 
en una nueva laptop con todos los datos y configuraciones.

🔧 REQUISITOS PREVIOS
====================

1️⃣ SOFTWARE NECESARIO:
   • Python 3.8+ instalado
   • PostgreSQL 12+ instalado y corriendo
   • Git instalado
   • Node.js 16+ (para el frontend)
   • VS Code (recomendado)

2️⃣ CONFIGURACIÓN DE BASE DE DATOS:
   • PostgreSQL corriendo en puerto 5432
   • Usuario postgres con contraseña configurada
   • Base de datos "axyoma_db" creada

🚀 PROCESO DE INSTALACIÓN PASO A PASO
====================================

PASO 1: CLONAR EL REPOSITORIO
-----------------------------
git clone https://github.com/FerDiaz19/Axyoma.git
cd Axyoma/Backend

PASO 2: CONFIGURAR ENTORNO VIRTUAL
----------------------------------
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

PASO 3: INSTALAR DEPENDENCIAS
-----------------------------
pip install -r requirements.txt

PASO 4: CONFIGURAR BASE DE DATOS
--------------------------------
# Editar config/settings/local.py con tus credenciales de PostgreSQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'axyoma_db',
        'USER': 'postgres',           # Tu usuario PostgreSQL
        'PASSWORD': 'tu_password',    # Tu contraseña PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

PASO 5: APLICAR MIGRACIONES
---------------------------
python manage.py makemigrations
python manage.py migrate

PASO 6: 🎯 CONFIGURAR SISTEMA COMPLETO (AUTOMÁTICO)
--------------------------------------------------
python sistema_completo_listo.py

⚠️ IMPORTANTE: Este script hará TODO automáticamente:
   • Resetea la base de datos completamente
   • Aplica todas las migraciones
   • Crea usuarios administrativos
   • Crea empresas con estructura organizacional completa
   • Crea empleados distribuidos en puestos
   • Configura planes y suscripciones
   • Procesa pagos demo

PASO 7: VERIFICAR INSTALACIÓN
-----------------------------
python verificar_estado_bd.py

PASO 8: INICIAR SERVIDOR
------------------------
python manage.py runserver

🔑 CREDENCIALES POR DEFECTO
===========================
Usuario: superadmin
Contraseña: admin123

🌐 ACCESO AL SISTEMA
===================
Backend API: http://localhost:8000
Admin Django: http://localhost:8000/admin
Frontend: http://localhost:3000 (cuando esté configurado)

📊 DATOS INCLUIDOS AUTOMÁTICAMENTE
=================================
• 2 empresas completamente configuradas
• 41 empleados distribuidos en la estructura organizacional
• 4 plantas operativas
• 14 departamentos activos
• 28 puestos definidos
• 3 planes de suscripción
• 2 suscripciones activas con pagos

🔍 VERIFICACIÓN DEL SISTEMA
===========================
Ejecuta estos comandos para verificar que todo funciona:

python verificacion_simple.py
python verificar_estado_bd.py

💾 RESPALDOS Y MANTENIMIENTO
===========================
python sistema_respaldos.py    # Sistema de respaldos automáticos
python respaldo_completo.py    # Respaldo manual

⚡ COMANDOS RÁPIDOS (Windows)
============================
cargar_datos_rapido.bat        # Cargar datos rápidamente
estado_inicial_rapido.bat      # Verificar estado
resetear_bd_rapido.bat         # Resetear sistema completo

🔧 SCRIPTS PRINCIPALES
======================
• sistema_completo_listo.py    → Configuración completa automática
• verificar_estado_bd.py       → Verificar estado de la base de datos
• verificacion_simple.py       → Resumen rápido del sistema
• crear_superadmin.py          → Crear administradores adicionales
• sistema_respaldos.py         → Sistema de respaldos

🆘 SOLUCIÓN DE PROBLEMAS
=======================

❌ Error de conexión a PostgreSQL:
   • Verificar que PostgreSQL esté corriendo
   • Verificar credenciales en config/settings/local.py
   • Crear base de datos "axyoma_db" manualmente

❌ Error en migraciones:
   • python manage.py makemigrations --empty [app_name]
   • python manage.py migrate --fake-initial

❌ Error en importaciones:
   • Verificar que el entorno virtual esté activado
   • pip install -r requirements.txt

❌ Login no funciona:
   • python sistema_completo_listo.py (reinicia todo)
   • Verificar con: python verificacion_simple.py

🎯 RESULTADO ESPERADO
====================
Después de seguir esta guía tendrás:
✅ Sistema Axyoma 100% funcional
✅ Base de datos con datos completos
✅ Login funcionando perfectamente
✅ Estructura organizacional completa
✅ Empleados, empresas, suscripciones configuradas
✅ Panel de administración accesible

📞 CONTACTO
===========
Si tienes problemas, verifica:
1. Que PostgreSQL esté corriendo
2. Que las credenciales sean correctas
3. Que el entorno virtual esté activado
4. Ejecutar: python sistema_completo_listo.py

================================================================
🎉 ¡LISTO! Tu sistema Axyoma estará configurado exactamente igual
================================================================
