# 🔧 BITÁCORA DE SOLUCIÓN: ERROR DE CONEXIÓN Y BD

## 📋 RESUMEN DEL PROBLEMA

El sistema presentaba múltiples errores:

1. **Error de conexión al backend**: La aplicación frontend intentaba conectarse a `http://localhost:8001` cuando el servidor estaba en el puerto `8000`.
2. **Error 401 Unauthorized**: Credenciales incorrectas al intentar iniciar sesión.
3. **Error de columna en BD**: `django.db.utils.ProgrammingError: column usuarios.admin_empresa_id does not exist`
4. **Error 500 en endpoints SuperAdmin**: Los endpoints del SuperAdmin retornaban error 500 (`http://localhost:8000/apisuperadmin/listar_empresas/`)

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

### 5️⃣ Creación de superadmin

**Problema**: Necesitábamos un usuario administrador para iniciar sesión.

**Solución**:
- El script `inicializar_db.py` creó automáticamente un usuario superadmin:
  - Usuario: `superadmin`
  - Contraseña: `1234`
  - Correo: `superadmin@axyoma.com`

### 6️⃣ Corrección de rutas de API en frontend y backend

**Problema**: Los endpoints del SuperAdmin retornaban error 500 porque el frontend estaba usando una URL incorrecta (`http://localhost:8000/apisuperadmin/listar_empresas/`).

**Solución**:
- Modificamos el servicio en el frontend para usar la URL correcta:
```typescript
// URL base para endpoints de superadmin
const BASE_URL = 'api/superadmin';

export const getEmpresas = async (buscar = '', status = ''): Promise<Empresa[]> => {
  // ...
  const response = await api.get(`${BASE_URL}/listar_empresas/?${params.toString()}`);
  // ...
};
```
- Verificamos las rutas en el backend para confirmar que estaban correctamente definidas
- Creamos el script `verificar_rutas.py` para diagnosticar problemas con las rutas API

## 📝 LECCIONES APRENDIDAS

1. **Siempre verificar puertos de conexión**: Asegurarse de que el frontend se conecte al puerto correcto del backend.

2. **Nomenclatura de columnas en Django**: Django añade automáticamente el sufijo `_id` a las ForeignKeys. Cuando la BD ya existe y no sigue esta convención, se debe especificar `db_column` para indicar el nombre exacto de la columna.

3. **Scripts de diagnóstico**: Crear scripts para verificar la estructura de la BD y diagnosticar problemas es extremadamente útil.

4. **Pruebas de credenciales**: Comprobar si existen usuarios en la BD y qué credenciales funcionan ayuda a identificar problemas de autenticación.

5. **Verificación de rutas API**: Comprobar que las rutas del frontend coincidan exactamente con las del backend, prestando atención a mayúsculas/minúsculas y estructura de la URL.

## 🔄 PROCEDIMIENTO PARA FUTUROS PROBLEMAS SIMILARES

1. **Verificar conectividad**: Comprobar que el frontend esté apuntando al puerto correcto del backend.

2. **Verificar estructura de BD**: Ejecutar `python inicializar_db.py` para diagnosticar problemas en la estructura de la BD.

3. **Verificar usuarios**: Ejecutar `python verificar_credenciales.py` para comprobar si existen usuarios y qué credenciales funcionan.

4. **Revisar logs del servidor**: Los errores de Django suelen dar pistas precisas sobre el problema (como el error de columna).

5. **Revisar definición de modelos**: Si hay errores de columna, verificar que los modelos Django coincidan con la estructura real de la BD.

6. **Verificar rutas API**: Ejecutar `python verificar_rutas.py` para ver todas las rutas disponibles y probar los endpoints específicos.

## 🔒 CREDENCIALES CREADAS

| Usuario    | Contraseña | Correo                | Nivel      |
|------------|------------|----------------------|------------|
| superadmin | 1234       | superadmin@axyoma.com | superadmin |
