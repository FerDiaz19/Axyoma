import axios from 'axios';
import api from '../api';

// No necesitamos configurar axios aquí, usamos la instancia principal

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
      const response = await api.get('/appraisal/evaluaciones/');
      const data = response.data.results || response.data;
      
      // Mapear la estructura del backend a nuestro formato
      return data.map((item: any) => ({
        id: item.evaluacion_id,
        tipo_norma: item.titulo.includes('030') ? 'NOM-030' : 'NOM-035',
        nombre: item.titulo,
        descripcion: item.descripcion,
        tiempo_limite: item.tiempo_limite || null
      }));
    } catch (error) {
      console.error('Error al obtener evaluaciones oficiales:', error);
      // En caso de error, retornar array vacío para que la UI no se rompa
      return [];
    }
  },

  // Obtener preguntas por normativa
  async getPreguntasPorNormativa(normativa: string): Promise<NormativaResponse> {
    try {
      const response = await api.get(`/appraisal/evaluaciones/${normativa}/`);
      return response.data;
    } catch (error) {
      console.error(`Error al obtener preguntas de ${normativa}:`, error);
      // Retornar respuesta vacía para que la UI no se rompa
      return {
        evaluacion: {
          id: 0,
          tipo_norma: normativa.toUpperCase().replace('_', '-'),
          nombre: `Evaluación ${normativa.toUpperCase().replace('_', '-')} Oficial`,
          descripcion: 'Error al cargar datos'
        },
        total_preguntas: 0,
        preguntas: []
      };
    }
  },

  // Obtener todas las preguntas oficiales
  async getPreguntasOficiales(): Promise<{ [key: string]: NormativaResponse }> {
    try {
      const response = await api.get('/appraisal/preguntas/');
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
      console.log('🌐 URL:', 'http://localhost:8000/api/appraisal/preguntas/');
      
      const response = await api.post('/appraisal/preguntas/', pregunta);
      
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
      console.log('🌐 URL:', `http://localhost:8000/api/appraisal/preguntas/${id}/`);
      
      const response = await api.put(`/appraisal/preguntas/${id}/`, pregunta);
      
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
      await api.delete(`/appraisal/preguntas/${id}/`);
    } catch (error) {
      console.error('Error al eliminar pregunta:', error);
      throw error;
    }
  }
};

export default evaluacionesOficialesAPI;