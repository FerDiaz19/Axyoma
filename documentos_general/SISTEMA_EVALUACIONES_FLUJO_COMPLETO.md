# 📋 SISTEMA DE EVALUACIONES Y NORMAS - AXYOMA

## 🎯 VISIÓN GENERAL DEL SISTEMA

### **Objetivo Principal:**
Implementar un sistema completo de evaluaciones normativas (NOM-035, NOM-030) y personalizadas que permita a las empresas evaluar a sus empleados de manera controlada y segura.

---

## 👥 ROLES Y PERMISOS

### **🔐 SuperAdmin - Control Total**
**Permisos:**
- ✅ **Gestión completa de preguntas**
  - Crear nuevas preguntas para ambas normas
  - Editar preguntas existentes
  - Eliminar preguntas
  - Modificar secciones de evaluaciones
  - Activar/desactivar evaluaciones completas

- ✅ **Administración de normas**
  - Gestionar NOM-035 (Factores de riesgo psicosocial)
  - Gestionar NOM-030 (Seguridad y salud)
  - Crear nuevas evaluaciones normativas
  - Configurar umbrales de aprobación

- ❌ **Restricciones:**
  - NO puede asignar evaluaciones a empleados específicos
  - NO puede ver resultados individuales de empresas

### **🏢 Admin Empresa - Gestión de Evaluaciones**
**Permisos:**
- ✅ **Asignación de evaluaciones**
  - Iniciar evaluaciones para empleados de su empresa
  - Seleccionar duración de la evaluación
  - Elegir empleados participantes (checkbox)
  - Generar tokens de acceso únicos

- ✅ **Gestión de sesiones activas**
  - Ver evaluaciones activas en su empresa
  - Agregar más empleados a evaluaciones en curso
  - Monitorear tiempo restante
  - Finalizar evaluaciones anticipadamente

- ❌ **Restricciones:**
  - NO puede modificar preguntas de las normas
  - NO puede crear nuevas evaluaciones normativas
  - Solo ve empleados de su empresa

### **🏭 Admin Planta - Gestión Limitada**
**Permisos:**
- ✅ **Asignación por planta**
  - Iniciar evaluaciones para empleados de su planta únicamente
  - Mismas funciones que Admin Empresa pero limitado a su planta

- ❌ **Restricciones:**
  - NO puede asignar a empleados de otras plantas
  - NO puede ver evaluaciones de otras plantas

---

## 🔄 FLUJO COMPLETO DEL SISTEMA

### **FASE 1: Preparación (SuperAdmin)**
```
1. SuperAdmin gestiona banco de preguntas
   ├── NOM-035: Preguntas de riesgo psicosocial
   ├── NOM-030: Preguntas de seguridad y salud
   └── Configuración de secciones y umbrales
```

### **FASE 2: Asignación (Admin Empresa/Planta)**
```
2. Admin selecciona evaluación a aplicar
   ├── Elige NOM-035 o NOM-030
   ├── Define duración (días/horas)
   ├── Selecciona empleados con checkbox
   ├── Genera tokens únicos de acceso
   └── Inicia sesión de evaluación
```

### **FASE 3: Ejecución (Empleados)**
```
3. Empleado accede con token
   ├── Ingresa desde Landing Page
   ├── Sección "Responder Evaluación"
   ├── Introduce token único
   ├── Completa evaluación asignada
   └── Envía respuestas
```

### **FASE 4: Monitoreo (Admin Empresa/Planta)**
```
4. Seguimiento de evaluaciones activas
   ├── Ver progreso en tiempo real
   ├── Agregar empleados adicionales
   ├── Monitorear tiempo restante
   └── Gestionar sesiones activas
```

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS

### **Tablas Principales:**

#### **TIPOS_EVALUACION**
```sql
- id (PK)
- nombre ('Normativa', 'Interna')
- descripcion
```

#### **EVALUACIONES**
```sql
- id (PK)
- nombre ('NOM-035', 'NOM-030')
- descripcion
- instrucciones
- tiempo_limite (NULL para sin límite)
- umbral_aprobacion (% mínimo)
- status (activo/inactivo)
- tipo_evaluacion (FK)
- empresa (FK - NULL para normativas)
- creado_por (FK)
```

#### **SECCIONES_EVAL**
```sql
- id (PK)
- nombre
- descripcion
- numero_orden
- es_evaluable (boolean)
- evaluacion (FK)
```

#### **PREGUNTAS**
```sql
- id (PK)
- texto_pregunta
- tipo_pregunta ('Múltiple', 'Abierta', etc.)
- es_obligatoria (boolean)
- pregunta_padre (FK - para preguntas condicionales)
- activador_padre (valor que activa la pregunta)
```

#### **ASIGNACIONES_EVALUACION** (Nueva tabla necesaria)
```sql
- id (PK)
- evaluacion (FK)
- empresa (FK)
- planta (FK - opcional)
- admin_asignador (FK)
- fecha_inicio
- fecha_fin
- duracion_dias
- status ('activa', 'finalizada', 'cancelada')
- token_sesion (único)
- empleados_asignados (JSON o tabla relacionada)
```

#### **RESPUESTAS_EMPLEADO** (Nueva tabla necesaria)
```sql
- id (PK)
- asignacion (FK)
- empleado (FK)
- pregunta (FK)
- respuesta_texto
- fecha_respuesta
- tiempo_respuesta (segundos)
```

---

## 🎨 INTERFACES DE USUARIO

### **1. Panel SuperAdmin - Gestión de Preguntas**
**Ubicación:** Dashboard SuperAdmin → Sección "Evaluaciones"

**Funcionalidades:**
- 📝 **Editor de Preguntas**
  - Lista de preguntas por norma (NOM-035/NOM-030)
  - Formulario de creación/edición
  - Preview de evaluación completa
  - Reordenamiento de preguntas por drag & drop

- 🔧 **Configuración de Evaluaciones**
  - Activar/desactivar evaluaciones
  - Modificar umbrales de aprobación
  - Editar instrucciones generales
  - Configurar tiempo límite global

### **2. Panel Admin Empresa - Asignación de Evaluaciones**
**Ubicación:** Dashboard Empresa → Sección "Evaluaciones"

**Sub-secciones:**
- 🎯 **Iniciar Nueva Evaluación**
  - Selector de evaluación (NOM-035/NOM-030)
  - Configuración de duración
  - Grid de empleados con checkboxes
  - Botón "Generar Tokens e Iniciar"

- 📊 **Evaluaciones Activas**
  - Tabla de sesiones en curso
  - Progreso por empleado
  - Tiempo restante
  - Opciones para agregar empleados

- 📈 **Historial de Evaluaciones**
  - Evaluaciones completadas
  - Resultados agregados
  - Reportes por planta/departamento

### **3. Landing Page - Acceso para Empleados**
**Ubicación:** Landing Page → Sección "Responder Evaluación"

**Características:**
- 🔑 **Portal de Acceso**
  - Campo para introducir token
  - Validación en tiempo real
  - Información de la evaluación asignada

- ✅ **Interfaz de Evaluación**
  - Diseño limpio y profesional
  - Progreso visual
  - Guardado automático
  - Confirmación de envío

---

## 🔐 SISTEMA DE TOKENS Y SEGURIDAD

### **Generación de Tokens:**
```
Token = EMPRESA_ID + EVALUACION_ID + EMPLEADO_ID + RANDOM_HASH
Ejemplo: "EMP5_EVAL1_EMP123_A7B9C2D4"
```

### **Validaciones de Seguridad:**
- ✅ Token único por empleado por evaluación
- ✅ Verificación de tiempo de vigencia
- ✅ Validación de empleado activo
- ✅ Control de sesión única por empleado
- ✅ Bloqueo tras completar evaluación

---

## 📱 FLUJO DE PANTALLAS DETALLADO

### **SuperAdmin:**
```
Dashboard SuperAdmin
└── Evaluaciones
    ├── Gestión NOM-035
    │   ├── Lista de Preguntas
    │   ├── Editar Pregunta
    │   └── Nueva Pregunta
    ├── Gestión NOM-030
    │   ├── Lista de Preguntas
    │   ├── Editar Pregunta
    │   └── Nueva Pregunta
    └── Configuración General
        ├── Umbrales de Aprobación
        ├── Tiempos Límite
        └── Estados de Evaluaciones
```

### **Admin Empresa/Planta:**
```
Dashboard Empresa
└── Evaluaciones
    ├── Iniciar Evaluación
    │   ├── Seleccionar Norma
    │   ├── Configurar Duración
    │   ├── Seleccionar Empleados
    │   └── Generar Tokens
    ├── Evaluaciones Activas
    │   ├── Ver Progreso
    │   ├── Agregar Empleados
    │   └── Gestionar Tiempo
    └── Historial
        ├── Resultados Anteriores
        └── Reportes Generados
```

### **Empleado (Landing Page):**
```
Landing Page
└── Responder Evaluación
    ├── Introducir Token
    ├── Validar Acceso
    ├── Mostrar Instrucciones
    ├── Ejecutar Evaluación
    │   ├── Sección 1
    │   ├── Sección 2
    │   └── Sección N
    └── Confirmar Envío
```

---

## ⚙️ CONFIGURACIONES TÉCNICAS

### **Variables de Entorno Adicionales:**
```env
# Evaluaciones
EVALUATION_TOKEN_EXPIRY_HOURS=72
EVALUATION_AUTO_SAVE_INTERVAL=30
EVALUATION_MAX_CONCURRENT_SESSIONS=100

# Seguridad
EVALUATION_RATE_LIMIT=10_per_minute
EVALUATION_SESSION_TIMEOUT=3600
```

### **Nuevos Endpoints API:**
```python
# SuperAdmin
POST /api/evaluaciones/preguntas/crear/
PUT /api/evaluaciones/preguntas/{id}/editar/
DELETE /api/evaluaciones/preguntas/{id}/eliminar/
GET /api/evaluaciones/{norma}/preguntas/

# Admin Empresa
POST /api/evaluaciones/asignar/
GET /api/evaluaciones/activas/
POST /api/evaluaciones/{id}/agregar-empleados/
PUT /api/evaluaciones/{id}/finalizar/

# Empleados (público)
POST /api/evaluaciones/validar-token/
GET /api/evaluaciones/obtener/{token}/
POST /api/evaluaciones/responder/
PUT /api/evaluaciones/guardar-progreso/
```

---

## 📊 DATOS DE PRUEBA NECESARIOS

### **Evaluaciones Base:**
```sql
-- NOM-035: ID 1
-- NOM-030: ID 2
-- Preguntas: 75+ para cada norma
-- Secciones: 14 para NOM-035, 5 para NOM-030
```

### **Empleados de Prueba:**
```sql
-- Mínimo 10 empleados por empresa
-- Distribuidos en diferentes plantas
-- Con puestos y departamentos asignados
```

### **Tokens de Prueba:**
```sql
-- Tokens válidos para testing
-- Diferentes estados (activo, expirado, usado)
-- Asociados a empleados reales
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### **Fase 1: SuperAdmin - Gestión de Preguntas** ⭐ PRIORIDAD
1. Crear modelos adicionales (AsignacionEvaluacion, RespuestaEmpleado)
2. Implementar CRUD de preguntas en SuperAdmin
3. Interface para editar NOM-035 y NOM-030
4. Sistema de validaciones

### **Fase 2: Admin Empresa - Asignación** 
1. Panel de selección de evaluaciones
2. Grid de empleados con checkboxes
3. Generador de tokens únicos
4. Sistema de duración configurable

### **Fase 3: Landing Page - Portal Empleados**
1. Sección "Responder Evaluación" en landing
2. Validador de tokens
3. Interface de evaluación
4. Sistema de guardado automático

### **Fase 4: Monitoreo y Gestión**
1. Dashboard de evaluaciones activas
2. Sistema de agregar empleados
3. Controles de tiempo restante
4. Reportes básicos

---

## 🎯 OBJETIVOS DE LA PRIMERA IMPLEMENTACIÓN

### **✅ Funcionalidades Mínimas Viables:**
1. SuperAdmin puede editar preguntas de NOM-035 y NOM-030
2. Admin Empresa puede asignar evaluación a empleados seleccionados
3. Sistema genera tokens únicos para cada empleado
4. Empleados pueden acceder con token desde landing page
5. Interface básica para responder evaluación
6. Guardado de respuestas en base de datos

### **📈 Métricas de Éxito:**
- SuperAdmin puede gestionar 100+ preguntas sin problemas
- Admin puede asignar evaluación a 50+ empleados simultáneamente
- Tokens únicos sin colisiones
- Interface responsive para empleados
- Tiempo de carga < 3 segundos para evaluaciones

---

*Este documento define el sistema completo de evaluaciones para Axyoma. Implementación por fases con enfoque en funcionalidad core primero.* 🚀
