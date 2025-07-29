# 🎨 FRONTEND - INTEGRACIÓN GESTIÓN BD

## 📋 **COMPONENTES A CREAR/MODIFICAR**

### 🆕 **NUEVOS COMPONENTES REQUERIDOS:**

#### **1. `GestionBD.tsx`** (Componente principal)
**Ubicación:** `frontend/src/components/GestionBD.tsx`
**Propósito:** Panel principal de gestión de BD para SuperAdmin

```typescript
interface GestionBDProps {
  usuario: PerfilUsuario;
}

const GestionBD: React.FC<GestionBDProps> = ({ usuario }) => {
  // Estado para tablas disponibles, estadísticas, etc.
  // Funciones para exportar, descargar, ver historial
}
```

#### **2. `ExportacionCSV.tsx`** (Componente de exportación)
**Ubicación:** `frontend/src/components/ExportacionCSV.tsx`
**Propósito:** Widget de exportación para dashboards

```typescript
interface ExportacionCSVProps {
  tablaNombre: string;
  descripcion: string;
  nivelUsuario: string;
}

const ExportacionCSV: React.FC<ExportacionCSVProps> = ({ tablaNombre, descripcion, nivelUsuario }) => {
  // Botón de exportación + estado de descarga
}
```

#### **3. `EstadisticasExportacion.tsx`** (Estadísticas)
**Ubicación:** `frontend/src/components/EstadisticasExportacion.tsx`
**Propósito:** Panel de estadísticas de exportaciones

---

## 🔧 **SERVICIOS A CREAR:**

#### **1. `adminBDService.ts`** (Servicio principal)
**Ubicación:** `frontend/src/services/adminBDService.ts`

```typescript
const API_BASE = '/api/admin-bd';

export const adminBDService = {
  // Exportación
  exportarTabla: (tablaNombre: string) => Promise<Blob>,
  listarTablasExportables: () => Promise<TablaExportable[]>,
  
  // Estadísticas
  obtenerEstadisticas: () => Promise<EstadisticasExportacion>,
  
  // Respaldos (Fase 2)
  crearRespaldoCompleto: () => Promise<ResponseRespaldo>,
  listarRespaldos: () => Promise<Respaldo[]>,
};
```

---

## 📊 **INTEGRACIÓN EN DASHBOARDS EXISTENTES:**

### **SuperAdminDashboard.tsx** - Agregar nueva pestaña

#### **Modificación requerida:**
```typescript
// En el estado de pestañas activas
const [activeSection, setActiveSection] = useState('empresas');

// Agregar nueva pestaña
const secciones = [
  'empresas', 'usuarios', 'plantas', 'departamentos', 
  'puestos', 'empleados', 'gestion-bd'  // ← Nueva pestaña
];

// En el renderizado
{activeSection === 'gestion-bd' && (
  <GestionBD usuario={user.perfil} />
)}
```

#### **Nuevos botones en la navegación:**
```jsx
<button 
  onClick={() => setActiveSection('gestion-bd')}
  className={`nav-tab ${activeSection === 'gestion-bd' ? 'active' : ''}`}
>
  📊 Gestión BD
</button>
```

### **EmpresaAdminDashboard.tsx** - Agregar sección de exportación

#### **Nueva sección en el dashboard:**
```typescript
// Agregar estado para exportaciones
const [mostrarExportaciones, setMostrarExportaciones] = useState(false);

// En el renderizado
<div className="dashboard-section">
  <h3>📤 Exportar Datos</h3>
  <div className="exportacion-grid">
    <ExportacionCSV tablaNombre="empleados" descripcion="Empleados de mi empresa" />
    <ExportacionCSV tablaNombre="plantas" descripcion="Plantas de mi empresa" />
    <ExportacionCSV tablaNombre="departamentos" descripcion="Departamentos" />
    <ExportacionCSV tablaNombre="puestos" descripcion="Puestos de trabajo" />
  </div>
</div>
```

---

## 🎨 **ESTILOS CSS REQUERIDOS:**

#### **`GestionBD.css`**
```css
.gestion-bd-container {
  padding: 20px;
  background: #f8f9fa;
}

.exportacion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.exportacion-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.exportacion-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.exportacion-button:hover {
  background: #0056b3;
}

.exportacion-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.estadisticas-panel {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 15px;
  margin: 20px 0;
}

.historial-tabla {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.historial-tabla th,
.historial-tabla td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.historial-tabla th {
  background-color: #f8f9fa;
  font-weight: 600;
}
```

---

## 📱 **FLUJO DE USUARIO:**

### **Para SuperAdmin:**

1. **Acceder a Gestión BD:**
   - Clic en pestaña "Gestión BD" en dashboard
   - Ver panel principal con opciones

2. **Exportar tabla:**
   - Seleccionar tabla de la lista
   - Clic en "Exportar CSV"
   - Descarga automática del archivo

3. **Ver estadísticas:**
   - Panel con contadores de exportaciones
   - Historial de operaciones recientes

### **Para Admin Empresa:**

1. **Ver sección de exportación:**
   - Nueva sección en dashboard existente
   - Botones para exportar datos de su empresa

2. **Exportar datos:**
   - Clic en botón de tabla específica
   - Descarga CSV filtrado por su empresa

---

## 🔧 **FUNCIONES JAVASCRIPT PRINCIPALES:**

#### **Función de exportación:**
```typescript
const handleExportarTabla = async (tablaNombre: string) => {
  try {
    setDescargando(true);
    
    const blob = await adminBDService.exportarTabla(tablaNombre);
    
    // Crear URL de descarga
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${tablaNombre}_${new Date().getTime()}.csv`;
    
    // Trigger descarga
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Limpiar URL
    window.URL.revokeObjectURL(url);
    
    toast.success('Exportación completada exitosamente');
    
  } catch (error) {
    toast.error('Error al exportar: ' + error.message);
  } finally {
    setDescargando(false);
  }
};
```

#### **Cargar estadísticas:**
```typescript
const cargarEstadisticas = async () => {
  try {
    const stats = await adminBDService.obtenerEstadisticas();
    setEstadisticas(stats);
  } catch (error) {
    console.error('Error cargando estadísticas:', error);
  }
};

useEffect(() => {
  cargarEstadisticas();
}, []);
```

---

## 🎯 **PRIORIDADES DE IMPLEMENTACIÓN:**

### **Fase 1 - Básico (Inmediato):**
1. ✅ Crear `adminBDService.ts`
2. ✅ Crear `ExportacionCSV.tsx`
3. ✅ Integrar en `EmpresaAdminDashboard.tsx`
4. ✅ Estilos básicos

### **Fase 2 - Avanzado:**
1. 🔄 Crear `GestionBD.tsx` completo
2. 🔄 Integrar en `SuperAdminDashboard.tsx`
3. 🔄 Componente de estadísticas
4. 🔄 Historial de exportaciones

### **Fase 3 - Respaldos (Futuro):**
1. 🔄 Panel de respaldos
2. 🔄 Gestión de archivos
3. 🔄 Restauración de datos

---

## 🚨 **CONSIDERACIONES IMPORTANTES:**

### **Experiencia de Usuario:**
- ✅ Indicadores de carga durante exportación
- ✅ Mensajes de éxito/error claros
- ✅ Descarga automática de archivos
- ✅ Nombres de archivo descriptivos

### **Rendimiento:**
- ✅ No bloquear UI durante exportación
- ✅ Manejar archivos grandes apropiadamente
- ✅ Timeouts configurables
- ✅ Reintentos en caso de error

### **Seguridad Frontend:**
- ✅ Validar permisos antes de mostrar opciones
- ✅ Manejar tokens de autenticación
- ✅ Sanitizar datos descargados
- ✅ Logs de errores sin información sensible

---

## 📝 **ARCHIVOS DE CONFIGURACIÓN:**

### **Actualizar `api.ts`:**
```typescript
// Agregar base URL para admin BD
export const ADMIN_BD_API = '/api/admin-bd';

// Configurar timeout mayor para exportaciones grandes
const exportApi = axios.create({
  baseURL: API_BASE + '/admin-bd',
  timeout: 30000, // 30 segundos para exportaciones
});
```

### **Actualizar `routes.tsx`:**
```typescript
// No se requieren nuevas rutas, se integra en dashboards existentes
```

---

**🎯 OBJETIVO:** Implementar la funcionalidad de exportación CSV de forma transparente en los dashboards existentes, sin modificar la estructura principal de navegación del sistema.
