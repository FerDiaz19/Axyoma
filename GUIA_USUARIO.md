# 🚀 Guía de Usuario - Sistema Axyoma

## 📋 Credenciales de Acceso

### 👑 SuperAdmin
- **Usuario:** `superadmin@axyoma.com`
- **Contraseña:** `admin123`
- **Email:** `superadmin@axyoma.com`
- **Permisos:** Acceso completo al sistema

### 🏢 Admin Empresa
- **Usuario:** `admin@empresa.com`
- **Contraseña:** `admin123`
- **Email:** `admin@empresa.com`
- **Permisos:** Gestión de empresa y plantas

### 🏭 Admin Planta
- **Usuario:** `planta@empresa.com`
- **Contraseña:** `admin123`
- **Email:** `planta@empresa.com`
- **Permisos:** Gestión de planta específica

## 🌐 URLs del Sistema

- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8000/api
- **Admin Django:** http://localhost:8000/admin

## 🔧 Cómo Iniciar el Sistema

### 1. Backend (Django)
```bash
cd Backend
python manage.py runserver
```

### 2. Frontend (React)
```bash
cd frontend
npm start
```

## ✨ Funcionalidades del SuperAdmin

### 👥 Gestión de Usuarios
- ✅ Ver lista de todos los usuarios del sistema
- ✅ Crear nuevos usuarios SuperAdmin
- ✅ Editar usuarios existentes
- ✅ Suspender/activar usuarios
- ✅ Eliminar usuarios

### 🏢 Gestión de Empresas
- ✅ Ver lista de todas las empresas
- ✅ Editar información de empresas
- ✅ Suspender/activar empresas
- ✅ Eliminar empresas (incluyendo todo su contenido)

### 🏭 Gestión de Plantas
- ✅ Ver todas las plantas del sistema
- ✅ Filtrar por empresa
- ✅ Suspender/activar plantas
- ✅ Eliminar plantas

### 👥 Gestión de Departamentos
- ✅ Ver todos los departamentos
- ✅ Filtrar por planta/empresa
- ✅ Gestión completa de departamentos

### 💼 Gestión de Puestos
- ✅ Ver todos los puestos
- ✅ Filtrar por departamento/planta/empresa
- ✅ Gestión completa de puestos

### 👤 Gestión de Empleados
- ✅ Ver todos los empleados del sistema
- ✅ Filtrar por empresa/planta/departamento
- ✅ Gestión completa de empleados

### 📊 Estadísticas del Sistema
- ✅ Total de empresas/plantas/departamentos/puestos/empleados
- ✅ Contadores de entidades activas
- ✅ Distribución de usuarios por nivel

## 🎨 Características del Botón "Crear Usuario SuperAdmin"

- 👑 **Diseño especial:** Gradiente púrpura con corona
- 🔒 **Acceso restringido:** Solo visible para usuarios SuperAdmin
- ✨ **Funcionalidad completa:** Crea usuarios con nivel superadmin
- 🎯 **Campos requeridos:**
  - Username (único)
  - Email
  - Nombre
  - Apellido Paterno
  - Apellido Materno (opcional)
  - Contraseña

## 🔄 Cómo Limpiar y Recrear Usuarios Base

Si necesitas resetear los usuarios del sistema:

```bash
cd Backend
python limpiar_usuarios.py
```

Este script:
1. 🧹 Limpia TODOS los datos existentes
2. 👤 Crea los 3 usuarios base (superadmin, admin.empresa, admin.planta)
3. 🏢 Crea una empresa de prueba
4. 🏭 Crea una planta de prueba
5. 📋 Crea departamento, puesto y empleado de ejemplo

## 🚨 Notas Importantes

1. **Contraseña:** Todos los usuarios base tienen la contraseña `admin123`
2. **Datos de prueba:** El script crea datos de ejemplo para probar el sistema
3. **Limpieza total:** El script `limpiar_usuarios.py` elimina TODO - úsalo con cuidado
4. **Permisos:** Solo el SuperAdmin puede crear nuevos usuarios SuperAdmin

## 🎯 Flujo de Prueba Recomendado

1. **Login como SuperAdmin** (`superadmin@axyoma.com` / `admin123`)
2. **Verificar estadísticas** en el dashboard
3. **Crear un nuevo usuario SuperAdmin** usando el botón especial
4. **Probar edición de empresas** y usuarios
5. **Verificar filtros** en las diferentes secciones
6. **Logout y probar** con otros usuarios

## 📞 Endpoints de API Disponibles

### Autenticación
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### SuperAdmin
- `GET /api/superadmin/estadisticas_sistema/` - Estadísticas
- `GET /api/superadmin/listar_empresas/` - Lista empresas
- `GET /api/superadmin/listar_usuarios/` - Lista usuarios
- `PUT /api/superadmin/editar_empresa/` - Editar empresa
- `PUT /api/superadmin/editar_usuario/` - Editar usuario
- `POST /api/superadmin/crear_usuario/` - Crear usuario SuperAdmin

¡El sistema está completamente funcional y listo para usar! 🎉
