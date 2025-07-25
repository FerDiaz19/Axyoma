# 🔧 BITÁCORA DE SOLUCIÓN: PROBLEMAS Y CORRECCIONES DEL PROYECTO AXYOMA

## 📋 RESUMEN DEL PROBLEMA

El sistema presentaba múltiples errores:

1. **Error de conexión al backend**: La aplicación frontend intentaba conectarse a `http://localhost:8001` cuando el servidor estaba en el puerto `8000`.
2. **Error 401 Unauthorized**: Credenciales incorrectas al intentar iniciar sesión.
3. **Error de columna en BD**: `django.db.utils.ProgrammingError: column usuarios.admin_empresa_id does not exist`
4. **Error 500 en endpoints SuperAdmin**: Los endpoints del SuperAdmin retornaban error 500 (`http://localhost:8000/apisuperadmin/listar_empresas/`)
5. **Error 404 en rutas API**: La ruta `auth/login/` no existía en el backend, debía ser `api/auth/login/`

## 🚀 PASOS DE SOLUCIÓN

### 1️⃣ Corrección de puerto en API frontend

**Problema**: El frontend intentaba conectarse al puerto 8001 en lugar del 8000.

**Solución**:
- Modificamos el archivo `api.ts` para usar el puerto correcto:
```typescript
const api = axios.create({
    baseURL: 'http://localhost:8000/api',  // Cambiado de 8001 a 8000
    // ...resto del código
});
```

### 2️⃣ Diagnóstico de usuarios en la base de datos

**Problema**: No había usuarios en la base de datos o las credenciales eran incorrectas.

**Solución**:
- Creamos el script `verificar_credenciales.py` para verificar los usuarios existentes
- Ejecutamos el script para confirmar que no había usuarios en la BD:
```bash
python verificar_credenciales.py
```
- El script mostró: "❌ NO HAY USUARIOS EN LA BASE DE DATOS"

### 3️⃣ Inicialización de la base de datos

**Problema**: La estructura de la BD no estaba completa o faltaban migraciones.

**Solución**:
- Creamos el script `inicializar_db.py` para:
  - Verificar la estructura de la BD
  - Ejecutar migraciones pendientes
  - Crear usuario superadmin básico
- Ejecutamos el script:
```bash
python inicializar_db.py
```

### 4️⃣ Corrección del error de columna

**Problema**: Django buscaba la columna `admin_empresa_id` pero en la BD se llamaba `admin_empresa`.

**Solución**:
- Modificamos el modelo `PerfilUsuario` en `apps/users/models.py`:
```python
admin_empresa = models.ForeignKey(
    'self', 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True, 
    db_column='admin_empresa'  # Especificar exactamente el nombre de la columna
)
```
- Este cambio hace que Django use el nombre exacto de la columna en la BD en lugar de añadir el sufijo `_id`

### 5️⃣ Creación de usuarios de prueba

**Problema**: Necesitábamos usuarios administradores para iniciar sesión.

**Solución**:
- Creamos el script `crear_usuarios_prueba.py` que generó automáticamente:
  - Usuario: `testuser` / `testpass123` (SuperAdmin)
  - Usuario: `admin_empresa` / `admin123` (Admin Empresa)
  - Usuario: `admin_planta` / `admin123` (Admin Planta)
  - Creación automática de empresa, planta y relaciones necesarias

### 6️⃣ Corrección de rutas de API en frontend y backend

**Problema**: Los endpoints del SuperAdmin retornaban error 500 porque el frontend estaba usando URLs incorrectas.

**Solución**:
- Modificamos el servicio en el frontend para usar la URL correcta:
```typescript
// URL base para endpoints de superadmin
const BASE_URL = 'superadmin';

export const getEmpresas = async (buscar = '', status = ''): Promise<Empresa[]> => {
  // ...
  const response = await api.get(`api/${BASE_URL}/listar_empresas/?${params.toString()}`);
  // ...
};
```
- Corregimos la ruta de autenticación en `authService.ts`:
```typescript
const context = "api/auth/";
```

### 7️⃣ Implementación de endpoint health-check

**Problema**: No existía un endpoint para verificar si el backend estaba activo.

**Solución**:
- Agregamos un endpoint `health-check` en `config/urls.py`:
```python
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    # ...existing code...
    path("api/health-check/", health_check),
]
```
- Creamos el script `testConnection.js/.mjs` para verificar si el backend está activo en diferentes puertos

## 📦 SCRIPTS Y UTILIDADES CREADOS

### 🐍 Scripts Python para diagnóstico

1. **`verificar_credenciales.py`**
   - **Función**: Verifica los usuarios existentes en la base de datos
   - **Uso**: `python Backend\verificar_credenciales.py`
   - **Resultado**: Muestra lista de usuarios y prueba credenciales comunes

2. **`crear_usuarios_prueba.py`**
   - **Función**: Crea usuarios de prueba para el sistema
   - **Uso**: `python Backend\crear_usuarios_prueba.py`
   - **Resultado**: Crea 3 usuarios con diferentes niveles de acceso

3. **`verificar_rutas.py`**
   - **Función**: Muestra todas las rutas API registradas en Django
   - **Uso**: `python Backend\verificar_rutas.py`
   - **Resultado**: Lista de todos los endpoints disponibles

### 📝 Scripts JavaScript para verificación

1. **`testConnection.js`**
   - **Función**: Verifica si el backend está activo
   - **Uso**: `node frontend\src\utils\testConnection.js`
   - **Resultado**: Prueba puertos 8000, 8001 y 8080 para encontrar el servidor

2. **`testConnection.mjs`** (versión ESM)
   - **Función**: Igual que el anterior, pero usando sintaxis ES Modules
   - **Uso**: `node frontend\src\utils\testConnection.mjs`
   - **Resultado**: Compatible con Node.js moderno

3. **`serverCheck.ts`**
   - **Función**: Utilidad TypeScript para verificar servidor desde el frontend
   - **Ubicación**: `frontend\src\utils\serverCheck.ts`
   - **Función principal**: `findBackendServer()` - Busca el servidor en puertos comunes

### 🔄 Scripts de automatización

1. **`setup.bat`**
   - **Función**: Configuración inicial completa del proyecto
   - **Uso**: `setup.bat`
   - **Acciones**:
     - Crea entorno virtual Python
     - Instala dependencias backend y frontend
     - Configura la base de datos PostgreSQL
     - Ejecuta migraciones iniciales
     - Crea superusuario básico

2. **`start.bat`**
   - **Función**: Inicia todos los servidores
   - **Uso**: `start.bat`
   - **Acciones**:
     - Inicia servidor Django en puerto 8000
     - Inicia servidor React en puerto 3000
     - Verifica conexiones antes de iniciar

3. **`reset.bat`**
   - **Función**: Reinicia la base de datos y configuración
   - **Uso**: `reset.bat`
   - **Acciones**:
     - Elimina la base de datos existente
     - Crea una nueva base de datos
     - Ejecuta migraciones desde cero
     - Crea datos iniciales de prueba

## 🔄 ESTADO ACTUAL DEL PROYECTO

### ✅ Conexión Frontend-Backend

- **Puerto Backend**: 8000
- **Puerto Frontend**: 3000
- **Verificación automática**: La aplicación verifica automáticamente la conexión al backend
- **Health-check endpoint**: Disponible en `http://localhost:8000/api/health-check/`

### 👥 Usuarios disponibles

| Usuario | Contraseña | Nivel | Descripción |
|---------|------------|-------|-------------|
| `testuser` | `testpass123` | SuperAdmin | Acceso total al sistema |
| `admin_empresa` | `admin123` | Admin Empresa | Administra una empresa específica |
| `admin_planta` | `admin123` | Admin Planta | Administra una planta específica |

### 🧪 Verificación del sistema

- **Test de conexión**: Ejecutar `node frontend\src\utils\testConnection.mjs`
- **Test de credenciales**: Ejecutar `python Backend\verificar_credenciales.py`
- **Test de rutas API**: Ejecutar `python Backend\verificar_rutas.py`

### 🌐 URLs importantes

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000/api/
- **Health Check**: http://localhost:8000/api/health-check/
- **Login Endpoint**: http://localhost:8000/api/auth/login/
- **Admin Django**: http://localhost:8000/admin/

## 📝 LECCIONES APRENDIDAS

1. **Verificación temprana de conexiones**: Implementar verificaciones de conexión para detectar problemas de red.

2. **Nomenclatura en modelos Django**: Usar `db_column` para especificar exactamente el nombre de las columnas cuando la BD ya existe.

3. **Scripts de diagnóstico**: Crear scripts para verificar rápidamente el estado del sistema.

4. **Health-check endpoints**: Implementar endpoints de verificación de salud para probar la disponibilidad del servidor.

5. **Normalización de URLs**: Mantener consistencia en las rutas API entre frontend y backend.

6. **Automatización de tareas**: Crear scripts `.bat` o `.sh` para automatizar tareas repetitivas.

## 📝 PRÓXIMAS TAREAS: MÓDULO DE EVALUACIONES

### 1️⃣ Tipos de Evaluaciones a Implementar

- **Evaluaciones Normativas**:
  - Evaluación 030 - Normativa oficial
  - Evaluación 035 - Normativa oficial
  - Estas evaluaciones son estándar y sus preguntas son fijas según normativa

- **Evaluación 360**:
  - Evaluación configurable por empresa o planta
  - Las preguntas pueden ser personalizadas según las necesidades

### 2️⃣ Matriz de Permisos por Rol

#### SuperAdmin
- ✅ Administración completa de evaluaciones normativas (030, 035)
- ✅ Crear, editar, borrar y gestionar preguntas de evaluaciones normativas
- ✅ Visualizar todas las evaluaciones en el sistema
- ✅ Estadísticas generales del sistema

#### AdminEmpresa
- ✅ Ver evaluaciones normativas (sin poder modificarlas)
- ✅ Asignar evaluaciones normativas a empleados
- ✅ Administración completa de la evaluación 360 de su empresa
- ✅ Crear, editar y borrar preguntas de la evaluación 360
- ✅ Gestionar asignaciones de evaluaciones
- ✅ Ver resultados de evaluaciones

#### AdminPlanta
- ✅ Ver evaluaciones normativas (sin poder modificarlas)
- ✅ Asignar evaluaciones normativas a empleados de su planta
- ✅ Administración completa de la evaluación 360 de su planta
- ✅ Crear, editar y borrar preguntas de la evaluación 360
- ✅ Gestionar asignaciones de evaluaciones para su planta
- ✅ Ver resultados de evaluaciones de su planta

### 3️⃣ Flujo de Trabajo para Asignación de Evaluaciones

1. **Selección de Evaluación**:
   - Administrador selecciona una evaluación (030, 035 o 360)
   - Se muestra lista de empleados disponibles para asignación

2. **Filtrado de Empleados**:
   - Implementar filtros por departamento, puesto, etc.
   - Permitir selección múltiple de empleados

3. **Asignación**:
   - Verificar que cada empleado solo tenga una evaluación asignada a la vez
   - Generar un token único para cada asignación
   - Establecer fechas de inicio y fin para la evaluación

4. **Monitoreo de Evaluaciones Activas**:
   - Crear sección "Evaluaciones Activas" 
   - Mostrar información de duración, progreso, etc.
   - Permitir ver empleados asignados a cada evaluación
   - Visualización de tokens de acceso para empleados
   - Opción para agregar empleados adicionales a evaluaciones en curso

### 4️⃣ Interfaz para Empleados

- Implementar pantalla de login mediante token
- Interfaz clara para responder preguntas de evaluación
- Indicador de progreso y tiempo restante
- Confirmación al completar la evaluación

### 5️⃣ Reportes y Análisis

- Estadísticas por evaluación
- Resultados agregados por departamento/puesto
- Comparativa entre evaluaciones
- Exportación de datos a formatos comunes (Excel, PDF)

### 6️⃣ Consideraciones Técnicas

- Diseñar modelo de datos para almacenar:
  - Tipos de evaluaciones
  - Preguntas y respuestas posibles
  - Asignaciones a empleados
  - Respuestas recopiladas
  - Tokens de acceso

- Implementar lógica para:
  - Generación segura de tokens
  - Control de acceso basado en roles
  - Validación de respuestas
  - Cálculo de resultados según tipo de evaluación

## 🔄 PROCEDIMIENTO PARA FUTUROS PROBLEMAS

1. **Verificar conexión**: Usar `testConnection.mjs` para verificar si el backend está activo.

2. **Verificar usuarios**: Usar `verificar_credenciales.py` para comprobar usuarios disponibles.

3. **Verificar rutas API**: Usar `verificar_rutas.py` para ver endpoints disponibles.

4. **Reiniciar sistema**: Si hay problemas persistentes, ejecutar `reset.bat` para reiniciar todo.

5. **Configuración nueva**: En un nuevo entorno, ejecutar `setup.bat` para la configuración inicial.

---

## 🚀 INSTRUCCIONES PARA DESARROLLADORES

### 🔧 Configuración inicial

```batch
# Desde la carpeta raíz del proyecto
setup.bat
```

### 🌐 Iniciar el sistema

```batch
# Desde la carpeta raíz del proyecto
start.bat
```

### 🔄 Reiniciar desde cero

```batch
# Desde la carpeta raíz del proyecto
reset.bat
```

### 🧪 Verificar estado del sistema

```batch
# Verificar conexión al backend
node frontend\src\utils\testConnection.mjs

# Verificar usuarios en la BD
python Backend\verificar_credenciales.py

# Verificar rutas API disponibles
python Backend\verificar_rutas.py
```

**Nota importante**: El sistema está configurado para usar PostgreSQL. Asegúrate de tener PostgreSQL instalado y configurado en puerto 5432 con usuario `postgres` y contraseña `12345678`.

## 🔄 ACTUALIZACIONES RECIENTES

### 1️⃣ Mejora de UX en SuperAdminDashboard

**Problema**: Los filtros de búsqueda no se limpiaban al cambiar entre pestañas del dashboard, lo que causaba confusión al usuario.

**Solución**:
- Implementado nuevo useEffect en `SuperAdminDashboard.tsx` para limpiar automáticamente los filtros:
```typescript
// Nuevo efecto para limpiar filtros cuando cambia la sección activa
useEffect(() => {
  // Limpiar todos los filtros al cambiar de sección
  setFiltroTexto('');
  setFiltroStatus('all');
  setFiltroNivelUsuario('');
  setFiltroEmpresa('');
  
  // Log para verificar que se están limpiando los filtros
  console.log(`🧹 Limpiando filtros al cambiar a sección: ${activeSection}`);
}, [activeSection]); // Este efecto solo se ejecutará cuando cambie activeSection
```
- Esto mejora la experiencia de usuario al mantener consistencia entre las distintas secciones del dashboard.

### 2️⃣ Corrección de error de sintaxis en map function

**Problema**: Error de compilación en `SuperAdminDashboard.tsx`: "Unexpected token, expected ','" en línea 509.

**Solución**:
- Corregido error de sintaxis en la función `map` dentro de `handleSaveEdit`:
```typescript
// Antes (con error)
setPlantas(prev => prev.map item => 
  item.planta_id === id ? { ...item, ...formData } : item
);

// Después (corregido)
setPlantas(prev => prev.map((item) => 
  item.planta_id === id ? { ...item, ...formData } : item
));
```
- Se agregaron los paréntesis necesarios alrededor del parámetro `item` en la función arrow dentro del método `map`.
- Este error impedía la compilación correcta del proyecto y ha sido resuelto.

### 3️⃣ Optimización del filtrado de datos

**Problema**: El sistema realizaba búsquedas instantáneas mientras el usuario escribía, causando múltiples llamadas a la API.

**Solución**:
- Implementado debounce para el filtro de texto en `SuperAdminDashboard.tsx`:
```typescript
// Aplicar debounce al filtro de texto
const debouncedFiltroTexto = useDebounce(filtroTexto, 500);
```
- Se utiliza un hook personalizado `useDebounce` que espera 500ms de inactividad antes de realizar la búsqueda.
- Esto mejora el rendimiento reduciendo llamadas innecesarias a la API y proporciona una mejor experiencia de usuario.

## 📝 LECCIONES ADICIONALES APRENDIDAS

6. **Uso efectivo de useEffect y dependencias**: Configurar adecuadamente las dependencias en useEffect para controlar cuándo se ejecuta el código, como en el caso de la limpieza de filtros.

7. **Importancia de la sintaxis en arrow functions**: Prestar especial atención a la sintaxis correcta de arrow functions, especialmente cuando se utilizan como callbacks en métodos como `map` o `filter`.

8. **Implementación de debounce para búsquedas**: Utilizar técnicas de debounce para optimizar las búsquedas en tiempo real y reducir la carga en el servidor.
