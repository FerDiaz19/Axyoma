// Servicio para gestión de respaldos y restauración
// Solo disponible para SuperAdmin

export interface RespaldoMetadata {
  tipo: 'tablas' | 'bd_completa';
  tablas?: string[];
  incluir_datos: boolean;
  descripcion: string;
  fecha_creacion: string;
  usuario: string;
  archivo: string;
  tamaño_bytes: number;
  tamaño_mb: number;
  base_datos: string;
  existe_archivo: boolean;
}

export interface InfoSistemaRespaldos {
  directorio_respaldos: string;
  base_datos: string;
  host: string;
  puerto: string;
  cantidad_respaldos: number;
  espacio_usado_mb: number;
  herramientas_disponibles: {
    pg_dump: boolean;
    psql: boolean;
  };
}

export interface CrearRespaldoTablasRequest {
  tablas: string[];
  incluir_datos: boolean;
  descripcion?: string;
}

export interface CrearRespaldoBDRequest {
  incluir_datos: boolean;
  descripcion?: string;
}

export interface RestaurarRespaldoRequest {
  archivo: string;
  confirmar: boolean;
  modo: 'replace' | 'append';
}

class RespaldosService {
  private baseURL = 'http://127.0.0.1:8000/api/admin-bd/respaldos';

  private async getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error('No hay token de autenticación');
    }
    
    return {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    };
  }

  /**
   * Obtener información del sistema de respaldos
   */
  async obtenerInfoSistema(): Promise<InfoSistemaRespaldos> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/info/`, {
        method: 'GET',
        headers
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al obtener información del sistema');
      }

      return await response.json();
    } catch (error) {
      console.error('Error al obtener info del sistema:', error);
      throw error;
    }
  }

  /**
   * Listar todos los respaldos disponibles
   */
  async listarRespaldos(): Promise<RespaldoMetadata[]> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/listar/`, {
        method: 'GET',
        headers
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al listar respaldos');
      }

      const data = await response.json();
      return data.respaldos;
    } catch (error) {
      console.error('Error al listar respaldos:', error);
      throw error;
    }
  }

  /**
   * Crear respaldo de tablas específicas
   */
  async crearRespaldoTablas(request: CrearRespaldoTablasRequest): Promise<any> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/tablas/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al crear respaldo de tablas');
      }

      return await response.json();
    } catch (error) {
      console.error('Error al crear respaldo de tablas:', error);
      throw error;
    }
  }

  /**
   * Crear respaldo completo de la base de datos
   */
  async crearRespaldoCompleto(request: CrearRespaldoBDRequest): Promise<any> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/bd-completa/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request)
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error completo del servidor:', errorData);
        
        // Mostrar información detallada del error para debug
        let errorMessage = errorData.error || 'Error al crear respaldo completo';
        if (errorData.directorio_backup) {
          errorMessage += `\nDirectorio: ${errorData.directorio_backup}`;
        }
        if (errorData.archivo_destino) {
          errorMessage += `\nArchivo: ${errorData.archivo_destino}`;
        }
        if (errorData.comando_ejecutado) {
          errorMessage += `\nComando: ${errorData.comando_ejecutado}`;
        }
        if (errorData.details) {
          errorMessage += `\nDetalles: ${errorData.details}`;
        }
        
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('Error al crear respaldo completo:', error);
      throw error;
    }
  }

  /**
   * Restaurar un respaldo
   */
  async restaurarRespaldo(request: RestaurarRespaldoRequest): Promise<any> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/restaurar/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al restaurar respaldo');
      }

      return await response.json();
    } catch (error) {
      console.error('Error al restaurar respaldo:', error);
      throw error;
    }
  }

  /**
   * Descargar un archivo de respaldo
   */
  async descargarRespaldo(archivo: string): Promise<void> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/descargar/${archivo}/`, {
        method: 'GET',
        headers: {
          'Authorization': headers.Authorization
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al descargar respaldo');
      }

      // Crear blob y descargar archivo
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = archivo;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error al descargar respaldo:', error);
      throw error;
    }
  }

  /**
   * Eliminar un respaldo
   */
  async eliminarRespaldo(archivo: string): Promise<void> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${this.baseURL}/eliminar/${archivo}/`, {
        method: 'DELETE',
        headers
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al eliminar respaldo');
      }
    } catch (error) {
      console.error('Error al eliminar respaldo:', error);
      throw error;
    }
  }

  /**
   * Obtener tablas disponibles para respaldo
   */
  getTablasDisponibles(): string[] {
    return [
      'usuarios',
      'empresas', 
      'plantas',
      'departamentos',
      'puestos',
      'empleados',
      'suscripciones_empresa',
      'planes',
      'admin_plantas'
    ];
  }

  /**
   * Formatear tamaño de archivo
   */
  formatearTamaño(bytes: number): string {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  /**
   * Formatear fecha
   */
  formatearFecha(fechaISO: string): string {
    return new Date(fechaISO).toLocaleString('es-MX', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }
}

// Exportar instancia singleton
const respaldosService = new RespaldosService();
export default respaldosService;
