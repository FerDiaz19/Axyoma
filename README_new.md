# 🏭 AXYOMA - Sistema de Gestión de Empleados

Sistema completo de gestión de empleados para empresas industriales con arquitectura modular.

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
- **Backend**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

## 👥 Usuarios de Prueba

| Rol | Email | Password | Descripción |
|-----|-------|----------|-------------|
| **SuperAdmin** | ed-rubio@axyoma.com | 1234 | Gestión completa del sistema |
| **Admin Empresa** | juan.perez@codewave.com | 1234 | Gestión de empresa CodeWave |
| **Admin Planta** | maria.gomez@codewave.com | 1234 | Gestión de planta específica |

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
