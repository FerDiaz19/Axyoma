# 📋 ASIGNACIÓN DE RESPONSABILIDADES - TABLAS DE BASE DE DATOS

## 👥 INTEGRANTES Y TABLAS ASIGNADAS

### 🔥 **Yael Contreras**
**Responsable de:** Gestión de Respaldos y Sistema Central
- **1. usuarios** - Tabla principal de usuarios del sistema
- **2. admin_plantas** - Administradores de plantas
- **3. log_respaldos** - Logs del sistema de respaldos
- **4. configuracion_bd** - Configuración de base de datos

### 💻 **Misael Rubio**
**Responsable de:** Respuestas y Resultados
- **5. conjunto_respuestas** - Conjuntos de opciones
- **6. posibles_respuestas** - Posibles respuestas
- **7. seccion_preguntas** - Relación sección-pregunta
- **8. respuestas_empleado** - Respuestas de empleados

### 🌟 **Fernanda Diaz**
**Responsable de:** Gestión de Personal
- **9. empleados** - Empleados del sistema
- **10. asignaciones** - Asignaciones de evaluaciones
- **11. asignaciones_empleado** - Asignaciones por empleado
- **12. resultados_evaluacion** - Resultados de evaluaciones

### ⚡ **Ernesto Garcia**
**Responsable de:** Sistema de Evaluaciones
- **13. tipos_evaluacion** - Tipos de evaluaciones
- **14. evaluaciones** - Evaluaciones del sistema
- **15. secciones_eval** - Secciones de evaluaciones
- **16. preguntas** - Preguntas de evaluaciones

### 🎯 **Angel Diaz**
**Responsable de:** Estructura Organizacional
- **17. empresas** - Empresas del sistema
- **18. plantas** - Plantas de las empresas
- **19. departamentos** - Departamentos por planta
- **20. puestos** - Puestos por departamento

---

## 📊 RESUMEN POR RESPONSABLE

| Responsable | Cantidad | Área Principal |
|------------|----------|----------------|
| **Yael Contreras** | 4 tablas | Gestión BD y Usuarios |
| **Misael Rubio** | 4 tablas | Respuestas y Resultados |
| **Fernanda Diaz** | 4 tablas | Gestión de Personal |
| **Ernesto Garcia** | 4 tablas | Sistema de Evaluaciones |
| **Angel Diaz** | 4 tablas | Estructura Empresarial |

**TOTAL:** 20 tablas principales (excluyendo tablas N-N y del sistema Django)

---

## 🔧 RESPONSABILIDADES ESPECÍFICAS

### Para **Yael Contreras** (Respaldos y BD):
- ✅ Mantenimiento del sistema de respaldos
- ✅ Gestión de usuarios y permisos
- ✅ Configuración de base de datos
- ✅ Logs y monitoreo del sistema

### Para **Misael Rubio** (Respuestas):
- ✅ Configuración de opciones de respuesta
- ✅ Relaciones pregunta-sección
- ✅ Captura de respuestas de empleados

### Para **Fernanda Diaz** (Personal):
- ✅ CRUD de empleados
- ✅ Asignaciones de evaluaciones
- ✅ Seguimiento de resultados

### Para **Ernesto Garcia** (Evaluaciones):
- ✅ Tipos y configuración de evaluaciones
- ✅ Estructura de evaluaciones y secciones
- ✅ Gestión de preguntas

### Para **Angel Diaz** (Estructura):
- ✅ CRUD de empresas, plantas, departamentos
- ✅ Jerarquía organizacional
- ✅ Gestión de estructura empresarial

---

## 📁 ARCHIVOS DE CÓDIGO PRINCIPALES

### Backend - Respaldos y BD:
- `Backend/apps/admin_bd/views_respaldos.py` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\Backend\apps\admin_bd\views_respaldos.py`
- `Backend/apps/admin_bd/models.py` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\Backend\apps\admin_bd\models.py`
- `Backend/apps/admin_bd/urls.py` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\Backend\apps\admin_bd\urls.py`

### Frontend - Gestión BD:
- `frontend/src/components/GestionRespaldos.tsx` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\frontend\src\components\GestionRespaldos.tsx`
- `frontend/src/services/adminBDService.ts` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\frontend\src\services\adminBDService.ts`
- `frontend/src/services/respaldosService.ts` - **Yael Contreras**
  📂 **Ubicación:** `c:\xampp2\htdocs\UTT4B\Axyoma2\frontend\src\services\respaldosService.ts`

---

*Asignación realizada el 28 de Enero 2025 - Sistema Axyoma v2.0*
