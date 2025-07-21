import api from '../api';

// Interfaces
export interface TipoEvaluacion {
  id: number;
  nombre: string;
  descripcion: string;
  normativa_oficial: boolean;
  activo: boolean;
}

export interface Pregunta {
  id: number;
  tipo_evaluacion: number;
  tipo_evaluacion_nombre: string;
  empresa: number | null;
  empresa_nombre: string | null;
  texto_pregunta: string;
  tipo_respuesta: 'multiple' | 'escala' | 'si_no' | 'texto';
  opciones_respuesta: string[];
  es_obligatoria: boolean;
  orden: number;
  activa: boolean;
  creada_por_nombre: string;
}

export interface EvaluacionCompleta {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_evaluacion: number;
  tipo_evaluacion_nombre: string;
  empresa: number;
  empresa_nombre: string;
  estado: 'borrador' | 'activa' | 'finalizada' | 'cancelada';
  fecha_inicio: string;
  fecha_fin: string;
  es_anonima: boolean;
  total_preguntas: number;
  total_respuestas: number;
  creada_por_nombre: string;
}

export interface RespuestaEvaluacion {
  id: number;
  evaluacion: number;
  evaluacion_titulo: string;
  empleado: number | null;
  empleado_nombre: string | null;
  fecha_respuesta: string;
  completada: boolean;
  tiempo_completado: number | null;
}

// Servicios
const evaluacionesAPI = {
  // Tipos de evaluación
  getTipos: () => api.get<TipoEvaluacion[]>('/evaluaciones/'),
  
  // Preguntas
  getPreguntas: (params?: any) => api.get<Pregunta[]>('/evaluaciones/preguntas/', { params }),
  
  createPregunta: (data: Partial<Pregunta>) => 
    api.post<Pregunta>('/evaluaciones/preguntas/', data),
  
  updatePregunta: (id: number, data: Partial<Pregunta>) => 
    api.put<Pregunta>(`/evaluaciones/preguntas/${id}/`, data),
  
  deletePregunta: (id: number) => 
    api.delete(`/evaluaciones/preguntas/${id}/`),
  
  crearPreguntasOficiales: () => 
    api.post<{ message: string; preguntas_creadas: number }>('/evaluaciones/preguntas/crear_oficiales/'),
  
  // Evaluaciones
  getEvaluaciones: () => api.get<EvaluacionCompleta[]>('/evaluaciones/'),
  
  getEvaluacion: (id: number) =>
    api.get<EvaluacionCompleta>(`/evaluaciones/${id}/`),  createEvaluacion: (data: {
    titulo: string;
    descripcion: string;
    tipo_evaluacion: number;
    fecha_inicio: string;
    fecha_fin: string;
    es_anonima: boolean;
    plantas?: number[];
    departamentos?: number[];
    empleados_objetivo?: number[];
    preguntas_seleccionadas?: Array<{
      pregunta_id: number;
      orden: number;
      es_obligatoria: boolean;
    }>;
  }) => api.post<EvaluacionCompleta>('/evaluaciones/', data),
  
  updateEvaluacion: (id: number, data: Partial<EvaluacionCompleta>) => 
    api.put<EvaluacionCompleta>(`/evaluaciones/${id}/`, data),
  
  activarEvaluacion: (id: number) => 
    api.post<{ message: string }>(`/evaluaciones/${id}/activar/`),
  
  getResultados: (id: number) => 
    api.get(`/evaluaciones/${id}/resultados/`),
  
  // Respuestas
  getMisEvaluaciones: () => 
    api.get<EvaluacionCompleta[]>('/evaluaciones/respuestas/mis_evaluaciones/'),
  
  getRespuestas: () => 
    api.get<RespuestaEvaluacion[]>('/evaluaciones/respuestas/'),
  
  createRespuesta: (data: {
    evaluacion: number;
    empleado?: number;
    respuestas: Array<{
      pregunta_id: number;
      respuesta_texto?: string;
      respuesta_numerica?: number;
      respuesta_multiple?: string[];
    }>;
  }) => api.post<RespuestaEvaluacion>('/evaluaciones/respuestas/', data),
};

export default evaluacionesAPI;
