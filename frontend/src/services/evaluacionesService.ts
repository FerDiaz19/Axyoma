
// -------------------------------------------------------------------------- //

import api from '../api';

// -------------------------------------------------------------------------- //

// Interfaz para el tipo de evaluación
export interface TipoEvaluacion {
  tipo_evaluacion_id: number;
  nombre: string;
  descripcion: string;
}

// Interfaz para una posible opción de respuesta
// Usada para enviar datos anidados para creación/actualización
export interface PosiblesRespuestasRequest {
  texto_opcion: string;
  valor_booleano?: boolean | null;
  valor_numerico?: number | null;
  valor_decimal?: number | null;
  numero_orden: number;
}

// Interfaz de respuesta completa para una opción de respuesta
export interface PosiblesRespuestas extends PosiblesRespuestasRequest {
  opcion_conjunto_id: number;
}

// Interfaz para un conjunto de respuestas (opciones)
// Usada para enviar datos anidados para creación/actualización
export interface ConjuntoRespuestasRequest {
  nombre: string;
  descripcion: string;
  opciones: PosiblesRespuestasRequest[];
}

// Interfaz de respuesta completa para un conjunto de respuestas
export interface ConjuntoRespuestas extends ConjuntoRespuestasRequest {
  conjunto_id: number;
  predefinido: boolean;
  opciones: PosiblesRespuestas[];
}

// Interfaz para la pregunta en sí
// Usada para enviar datos anidados para creación/actualización
export interface PreguntaRequest {
  texto_pregunta: string;
  tipo_pregunta: 'Abierta' | 'Múltiple' | 'Escala' | 'Bool';
  es_obligatoria: boolean;
  pregunta_padre?: number | null;
  activador_padre?: string | null;
}

// Interfaz de respuesta completa para una pregunta
export interface Pregunta extends PreguntaRequest {
  pregunta_id: number;
}

// Interfaz para la relación entre una sección y una pregunta
// Usada para enviar datos anidados para creación/actualización
export interface SeccionPreguntaRequest {
  pregunta_id: number;
  numero_orden: number;
  conjunto_respuestas_id?: number | null;
  respuesta_correcta?: number | null;
}

// Interfaz de respuesta completa para una relación entre una sección y una pregunta
export interface SeccionPregunta extends SeccionPreguntaRequest {
  seccion_pregunta_id: number;
  pregunta: Pregunta;
  conjunto_respuestas?: ConjuntoRespuestas; // Opcional
}

// Interfaz para una sección de una evaluación
// Usada para enviar datos anidados para creación/actualización
export interface SeccionEvalRequest {
  nombre: string;
  descripcion?: string | null;
  numero_orden: number;
  es_evaluable: boolean;
  preguntas_seccion: SeccionPreguntaRequest[];
}

// Interfaz de respuesta completa para una sección de una evaluación
export interface SeccionEval extends SeccionEvalRequest {
  seccion_id: number;
  preguntas_seccion: SeccionPregunta[];
}

// Interfaz principal para la evaluación
// Usada para enviar datos anidados para creación/actualización
export interface EvaluacionRequest {
  titulo: string;
  descripcion?: string | null;
  instrucciones?: string | null;
  contenido_informativo?: string | null;
  tiempo_limite?: number | null;
  umbral_aprobacion?: number | null;
  estado: boolean;
  tipo_evaluacion_id: number;
  empresa_id?: number | null;
  creado_por_id?: number | null;
  secciones: SeccionEvalRequest[];
}

// Interfaz de respuesta completa para la evaluación
export interface Evaluacion extends EvaluacionRequest {
  evaluacion_id: number;
  fecha_registro: string;
  fecha_modificacion: string;
  tipo_evaluacion: string;
  empresa_nombre: string | null;
  empresa_id: number | null;
  creado_por_nombre: string | null;
  creado_por_id: number | null;
  secciones: SeccionEval[];
}

// Interfaz para el resultado de una evaluación
export interface AsignacionRequest {
  evaluacion: number;
  fecha_inicio: string;
  fecha_fin: string;
  status?: boolean;
}

// Interfaz de respuesta completa para la asignación
export interface Asignacion extends AsignacionRequest {
  asignacion_id: number;
  status: boolean;
  empleado_evaluado: number | null;
  puesto_al_momento: string | null;
  departamento_al_momento: string | null;
  asignaciones_empleado: AsignacionEmpleado[];
}

// Interfaz para la asignación de un empleado específico
export interface AsignacionEmpleado {
  asignacion_empleado_id: number;
  asignacion: number;
  empleado: number;
  empleado_nombre: string;
  empleado_puesto: string;
  empleado_puesto_id: number;
  empleado_departamento: string;
  empleado_departamento_id: number;
  empleado_planta: string;
  empleado_planta_id: number;
  empleado_empresa: string;
  empleado_empresa_id: number;
  token_acceso: string;
  status: 'Pendiente' | 'Desactivada' | 'Completada' | 'Expirada';
  fecha_inicio: string;
  fecha_completado: string | null;
}

// Interfaz para la respuesta de un empleado
export interface RespuestaEmpleado {
  respuesta_empleado_id: number;
  asignacion_empleado: number;
  seccion_pregunta: number;
  opcion_seleccionada: number | null;
  respuesta_texto: string | null;
  respuesta_valor_numerico: number | null;
  respuesta_valor_decimal: number | null;
  respuesta_valor_booleano: boolean | null;
  es_correcta: boolean | null;
  fecha_respuesta: string;
}

// Interfaz de resultados obtenidos.
export interface ResultadoEvaluacion {
  resultado_id: number;
  asignacion_empleado: number;
  puntaje_total?: number;
  num_respuestas_correctas?: number;
  num_preguntas_evaluables?: number;
  porcentaje_correctas?: number;
  aprobado: boolean;
}

// -------------------------------------------------------------------------- //

const evaluacionesAPI = {
  // Tipos de evaluación
  getTipos: () => api.get<TipoEvaluacion[]>('/appraisal/tipos-evaluacion/'),
  createTipo: (data: Partial<TipoEvaluacion>) => api.post<TipoEvaluacion>('/appraisal/tipos-evaluacion/', data),

  // Evaluaciones
  getEvaluaciones: () => api.get<Evaluacion[]>('/appraisal/evaluaciones/'),
  getEvaluacion: (id: number) => api.get<Evaluacion>(`/appraisal/evaluaciones/${id}/`),
  createEvaluacion: (data: EvaluacionRequest) => api.post<Evaluacion>('/appraisal/evaluaciones/', data),
  updateEvaluacion: (id: number, data: EvaluacionRequest) => api.put<Evaluacion>(`/appraisal/evaluaciones/${id}/`, data),
  desactivarEvaluacion: (id: number) => api.patch<{ status: string }>(`/appraisal/evaluaciones/${id}/desactivar/`),
  activarEvaluacion: (id: number) => api.patch<{ status: string }>(`/appraisal/evaluaciones/${id}/activar/`),

  // ! Nota: Las secciones se gestionan anidadamente dentro de la Evaluación.
  // Preguntas
  getPreguntas: () => api.get<Pregunta[]>('/appraisal/preguntas/'),
  createPregunta: (data: PreguntaRequest) => api.post<Pregunta>('/appraisal/preguntas/', data),
  updatePregunta: (id: number, data: PreguntaRequest) => api.put<Pregunta>(`/appraisal/preguntas/${id}/`, data),
  deletePregunta: (id: number) => api.delete(`/appraisal/preguntas/${id}/`),

  // Conjuntos de Respuestas
  getConjuntosRespuestas: () => api.get<ConjuntoRespuestas[]>('/appraisal/conjuntos-respuestas/'),
  createConjuntoRespuestas: (data: ConjuntoRespuestasRequest) => api.post<ConjuntoRespuestas>('/appraisal/conjuntos-respuestas/', data),
  updateConjuntoRespuestas: (id: number, data: ConjuntoRespuestasRequest) => api.put<ConjuntoRespuestas>(`/appraisal/conjuntos-respuestas/${id}/`, data),

  // Asignaciones
  getAsignaciones: () => api.get<Asignacion[]>('/appraisal/asignaciones/'),
  getAsignacion: (id: number) => api.get<Asignacion>(`/appraisal/asignaciones/${id}/`),
  createAsignacion: (data: AsignacionRequest) => api.post<Asignacion>('/appraisal/asignaciones/', data),
  desactivarAsignacion: (id: number) => api.patch<{ status: string }>(`/appraisal/asignaciones/${id}/desactivar_asignacion/`),
  activarAsignacion: (id: number) => api.patch<{ status: string }>(`/appraisal/asignaciones/${id}/activar_asignacion/`),
  asignarEmpleados: (id: number, data: { empleado_ids?: number[], planta_ids?: number[], puesto_ids?: number[], departamento_ids?: number[] }) =>
    api.post<{ status: string }>(`/appraisal/asignaciones/${id}/asignar_empleados/`, data),


  // Asignaciones de Empleados
  getAsignacionesEmpleado: () => api.get<AsignacionEmpleado[]>('/appraisal/asignaciones-empleado/'),
  getAsignacionEmpleado: (id: number) => api.get<AsignacionEmpleado>(`/appraisal/asignaciones-empleado/${id}/`),


  // Aactivar y desactivar asignaciones individuales
  desactivarAsignacionEmpleado: (id: number) => api.patch<{ status: string }>(`/appraisal/asignaciones-empleado/${id}/desactivar/`),
  activarAsignacionEmpleado: (id: number) => api.patch<{ status: string }>(`/appraisal/asignaciones-empleado/${id}/activar/`),


  // Respuestas del Empleado
  getRespuestasEmpleado: () => api.get<RespuestaEmpleado[]>('/appraisal/respuestas-empleado/'),
  createRespuestaEmpleado: (data: Partial<RespuestaEmpleado>) => api.post<RespuestaEmpleado>('/appraisal/respuestas-empleado/', data),


  // Resultados de Evaluación
  getResultadosEvaluacion: () => api.get<ResultadoEvaluacion[]>('/appraisal/resultados-evaluacion/'),
  getResultadoEvaluacion: (id: number) => api.get<ResultadoEvaluacion>(`/appraisal/resultados-evaluacion/${id}/`),
};

// -------------------------------------------------------------------------- //

export default evaluacionesAPI;

// -------------------------------------------------------------------------- //
