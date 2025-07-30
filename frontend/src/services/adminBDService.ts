/**
 * 🗄️ SERVICIO DE ADMINISTRACIÓN DE BASE DE DATOS
 * ===============================================
 * 
 * Servicio TypeScript para gestión avanzada de BD y exportaciones.
 * Funciones de SuperAdmin para respaldos, reseteo y datos iniciales.
 * 
 * 📋 Responsable: Yael Contreras
 * 📅 Fecha: Enero 2025
 * 🔢 Versión: 2.0
 * 
 * 🚀 Funcionalidades:
 * - Servicios de exportación de datos
 * - Gestión de respaldos de BD
 * - Reseteo completo del sistema
 * - Carga de datos iniciales
 * - Integración con backend Django
 * 
 * 🔒 Seguridad: Token-based authentication para SuperAdmin
 */

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
      console.log(`🔄 AdminBD: Exportando tabla ${tablaNombre}...`);
      
      // Usar endpoints directos solo para las tablas problemáticas
      const tablasProblematicas = ['empleados'];
      const endpoint = tablasProblematicas.includes(tablaNombre) 
        ? `/directo/exportar/${tablaNombre}/`
        : `/exportar/${tablaNombre}/`;
      
      const response = await adminBDApi.get(endpoint, {
        responseType: 'blob',
      });
      
      console.log(`✅ AdminBD: Exportación exitosa de tabla ${tablaNombre}`);
      return response.data;
    } catch (error) {
      console.error(`❌ AdminBD: Error al exportar tabla ${tablaNombre}:`, error);
      
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

  // Crear respaldo limpio compatible con pgAdmin
  async crearRespaldoPgAdmin(): Promise<any> {
    try {
      console.log('🔄 Creando respaldo compatible con pgAdmin...');
      const response = await adminBDApi.post('/respaldos/pgadmin/');
      console.log('✅ Respaldo pgAdmin creado:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al crear respaldo pgAdmin:', error);
      throw error;
    }
  }

  // PELIGROSO: Resetear toda la base de datos
  async resetearBD(): Promise<any> {
    try {
      console.log('⚠️ RESETEANDO BASE DE DATOS...');
      const response = await adminBDApi.post('/sistema/resetear-bd/', {
        confirmacion: 'CONFIRMO_RESETEAR_BD'
      });
      console.log('✅ Base de datos reseteada:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al resetear BD:', error);
      throw error;
    }
  }

  // Cargar datos iniciales de prueba
  async cargarDatosIniciales(): Promise<any> {
    try {
      console.log('🔄 Cargando datos iniciales...');
      const response = await adminBDApi.post('/sistema/datos-iniciales/');
      console.log('✅ Datos iniciales cargados:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al cargar datos iniciales:', error);
      throw error;
    }
  }

  // Restaurar BD al estado inicial (resetear + cargar datos)
  async restaurarEstadoInicial(): Promise<any> {
    try {
      console.log('🔄 Restaurando BD al estado inicial...');
      const response = await adminBDApi.post('/sistema/estado-inicial/', {
        confirmacion: 'CONFIRMO_RESTAURAR_INICIAL'
      });
      console.log('✅ BD restaurada al estado inicial:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al restaurar estado inicial:', error);
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
  }
];

// Exportar solo las nuevas funciones del SuperAdmin
export const crearRespaldoPgAdmin = adminBDService.crearRespaldoPgAdmin.bind(adminBDService);
export const resetearBD = adminBDService.resetearBD.bind(adminBDService);
export const cargarDatosIniciales = adminBDService.cargarDatosIniciales.bind(adminBDService);
export const restaurarEstadoInicial = adminBDService.restaurarEstadoInicial.bind(adminBDService);
