import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configurar axios con autenticación
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de respuesta
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('⚠️ Sin autenticación para evaluaciones oficiales, continuando sin token...');
      // No lanzar error, permitir que continue sin token
      return Promise.resolve({ data: null });
    }
    return Promise.reject(error);
  }
);

// Tipos de datos
export interface PreguntaOficial {
  id: number;
  numero_orden: number;
  texto: string;
  tipo: 'multiple' | 'si_no' | 'escala' | 'texto';
  opciones: string[];
  obligatoria: boolean;
  normativa: string;
  seccion: {
    id: number;
    nombre: string;
    numero_orden: number;
  };
}

export interface EvaluacionOficial {
  id: number;
  tipo_norma: string;
  nombre: string;
  descripcion: string;
  tiempo_limite?: number;
}

export interface NormativaResponse {
  evaluacion: EvaluacionOficial;
  total_preguntas: number;
  preguntas: PreguntaOficial[];
}

// Servicios de API
export const evaluacionesOficialesAPI = {
  // Obtener todas las evaluaciones oficiales
  async getEvaluaciones(): Promise<EvaluacionOficial[]> {
    try {
      const response = await api.get('/evaluaciones/oficial/evaluaciones-oficiales/');
      
      // Si la respuesta es null (error 401 manejado), retornar array vacío
      if (!response.data) {
        return [];
      }
      
      return response.data.results || response.data;
    } catch (error) {
      console.error('Error al obtener evaluaciones oficiales:', error);
      throw error;
    }
  },

  // Obtener preguntas por normativa
  async getPreguntasPorNormativa(normativa: string): Promise<NormativaResponse> {
    try {
      const response = await api.get(`/evaluaciones/oficial/normativa/${normativa}/`);
      
      // Si la respuesta es null (error 401 manejado), crear una respuesta vacía
      if (!response.data) {
        return {
          evaluacion: {
            id: 0,
            tipo_norma: normativa.toUpperCase().replace('_', '-'),
            nombre: `Evaluación ${normativa.toUpperCase().replace('_', '-')} Oficial`,
            descripcion: 'Datos no disponibles sin autenticación'
          },
          total_preguntas: 0,
          preguntas: []
        };
      }
      
      return response.data;
    } catch (error) {
      console.error(`Error al obtener preguntas de ${normativa}:`, error);
      throw error;
    }
  },

  // Obtener todas las preguntas oficiales
  async getPreguntasOficiales(): Promise<{ [key: string]: NormativaResponse }> {
    try {
      const response = await api.get('/evaluaciones/oficial/preguntas-oficiales/');
      return response.data.normativas || {};
    } catch (error) {
      console.error('Error al obtener preguntas oficiales:', error);
      throw error;
    }
  },

  // Crear nueva pregunta (si se necesita en el futuro)
  async crearPregunta(pregunta: Partial<PreguntaOficial>): Promise<PreguntaOficial> {
    try {
      console.log('🚀 crearPregunta API - Enviando:', pregunta);
      console.log('🌐 URL:', `${API_BASE_URL}/evaluaciones/oficial/preguntas-oficiales/`);
      
      const response = await api.post('/evaluaciones/oficial/preguntas-oficiales/', pregunta);
      
      console.log('✅ crearPregunta API - Respuesta:', response.data);
      console.log('📊 Status:', response.status);
      
      return response.data;
    } catch (error) {
      console.error('❌ Error en crearPregunta API:', error);
      
      if (axios.isAxiosError(error)) {
        console.error('📊 Status:', error.response?.status);
        console.error('📋 Data:', error.response?.data);
        console.error('🌐 URL:', error.config?.url);
        console.error('📤 Request data:', error.config?.data);
      }
      
      throw error;
    }
  },

  // Actualizar pregunta existente
  async actualizarPregunta(id: number, pregunta: Partial<PreguntaOficial>): Promise<PreguntaOficial> {
    try {
      console.log('🚀 actualizarPregunta API - Enviando:', { id, pregunta });
      console.log('🌐 URL:', `${API_BASE_URL}/evaluaciones/oficial/preguntas-oficiales/${id}/`);
      
      const response = await api.put(`/evaluaciones/oficial/preguntas-oficiales/${id}/`, pregunta);
      
      console.log('✅ actualizarPregunta API - Respuesta:', response.data);
      console.log('📊 Status:', response.status);
      
      return response.data;
    } catch (error) {
      console.error('❌ Error en actualizarPregunta API:', error);
      
      if (axios.isAxiosError(error)) {
        console.error('📊 Status:', error.response?.status);
        console.error('📋 Data:', error.response?.data);
        console.error('🌐 URL:', error.config?.url);
        console.error('📤 Request data:', error.config?.data);
      }
      
      throw error;
    }
  },

  // Eliminar pregunta
  async eliminarPregunta(id: number): Promise<void> {
    try {
      await api.delete(`/evaluaciones/oficial/preguntas-oficiales/${id}/`);
    } catch (error) {
      console.error('Error al eliminar pregunta:', error);
      throw error;
    }
  }
};

export default evaluacionesOficialesAPI;