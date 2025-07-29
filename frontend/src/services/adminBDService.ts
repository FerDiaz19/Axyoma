// Servicio para gestión de BD y exportaciones
import axios from 'axios';
import api from '../api';

// Configurar axios para admin BD
const API_BASE = 'http://localhost:8000/api';
const adminBDApi = axios.create({
  baseURL: `${API_BASE}/admin-bd`,
  timeout: 30000, // 30 segundos para exportaciones grandes
});

// Interceptor para agregar token de autenticación
adminBDApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export interface TablaExportable {
  nombre: string;
  descripcion: string;
}

export interface EstadisticasExportacion {
  total_exportaciones: number;
  exportaciones_exitosas: number;
  exportaciones_fallidas: number;
  exportaciones_recientes: {
    archivo: string;
    fecha: string;
    tablas: string[];
    exitoso: boolean;
  }[];
}

export interface EstadisticasBD {
  empresas: number;
  plantas: number;
  departamentos: number;
  puestos: number;
  empleados: number;
  usuarios: number;
  suscripciones: number;
  pagos: number;
}

class AdminBDService {
  // Obtener tablas que el usuario puede exportar
  async listarTablasExportables(): Promise<{
    tablas_disponibles: TablaExportable[];
    nivel_usuario: string;
  }> {
    try {
      const response = await adminBDApi.get('/tablas-exportables/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener tablas exportables:', error);
      throw error;
    }
  }

  // Exportar una tabla específica a CSV
  async exportarTabla(tablaNombre: string): Promise<Blob> {
    try {
      console.log(`🔄 Iniciando exportación de tabla: ${tablaNombre}`);
      
      const response = await adminBDApi.get(`/exportar/${tablaNombre}/`, {
        responseType: 'blob',
      });
      
      console.log(`✅ Exportación exitosa de tabla: ${tablaNombre}`);
      return response.data;
    } catch (error) {
      console.error(`❌ Error al exportar tabla ${tablaNombre}:`, error);
      
      // Información adicional de debug
      if (axios.isAxiosError(error)) {
        console.error('Status:', error.response?.status);
        console.error('Headers:', error.response?.headers);
        console.error('Data:', error.response?.data);
      }
      
      throw error;
    }
  }

  // Obtener estadísticas de exportaciones
  async obtenerEstadisticas(): Promise<EstadisticasExportacion> {
    try {
      const response = await adminBDApi.get('/estadisticas-exportacion/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
      throw error;
    }
  }

  // Crear respaldo completo de la BD (SQL)
  async crearRespaldoCompleto(): Promise<any> {
    try {
      console.log('🔄 Creando respaldo completo de la BD...');
      const response = await adminBDApi.post('/respaldar-completo/');
      console.log('✅ Respaldo completo creado:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al crear respaldo completo:', error);
      throw error;
    }
  }

  // Crear respaldo parcial de tablas específicas (SQL)
  async crearRespaldoParcial(tablas: string[]): Promise<any> {
    try {
      console.log('🔄 Creando respaldo parcial...', tablas);
      const response = await adminBDApi.post('/respaldar-parcial/', {
        tablas: tablas
      });
      console.log('✅ Respaldo parcial creado:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al crear respaldo parcial:', error);
      throw error;
    }
  }

  // Descargar archivo de respaldo
  async descargarRespaldo(nombreArchivo: string): Promise<Blob> {
    try {
      console.log(`🔄 Descargando respaldo: ${nombreArchivo}`);
      const response = await adminBDApi.get(`/descargar-respaldo/${nombreArchivo}/`, {
        responseType: 'blob'
      });
      console.log(`✅ Respaldo descargado: ${nombreArchivo}`);
      return response.data;
    } catch (error) {
      console.error(`❌ Error al descargar respaldo ${nombreArchivo}:`, error);
      throw error;
    }
  }

  // Restaurar base de datos desde archivo SQL
  async restaurarBD(archivoSQL: File): Promise<any> {
    try {
      console.log('🔄 Restaurando base de datos...');
      const formData = new FormData();
      formData.append('archivo_sql', archivoSQL);
      
      const response = await adminBDApi.post('/restaurar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('✅ Base de datos restaurada exitosamente:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al restaurar base de datos:', error);
      throw error;
    }
  }

  // Función helper para descargar archivo
  descargarArchivo(blob: Blob, nombreArchivo: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = nombreArchivo;
    
    // Trigger descarga
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Limpiar URL
    window.URL.revokeObjectURL(url);
  }
}

const adminBDService = new AdminBDService();
export default adminBDService;

export const obtenerEstadisticasBD = async (): Promise<EstadisticasBD> => {
  try {
    console.log('🔍 AdminBD: Obteniendo estadísticas de BD...');
    const response = await api.get('/admin-bd/estadisticas/');
    console.log('✅ AdminBD: Estadísticas obtenidas:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ AdminBD: Error obteniendo estadísticas:', error);
    throw error;
  }
};

export const exportarTabla = async (tabla: string): Promise<void> => {
  try {
    console.log(`📤 AdminBD: Exportando tabla ${tabla}...`);
    
    const response = await api.get(`/admin-bd/exportar/${tabla}/`, {
      responseType: 'blob'
    });
    
    console.log('✅ AdminBD: Tabla exportada exitosamente');
    
    // Crear enlace de descarga
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${tabla}_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
  } catch (error) {
    console.error(`❌ AdminBD: Error al exportar tabla ${tabla}:`, error);
    throw error;
  }
};

export const tablas = [
  { 
    nombre: 'empresas', 
    descripcion: 'Lista de todas las empresas registradas en el sistema'
  },
  { 
    nombre: 'plantas', 
    descripcion: 'Lista de todas las plantas de las empresas'
  },
  { 
    nombre: 'departamentos', 
    descripcion: 'Lista de todos los departamentos por planta'
  },
  { 
    nombre: 'puestos', 
    descripcion: 'Lista de todos los puestos por departamento'
  },
  { 
    nombre: 'empleados', 
    descripcion: 'Lista de todos los empleados del sistema'
  },
  { 
    nombre: 'usuarios', 
    descripcion: 'Lista de todos los usuarios del sistema'
  },
  { 
    nombre: 'suscripciones', 
    descripcion: 'Lista de todas las suscripciones de empresas'
  },
  { 
    nombre: 'pagos', 
    descripcion: 'Lista de todos los pagos realizados'
  }
];
