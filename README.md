# 🚀 AXYOMA - Sistema de Gestión de Empleados

Sistema completo de gestión de empleados con múltiples niveles de acceso, desarrollado con Django (Backend) y React (Frontend).

## 📋 Características Principales

- **👤 Gestión de Usuarios**: SuperAdmin, Admin Empresa, Admin Planta
- **🏢 Gestión de Empresas**: Múltiples empresas con suscripciones
- **🏭 Gestión de Plantas**: Múltiples plantas por empresa
- **👥 Gestión de Empleados**: CRUD completo con filtros avanzados
- **� Planes de Suscripción**: Básico, Profesional, Empresarial
- **🔒 Autenticación**: Sistema de login seguro
- **📱 Dashboard Responsivo**: Interfaz moderna y adaptable

## 🛠️ Tecnologías Utilizadas

**Backend:**
- Python 3.11+
- Django 5.2.3
- Django REST Framework
- PostgreSQL
- Django CORS Headers

**Frontend:**
- React 18
- TypeScript
- CSS3 (Diseño personalizado)
- Fetch API

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **Node.js LTS** - [Descargar](https://nodejs.org/)
- **PostgreSQL 14+** - [Descargar](https://www.postgresql.org/download/)

### 2. Configuración de Base de Datos
```sql
-- La base de datos se crea automáticamente durante el setup
-- Solo necesitas tener PostgreSQL instalado y ejecutándose con:

-- Usuario: postgres
-- Password: 123456789
-- Host: localhost
-- Puerto: 5432

-- El script setup_project.bat:
-- 1. Verifica conectividad a PostgreSQL
-- 2. Crea automáticamente la base de datos 'axyomadb' si no existe
-- 3. Ejecuta migraciones
-- 4. Crea todos los datos iniciales (usuarios, empresa, planta, etc.)
```

### 3. Configuración del Proyecto
```bash
# Ejecutar configuración completa
setup_project.bat
```

### 4. Iniciar el Sistema
```bash
# Iniciar backend y frontend
iniciar_sistema.bat
```

## � URLs del Sistema

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

## 👤 Usuarios de Prueba

| Tipo Usuario | Email | Password | Permisos |
|-------------|--------|----------|----------|
| **SuperAdmin** | ed-rubio@axyoma.com | 1234 | Gestión completa del sistema |
| **Admin Empresa** | juan.perez@codewave.com | 1234 | Gestión de su empresa |
| **Admin Planta** | maria.gomez@codewave.com | 1234 | Gestión de su planta |

## 🏢 Datos de Prueba Incluidos

**Empresa:**
- **Nombre**: CodeWave Technologies S.A. de C.V.
- **RFC**: CWT240701ABC
- **Plan**: Profesional (200 empleados, 5 plantas)

**Estructura Organizacional:**
- **Planta**: Planta Principal
- **Departamentos**: RRHH, Producción, Calidad, Mantenimiento, Logística
- **Puestos**: 12 puestos distribuidos en departamentos
- **Empleados**: 5 empleados de muestra

**Planes de Suscripción:**
- **Básico**: 50 empleados, 1 planta - $499/mes
- **Profesional**: 200 empleados, 5 plantas - $999/mes
- **Empresarial**: 1000 empleados, 20 plantas - $1999/mes

## � Estructura del Proyecto

```
Axyoma/
├── Backend/                 # Django Backend
│   ├── apps/               # Aplicaciones Django
│   ├── config/             # Configuración del proyecto
│   ├── env/                # Entorno virtual Python
│   ├── create_initial_data.py  # Script de datos iniciales
│   ├── manage.py           # Administrador Django
│   └── requirements.txt    # Dependencias Python
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── services/       # Servicios API
│   │   ├── css/           # Estilos CSS
│   │   └── ...
│   ├── public/            # Archivos estáticos
│   └── package.json       # Dependencias Node.js
├── setup_project.bat      # Configuración completa
└── iniciar_sistema.bat    # Iniciar sistema
```

## 🔧 Scripts Disponibles

- **`setup_project.bat`** - Configuración completa del proyecto (ejecutar una vez)
- **`iniciar_sistema.bat`** - Iniciar backend y frontend (uso diario)

## 🎯 Funcionalidades por Usuario

### SuperAdmin
- ✅ Gestión completa de empresas
- ✅ Gestión de planes de suscripción
- ✅ Gestión de todas las suscripciones
- ✅ Acceso a todas las funcionalidades

### Admin Empresa
- ✅ Gestión de plantas de su empresa
- ✅ Gestión de empleados de su empresa
- ✅ Gestión de departamentos y puestos
- ✅ Visualización de su suscripción

### Admin Planta
- ✅ Gestión de empleados de su planta
- ✅ Gestión de departamentos de su planta
- ✅ Gestión de puestos de su planta

## 🚨 Solución de Problemas

### Error: "Python no está instalado"
```bash
# Instalar Python desde https://www.python.org/
# Asegurarse de marcar "Add Python to PATH"
```

### Error: "Node.js no está instalado"
```bash
# Instalar Node.js desde https://nodejs.org/
# Descargar versión LTS
```

### Error: "No se puede conectar a PostgreSQL"
```bash
# 1. Verificar que PostgreSQL esté ejecutándose
# Ve a Windows Services y busca 'postgresql'
# Asegúrate que esté en estado 'Iniciado'

# 2. Verificar configuración
# Usuario: postgres, Password: 123456789
# Puerto: 5432

# 3. El script creará automáticamente la base de datos 'axyomadb'
# No es necesario crearla manualmente
```

### Error: "Credenciales incorrectas" al hacer login
```bash
# Si aparece este error, verifica:
# 1. Que ejecutaste setup_project.bat completamente
# 2. Que no hubo errores durante la creación de datos iniciales
# 3. Usa las credenciales exactas (copiar y pegar):

# SuperAdmin: ed-rubio@axyoma.com / 1234
# Admin Empresa: juan.perez@codewave.com / 1234  
# Admin Planta: maria.gomez@codewave.com / 1234

# Si persiste el problema, ejecuta:
cd Backend
py create_initial_data.py
```

### Error: "Scripts se cierran inmediatamente"
```bash
# 1. Ejecutar desde PowerShell como administrador
# 2. Verificar políticas de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Asegurarse de que todos los requisitos estén instalados
# 4. Ejecutar setup_project.bat primero
# 5. Si persiste, ejecutar diagnostico.bat para identificar problemas
```

## 🎉 ¡Listo para usar!

1. Ejecuta `setup_project.bat` (solo la primera vez)
2. Ejecuta `iniciar_sistema.bat` (cada vez que uses el sistema)
3. Ve a http://localhost:3000
4. Inicia sesión con cualquier usuario de prueba
5. ¡Explora el sistema!

---

**Desarrollado con ❤️ para la gestión eficiente de empleados**
