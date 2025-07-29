# 🏭 AXYOMA - Sistema de Gestión de Empleados

Sistema completo de gestión de empleados para empresas industriales con arquitectura modular.

## 🚀 Estado del Proyecto: ✅ COMPLETAMENTE FUNCIONAL

El sistema Axyoma está completamente configurado y funcional. Incluye un backend Django con API REST, frontend React, y funcionalidades completas de login, registro, gestión empresarial, y **gestión avanzada de base de datos con PostgreSQL**.

## ⚠️ CONFIGURACIÓN OBLIGATORIA DE PostgreSQL

**IMPORTANTE:** Para usar las funciones de respaldo y restauración de base de datos, debe configurar PostgreSQL en las variables de entorno del sistema.

### 🔧 Configuración de PostgreSQL PATH (OBLIGATORIO)

#### Opción 1: Configuración Manual (Recomendado)
1. **Presionar** `Win + R`, escribir `sysdm.cpl` y presionar Enter
2. **Clic** en "Variables de entorno..."
3. **En "Variables del sistema"**, seleccionar `Path` y clic en "Editar..."
4. **Clic** en "Nuevo" y agregar:
   ```
   C:\Program Files\PostgreSQL\17\bin
   ```
5. **Clic** "OK" en todas las ventanas
6. **Reiniciar PowerShell** y verificar con: `pg_dump --version`

#### Opción 2: PowerShell como Administrador
```powershell
# Ejecutar PowerShell como Administrador y ejecutar:
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\17\bin", "Machine")
```

#### ✅ Verificar la Configuración
Abrir una nueva terminal PowerShell y ejecutar:
```powershell
pg_dump --version
# Debe mostrar: pg_dump (PostgreSQL) 17.5
```

**Sin esta configuración, las funciones de respaldo SQL no funcionarán.**

## 🚀 Inicio Rápido

### Primera Vez (Setup Completo)
```bash
# 1. Ejecutar configuración inicial
setup.bat

# 2. Iniciar el sistema
start.bat
```

### Uso Diario
```bash
# Iniciar sistema
start.bat
```

### Si hay problemas
```bash
# Limpiar y reconfigurar todo
reset.bat
```

## 📋 Requisitos

- **Python 3.10+** 
- **Node.js 16+** 
- **PostgreSQL 17** (usuario: postgres, password: 12345678)
- **Variables de entorno**: PostgreSQL bin configurado en PATH

## 🌐 Accesos del Sistema

Una vez iniciado:
- **Frontend**: http://localhost:3000
- **Registro**: http://localhost:3000/registro
- **Backend**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

## 👥 Usuarios de Prueba

| Rol | Username | Password | Descripción |
|-----|----------|----------|-------------|
| **SuperAdmin** | superadmin | 1234 | Gestión completa del sistema |
| **Admin Empresa** | admin_empresa | 1234 | Gestión de empresa CodeWave |
| **Admin Planta** | admin_planta | 1234 | Gestión de planta específica |

## 📁 Estructura del Proyecto

```
Axyoma2/
├── setup.bat          # Configuración inicial
├── start.bat          # Inicio del sistema
├── reset.bat          # Limpiar y reconfigurar
├── Backend/           # Servidor Django
│   ├── apps/          # Aplicaciones Django
│   ├── config/        # Configuración
│   └── env/           # Entorno virtual
└── frontend/          # Aplicación React
    ├── src/           # Código fuente
    └── public/        # Archivos estáticos
```

## 🛠️ Comandos Útiles

- `setup.bat` - Configuración inicial completa
- `start.bat` - Iniciar frontend y backend
- `reset.bat` - Limpiar BD y reconfigurar todo

## 🔧 Solución de Problemas

### Error de PostgreSQL
```bash
# Verificar que PostgreSQL esté ejecutándose
# Usuario: postgres, Password: 12345678
# Base de datos: axyomadb
```

### Error de dependencias
```bash
# Ejecutar setup completo
setup.bat
```

### Error de autenticación
```bash
# Limpiar y reconfigurar
reset.bat
```

## 🏗️ Tecnologías

- **Backend**: Django + PostgreSQL + Django REST Framework
- **Frontend**: React + TypeScript + Axios
- **Base de Datos**: PostgreSQL
- **Autenticación**: Token-based authentication

## 🎯 Funcionalidades Principales

### ✅ Sistema de Autenticación
- Login con username/password
- Registro de nuevas empresas
- Gestión de perfiles de usuario
- Diferentes niveles de acceso

### ✅ Gestión Empresarial
- Registro automático de empresas
- Creación automática de estructura organizacional
- Gestión de plantas, departamentos y puestos
- Panel de administración por nivel de usuario

### ✅ Estructura Organizacional
Al registrar una empresa, se crea automáticamente:
- Planta Principal
- Departamentos básicos (Administración, RRHH, Finanzas, etc.)
- Puestos de trabajo predefinidos
- Suscripción básica automática

### ✅ Módulo de Evaluaciones
- **Normativas Oficiales:** NOM-030, NOM-035, Evaluación 360°
- **Gestión de Preguntas:** Creación de preguntas por normativa
- **Tipos de Preguntas:** Opción múltiple, Sí/No, Escala, Texto libre
- **Roles de Acceso:** SuperAdmin gestiona normativas, Empresas crean evaluaciones

## 🔄 Workflow de Registro

1. **Acceso al Registro:** `/registro`
2. **Datos de Empresa:** Información básica de la empresa
3. **Datos de Admin:** Credenciales del usuario administrador
4. **Creación Automática:** Se crea toda la estructura organizacional
5. **Selección de Plan:** (Opcional) Elegir plan de suscripción
6. **Acceso Inmediato:** Login automático al sistema

## 🔄 Workflow de Evaluaciones

1. **SuperAdmin:** Gestiona normativas oficiales y crea preguntas base
2. **Admin Empresa:** Accede a evaluaciones y puede crear evaluaciones internas
3. **Admin Planta:** Gestiona evaluaciones específicas de su planta
4. **Empleados:** Responden evaluaciones asignadas (próximamente)

## �️ GESTIÓN AVANZADA DE BASE DE DATOS

### ✅ Características Disponibles

#### 📊 Exportación CSV
- **Exportación por tablas:** Empresas, empleados, plantas, departamentos, puestos, suscripciones
- **Permisos por rol:** SuperAdmin accede a todo, Admin-Empresa solo a sus datos
- **Formato optimizado:** Compatible con Excel, encoding UTF-8 con BOM
- **Filtrado automático:** Los datos se filtran por empresa según el usuario

#### 💾 Respaldos SQL (Requiere PostgreSQL PATH)
- **Respaldo Completo:** Toda la base de datos (solo SuperAdmin)
- **Respaldo Parcial:** Tablas específicas seleccionables
- **Formato estándar:** Archivos `.sql` compatibles con PostgreSQL
- **Compresión y metadatos:** Archivos optimizados con información de creación

#### 🔄 Restauración de BD
- **Restauración completa:** Desde archivos SQL (solo SuperAdmin)
- **Validación de archivos:** Verificación de integridad antes de restaurar
- **Logs de actividad:** Registro completo de todas las operaciones

#### 📋 Sistema de Logs
- **Registro de actividad:** Todas las operaciones quedan registradas
- **Información detallada:** Usuario, fecha, tablas afectadas, resultado
- **Control de acceso:** Cada usuario ve solo sus operaciones (excepto SuperAdmin)

### 🎯 Cómo usar la Gestión de BD

1. **Acceso:** Login como SuperAdmin o Admin-Empresa
2. **Navegación:** Ir a la sección "Gestión BD" en el menú principal
3. **Exportar CSV:** Seleccionar tabla y descargar
4. **Crear Respaldo:** Elegir completo o parcial (requiere PostgreSQL PATH)
5. **Restaurar:** Subir archivo SQL para restaurar (solo SuperAdmin)

### ⚠️ Requisitos para Respaldos SQL
- PostgreSQL 17 instalado
- PATH configurado correctamente (ver instrucciones arriba)
- Permisos de SuperAdmin para respaldos completos
- Conexión activa a la base de datos

## �🔧 Scripts Disponibles

- `setup.bat` - Configuración inicial completa del proyecto
- `start.bat` - Iniciar servidores backend y frontend
- `reset.bat` - Resetear base de datos y configuración
- `test_project.bat` - Ejecutar pruebas de funcionalidad

## 🎯 Estado de Desarrollo

### ✅ Completado
- [x] Sistema de autenticación completo
- [x] Registro de empresas funcional
- [x] Estructura organizacional automática
- [x] Dashboards por nivel de usuario
- [x] API REST completa
- [x] Frontend React responsivo
- [x] Scripts de configuración e inicio
- [x] Documentación completa
- [x] Módulo de evaluaciones con normativas oficiales
- [x] Gestión de preguntas por normativa (NOM-030, NOM-035, 360°)
- [x] Formularios dinámicos para diferentes tipos de preguntas
- [x] **Sistema completo de gestión de base de datos**
- [x] **Exportación CSV con filtros por usuario**
- [x] **Respaldos SQL completos y parciales con PostgreSQL**
- [x] **Restauración de base de datos**
- [x] **Sistema de logs y auditoría**

### 🔄 En Desarrollo
- [ ] Sistema de reportes avanzados
- [ ] Integración con sistemas externos
- [ ] Módulo de respuestas y análisis de evaluaciones
