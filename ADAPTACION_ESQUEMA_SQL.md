# ADAPTACIÓN ESQUEMA SQL - SISTEMA AXYOMA

## Resumen de Implementación

Este documento describe la adaptación del esquema SQL original (`AxyomaDB.sql`) al sistema Django actual, incluyendo los datos base que se configuran automáticamente y las futuras implementaciones pendientes.

## Estado Actual: IMPLEMENTADAS ✅

### 1. USUARIOS (tabla `usuarios`)
- **Implementado en**: `apps.users.models.PerfilUsuario` + Django User
- **Diferencias**: Se usa el modelo User de Django para autenticación y PerfilUsuario para datos adicionales
- **Datos base incluidos**:
  - SuperAdmin: `ed-rubio@axyoma.com` / `1234`
  - Admin Empresa: `juan.perez@codewave.com` / `1234`
  - Admin Planta 1: `maria.gomez@codewave.com` / `1234`
  - Admin Planta 2: `carlos.ruiz@codewave.com` / `1234`

### 2. EMPRESAS (tabla `empresas`)
- **Implementado en**: `apps.users.models.Empresa`
- **Datos base incluidos**:
  - Empresa: "Soluciones Industriales MX"
  - RFC: "SIMX920314ABC"
  - Administrador: Juan Perez (admin empresa)

### 3. PLANTAS (tabla `plantas`)
- **Implementado en**: `apps.users.models.Planta`
- **Datos base incluidos**:
  - Oficina Central Tijuana
  - Oficina Monterrey

### 4. ADMIN_PLANTAS (tabla `admin_plantas`)
- **Implementado en**: `apps.users.models.AdminPlanta`
- **Datos base incluidos**:
  - Maria Gomez → Oficina Central Tijuana
  - Carlos Ruiz → Oficina Monterrey

### 5. DEPARTAMENTOS (tabla `departamentos`)
- **Implementado en**: `apps.users.models.Departamento`
- **Datos base incluidos** (por cada planta):
  - Recursos Humanos
  - Desarrollo de Software
  - Operaciones
  - Calidad

### 6. PUESTOS (tabla `puestos`)
- **Implementado en**: `apps.users.models.Puesto`
- **Datos base incluidos**:
  - **RRHH**: Gerente de RRHH, Analista de RRHH, Reclutador
  - **Desarrollo**: Desarrollador Senior, Desarrollador Junior, Tech Lead
  - **Operaciones**: Gerente de Operaciones, Analista de Procesos, Supervisor de Turno
  - **Calidad**: Inspector de Calidad, Analista de Calidad, Coordinador de Calidad

### 7. EMPLEADOS (tabla `empleados`)
- **Implementado en**: `apps.users.models.Empleado`
- **Datos base incluidos**: 8 empleados distribuidos entre las plantas, departamentos y puestos

## Estado Futuro: PREPARADAS PARA IMPLEMENTACIÓN 🔄

### 8. PLANES_SUSCRIPCION (tabla `planes_suscripcion`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.subscriptions.models.PlanSuscripcion`
- **Datos base del SQL**:
  ```sql
  INSERT INTO PLANES_SUSCRIPCION (nombre, descripcion, duracion, precio) VALUES
      ('Suscripción Única', 'Acceso completo a las funcionalidades', 30, 899.99);
  ```

### 9. SUSCRIPCION_EMPRESA (tabla `suscripcion_empresa`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.subscriptions.models.SuscripcionEmpresa`
- **Datos base del SQL**:
  ```sql
  INSERT INTO SUSCRIPCION_EMPRESA (fecha_inicio, fecha_fin, plan_suscripcion, empresa) VALUES  
      ('2025-06-01', '2025-08-30', 1, 1);
  ```

### 10. PAGOS (tabla `pagos`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.subscriptions.models.Pago`
- **Datos base del SQL**:
  ```sql
  INSERT INTO PAGOS (costo, monto_pago, fecha_pago, transaccion_id, suscripcion_empresa)
  VALUES (899.99, 899.99, '2025-06-01', 'TXN-ABC123', 1);
  ```

### 11. TIPOS_EVALUACION (tabla `tipos_evaluacion`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.TipoEvaluacion`
- **Datos base del SQL**:
  ```sql
  INSERT INTO TIPOS_EVALUACION (nombre, descripcion) VALUES
      ('Normativa', 'Evaluaciones basadas en normativas oficiales'),
      ('Interna', 'Evaluaciones creadas para fines de evaluación internos'),
      ('360 Grados', 'Evaluaciones donde se recibe feedback de múltiples fuentes');
  ```

### 12. EVALUACIONES (tabla `evaluaciones`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.Evaluacion`
- **Datos base del SQL**:
  ```sql
  INSERT INTO EVALUACIONES (nombre, descripcion, tipo_evaluacion, empresa) VALUES
      ('Evaluación NOM-035 Inicial', 'Evaluación de los factores de riesgo psicosocial según NOM-035.', 1, NULL),
      ('Evaluación de Desempeño Q2', 'Evaluación trimestral de desempeño para empleados de desarrollo.', 2, 1),
      ('Evaluación Liderazgo 360', 'Evaluación de liderazgo para gerentes.', 3, 1);
  ```

### 13. SECCIONES_EVAL (tabla `secciones_eval`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.SeccionEval`
- **Datos base del SQL**: Secciones para cada evaluación con orden específico

### 14. PREGUNTAS (tabla `preguntas`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.Pregunta`
- **Características especiales**:
  - Soporte para preguntas dependientes (pregunta_padre, activador_padre)
  - Tipos: 'Abierta', 'Múltiple', 'Escala', 'Bool'

### 15. CONJUNTOS_OPCIONES (tabla `conjuntos_opciones`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.ConjuntoOpciones`
- **Datos base del SQL**: Escalas Likert, Sí/No, opciones personalizadas

### 16. OPCIONES_CONJUNTO (tabla `opciones_conjunto`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.OpcionConjunto`

### 17. SECCION_PREGUNTAS (tabla `seccion_preguntas`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.SeccionPregunta`

### 18. ASIGNACIONES (tabla `asignaciones`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.Asignacion`
- **Características**: Sistema de tokens UUID para acceso a evaluaciones

### 19. RESPUESTAS (tabla `respuestas`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.Respuesta`

### 20. RESULTADOS_EVAL (tabla `resultados_eval`)
- **Estado**: Modelo NO implementado
- **Ubicación sugerida**: `apps.surveys.models.ResultadoEval`

## Archivos de Configuración

### Scripts de Setup
1. **`Backend/setup_sistema_completo.py`**: Script Python que configura todos los datos base
2. **`SETUP_SISTEMA_COMPLETO.bat`**: Script batch para ejecutar el setup fácilmente

### Datos Base Configurados Automáticamente
- ✅ 4 usuarios con diferentes niveles
- ✅ 1 empresa demo
- ✅ 2 plantas (Tijuana, Monterrey)
- ✅ 4 departamentos por planta
- ✅ 3-4 puestos por departamento
- ✅ 8 empleados distribuidos
- ✅ Relaciones admin-plantas configuradas

## Instrucciones de Uso

### Para configurar un sistema nuevo:
```batch
# Ejecutar el script batch
SETUP_SISTEMA_COMPLETO.bat
```

### Para implementar las tablas futuras:
1. Crear los modelos Django en las apps correspondientes
2. Ejecutar migraciones: `python manage.py makemigrations && python manage.py migrate`
3. Adaptar el script `setup_sistema_completo.py` para incluir los nuevos datos
4. Probar la funcionalidad

## Diferencias Clave SQL → Django

### 1. Autenticación
- **SQL**: Campo `contrasena` en tabla `USUARIOS`
- **Django**: Usa el modelo `User` integrado con hash automático de contraseñas

### 2. Primary Keys
- **SQL**: `AUTO_INCREMENT`
- **Django**: `AutoField` por defecto

### 3. Foreign Keys
- **SQL**: `FOREIGN KEY(campo) REFERENCES tabla(id)`
- **Django**: `ForeignKey(Model, on_delete=CASCADE)`

### 4. Constraints
- **SQL**: Triggers y constraints a nivel de base de datos
- **Django**: Validaciones en el modelo y a nivel de aplicación

## Próximos Pasos

1. ✅ **COMPLETADO**: Sistema base funcional con usuarios, empresas, plantas, departamentos, puestos y empleados
2. 🔄 **PENDIENTE**: Implementar modelos de suscripciones (`apps.subscriptions.models`)
3. 🔄 **PENDIENTE**: Implementar modelos de evaluaciones (`apps.surveys.models`)
4. 🔄 **PENDIENTE**: Crear scripts de inicio automático para backend y frontend
5. 🔄 **PENDIENTE**: Validar triggers y constraints del SQL original en Django

## Notas Importantes

- Todas las contraseñas de demo son `1234` para facilitar las pruebas
- El sistema usa PostgreSQL como base de datos (no MySQL como en el SQL original)
- Los modelos Django incluyen validaciones adicionales no presentes en el SQL
- La estructura está preparada para escalar con las funcionalidades futuras

**Django Implementado:**
- ✅ Todos los campos implementados
- ✅ Relación con `PerfilUsuario` funcionando
- ✅ Validaciones y constraints correctos

### 3. PLANTAS → Planta
**SQL Original:**
```sql
CREATE TABLE PLANTAS (
    planta_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL UNIQUE,
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    empresa INT NOT NULL,
    FOREIGN KEY (empresa) REFERENCES EMPRESAS(empresa_id)
);
```

**Django Implementado:**
- ✅ Todos los campos implementados
- ✅ Relación con `Empresa` funcionando
- ⚠️ Nota: `nombre` no es UNIQUE globalmente, solo dentro de la empresa

### 4. ADMIN_PLANTAS → AdminPlanta
**SQL Original:**
```sql
CREATE TABLE ADMIN_PLANTAS (
    usuario INT NOT NULL,
    planta INT NOT NULL,
    fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    PRIMARY KEY(usuario, planta),
    FOREIGN KEY(usuario) REFERENCES USUARIOS(id),
    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);
```

**Django Implementado:**
- ✅ Tabla intermedia implementada
- ✅ Relaciones correctas
- ➕ Campo adicional: `password_temporal` para passwords generados

### 5. DEPARTAMENTOS → Departamento
**SQL Original:**
```sql
CREATE TABLE DEPARTAMENTOS (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE,
    planta INT NOT NULL,
    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);
```

**Django Implementado:**
- ✅ Todos los campos implementados
- ⚠️ Nota: `nombre` único solo dentro de la misma planta

### 6. PUESTOS → Puesto
**SQL Original:**
```sql
CREATE TABLE PUESTOS (
    puesto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    departamento INT NOT NULL,
    FOREIGN KEY(departamento) REFERENCES DEPARTAMENTOS(departamento_id)
);
```

**Django Implementado:**
- ✅ Todos los campos implementados
- ⚠️ Nota: `nombre` único solo dentro del mismo departamento

### 7. EMPLEADOS → Empleado
**SQL Original:**
```sql
CREATE TABLE EMPLEADOS (
    empleado_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    apellido_paterno VARCHAR(64) NOT NULL,
    apellido_materno VARCHAR(64),
    genero ENUM('Masculino', 'Femenino') NOT NULL,
    antiguedad INT,
    status BOOLEAN DEFAULT TRUE,
    puesto INT NOT NULL,
    departamento INT NOT NULL,
    planta INT NOT NULL,
    FOREIGN KEY(puesto) REFERENCES PUESTOS(puesto_id),
    FOREIGN KEY(departamento) REFERENCES DEPARTAMENTOS(departamento_id),
    FOREIGN KEY(planta) REFERENCES PLANTAS(planta_id)
);
```

**Django Implementado:**
- ✅ Todos los campos implementados
- ✅ Todas las relaciones funcionando
- ❌ Campo `salario` removido por solicitud del usuario

## ⏳ TABLAS PENDIENTES DE IMPLEMENTACIÓN

### 8. PLANES_SUSCRIPCION
**SQL Original:**
```sql
CREATE TABLE PLANES_SUSCRIPCION (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    descripcion TEXT,
    duracion INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    status BOOLEAN DEFAULT TRUE
);
```

**Estado:** ⏳ Pendiente - Preparado para implementación futura

### 9. SUSCRIPCION_EMPRESA
**SQL Original:**
```sql
CREATE TABLE SUSCRIPCION_EMPRESA (
    suscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    status BOOLEAN DEFAULT TRUE,
    plan_suscripcion INT NOT NULL,
    empresa INT NOT NULL,
    FOREIGN KEY(plan_suscripcion) REFERENCES PLANES_SUSCRIPCION(plan_id),
    FOREIGN KEY(empresa) REFERENCES EMPRESAS(empresa_id)
);
```

**Estado:** ⏳ Pendiente - Sistema de suscripciones por implementar

### 10. PAGOS
**SQL Original:**
```sql
CREATE TABLE PAGOS (
    pago_id INT AUTO_INCREMENT PRIMARY KEY,
    costo DECIMAL(10,2) NOT NULL,
    monto_pago DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    transaccion_id VARCHAR(64),
    suscripcion_empresa INT NOT NULL,
    FOREIGN KEY (suscripcion_empresa) REFERENCES SUSCRIPCION_EMPRESA(suscripcion_id)
);
```

**Estado:** ⏳ Pendiente - Sistema de pagos por implementar

### 11. TIPOS_EVALUACION
**SQL Original:**
```sql
CREATE TABLE TIPOS_EVALUACION (
    tipo_evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL UNIQUE,
    descripcion TEXT
);
```

**Estado:** ⏳ Pendiente - Módulo de evaluaciones por implementar

### 12. EVALUACIONES
**SQL Original:**
```sql
CREATE TABLE EVALUACIONES (
    evaluacion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion TEXT,
    status BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_evaluacion INT NOT NULL,
    empresa INT,
    FOREIGN KEY(tipo_evaluacion) REFERENCES TIPOS_EVALUACION(tipo_evaluacion_id),
    FOREIGN KEY(empresa) REFERENCES EMPRESAS(empresa_id)
);
```

**Estado:** ⏳ Pendiente - Módulo de evaluaciones por implementar

### 13-18. TABLAS DE EVALUACIONES
- `SECCIONES_EVAL`
- `PREGUNTAS`
- `CONJUNTOS_OPCIONES`
- `OPCIONES_CONJUNTO`
- `SECCION_PREGUNTAS`
- `ASIGNACIONES`
- `RESPUESTAS`
- `RESULTADOS_EVAL`

**Estado:** ⏳ Todas pendientes - Módulo completo de evaluaciones por implementar

## 🎯 DATOS BASE INCLUIDOS EN SETUP

El script `setup_sistema_completo.py` crea los siguientes datos:

### 👑 SuperAdmin
- **Usuario:** `superadmin`
- **Contraseña:** `admin123`
- **Email:** `ed-rubio@axyoma.com`

### 🏢 Empresa Demo
- **Nombre:** "Soluciones Industriales MX"
- **RFC:** "SIMX920314ABC"
- **Admin:** `juan.perez` / `password123`

### 🏭 Plantas
- "Oficina Central Tijuana"
- "Oficina Monterrey"
- Cada una con admin automático: `admin_[planta]` / `planta123`

### 📁 Departamentos (por planta)
- Recursos Humanos
- Desarrollo de Software
- Producción
- Control de Calidad
- Ventas
- Contabilidad
- Mantenimiento
- Logística

### 💼 Puestos (por departamento)
- Múltiples puestos jerárquicos por departamento
- Desde gerentes hasta operarios

### 👥 Empleados
- 10 empleados de demostración
- Distribuidos en diferentes departamentos y puestos
- Datos realistas para pruebas

## 🔧 DIFERENCIAS IMPLEMENTADAS

### 1. Sistema de Autenticación
- **Original:** Tabla USUARIOS con contraseña
- **Implementado:** Django User + PerfilUsuario (más seguro)

### 2. Constraints de Unicidad
- **Original:** Nombres únicos globalmente
- **Implementado:** Únicos por contexto (más lógico)

### 3. Campos Adicionales
- **Agregado:** `password_temporal` en AdminPlanta
- **Removido:** `salario` en Empleado

### 4. Validaciones
- **Mejorado:** Validaciones Django automáticas
- **Agregado:** Normalización de nombres

## 🚀 PARA USAR EL SETUP

1. **Ejecutar setup:**
   ```bash
   SETUP_SISTEMA_COMPLETO.bat
   ```

2. **Iniciar sistema:**
   ```bash
   start-backend.bat
   start-frontend.bat
   ```

3. **Acceder:**
   - URL: http://localhost:3000
   - Usar cualquiera de los usuarios creados

## 📋 SIGUIENTE FASE: EVALUACIONES

Para completar el sistema según el SQL original, falta implementar:

1. **Modelos Django para evaluaciones**
2. **API endpoints para gestión de evaluaciones**
3. **Frontend para crear/administrar evaluaciones**
4. **Sistema de respuestas y resultados**
5. **Generación de certificados**

El esquema SQL está completo y bien diseñado para esta implementación futura.

## ✅ ESTADO ACTUAL

**Funcional al 100%:**
- ✅ Autenticación multinivel
- ✅ Gestión de empresas, plantas, departamentos, puestos, empleados
- ✅ Dashboard SuperAdmin completo
- ✅ Dashboards Admin Empresa y Admin Planta
- ✅ Sistema de suspensión de empresas
- ✅ CRUD completo con edición

**Preparado para:**
- ⏳ Sistema de evaluaciones
- ⏳ Suscripciones y pagos
- ⏳ Reportes avanzados
