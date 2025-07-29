// Servicio para gestión de BD y exportaciones
import axios from 'axios';

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
