# CRUD de Usuarios SuperAdmin

## Descripción

El sistema Axyoma incluye un módulo completo de gestión de usuarios SuperAdmin, que permite crear, leer, actualizar y eliminar usuarios con permisos de SuperAdmin desde el panel de administración.

## Características Implementadas

### ✅ **Create (Crear)**
- **Endpoint**: `POST /api/superadmin/crear_usuario/`
- **Funcionalidad**: Crear nuevos usuarios SuperAdmin
- **Restricción**: Solo se pueden crear usuarios con nivel 'superadmin'
- **Campos requeridos**:
  - `username`: Nombre de usuario único
  - `email`: Email único
  - `nombre`: Nombre del usuario
  - `apellido_paterno`: Apellido paterno
  - `apellido_materno`: Apellido materno (opcional)
  - `password`: Contraseña (por defecto: "1234")
  - `is_active`: Estado activo (por defecto: true)

### ✅ **Read (Leer)**
- **Endpoint**: `GET /api/superadmin/listar_usuarios/`
- **Funcionalidad**: Listar todos los usuarios del sistema
- **Filtros disponibles**:
  - `buscar`: Búsqueda por nombre, apellido, email o username
  - `nivel_usuario`: Filtrar por nivel de usuario (superadmin, admin-empresa, admin-planta, empleado)
  - `activo`: Filtrar por estado activo/inactivo
- **Información mostrada**:
  - ID de usuario
  - Username y email
  - Nombre completo
  - Nivel de usuario
  - Empresa/Planta asociada (si aplica)
  - Fecha de registro
  - Estado activo/inactivo

### ✅ **Update (Actualizar)**
- **Endpoint**: `PUT /api/superadmin/editar_usuario/`
- **Funcionalidad**: Editar datos de usuarios existentes
- **Campos editables**:
  - `username`: Nombre de usuario
  - `email`: Email
  - `nombre_completo`: Nombre completo
  - `nivel_usuario`: Nivel de usuario
  - `is_active`: Estado activo/inactivo

### ✅ **Delete (Eliminar)**
- **Endpoint**: `DELETE /api/superadmin/eliminar_usuario/`
- **Funcionalidad**: Eliminar usuarios del sistema
- **Validaciones**:
  - No se puede eliminar administradores de empresa (debe eliminarse la empresa primero)
  - Se elimina el perfil y todas las relaciones asociadas
- **Proceso**:
  1. Verificar permisos de SuperAdmin
  2. Verificar si es administrador de empresa
  3. Eliminar relaciones (AdminPlanta si aplica)
  4. Eliminar perfil de usuario
  5. Eliminar usuario de Django Auth

### ✅ **Suspend/Activate (Suspender/Activar)**
- **Endpoint**: `POST /api/superadmin/suspender_usuario/`
- **Funcionalidad**: Suspender o activar usuarios
- **Parámetros**:
  - `user_id`: ID del usuario
  - `accion`: 'suspender' o 'activar'

## Interfaz de Usuario

### Panel de Gestión de Usuarios
- **Ubicación**: SuperAdmin Dashboard > Usuarios
- **Vista**: Tabla con todos los usuarios del sistema
- **Acciones disponibles**:
  - ➕ **Crear Usuario SuperAdmin**: Botón verde en la esquina superior derecha
  - ✏️ **Editar**: Botón azul para modificar datos
  - ⏸️ **Suspender**: Botón naranja para suspender usuarios
  - ▶️ **Activar**: Botón verde para reactivar usuarios
  - 🗑️ **Eliminar**: Botón rojo para eliminar permanentemente

### Modal de Creación
- **Campos**:
  - Nombre de Usuario (requerido)
  - Email (requerido)
  - Nombre (requerido)
  - Apellido Paterno (requerido)
  - Apellido Materno (opcional)
  - Contraseña Temporal (por defecto: "1234")
  - Usuario Activo (checkbox, por defecto: activado)

### Filtros Disponibles
- **Búsqueda**: Buscar por nombre, apellido, email o username
- **Estado**: Todos / Solo activos / Solo suspendidos
- **Nivel**: Todos / SuperAdmin / Admin Empresa / Admin Planta / Empleado
- **Empresa**: Filtrar por empresa específica

## Seguridad

### Autenticación
- Requiere token de autenticación válido
- Solo usuarios con nivel 'superadmin' pueden acceder

### Validaciones
- Verificación de permisos en cada endpoint
- Validación de datos de entrada
- Prevención de duplicados (username y email únicos)
- Validación de email con regex

### Restricciones
- Solo se pueden crear usuarios SuperAdmin desde esta interfaz
- No se pueden eliminar administradores de empresa sin eliminar la empresa
- Confirmación requerida para eliminación permanente

## Ejemplos de Uso

### Crear Usuario SuperAdmin
```bash
curl -X POST http://localhost:8000/api/superadmin/crear_usuario/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_superadmin",
    "email": "nuevo@ejemplo.com",
    "nombre": "Nuevo",
    "apellido_paterno": "SuperAdmin",
    "apellido_materno": "Usuario",
    "password": "mi_password_segura"
  }'
```

### Listar Usuarios
```bash
curl -X GET "http://localhost:8000/api/superadmin/listar_usuarios/?nivel_usuario=superadmin" \
  -H "Authorization: Token YOUR_TOKEN"
```

### Editar Usuario
```bash
curl -X PUT http://localhost:8000/api/superadmin/editar_usuario/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 4,
    "username": "superadmin_actualizado",
    "email": "actualizado@ejemplo.com"
  }'
```

### Suspender Usuario
```bash
curl -X POST http://localhost:8000/api/superadmin/suspender_usuario/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 4,
    "accion": "suspender"
  }'
```

### Eliminar Usuario
```bash
curl -X DELETE http://localhost:8000/api/superadmin/eliminar_usuario/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 4
  }'
```

## Arquitectura

### Backend
- **Vista**: `SuperAdminViewSet` en `apps/views.py`
- **Modelo**: `User` (Django Auth) + `PerfilUsuario` (Custom)
- **Serializers**: Integrados en el servicio
- **Permisos**: `IsAuthenticated` + verificación de SuperAdmin

### Frontend
- **Componente**: `SuperAdminDashboard.tsx`
- **Servicio**: `superAdminService.ts`
- **Modal**: `EditModal.tsx` (reutilizable)
- **Estilos**: `SuperAdminDashboard.css`

## Estados y Flujos

### Estados de Usuario
- **Activo**: Usuario puede acceder al sistema
- **Suspendido**: Usuario no puede acceder al sistema
- **Eliminado**: Usuario removido permanentemente

### Flujo de Creación
1. Usuario hace clic en "Crear Usuario SuperAdmin"
2. Se abre modal con formulario
3. Usuario completa datos requeridos
4. Sistema valida datos
5. Se crea usuario y perfil
6. Se actualiza la lista de usuarios
7. Se muestra confirmación con credenciales

### Flujo de Eliminación
1. Usuario hace clic en "Eliminar"
2. Sistema solicita confirmación (escribir "ELIMINAR")
3. Sistema valida que no sea admin de empresa
4. Se eliminan relaciones asociadas
5. Se elimina perfil y usuario
6. Se actualiza la lista de usuarios
7. Se muestra confirmación

## Mensajes de Respuesta

### Éxito
- `"Usuario SuperAdmin \"username\" creado exitosamente"`
- `"Usuario \"username\" actualizado exitosamente"`
- `"Usuario \"username\" eliminado exitosamente"`
- `"Usuario suspendido exitosamente"`
- `"Usuario activado exitosamente"`

### Errores
- `"Solo se pueden crear usuarios SuperAdmin desde esta interfaz"`
- `"El nombre de usuario ya existe"`
- `"El email ya está registrado"`
- `"No se puede eliminar el administrador de la empresa"`
- `"Usuario sin permisos de SuperAdmin"`
- `"Faltan campos requeridos"`

## Logging

El sistema registra todas las operaciones CRUD:
- Creación de usuarios
- Modificaciones de datos
- Suspensiones y activaciones
- Eliminaciones
- Intentos de acceso no autorizados

## Próximas Mejoras

- [ ] Historial de cambios por usuario
- [ ] Exportación de lista de usuarios
- [ ] Importación masiva de usuarios
- [ ] Roles y permisos más granulares
- [ ] Notificaciones por email
- [ ] Auditoría de acciones
- [ ] Recuperación de contraseñas
- [ ] Autenticación de dos factores

---

**Nota**: Este CRUD está diseñado específicamente para usuarios SuperAdmin y mantiene la integridad y seguridad del sistema mediante validaciones estrictas y verificaciones de permisos.
