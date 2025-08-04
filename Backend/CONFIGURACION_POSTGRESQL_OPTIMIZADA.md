# 🚀 CONFIGURACIÓN POSTGRESQL OPTIMIZADA PARA BACKUPS GRANDES
# ============================================================================

## **CONFIGURACIÓN RECOMENDADA PARA POSTGRESQL.CONF**

Para obtener el máximo rendimiento en backups de bases de datos grandes,
se recomienda ajustar los siguientes parámetros en PostgreSQL:

### 📊 **CONFIGURACIÓN PARA BASES DE DATOS GRANDES (>500MB):**

```postgresql
# ============================================================================
# OPTIMIZACIONES PARA BACKUP DE BD GRANDES
# ============================================================================

# Memoria y Buffer
shared_buffers = 256MB                    # 25% de la RAM disponible (mínimo)
work_mem = 256MB                         # Memoria para operaciones de ordenamiento
maintenance_work_mem = 512MB             # Memoria para operaciones de mantenimiento
effective_cache_size = 1GB               # Tamaño estimado del cache del SO

# Checkpoint y WAL (Write-Ahead Logging)
checkpoint_completion_target = 0.9       # Distribuir I/O de checkpoint
checkpoint_timeout = 15min               # Intervalo entre checkpoints
wal_buffers = 16MB                       # Buffer para WAL
max_wal_size = 2GB                       # Tamaño máximo de WAL

# Paralelización
max_worker_processes = 8                 # Máximo de workers paralelos
max_parallel_workers = 6                 # Workers paralelos por consulta
max_parallel_workers_per_gather = 4     # Workers por operación gather

# I/O y Concurrencia
effective_io_concurrency = 200          # Concurrencia de I/O
random_page_cost = 1.1                  # Costo de acceso aleatorio (SSD)
seq_page_cost = 1.0                     # Costo de acceso secuencial

# Logging (reducir durante backup)
log_min_duration_statement = 1000       # Solo logs de queries >1s
log_autovacuum_min_duration = -1        # Desactivar logs de autovacuum
log_checkpoints = off                    # Desactivar logs de checkpoint

# Autovacuum (ajustar para no interferir con backup)
autovacuum_max_workers = 2               # Reducir workers de autovacuum
autovacuum_work_mem = 256MB              # Memoria para autovacuum
```

### 📊 **CONFIGURACIÓN TEMPORAL DURANTE BACKUP:**

Estas configuraciones se pueden aplicar temporalmente durante el backup:

```sql
-- Aplicar antes del backup
SET work_mem = '512MB';
SET maintenance_work_mem = '1GB';
SET checkpoint_completion_target = 0.9;
SET log_autovacuum_min_duration = -1;
SET random_page_cost = 1.1;

-- Restaurar después del backup
RESET work_mem;
RESET maintenance_work_mem;
RESET checkpoint_completion_target;
RESET log_autovacuum_min_duration;
RESET random_page_cost;
```

---

## **CONFIGURACIÓN POR TAMAÑO DE SISTEMA:**

### 🖥️ **Sistema Pequeño (4GB RAM, BD <100MB):**
```postgresql
shared_buffers = 128MB
work_mem = 64MB
maintenance_work_mem = 128MB
effective_cache_size = 512MB
max_worker_processes = 4
max_parallel_workers = 2
```

### 🖥️ **Sistema Mediano (8GB RAM, BD 100-500MB):**
```postgresql
shared_buffers = 256MB
work_mem = 128MB  
maintenance_work_mem = 256MB
effective_cache_size = 1GB
max_worker_processes = 6
max_parallel_workers = 4
```

### 🖥️ **Sistema Grande (16GB+ RAM, BD >500MB):**
```postgresql
shared_buffers = 512MB
work_mem = 256MB
maintenance_work_mem = 512MB
effective_cache_size = 2GB
max_worker_processes = 8
max_parallel_workers = 6
```

---

## **COMANDOS DE OPTIMIZACIÓN MANUAL:**

### 🛠️ **Antes de hacer backup grande:**
```sql
-- Forzar checkpoint antes del backup
CHECKPOINT;

-- Actualizar estadísticas para mejor planificación
ANALYZE;

-- Verificar locks activos
SELECT * FROM pg_locks WHERE NOT granted;

-- Terminar conexiones idle (opcional)
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' AND state_change < now() - interval '1 hour';
```

### 🛠️ **Monitoreo durante backup:**
```sql
-- Ver progreso de backup (en otra sesión)
SELECT 
    pid,
    application_name,
    state,
    query_start,
    now() - query_start AS duration,
    query
FROM pg_stat_activity 
WHERE application_name LIKE '%pg_dump%' OR query LIKE '%pg_dump%';

-- Ver I/O del sistema
SELECT * FROM pg_stat_bgwriter;

-- Ver uso de memoria
SELECT * FROM pg_stat_database WHERE datname = current_database();
```

---

## **OPTIMIZACIONES DEL SISTEMA OPERATIVO:**

### 🖥️ **Windows (Configuración adicional):**
```powershell
# Aumentar prioridad del proceso pg_dump
wmic process where name="pg_dump.exe" CALL setpriority "above normal"

# Verificar memoria disponible
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value

# Optimizar disco (si es HDD)
fsutil behavior set DisableLastAccess 1
```

### 🖥️ **Configuración de Red (si BD está remota):**
```postgresql
# En postgresql.conf para conexiones remotas
listen_addresses = '*'
max_connections = 200
tcp_keepalives_idle = 7200
tcp_keepalives_interval = 75
tcp_keepalives_count = 9
```

---

## **TROUBLESHOOTING COMÚN:**

### ❌ **Problema: Backup muy lento**
**Solución:**
```sql
-- Verificar configuración actual
SHOW shared_buffers;
SHOW work_mem;
SHOW maintenance_work_mem;

-- Aumentar memoria temporalmente
SET work_mem = '512MB';
SET maintenance_work_mem = '1GB';
```

### ❌ **Problema: Timeout durante backup**
**Solución:**
```python
# En el código Python, aumentar timeout dinámicamente
timeout_segundos = 3600  # 1 hora para BD muy grandes
```

### ❌ **Problema: Locks durante backup**
**Solución:**
```sql
-- Ver locks bloqueantes
SELECT * FROM pg_locks WHERE NOT granted;

-- Terminar conexiones problemáticas (cuidado!)
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction';
```

### ❌ **Problema: Poco espacio en disco**
**Solución:**
```bash
# Backup con máxima compresión
pg_dump --compress=9 --format=custom

# Limpiar logs antiguos
find /var/log/postgresql/ -name "*.log" -mtime +7 -delete
```

---

## **VERIFICACIÓN DE CONFIGURACIÓN:**

### ✅ **Script de verificación:**
```sql
-- Verificar configuración actual
SELECT 
    name,
    setting,
    unit,
    context
FROM pg_settings 
WHERE name IN (
    'shared_buffers',
    'work_mem', 
    'maintenance_work_mem',
    'effective_cache_size',
    'max_worker_processes',
    'max_parallel_workers'
);

-- Verificar memoria del sistema
SELECT 
    pg_size_pretty(pg_database_size(current_database())) as db_size,
    pg_size_pretty(pg_total_relation_size('pg_class')) as catalog_size;
```

---

## **APLICACIÓN AUTOMÁTICA:**

El sistema de backup optimizado que implementamos ya aplica automáticamente
muchas de estas configuraciones durante el proceso de backup:

✅ **Configuraciones aplicadas automáticamente:**
- `work_mem = '256MB'`
- `checkpoint_completion_target = 0.9`
- `log_autovacuum_min_duration = -1`

✅ **Parámetros de pg_dump optimizados:**
- `--jobs=N` (paralelización automática)
- `--compress=9` (máxima compresión)
- `--format=custom` (formato optimizado)
- Exclusión de datos temporales

✅ **Timeouts dinámicos:**
- BD pequeñas: 15 minutos
- BD medianas: 30 minutos  
- BD grandes: 45 minutos

El sistema detecta automáticamente el tamaño de la BD y aplica la configuración óptima.
