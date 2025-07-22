# 🚀 AXYOMA - Sistema de Gestión Empresarial

## 📋 RESUMEN DEL PROYECTO

**Axyoma** es un sistema integral de gestión empresarial con arquitectura completa Django + React. Permite administrar estructuras organizacionales, empleados, evaluaciones laborales y múltiples empresas desde una plataforma centralizada.

## 🏗️ ARQUITECTURA TÉCNICA

### Backend (Django 5.2.3)
- **Framework**: Django REST Framework
- **Base de datos**: PostgreSQL (axyomadb)
- **Autenticación**: Token-based authentication
- **API**: RESTful endpoints con serializers

### Frontend (React 18 + TypeScript)
- **Framework**: React con TypeScript estricto
- **State Management**: React hooks (useState, useEffect)
- **HTTP Client**: Axios con interceptors
- **Build Tool**: Create React App

## 👥 USUARIOS BASE DEL SISTEMA

### 🔧 SUPERADMIN (Acceso Total)
```
Username: superadmin
Password: 1234
Permisos: Gestión completa del sistema, todas las empresas, normativas oficiales
Funciones: Crear normativas, gestionar usuarios globales, configuración del sistema
```

### 👨‍💼 ADMIN EMPRESA (Gestión Empresarial)
```
Username: admin_empresa
Password: 1234  
Empresa: CodeWave
Permisos: CRUD completo de su empresa (plantas, departamentos, puestos, empleados)
Funciones: Gestión organizacional, evaluaciones internas, reportes empresariales
```

### 🏭 ADMIN PLANTA (Gestión Local)
```
Username: admin_planta
Password: 1234
Planta: Planta Principal
Permisos: Gestión de empleados y estructura de su planta específica
Funciones: Empleados de planta, evaluaciones locales, reportes por planta
```

## 🚀 INICIO RÁPIDO

### Primera Vez (Setup Completo)
```bash
# 1. Configuración inicial automática
setup.bat

# 2. Iniciar sistema completo  
start.bat
```

### Uso Diario
```bash
# Iniciar frontend y backend
start.bat
```

### En caso de problemas
```bash
# Resetear base de datos y configuración
reset.bat
```

## 🌐 ACCESOS DEL SISTEMA

Una vez iniciado el sistema:
- **Frontend**: http://localhost:3000
- **Registro Público**: http://localhost:3000/registro
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

## �️ ESTRUCTURA DE BASE DE DATOS

### Tablas Principales:
- **usuarios**: Perfiles con niveles jerárquicos (superadmin → admin-empresa → admin-planta)
- **empresas**: Información de empresas registradas con suscripciones
- **plantas**: Plantas/sucursales por empresa con ubicaciones
- **departamentos**: Departamentos organizacionales por planta
- **puestos**: Puestos de trabajo por departamento con descripción
- **empleados**: Empleados con información completa y asignación jerárquica
- **evaluaciones_preguntas**: Preguntas por normativa (NOM-030, NOM-035, 360°)
- **subscriptions**: Planes de suscripción por empresa

## 🔄 OPERACIONES CRUD - ESTADO ACTUAL

### ✅ **PLANTAS** - FUNCIONANDO
- ✅ Crear plantas con validación de empresa
- ✅ Listar plantas filtradas por empresa del usuario
- ✅ Actualizar información y ubicación
- ✅ Validación de campos requeridos

### ✅ **DEPARTAMENTOS** - FUNCIONANDO  
- ✅ Crear departamentos vinculados a plantas
- ✅ Listar departamentos por empresa/planta
- ✅ Actualizar descripción y estructura
- ✅ Nombres únicos por planta

### ✅ **PUESTOS** - FUNCIONANDO
- ✅ Crear puestos vinculados a departamentos
- ✅ Listar con jerarquía completa (empresa→planta→departamento)
- ✅ Actualizar descripción y requisitos
- ✅ Nombres únicos por departamento

### ✅ **EMPLEADOS** - MAYORMENTE FUNCIONANDO
- ✅ **CREAR**: Empleados con información completa (nombre, apellidos, email, teléfono, fecha_ingreso)
- ✅ **LEER**: Listar empleados con información jerárquica completa
- ✅ **ACTUALIZAR**: Modificar datos y reasignar puestos
- ⚠️ **ELIMINAR**: Error por dependencia con tabla evaluaciones (`evaluaciones_respuestaevaluacion` no existe)

### 🔧 **PROBLEMA CONOCIDO - DELETE EMPLEADOS**
```
Error SQL: no existe la relación «evaluaciones_respuestaevaluacion»
Causa: Tabla de evaluaciones no migrada correctamente
Estado: CREATE/READ/UPDATE funcionan perfectamente
Solución temporal: Evitar DELETE hasta resolver dependencias de BD
```

## 📋 REQUISITOS DEL SISTEMA

- **Python 3.10+** con pip actualizado
- **Node.js 16+** con npm/yarn
- **PostgreSQL 12+** 
  - Usuario: `postgres` 
  - Password: `12345678`
  - Base de datos: `axyomadb`

## 🔗 ENDPOINTS API PRINCIPALES

### Autenticación
- `POST /api/auth/login/` - Login con username/password
- `POST /api/auth/logout/` - Logout con invalidación de token
- `POST /api/auth/register/` - Registro de nuevos usuarios

### Gestión Organizacional (Requiere autenticación)
- `GET|POST /api/plantas/` - Gestión de plantas por empresa
- `GET|POST /api/departamentos/` - Gestión de departamentos por planta
- `GET|POST /api/puestos/` - Gestión de puestos por departamento  
- `GET|POST|PUT /api/empleados/` - Gestión completa de empleados
- `DELETE /api/empleados/{id}/` - ⚠️ Pendiente por dependencia BD

### Registro Público
- `POST /api/registro/empresa/` - Registro automático de empresas con estructura inicial

### Evaluaciones
- `GET /api/evaluaciones/preguntas/` - Preguntas por normativa
- `GET /api/normativas/` - Normativas oficiales disponibles

## 🔐 NIVELES DE ACCESO Y PERMISOS

### **SUPERADMIN**
- ✅ Acceso a todas las empresas del sistema
- ✅ Gestión completa de normativas oficiales (NOM-030, NOM-035, 360°)
- ✅ Configuración global del sistema
- ✅ Creación y gestión de usuarios administradores

### **ADMIN EMPRESA**  
- ✅ Gestión completa de SU empresa específica
- ✅ CRUD total: plantas, departamentos, puestos, empleados de SU empresa
- ✅ Creación de evaluaciones internas
- ❌ No puede acceder a otras empresas

### **ADMIN PLANTA**
- ✅ Gestión de SU planta específica únicamente
- ✅ Empleados y estructura organizacional de SU planta
- ✅ Evaluaciones y reportes por planta
- ❌ No puede gestionar otras plantas

## 📁 ARCHIVOS TÉCNICOS IMPORTANTES

### Backend Django
- `Backend/apps/users/models.py` - Modelos de datos principales con relaciones
- `Backend/apps/users/views.py` - Lógica de negocio, APIs y permisos  
- `Backend/apps/users/serializers.py` - Serialización y validación de datos
- `Backend/apps/evaluaciones/models.py` - Sistema de evaluaciones y normativas
- `Backend/config/settings/local.py` - Configuración de desarrollo

### Frontend React TypeScript
- `frontend/src/services/empleadoService.ts` - ✅ API service corregido con interfaces
- `frontend/src/components/EmpleadosCRUD.tsx` - ✅ Componente principal corregido
- `frontend/src/services/organizacionService.ts` - ✅ Servicios organizacionales
- `frontend/src/components/GestionPlantas.tsx` - Gestión de plantas
- `frontend/src/routes.tsx` - Enrutamiento y protección de rutas

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### ✅ **Sistema de Autenticación Completo**
- Login/logout con gestión de tokens
- Registro público de empresas
- Perfiles diferenciados por nivel
- Protección de rutas por permisos

### ✅ **Gestión Empresarial Integral**
- Registro automático con estructura inicial
- Plantas → Departamentos → Puestos → Empleados
- Jerarquía organizacional completa
- Filtros automáticos por empresa/usuario

### ✅ **Estructura Organizacional Automática**
Al registrar empresa se crea:
- ✅ Planta Principal automática
- ✅ Departamentos base (Administración, RRHH, Finanzas, Operaciones)
- ✅ Puestos predefinidos por departamento
- ✅ Suscripción básica automática
- ✅ Usuario admin-empresa con permisos

### ✅ **Sistema de Evaluaciones Oficial**
- ✅ Normativas oficiales: **NOM-030**, **NOM-035**, **Evaluación 360°**
- ✅ Gestión de preguntas por normativa con tipos variados
- ✅ Tipos de pregunta: Opción múltiple, Sí/No, Escala Likert, Texto libre
- ✅ Control de acceso: SuperAdmin→normativas, Empresas→evaluaciones internas

## 🔄 WORKFLOW COMPLETO DE USO

### 1. **Registro de Empresa** (`/registro`)
1. Completar datos de empresa (nombre, dirección, teléfono)
2. Crear credenciales de admin-empresa
3. Selección de plan de suscripción
4. **Creación automática**: estructura organizacional completa
5. **Login automático**: acceso inmediato al sistema

### 2. **Gestión Admin-Empresa**
1. **Dashboard**: Resumen de empresa con estadísticas
2. **Plantas**: Crear/editar plantas adicionales
3. **Departamentos**: Gestionar estructura por planta
4. **Puestos**: Definir puestos con descripción y requisitos
5. **Empleados**: Alta/baja/modificación con asignación de puestos
6. **Evaluaciones**: Crear evaluaciones internas y asignar

### 3. **Gestión Admin-Planta**
1. **Vista filtrada**: Solo empleados y estructura de su planta
2. **Gestión local**: CRUD de empleados de su planta
3. **Reportes**: Estadísticas y reportes por planta
4. **Evaluaciones**: Aplicar evaluaciones a empleados locales

## 🔧 SCRIPTS Y COMANDOS DISPONIBLES

- `setup.bat` - **Setup inicial**: Instala dependencias, crea BD, migra, datos iniciales
- `start.bat` - **Inicio normal**: Levanta backend (puerto 8000) y frontend (puerto 3000) 
- `reset.bat` - **Reset completo**: Limpia BD, reinstala, reconfigura todo
- `test_project.bat` - **Testing**: Ejecuta pruebas de funcionalidad y APIs

### Comandos manuales útiles:
```bash
# Backend
cd Backend
python manage.py runserver                    # Iniciar servidor Django
python manage.py migrate                      # Aplicar migraciones
python manage.py createsuperuser              # Crear superusuario
python manage.py shell                        # Consola Django

# Frontend  
cd frontend
npm start                                      # Iniciar React en modo desarrollo
npm run build                                 # Build para producción
npm test                                      # Ejecutar pruebas Jest
```

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ **Error PostgreSQL**
```bash
# Verificar PostgreSQL ejecutándose en puerto 5432
# Credenciales: postgres/12345678
# Base de datos: axyomadb debe existir
```

### ❌ **Error dependencias Python/Node**
```bash
# Reinstalar todo desde cero
reset.bat
setup.bat
```

### ❌ **Error de autenticación/tokens**
```bash
# Limpiar tokens y sesiones
reset.bat
# O manualmente limpiar localStorage del navegador
```

### ❌ **Error compilación TypeScript** 
```bash
# Frontend - limpiar cache y reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## ✅ ESTADO ACTUAL DEL PROYECTO

### **Backend: COMPLETAMENTE FUNCIONAL ✅**
- ✅ APIs REST operativas con documentación Swagger
- ✅ Autenticación robusta con tokens JWT  
- ✅ CRUD operations: CREATE ✅, READ ✅, UPDATE ✅, DELETE ⚠️ (solo empleados)
- ✅ Filtros automáticos por empresa/usuario
- ✅ Validaciones y serializadores completos

### **Frontend: COMPLETAMENTE FUNCIONAL ✅**
- ✅ Componentes TypeScript corregidos y tipados
- ✅ Interfaces alineadas con backend APIs
- ✅ Formularios reactivos con validación
- ✅ Listados con paginación y filtros
- ✅ Navegación protegida por roles

### **Integración: COMPLETAMENTE FUNCIONAL ✅**  
- ✅ Frontend ↔ Backend comunicación establecida
- ✅ Campos de formularios alineados correctamente
- ✅ Manejo de errores y estados de carga
- ✅ Autenticación end-to-end funcional

## 🎯 PRÓXIMOS DESARROLLOS

### 🔄 **Inmediato (Alta Prioridad)**
- [ ] **Corregir DELETE empleados**: Resolver dependencia con tabla evaluaciones_respuestaevaluacion
- [ ] **Testing integral**: Pruebas automatizadas frontend + backend
- [ ] **Validaciones mejoradas**: Mensajes de error más descriptivos

### 🔄 **Mediano Plazo**
- [ ] **Sistema de reportes**: Dashboards analíticos por empresa/planta
- [ ] **Módulo de respuestas**: Empleados completando evaluaciones asignadas
- [ ] **Notificaciones**: Sistema de alertas y recordatorios
- [ ] **Integración API**: Conexión con sistemas externos (nómina, RRHH)

### 🔄 **Largo Plazo**
- [ ] **Mobile App**: Aplicación móvil React Native
- [ ] **BI y Analytics**: Inteligencia de negocio con gráficos avanzados
- [ ] **Multi-idioma**: Soporte para múltiples idiomas
- [ ] **Auditoría**: Log completo de cambios y acciones

---

**🔧 Desarrollado por**: Equipo Axyoma  
**📅 Última actualización**: Julio 2025  
**🚀 Versión**: 1.0.0 - Producción estable  
**📞 Soporte**: Revisar issues en repositorio o contactar al equipo técnico
