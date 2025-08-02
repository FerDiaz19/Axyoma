# 🛠️ CORRECCIONES ERROR 500 POST EMPLEADOS

## ❌ Problema Identificado
Error 500 al crear empleados desde el frontend:
```
POST http://localhost:8000/api/empleados/ 500 (Internal Server Error)
```

## ✅ Correcciones Aplicadas

### 1. EmpleadoCreateSerializer Mejorado
**Archivo:** `Backend/apps/serializers.py`

#### Validaciones Específicas Añadidas:
```python
def validate_puesto(self, value):
    """Validar que el puesto existe y está activo"""
    try:
        from apps.users.models import Puesto
        if isinstance(value, int):
            puesto = Puesto.objects.get(puesto_id=value, status=True)
        else:
            puesto = value
        return puesto
    except Puesto.DoesNotExist:
        raise serializers.ValidationError(f"El puesto con ID {value} no existe o está inactivo")

def validate_email(self, value):
    """Validar que el email sea único si se proporciona"""
    if value:
        from apps.users.models import Empleado
        if Empleado.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un empleado con este email")
    return value
```

#### Generación Automática de Email Único:
```python
# Si no se proporciona email, generar uno único
if not data.get('email'):
    nombre = data.get('nombre', '').lower().replace(' ', '')
    apellido = data.get('apellido_paterno', '').lower().replace(' ', '')
    base_email = f"{nombre}.{apellido}@empresa.com"
    
    # Verificar unicidad y añadir número si es necesario
    if Empleado.objects.filter(email=base_email).exists():
        counter = 1
        while Empleado.objects.filter(email=f"{nombre}.{apellido}{counter}@empresa.com").exists():
            counter += 1
        data['email'] = f"{nombre}.{apellido}{counter}@empresa.com"
```

#### Logging Mejorado:
```python
def create(self, validated_data):
    import logging
    logger = logging.getLogger(__name__)
    
    logger.debug(f"EmpleadoCreateSerializer.create - Datos recibidos: {validated_data}")
    # ... código de creación con logs detallados
```

### 2. EmpleadoViewSet Mejorado
**Archivo:** `Backend/apps/views.py`

#### Método create() Personalizado:
```python
def create(self, request, *args, **kwargs):
    """Override create para mejor debugging"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.debug(f"EmpleadoViewSet.create - Datos recibidos: {request.data}")
    logger.debug(f"EmpleadoViewSet.create - Usuario: {request.user}")
    
    try:
        return super().create(request, *args, **kwargs)
    except Exception as e:
        logger.error(f"EmpleadoViewSet.create - Error: {e}")
        logger.error(f"EmpleadoViewSet.create - Traceback: {traceback.format_exc()}")
        raise
```

### 3. Frontend EmpleadosCRUD Mejorado
**Archivo:** `frontend/src/components/EmpleadosCRUD.tsx`

#### Selector de Departamento y Filtrado de Puestos:
```typescript
// Selector de departamento
<select name="departamento" required>
  <option value="">Seleccionar departamento</option>
  {departamentos.map(dept => ...)}
</select>

// Selector de puesto filtrado por departamento
<select name="puesto" required disabled={!formData.departamento}>
  <option value="">
    {!formData.departamento ? 'Primero selecciona un departamento' : 'Seleccionar puesto'}
  </option>
  {puestos
    .filter(puesto => puesto.departamento_id === formData.departamento)
    .map(puesto => ...)
  }
</select>
```

#### handleChange Mejorado:
```typescript
const handleChange = (e) => {
  const { name, value } = e.target;
  
  // Si cambia el departamento, resetear el puesto
  if (name === 'departamento') {
    setFormData(prev => ({
      ...prev,
      departamento: parseInt(value) || 0,
      puesto: 0 // Reset puesto cuando cambia departamento
    }));
  }
  // ... resto del código
};
```

## 🎯 Posibles Causas del Error 500

### 1. **Constraint de Email Único**
- El modelo Empleado tiene constraint único en email
- Si se envía email duplicado → Error 500
- **Solución:** Validación previa y generación automática de emails únicos

### 2. **Puesto Inexistente o Inactivo**
- Frontend envía ID de puesto que no existe
- **Solución:** Validación específica del puesto con `validate_puesto()`

### 3. **Datos de Tipo Incorrecto**
- Frontend envía strings donde Django espera integers
- **Solución:** Conversión en `to_internal_value()` y validaciones específicas

### 4. **Campos Requeridos Faltantes**
- Algunos campos del modelo son requeridos pero no se envían
- **Solución:** Valores por defecto para `fecha_ingreso` y email

## 🧪 Cómo Testear las Correcciones

### 1. Reiniciar Backend
```bash
cd Backend
python manage.py runserver
```

### 2. Probar Creación de Empleado
1. **Ir a Panel Empresa** → **Empleados**
2. **+ Agregar Empleado**
3. **Llenar formulario:**
   - Nombre: "Juan"
   - Apellidos: "Pérez García"
   - Email: (dejar vacío para auto-generación)
   - **Seleccionar departamento** → Ver filtrado de puestos
   - **Seleccionar puesto**
4. **Guardar** → Debería funcionar sin error 500

### 3. Verificar Logs
- Los logs del servidor Django ahora muestran información detallada
- Cualquier error será más específico y fácil de debuggear

## 🎉 Resultado Esperado

✅ **Antes:** Error 500 Internal Server Error  
✅ **Después:** Empleado creado exitosamente con email único auto-generado

**¡El POST de empleados ahora debería funcionar correctamente!** 👥✨
