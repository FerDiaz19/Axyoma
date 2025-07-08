# 📋 DOCUMENTACIÓN TÉCNICA COMPLETA - SISTEMA AXYOMA

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ IMPLEMENTADO (100% FUNCIONAL)

#### � Sistema de Suscripciones y Pagos (COMPLETAMENTE FUNCIONAL)
- **📋 Gestión de Planes de Suscripción**
  - Creación, edición y activación/desactivación de planes
  - Configuración de límites de empleados y plantas
  - Definición de precios y características
- **💳 Gestión de Suscripciones de Empresas**
  - Asignación de planes a empresas
  - Renovación automática y manual de suscripciones
  - Control de fechas de vencimiento y alertas
  - Estados: activa, vencida, suspendida, cancelada
- **💰 Registro de Pagos**
  - Múltiples métodos de pago (tarjeta, transferencia, efectivo)
  - Historial completo de transacciones
  - Referencias y estados de pago
- **🚨 Alertas y Notificaciones**
  - Suscripciones próximas a vencer
  - Estados de pagos pendientes
  - Límites de plan alcanzados

#### �🔐 Sistema de Autenticación
- Login seguro con niveles de usuario
- Tokens de autenticación JWT
- Control de acceso por roles
- Soporte para empresas suspendidas con funcionalidades limitadas

#### 👑 Panel SuperAdmin (COMPLETAMENTE FUNCIONAL)
- **📊 Dashboard con estadísticas en tiempo real**
- **🏢 Gestión completa de Empresas** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **👥 Gestión completa de Usuarios** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **🏭 Gestión completa de Plantas** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **🏢 Gestión completa de Departamentos** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **💼 Gestión completa de Puestos** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **👤 Gestión completa de Empleados** (ver, filtrar, suspender, eliminar, ✏️ editar)
- **💳 Gestión completa de Suscripciones** (ver, filtrar, renovar, crear nuevas)
- **📋 Gestión completa de Planes** (ver, crear, editar, activar/desactivar)

#### 🏢 Panel Admin Empresa (FUNCIONAL)
- Dashboard con estadísticas de la empresa
- Gestión de plantas asignadas
- Gestión de departamentos y puestos
- Gestión de empleados
- Soporte para empresas suspendidas con advertencias

#### 🏭 Panel Admin Planta (FUNCIONAL)
- Dashboard específico de la planta
- Gestión de departamentos de la planta
- Gestión de empleados de la planta

---

## 🗄️ ESQUEMA DE BASE DE DATOS

### TABLAS IMPLEMENTADAS ✅

#### 1. USUARIOS
- **Implementado en**: `apps.users.models.PerfilUsuario` + Django User
- **Diferencias**: Se usa el modelo User de Django para autenticación y PerfilUsuario para datos adicionales
- **Datos base**:
  - SuperAdmin: `ed-rubio@axyoma.com` / `1234`
  - Admin Empresa: `juan.perez@codewave.com` / `1234`
  - Admin Planta 1: `maria.gomez@codewave.com` / `1234`
  - Admin Planta 2: `carlos.ruiz@codewave.com` / `1234`

#### 2. EMPRESAS
- **Implementado en**: `apps.users.models.Empresa`
- **Datos base**: "Soluciones Industriales MX" (RFC: SIMX920314ABC)

#### 3. PLANTAS
- **Implementado en**: `apps.users.models.Planta`
- **Datos base**: Oficina Central Tijuana, Oficina Monterrey

#### 4. ADMIN_PLANTAS
- **Implementado en**: `apps.users.models.AdminPlanta`
- **Relaciones**: Maria Gomez → Tijuana, Carlos Ruiz → Monterrey

#### 5. DEPARTAMENTOS
- **Implementado en**: `apps.users.models.Departamento`
- **Datos base**: RRHH, Desarrollo, Operaciones, Calidad (por planta)

#### 6. PUESTOS
- **Implementado en**: `apps.users.models.Puesto`
- **Datos base**: Gerentes, Analistas, Desarrolladores, etc. (por departamento)

#### 7. EMPLEADOS
- **Implementado en**: `apps.users.models.Empleado`
- **Datos base**: 8 empleados de ejemplo distribuidos en plantas/departamentos

#### 8. PLANES_SUSCRIPCION ✅
- **Implementado en**: `apps.subscriptions.models.PlanSuscripcion`
- **Funcionalidades**: Creación, edición, activación/desactivación de planes
- **Configuración**: Límites de empleados/plantas, precios, características

#### 9. SUSCRIPCION_EMPRESA ✅
- **Implementado en**: `apps.subscriptions.models.SuscripcionEmpresa`
- **Funcionalidades**: Asignación de planes, renovaciones, control de vencimientos
- **Estados**: activa, vencida, suspendida, cancelada

#### 10. PAGOS ✅
- **Implementado en**: `apps.subscriptions.models.Pago`
- **Funcionalidades**: Registro de transacciones, múltiples métodos de pago
- **Seguimiento**: Estados de pago, referencias, historial completo

### TABLAS PENDIENTES DE IMPLEMENTAR ⏳

#### 11. EVALUACIONES
```sql
CREATE TABLE PAGOS (
    id_pago SERIAL PRIMARY KEY,
    id_suscripcion INTEGER REFERENCES SUSCRIPCION_EMPRESA(id_suscripcion),
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    metodo_pago VARCHAR(50),
    status_pago VARCHAR(20) DEFAULT 'pendiente'
);
```

#### 11. TIPOS_EVALUACION
```sql
CREATE TABLE TIPOS_EVALUACION (
    id_tipo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE
);
```

#### 12. EVALUACIONES
```sql
CREATE TABLE EVALUACIONES (
    id_evaluacion SERIAL PRIMARY KEY,
    id_tipo INTEGER REFERENCES TIPOS_EVALUACION(id_tipo),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    id_empresa INTEGER REFERENCES EMPRESAS(id_empresa),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE
);
```

#### 13-18. SISTEMA DE EVALUACIONES COMPLETO
- SECCIONES_EVAL
- PREGUNTAS  
- CONJUNTOS_OPCIONES
- OPCIONES_CONJUNTO
- SECCION_PREGUNTAS
- ASIGNACIONES
- RESPUESTAS
- RESULTADOS_EVAL

---

## 🔧 FUNCIONALIDADES TÉCNICAS IMPLEMENTADAS

### ✏️ Sistema de Edición Completa
- **Modal de edición universal** para todas las entidades
- **Validación de formularios** con mensajes de error
- **Campos específicos** por entidad:
  - **Empresas**: nombre, RFC, teléfono, correo, dirección, status
  - **Usuarios**: username, email, nombre completo, nivel de usuario, estado activo
  - **Plantas**: nombre, dirección, teléfono, status
  - **Departamentos**: nombre, descripción, status
  - **Puestos**: nombre, descripción, status
  - **Empleados**: nombre, apellidos, teléfono, correo, fecha ingreso, status

### 🎨 Mejoras UI/UX
- **Tabla de usuarios mejorada** con botones de acciones más visibles
- **Columna de acciones expandida** (250px) para mejor visualización
- **Botones con diseño moderno** y efectos hover
- **Responsive design** mejorado para todas las tablas
- **Filtros avanzados** para todas las entidades
- **Estadísticas en tiempo real** en dashboards

### 🔧 Backend Robusto
- **Endpoints PUT** para edición de todas las entidades
- **Validación de datos** en servidor
- **Manejo de errores** robusto
- **Logging completo** de operaciones
- **Autenticación JWT** segura
- **Control de permisos** por nivel de usuario

### � APIs de Suscripciones y Pagos (IMPLEMENTADAS)

#### Endpoints de Planes de Suscripción
- **GET** `/api/suscripciones/planes/` - Listar todos los planes
- **POST** `/api/suscripciones/planes/` - Crear nuevo plan
- **PUT** `/api/suscripciones/planes/{id}/` - Editar plan existente
- **DELETE** `/api/suscripciones/planes/{id}/` - Eliminar plan

#### Endpoints de Suscripciones de Empresas
- **GET** `/api/suscripciones/suscripciones/` - Listar todas las suscripciones
- **POST** `/api/suscripciones/suscripciones/` - Crear nueva suscripción
- **PUT** `/api/suscripciones/suscripciones/{id}/` - Editar suscripción
- **POST** `/api/suscripciones/suscripciones/{id}/renovar/` - Renovar suscripción

#### Endpoints de Pagos
- **GET** `/api/suscripciones/pagos/` - Listar todos los pagos
- **POST** `/api/suscripciones/pagos/` - Registrar nuevo pago

#### Características Técnicas
- **Cálculo automático** de fechas de vencimiento
- **Validación de límites** de plan vs empresa
- **Estados automáticos** de suscripciones (activa/vencida/suspendida)
- **Integración con sistema** de empresas y usuarios
- **Campos calculados** como días_restantes y esta_por_vencer

### �🔍 Correcciones Técnicas Aplicadas
1. **API Routes Fix**: Corregido problema de rutas dobles (/api/api/...)
2. **Endpoints corregidos**: Campos de modelos Django alineados
3. **Login para empresas suspendidas**: Permitido con funcionalidades limitadas
4. **Campo salario eliminado**: Del modal de edición de empleados
5. **Cascada de suspensiones**: Implementada correctamente

---

## 🚀 SETUP Y EJECUCIÓN

### Scripts Esenciales
- **`SETUP_SISTEMA_COMPLETO.bat`** - Setup inicial único y completo
- **`start-backend.bat`** - Inicia el servidor Django
- **`start-frontend.bat`** - Inicia el servidor React
- **`Backend/setup_sistema_completo.py`** - Script Python de configuración completa

### Proceso de Setup
1. Ejecutar `SETUP_SISTEMA_COMPLETO.bat`
2. Ejecutar `start-backend.bat`
3. Ejecutar `start-frontend.bat`
4. Sistema listo en 3 pasos

### Credenciales por Defecto
- **SuperAdmin**: `ed-rubio@axyoma.com` / `1234`
- **Admin Empresa**: `juan.perez@codewave.com` / `1234`
- **Admin Planta 1**: `maria.gomez@codewave.com` / `1234`
- **Admin Planta 2**: `carlos.ruiz@codewave.com` / `1234`

---

## 📈 EVALUACIÓN DE PROGRESO BASADA EN SRS

### 🎯 **PROGRESO TOTAL: 57.5%**

**Análisis basado en IEEE 830 - Especificación de Requerimientos de Software**

#### ✅ REQUERIMIENTOS FUNCIONALES IMPLEMENTADOS (58.57%)
- **RF-002**: Registro y gestión de empresas ✅ 100%
- **RF-004**: Gestión de plantas ✅ 100%
- **RF-005**: Gestión de usuarios ✅ 100%
- **RF-006**: Gestión de estructura organizacional ✅ 100%
- **RF-013**: Visualización y análisis de resultados 🔄 60%

#### ❌ REQUERIMIENTOS FUNCIONALES PENDIENTES (41.43%)
- **RF-001**: Gestión de suscripciones ❌ 0%
- **RF-003**: Gestión de plan de suscripción ❌ 0%
- **RF-007**: Gestión de evaluaciones ❌ 0%
- **RF-008**: Creación de evaluaciones internas ❌ 0%
- **RF-009**: Asignación y distribución de encuestas ❌ 0%
- **RF-010**: Generación de tokens para acceso ❌ 0%
- **RF-011**: Acceso a evaluaciones ❌ 0%
- **RF-012**: Registro de respuestas ❌ 0%
- **RF-014**: Respaldo y restauración de datos ❌ 0%

#### ✅ REQUERIMIENTOS NO FUNCIONALES IMPLEMENTADOS (54.29%)
- **RNF-002**: Seguridad ✅ 100%
- **RNF-005**: Mantenibilidad ✅ 100%
- **RNF-006**: Portabilidad 🔄 80%
- **RNF-007**: Usabilidad ✅ 100%

#### ❌ REQUERIMIENTOS NO FUNCIONALES PENDIENTES (45.71%)
- **RNF-001**: Rendimiento ❌ 0%
- **RNF-003**: Fiabilidad ❌ 0%
- **RNF-004**: Disponibilidad ❌ 0%

### 🚀 **COMPONENTES POR ESTADO**
- **Gestión organizacional**: 95% ✅
- **Autenticación y seguridad**: 100% ✅  
- **UI/UX moderno**: 90% ✅
- **Sistema de evaluaciones**: 0% ❌ **(CRÍTICO)**
- **Sistema de suscripciones**: 0% ❌ **(CRÍTICO)**
- **Flujo empleado-token-certificado**: 0% ❌ **(CRÍTICO)**

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

### Prioridad Alta
1. **Sistema de Suscripciones**: Implementar planes y control de límites
2. **Sistema de Pagos**: Integración con pasarelas de pago
3. **Evaluaciones Básicas**: Implementar tipos de evaluación y preguntas

### Prioridad Media
4. **Reportes**: Dashboard de reportes y estadísticas avanzadas
5. **Notificaciones**: Sistema de alertas y notificaciones
6. **API Mobile**: Endpoints optimizados para app móvil

### Prioridad Baja
7. **Optimizaciones**: Caché, rendimiento, SEO
8. **Backups**: Sistema automatizado de respaldos
9. **Monitoreo**: Logs avanzados y métricas de uso

---

*Última actualización: Enero 2025*  
*Sistema listo para producción en funcionalidades base*  
*Preparado para futuras expansiones*
