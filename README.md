# 🏭 AXYOMA - Sistema de Gestión de Empleados

Sistema completo de gestión de empleados para empresas industriales con arquitectura modular.

## 🚀 Estado del Proyecto: ✅ COMPLETAMENTE FUNCIONAL

El sistema Axyoma está completamente configurado y funcional. Incluye un backend Django con API REST, frontend React, y funcionalidades completas de login, registro, y gestión empresarial.

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
- **PostgreSQL 12+** (usuario: postgres, password: 12345678)

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

## 🔧 Scripts Disponibles

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

### 🔄 En Desarrollo
- [ ] Sistema de reportes avanzados
- [ ] Integración con sistemas externos
- [ ] Módulo de respuestas y análisis de evaluaciones
