import React, { useState, useEffect, useCallback } from 'react';
import { evaluacionesOficialesAPI, PreguntaOficial, NormativaResponse } from '../services/evaluacionesOficialesAPI';
import './EvaluacionesGestion.css';

interface Pregunta {
  id: number;
  texto: string;
  tipo: 'multiple' | 'si_no' | 'escala' | 'texto';
  opciones: string[];
  obligatoria: boolean;
  normativa: string;
}

interface FormularioPregunta {
  texto: string;
  tipo: 'multiple' | 'si_no' | 'escala' | 'texto';
  opciones: string[];
  obligatoria: boolean;
}

interface EvaluacionesGestionProps {
  userData?: {
    nivel_usuario: string;
    empresa_id?: number;
  };
}

const EvaluacionesGestion: React.FC<EvaluacionesGestionProps> = ({ userData }) => {
  const [normativaSeleccionada, setNormativaSeleccionada] = useState<string>('nom_035');
  const [preguntas, setPreguntas] = useState<Pregunta[]>([]);
  const [loading, setLoading] = useState(true);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [editandoPregunta, setEditandoPregunta] = useState<Pregunta | null>(null);
  
  const [formulario, setFormulario] = useState<FormularioPregunta>({
    texto: '',
    tipo: 'multiple',
    opciones: ['', ''],
    obligatoria: true
  });

  const cargarPreguntas = useCallback(async () => {
    try {
      setLoading(true);
      
      // Cargar preguntas NOM-030
      const preguntasNOM030: NormativaResponse = await evaluacionesOficialesAPI.getPreguntasPorNormativa('nom_030');
      
      // Cargar preguntas NOM-035  
      const preguntasNOM035: NormativaResponse = await evaluacionesOficialesAPI.getPreguntasPorNormativa('nom_035');
      
      // Fallback a datos de muestra si no hay datos de la API
      if (!preguntasNOM030.preguntas?.length && !preguntasNOM035.preguntas?.length) {
        console.log('🔄 Usando datos de muestra - Sin conexión a API');
        setPreguntas(preguntasMuestra);
        return;
      }

      // Convertir preguntas oficiales al formato local
      const todasLasPreguntas: Pregunta[] = [];

      // Agregar preguntas NOM-030
      preguntasNOM030.preguntas.forEach((p: PreguntaOficial) => {
        todasLasPreguntas.push({
          id: p.id,
          texto: p.texto,
          tipo: mapearTipoOficial(p.tipo),
          opciones: p.opciones || [],
          obligatoria: p.obligatoria,
          normativa: 'nom_030'
        });
      });

      // Agregar preguntas NOM-035
      preguntasNOM035.preguntas.forEach((p: PreguntaOficial) => {
        todasLasPreguntas.push({
          id: p.id,
          texto: p.texto,
          tipo: mapearTipoOficial(p.tipo),
          opciones: p.opciones || [],
          obligatoria: p.obligatoria,
          normativa: 'nom_035'
        });
      });

      setPreguntas(todasLasPreguntas);
      
    } catch (error) {
      console.error('Error cargando preguntas:', error);
      console.log('🔄 Usando datos de muestra - Error de conexión');
      setPreguntas(preguntasMuestra);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    cargarPreguntas();
  }, [cargarPreguntas]);

  // Mapear tipos de preguntas oficiales a tipos locales
  const mapearTipoOficial = (tipoOficial: string): 'multiple' | 'si_no' | 'escala' | 'texto' => {
    switch (tipoOficial.toLowerCase()) {
      case 'múltiple':
      case 'multiple':
        return 'multiple';
      case 'si/no':
      case 'si_no':
        return 'si_no';
      case 'escala':
        return 'escala';
      case 'abierta':
      case 'texto':
        return 'texto';
      default:
        return 'texto';
    }
  };

  // Función para detectar automáticamente el tipo basándose en las opciones
  const detectarTipo = (opciones: string[]): 'multiple' | 'si_no' | 'escala' | 'texto' => {
    if (!opciones || opciones.length === 0) {
      return 'texto';
    }
    
    // Detectar Si/No
    if (opciones.length === 2 && 
        opciones.some(o => o.toLowerCase().includes('sí') || o.toLowerCase().includes('si')) &&
        opciones.some(o => o.toLowerCase().includes('no'))) {
      return 'si_no';
    }
    
    // Detectar escala (números o palabras que indican gradación)
    const esEscala = opciones.every(opcion => {
      return /^\d/.test(opcion) || // Comienza con número
             opcion.toLowerCase().includes('acuerdo') ||
             opcion.toLowerCase().includes('desacuerdo') ||
             opcion.toLowerCase().includes('nunca') ||
             opcion.toLowerCase().includes('siempre') ||
             opcion.toLowerCase().includes('frecuent');
    });
    
    if (esEscala && opciones.length >= 3) {
      return 'escala';
    }
    
    // Si tiene opciones múltiples pero no es escala ni si/no
    if (opciones.length >= 2) {
      return 'multiple';
    }
    
    return 'texto';
  };

  const preguntasFiltradas = preguntas.filter(p => p.normativa === normativaSeleccionada);

  const limpiarFormulario = () => {
    setFormulario({
      texto: '',
      tipo: 'multiple',
      opciones: ['', ''],
      obligatoria: true
    });
    setEditandoPregunta(null);
    setMostrarFormulario(false);
  };

  const manejarSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('🔄 Iniciando envío de formulario...', {
      editando: !!editandoPregunta,
      formulario: formulario,
      normativa: normativaSeleccionada
    });
    
    try {
      // Mapear tipos locales a tipos de backend
      const tipoBackend = {
        'multiple': 'multiple',
        'si_no': 'si_no', 
        'escala': 'escala',
        'texto': 'texto'
      }[formulario.tipo];

      if (editandoPregunta) {
        console.log('📝 Editando pregunta existente...', editandoPregunta.id);
        
        // Editar pregunta existente - usando función personalizada
        const preguntaActualizada = await actualizarPreguntaBackend(
          editandoPregunta.id,
          {
            texto: formulario.texto,
            tipo: tipoBackend,
            opciones: formulario.opciones.filter(o => o.trim()),
            obligatoria: formulario.obligatoria
          }
        );

        console.log('✅ Pregunta actualizada:', preguntaActualizada);

        // Actualizar en el estado local
        setPreguntas(prev => prev.map(p => 
          p.id === editandoPregunta.id 
            ? {
                ...p,
                texto: preguntaActualizada.texto,
                tipo: mapearTipoOficial(preguntaActualizada.tipo),
                opciones: preguntaActualizada.opciones || [],
                obligatoria: preguntaActualizada.obligatoria
              }
            : p
        ));
        
        alert('✅ Pregunta actualizada exitosamente');
        
      } else {
        console.log('🆕 Creando nueva pregunta...');
        
        // Crear nueva pregunta - usando función personalizada
        const nuevaPreguntaData = await crearPreguntaBackend({
          texto: formulario.texto,
          tipo: tipoBackend,
          opciones: formulario.opciones.filter(o => o.trim()),
          obligatoria: formulario.obligatoria,
          normativa: normativaSeleccionada
        });

        console.log('✅ Nueva pregunta creada:', nuevaPreguntaData);

        const nuevaPregunta: Pregunta = {
          id: nuevaPreguntaData.id,
          texto: nuevaPreguntaData.texto,
          tipo: mapearTipoOficial(nuevaPreguntaData.tipo),
          opciones: nuevaPreguntaData.opciones || [],
          obligatoria: nuevaPreguntaData.obligatoria,
          normativa: normativaSeleccionada
        };
        
        setPreguntas(prev => [...prev, nuevaPregunta]);
        
        alert('✅ Pregunta creada exitosamente');
      }
      
      limpiarFormulario();
      
    } catch (error) {
      console.error('❌ Error al guardar pregunta:', error);
      
      // Mostrar detalles del error
      if (error instanceof Error) {
        console.error('Detalles del error:', error.message);
        alert(`❌ Error al guardar la pregunta: ${error.message}`);
      } else {
        console.error('Error desconocido:', error);
        alert('❌ Error desconocido al guardar la pregunta. Revisa la consola para más detalles.');
      }
    }
  };

  // Funciones auxiliares para llamadas a API
  const crearPreguntaBackend = async (pregunta: {
    texto: string;
    tipo: string;
    opciones: string[];
    obligatoria: boolean;
    normativa: string;
  }) => {
    console.log('🔄 crearPreguntaBackend - Iniciando...', pregunta);
    
    try {
      // Preparar datos para la API con los nombres correctos
      const preguntaData: Partial<PreguntaOficial> = {
        texto: pregunta.texto,
        tipo: pregunta.tipo as 'multiple' | 'si_no' | 'escala' | 'texto',
        opciones: pregunta.opciones,
        obligatoria: pregunta.obligatoria,
        numero_orden: preguntas.length + 1, // Asignar siguiente número de orden
        normativa: pregunta.normativa
      };
      
      console.log('📤 Enviando datos a API:', preguntaData);
      
      // Crear pregunta en la base de datos usando la API
      const nuevaPregunta = await evaluacionesOficialesAPI.crearPregunta(preguntaData);
      
      console.log('✅ Respuesta de API:', nuevaPregunta);
      
      return {
        id: nuevaPregunta.id,
        texto: nuevaPregunta.texto,
        tipo: nuevaPregunta.tipo,
        opciones: nuevaPregunta.opciones,
        obligatoria: nuevaPregunta.obligatoria
      };
    } catch (error) {
      console.error('❌ Error en crearPreguntaBackend:', error);
      throw error; // Re-throw para que el componente principal pueda manejar el error
    }
  };

  const actualizarPreguntaBackend = async (id: number, pregunta: {
    texto: string;
    tipo: string;
    opciones: string[];
    obligatoria: boolean;
  }) => {
    console.log('🔄 actualizarPreguntaBackend - Iniciando...', { id, pregunta });
    
    try {
      // Preparar datos para la API con los nombres correctos
      const preguntaData: Partial<PreguntaOficial> = {
        texto: pregunta.texto,
        tipo: pregunta.tipo as 'multiple' | 'si_no' | 'escala' | 'texto',
        opciones: pregunta.opciones,
        obligatoria: pregunta.obligatoria
      };
      
      console.log('📤 Actualizando pregunta en API:', preguntaData);
      
      // Actualizar pregunta en la base de datos usando la API
      const preguntaActualizada = await evaluacionesOficialesAPI.actualizarPregunta(id, preguntaData);
      
      console.log('✅ Pregunta actualizada:', preguntaActualizada);
      
      return {
        id: preguntaActualizada.id,
        texto: preguntaActualizada.texto,
        tipo: preguntaActualizada.tipo,
        opciones: preguntaActualizada.opciones,
        obligatoria: preguntaActualizada.obligatoria
      };
    } catch (error) {
      console.error('❌ Error en actualizarPreguntaBackend:', error);
      throw error; // Re-throw para que el componente principal pueda manejar el error
    }
  };

  const editarPregunta = (pregunta: Pregunta) => {
    setEditandoPregunta(pregunta);
    
    // Detectar automáticamente el tipo basándose en las opciones existentes
    const tipoDetectado = detectarTipo(pregunta.opciones);
    
    setFormulario({
      texto: pregunta.texto,
      tipo: tipoDetectado,
      opciones: pregunta.opciones.length > 0 ? [...pregunta.opciones] : (tipoDetectado === 'multiple' ? ['', ''] : []),
      obligatoria: pregunta.obligatoria
    });
    setMostrarFormulario(true);
  };

  const eliminarPregunta = async (id: number) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar esta pregunta?')) {
      return;
    }
    
    try {
      // Para preguntas reales de la base de datos, usar la API
      const pregunta = preguntas.find(p => p.id === id);
      if (pregunta && pregunta.id > 1000) { // IDs reales vs temporales
        await evaluacionesOficialesAPI.eliminarPregunta(id);
      }
      
      // Actualizar el estado local
      setPreguntas(prev => prev.filter(p => p.id !== id));
      
    } catch (error) {
      console.error('Error al eliminar pregunta:', error);
      alert('Error al eliminar la pregunta. Por favor intenta de nuevo.');
    }
  };

  const cambiarTipo = (tipo: string) => {
    const nuevoFormulario = { ...formulario, tipo: tipo as any };
    
    // Configurar opciones predeterminadas según el tipo
    if (tipo === 'si_no') {
      nuevoFormulario.opciones = ['Sí', 'No'];
    } else if (tipo === 'escala') {
      nuevoFormulario.opciones = ['1 - Totalmente en desacuerdo', '2 - En desacuerdo', '3 - Neutral', '4 - De acuerdo', '5 - Totalmente de acuerdo'];
    } else if (tipo === 'multiple') {
      // Si ya hay opciones, conservarlas, si no crear plantilla
      if (formulario.opciones.length === 0) {
        nuevoFormulario.opciones = ['', ''];
      }
    } else if (tipo === 'texto') {
      // Tipo abierta no necesita opciones
      nuevoFormulario.opciones = [];
    }
    
    setFormulario(nuevoFormulario);
  };

  const agregarOpcion = () => {
    setFormulario(prev => ({
      ...prev,
      opciones: [...prev.opciones, '']
    }));
  };

  const actualizarOpcion = (index: number, valor: string) => {
    const nuevasOpciones = [...formulario.opciones];
    nuevasOpciones[index] = valor;
    setFormulario(prev => ({
      ...prev,
      opciones: nuevasOpciones
    }));
  };

  const eliminarOpcion = (index: number) => {
    const nuevasOpciones = formulario.opciones.filter((_, i) => i !== index);
    setFormulario(prev => ({
      ...prev,
      opciones: nuevasOpciones
    }));
  };

  if (loading) {
    return (
      <div className="evaluaciones-loading">
        <div className="loading-spinner"></div>
        <p>Cargando preguntas oficiales...</p>
      </div>
    );
  }

  return (
    <div className="evaluaciones-gestion">
      {/* Header */}
      <div className="evaluaciones-header">
        <h2>🎯 Gestión de Evaluaciones Oficiales</h2>
        <p>Administra las preguntas de las normativas NOM-030 y NOM-035</p>
      </div>

      {/* Selector de Normativa */}
      <div className="normativa-selector">
        <div className="normativa-tabs">
          <button 
            className={`normativa-tab ${normativaSeleccionada === 'nom_035' ? 'active' : ''}`}
            onClick={() => setNormativaSeleccionada('nom_035')}
          >
            🧠 NOM-035
            <span className="tab-count">{preguntas.filter(p => p.normativa === 'nom_035').length}</span>
          </button>
          <button 
            className={`normativa-tab ${normativaSeleccionada === 'nom_030' ? 'active' : ''}`}
            onClick={() => setNormativaSeleccionada('nom_030')}
          >
            🛡️ NOM-030
            <span className="tab-count">{preguntas.filter(p => p.normativa === 'nom_030').length}</span>
          </button>
        </div>
        
        <button 
          onClick={() => setMostrarFormulario(true)}
          className="btn-nueva-pregunta"
        >
          ➕ Nueva Pregunta
        </button>
      </div>

      {/* Lista de Preguntas */}
      <div className="preguntas-lista">
        {preguntasFiltradas.length === 0 ? (
          <div className="estado-vacio">
            <div className="icono-vacio">📝</div>
            <h3>No hay preguntas para {normativaSeleccionada.toUpperCase()}</h3>
            <p>Comienza creando la primera pregunta de esta normativa</p>
            <button 
              onClick={() => setMostrarFormulario(true)}
              className="btn-primary"
            >
              Crear primera pregunta
            </button>
          </div>
        ) : (
          preguntasFiltradas.map((pregunta, index) => {
            const tipoDetectado = detectarTipo(pregunta.opciones);
            const iconoTipo = {
              'multiple': '📋',
              'si_no': '✅',
              'escala': '📊',
              'texto': '✏️'
            }[tipoDetectado];
            
            const nombreTipo = {
              'multiple': 'Opción Múltiple',
              'si_no': 'Sí/No',
              'escala': 'Escala Likert',
              'texto': 'Respuesta Abierta'
            }[tipoDetectado];
            
            return (
              <div key={pregunta.id} className="pregunta-item">
                <div className="pregunta-header">
                  <span className="pregunta-numero">#{index + 1}</span>
                  <span className="pregunta-tipo">
                    {iconoTipo} {nombreTipo}
                  </span>
                  {pregunta.obligatoria && <span className="pregunta-obligatoria">* OBLIGATORIA</span>}
                </div>
                
                <div className="pregunta-contenido">
                  <h4>{pregunta.texto}</h4>
                  
                  {pregunta.opciones.length > 0 && (
                    <div className="pregunta-opciones">
                      <strong>
                        {tipoDetectado === 'escala' ? 'Niveles de la escala:' : 'Opciones disponibles:'}
                      </strong>
                      <ul className={`opciones-list ${tipoDetectado}`}>
                        {pregunta.opciones.map((opcion, idx) => (
                          <li key={idx} className={`opcion-item ${tipoDetectado}`}>
                            {tipoDetectado === 'escala' && <span className="nivel-numero">{idx + 1}</span>}
                            {opcion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {tipoDetectado === 'texto' && (
                    <div className="info-tipo-texto">
                      <em>💬 Los empleados podrán escribir una respuesta libre</em>
                    </div>
                  )}
                </div>
                
                <div className="pregunta-acciones">
                  <button 
                    onClick={() => editarPregunta(pregunta)}
                    className="btn-editar"
                    title="Editar esta pregunta"
                  >
                    ✏️ Editar
                  </button>
                  <button 
                    onClick={() => eliminarPregunta(pregunta.id)}
                    className="btn-eliminar"
                    title="Eliminar esta pregunta"
                  >
                    🗑️ Eliminar
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Modal de Formulario */}
      {mostrarFormulario && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{editandoPregunta ? '✏️ Editar Pregunta' : '➕ Nueva Pregunta'}</h3>
              <button 
                onClick={limpiarFormulario}
                className="modal-close"
              >
                ✕
              </button>
            </div>

            <form onSubmit={manejarSubmit} className="pregunta-form">
              <div className="form-group">
                <label>Texto de la pregunta *</label>
                <textarea
                  value={formulario.texto}
                  onChange={(e) => setFormulario(prev => ({...prev, texto: e.target.value}))}
                  placeholder="Escriba la pregunta..."
                  required
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Tipo de pregunta *</label>
                <select
                  value={formulario.tipo}
                  onChange={(e) => cambiarTipo(e.target.value)}
                  required
                >
                  <option value="multiple">📋 Opción múltiple</option>
                  <option value="si_no">✅ Sí/No</option>
                  <option value="escala">📊 Escala Likert (1-5)</option>
                  <option value="texto">✏️ Respuesta abierta</option>
                </select>
                
                {/* Ayuda contextual para cada tipo */}
                <div className="tipo-ayuda">
                  {formulario.tipo === 'multiple' && (
                    <small>👉 El empleado podrá seleccionar una opción de varias disponibles</small>
                  )}
                  {formulario.tipo === 'si_no' && (
                    <small>👉 Pregunta binaria con respuesta Sí o No</small>
                  )}
                  {formulario.tipo === 'escala' && (
                    <small>👉 Escala de valoración del 1 al 5 (Likert)</small>
                  )}
                  {formulario.tipo === 'texto' && (
                    <small>👉 El empleado podrá escribir una respuesta libre</small>
                  )}
                </div>
              </div>

              {(formulario.tipo === 'multiple' || formulario.tipo === 'escala') && (
                <div className="form-group">
                  <label>
                    {formulario.tipo === 'multiple' ? 'Opciones de respuesta' : 'Escala de valoración'}
                    {formulario.tipo === 'escala' && <small> (recomendado: mantener 5 opciones)</small>}
                  </label>
                  {formulario.opciones.map((opcion, index) => (
                    <div key={index} className="opcion-input">
                      <span className="opcion-numero">{index + 1}.</span>
                      <input
                        type="text"
                        value={opcion}
                        onChange={(e) => actualizarOpcion(index, e.target.value)}
                        placeholder={
                          formulario.tipo === 'escala' 
                            ? `Nivel ${index + 1} (ej: ${index + 1} - Totalmente en desacuerdo)`
                            : `Opción ${index + 1}`
                        }
                        required
                      />
                      {formulario.opciones.length > 2 && (
                        <button 
                          type="button"
                          onClick={() => eliminarOpcion(index)}
                          className="btn-danger btn-sm"
                          title="Eliminar esta opción"
                        >
                          ✕
                        </button>
                      )}
                    </div>
                  ))}
                  
                  {formulario.tipo === 'multiple' && (
                    <button 
                      type="button"
                      onClick={agregarOpcion}
                      className="btn-secondary btn-sm"
                    >
                      ➕ Agregar opción
                    </button>
                  )}
                  
                  {formulario.tipo === 'escala' && formulario.opciones.length < 7 && (
                    <button 
                      type="button"
                      onClick={agregarOpcion}
                      className="btn-secondary btn-sm"
                    >
                      ➕ Agregar nivel
                    </button>
                  )}
                </div>
              )}
              
              {formulario.tipo === 'si_no' && (
                <div className="form-group">
                  <label>Opciones de respuesta</label>
                  <div className="opciones-fijas">
                    <span className="opcion-fija">✅ Sí</span>
                    <span className="opcion-fija">❌ No</span>
                  </div>
                  <small>Las opciones Sí/No son fijas para este tipo de pregunta</small>
                </div>
              )}
              
              {formulario.tipo === 'texto' && (
                <div className="form-group">
                  <label>Tipo de respuesta</label>
                  <div className="info-respuesta">
                    <span className="info-icon">✏️</span>
                    <span>El empleado podrá escribir una respuesta libre de texto</span>
                  </div>
                </div>
              )}

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={formulario.obligatoria}
                    onChange={(e) => setFormulario(prev => ({...prev, obligatoria: e.target.checked}))}
                  />
                  Pregunta obligatoria
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  {editandoPregunta ? 'Guardar Cambios' : 'Crear Pregunta'}
                </button>
                <button 
                  type="button" 
                  onClick={limpiarFormulario}
                  className="btn-secondary"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Datos de muestra para fallback
const preguntasMuestra: Pregunta[] = [
  {
    id: 1,
    texto: "¿Considera que su carga de trabajo es adecuada?",
    tipo: "escala",
    opciones: ["1 - Totalmente en desacuerdo", "2 - En desacuerdo", "3 - Neutral", "4 - De acuerdo", "5 - Totalmente de acuerdo"],
    obligatoria: true,
    normativa: "nom_035"
  },
  {
    id: 2,
    texto: "¿Su jefe inmediato le proporciona información clara sobre sus responsabilidades?",
    tipo: "si_no",
    opciones: ["Sí", "No"],
    obligatoria: true,
    normativa: "nom_035"
  },
  {
    id: 3,
    texto: "Describa las medidas de seguridad implementadas en su área de trabajo",
    tipo: "texto",
    opciones: [],
    obligatoria: false,
    normativa: "nom_030"
  }
];

export default EvaluacionesGestion;
