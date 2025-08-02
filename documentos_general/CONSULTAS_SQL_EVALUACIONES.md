# 🗄️ CONSULTAS SQL - EVALUACIONES OFICIALES NOM

## 📋 INFORMACIÓN GENERAL

Las preguntas oficiales de NOM-030 y NOM-035 están almacenadas en estas tablas:

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| `evaluaciones_oficiales` | 2 | Evaluaciones NOM-030 y NOM-035 |
| `secciones_oficiales` | 23 | Secciones organizadas por normativa |
| `preguntas_oficiales` | 39 | Preguntas reales (27 NOM-035 + 12 NOM-030) |

---

## 🔍 CONSULTAS BÁSICAS

### Ver todas las evaluaciones oficiales
```sql
SELECT 
    id,
    tipo_norma,
    nombre,
    descripcion,
    activa,
    fecha_creacion
FROM evaluaciones_oficiales
ORDER BY tipo_norma;
```

### Ver estructura de normativas
```sql
SELECT 
    e.tipo_norma,
    COUNT(DISTINCT s.id) as total_secciones,
    COUNT(p.id) as total_preguntas
FROM evaluaciones_oficiales e
LEFT JOIN secciones_oficiales s ON e.id = s.evaluacion_oficial_id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
GROUP BY e.tipo_norma, e.nombre
ORDER BY e.tipo_norma;
```

---

## 📂 CONSULTAS POR SECCIONES

### Ver todas las secciones con sus evaluaciones
```sql
SELECT 
    s.id,
    s.numero_orden,
    s.nombre as seccion,
    s.descripcion,
    e.tipo_norma,
    e.nombre as evaluacion,
    COUNT(p.id) as total_preguntas
FROM secciones_oficiales s 
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
GROUP BY s.id, s.numero_orden, s.nombre, s.descripcion, e.tipo_norma, e.nombre
ORDER BY e.tipo_norma, s.numero_orden;
```

### Secciones de NOM-035 solamente
```sql
SELECT 
    s.numero_orden,
    s.nombre as seccion,
    COUNT(p.id) as preguntas
FROM secciones_oficiales s
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
WHERE e.tipo_norma = 'NOM-035'
GROUP BY s.numero_orden, s.nombre
ORDER BY s.numero_orden;
```

### Secciones de NOM-030 solamente
```sql
SELECT 
    s.numero_orden,
    s.nombre as seccion,
    COUNT(p.id) as preguntas
FROM secciones_oficiales s
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
WHERE e.tipo_norma = 'NOM-030'
GROUP BY s.numero_orden, s.nombre
ORDER BY s.numero_orden;
```

---

## ❓ CONSULTAS DE PREGUNTAS

### Ver todas las preguntas de NOM-035
```sql
SELECT 
    p.id,
    p.numero_orden,
    p.texto_pregunta,
    p.tipo_pregunta,
    p.opciones_respuesta,
    p.es_obligatoria,
    s.nombre as seccion
FROM preguntas_oficiales p
JOIN secciones_oficiales s ON p.seccion_id = s.id
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
WHERE e.tipo_norma = 'NOM-035'
ORDER BY p.numero_orden;
```

### Ver todas las preguntas de NOM-030
```sql
SELECT 
    p.id,
    p.numero_orden,
    p.texto_pregunta,
    p.tipo_pregunta,
    p.opciones_respuesta,
    p.es_obligatoria,
    s.nombre as seccion
FROM preguntas_oficiales p
JOIN secciones_oficiales s ON p.seccion_id = s.id
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
WHERE e.tipo_norma = 'NOM-030'
ORDER BY p.numero_orden;
```

### Buscar preguntas por palabra clave
```sql
SELECT 
    p.texto_pregunta,
    p.tipo_pregunta,
    s.nombre as seccion,
    e.tipo_norma
FROM preguntas_oficiales p
JOIN secciones_oficiales s ON p.seccion_id = s.id
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
WHERE p.texto_pregunta ILIKE '%seguridad%'  -- Cambiar 'seguridad' por la palabra que busques
ORDER BY e.tipo_norma, p.numero_orden;
```

### Preguntas por tipo
```sql
SELECT 
    e.tipo_norma,
    p.tipo_pregunta,
    COUNT(*) as cantidad
FROM preguntas_oficiales p
JOIN secciones_oficiales s ON p.seccion_id = s.id
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
GROUP BY e.tipo_norma, p.tipo_pregunta
ORDER BY e.tipo_norma, p.tipo_pregunta;
```

---

## 📊 CONSULTAS DE ANÁLISIS

### Resumen completo por normativa
```sql
SELECT 
    e.tipo_norma,
    e.nombre as evaluacion,
    e.descripcion,
    COUNT(DISTINCT s.id) as total_secciones,
    COUNT(p.id) as total_preguntas,
    COUNT(CASE WHEN p.es_obligatoria = true THEN 1 END) as preguntas_obligatorias,
    COUNT(CASE WHEN p.tipo_pregunta = 'Escala' THEN 1 END) as preguntas_escala,
    COUNT(CASE WHEN p.tipo_pregunta = 'Múltiple' THEN 1 END) as preguntas_multiple,
    COUNT(CASE WHEN p.tipo_pregunta = 'Si/No' THEN 1 END) as preguntas_sino
FROM evaluaciones_oficiales e
LEFT JOIN secciones_oficiales s ON e.id = s.evaluacion_oficial_id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
GROUP BY e.tipo_norma, e.nombre, e.descripcion
ORDER BY e.tipo_norma;
```

### Estructura detallada de NOM-035
```sql
SELECT 
    s.numero_orden as "Orden Sección",
    s.nombre as "Sección",
    COUNT(p.id) as "Total Preguntas",
    STRING_AGG(
        CONCAT(p.numero_orden, '. ', LEFT(p.texto_pregunta, 50), '...'),
        CHR(10)
    ) as "Preguntas (primeras 50 chars)"
FROM secciones_oficiales s
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
LEFT JOIN preguntas_oficiales p ON s.id = p.seccion_id
WHERE e.tipo_norma = 'NOM-035'
GROUP BY s.numero_orden, s.nombre
ORDER BY s.numero_orden;
```

### Verificar integridad de datos
```sql
SELECT 
    'Total Evaluaciones' as verificacion,
    COUNT(*) as cantidad
FROM evaluaciones_oficiales
UNION ALL
SELECT 
    'Total Secciones',
    COUNT(*)
FROM secciones_oficiales
UNION ALL
SELECT 
    'Total Preguntas',
    COUNT(*)
FROM preguntas_oficiales
UNION ALL
SELECT 
    'Secciones huérfanas (sin evaluación)',
    COUNT(*)
FROM secciones_oficiales 
WHERE evaluacion_oficial_id IS NULL
UNION ALL
SELECT 
    'Preguntas huérfanas (sin sección)',
    COUNT(*)
FROM preguntas_oficiales 
WHERE seccion_id IS NULL
UNION ALL
SELECT 
    'Evaluaciones activas',
    COUNT(*)
FROM evaluaciones_oficiales
WHERE activa = true;
```

---

## 🌐 ENDPOINTS API DISPONIBLES

Para acceder a estos datos programáticamente:

```bash
# Ver preguntas de NOM-030
GET /api/evaluaciones/oficial/normativa/nom_030/

# Ver preguntas de NOM-035  
GET /api/evaluaciones/oficial/normativa/nom_035/

# Listar todas las evaluaciones
GET /api/evaluaciones/oficial/evaluaciones-oficiales/

# Obtener todas las preguntas
GET /api/evaluaciones/oficial/preguntas-oficiales/
```

---

## 🔧 SCRIPTS DE MANTENIMIENTO

### Cargar preguntas oficiales
```bash
python cargar_preguntas_oficiales.py
```

### Verificar preguntas en BD
```bash
python verificar_preguntas_oficiales.py
```

### Ver estructura de tablas
```bash
python verificar_tablas_bd.py
```

### Resumen de integración
```bash
python resumen_integracion_final.py
```

---

## 📈 ESTADÍSTICAS ACTUALES

- **✅ 2 evaluaciones oficiales** (NOM-030 y NOM-035)
- **✅ 23 secciones oficiales** organizadas
- **✅ 39 preguntas oficiales** reales
  - 🧠 **27 preguntas NOM-035** (Factores de Riesgo Psicosocial)
  - 🛡️ **12 preguntas NOM-030** (Servicios Preventivos)
- **✅ Integridad de datos perfecta** (sin registros huérfanos)

---

*Todas las consultas han sido probadas y funcionan correctamente en PostgreSQL. Las preguntas son REALES extraídas de los documentos oficiales NOM-030 y NOM-035.*
