import React, { useState, useEffect } from 'react';
import '../css/GestionEvaluaciones.css';

interface Evaluacion {
  id: number;
  titulo: string;
  descripcion: string;
  tipo: 'normativa' | 'interna';
  tipo_display: string;
  estado: 'activa' | 'inactiva';
  estado_display: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  creado_por_nombre: string;
  empresa_nombre?: string;
  planta_nombre?: string;
  total_preguntas: number;
  instrucciones: string;
  tiempo_limite?: number;
}

interface Pregunta {
  id?: number;
  orden: number;
  texto: string;
  tipo: 'texto' | 'multiple' | 'verdadero_falso' | 'escala' | 'fecha';
  es_requerida: boolean;
  opciones: string[];
  escala_min?: number;
  escala_max?: number;
}

interface Usuario {
  is_superuser: boolean;
  perfil_usuario: {
    tipo_usuario: string;
    empresa: {
      id: number;
      nombre: string;
    };
  };
}

interface GestionEvaluacionesProps {
  usuario: Usuario;
}

const GestionEvaluaciones: React.FC<GestionEvaluacionesProps> = ({ usuario }) => {
  const [evaluaciones, setEvaluaciones] = useState<Evaluacion[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showPreguntasModal, setShowPreguntasModal] = useState(false);
  const [editingEvaluacion, setEditingEvaluacion] = useState<Evaluacion | null>(null);
  const [evaluacionSeleccionada, setEvaluacionSeleccionada] = useState<Evaluacion | null>(null);
  const [preguntas, setPreguntas] = useState<Pregunta[]>([]);
  const [error, setError] = useState<string>('');
  
  // Estados para filtros
  const [filtroTipo, setFiltroTipo] = useState<'todas' | 'normativa' | 'interna'>('todas');
  const [filtroEstado, setFiltroEstado] = useState<'todos' | 'activa' | 'inactiva'>('todos');
  const [busqueda, setBusqueda] = useState('');

  // Formulario de evaluación
  const [formData, setFormData] = useState({
    titulo: '',
    descripcion: '',
    tipo: 'interna' as 'normativa' | 'interna',
    estado: 'activa' as 'activa' | 'inactiva',
    instrucciones: '',
    tiempo_limite: ''
  });

  // Formulario de pregunta
  const [preguntaForm, setPreguntaForm] = useState<Pregunta>({
    orden: 1,
    texto: '',
    tipo: 'texto',
    es_requerida: true,
    opciones: [],
    escala_min: 1,
    escala_max: 5
  });

  const [editingPregunta, setEditingPregunta] = useState<Pregunta | null>(null);

  // Función para filtrar evaluaciones
  const evaluacionesFiltradas = evaluaciones.filter(evaluacion => {
    // Filtro por tipo
    if (filtroTipo !== 'todas' && evaluacion.tipo !== filtroTipo) {
      return false;
    }
    
    // Filtro por estado
    if (filtroEstado !== 'todos' && evaluacion.estado !== filtroEstado) {
      return false;
    }
    
    // Filtro por búsqueda
    if (busqueda && !evaluacion.titulo.toLowerCase().includes(busqueda.toLowerCase()) && 
        !evaluacion.descripcion.toLowerCase().includes(busqueda.toLowerCase())) {
      return false;
    }
    
    return true;
  });

  useEffect(() => {
    cargarEvaluaciones();
  }, []);

  const cargarEvaluaciones = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/surveys/evaluaciones/', {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setEvaluaciones(data.results || data);
      } else {
        setError('Error al cargar evaluaciones');
      }
    } catch (error) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  const cargarPreguntas = async (evaluacionId: number) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/surveys/preguntas/?evaluacion_id=${evaluacionId}`, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setPreguntas(data.results || data);
      } else {
        setError('Error al cargar preguntas');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const url = editingEvaluacion 
        ? `/api/surveys/evaluaciones/${editingEvaluacion.id}/`
        : '/api/surveys/evaluaciones/';
      
      const method = editingEvaluacion ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          tiempo_limite: formData.tiempo_limite ? parseInt(formData.tiempo_limite) : null
        })
      });

      if (response.ok) {
        await cargarEvaluaciones();
        setShowModal(false);
        resetForm();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al guardar evaluación');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleSubmitPregunta = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!evaluacionSeleccionada) return;

    try {
      const token = localStorage.getItem('token');
      const url = editingPregunta 
        ? `/api/surveys/preguntas/${editingPregunta.id}/`
        : '/api/surveys/preguntas/';
      
      const method = editingPregunta ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...preguntaForm,
          evaluacion: evaluacionSeleccionada.id
        })
      });

      if (response.ok) {
        await cargarPreguntas(evaluacionSeleccionada.id);
        resetPreguntaForm();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Error al guardar pregunta');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleDesactivar = async (id: number) => {
    if (!window.confirm('¿Estás seguro de que quieres desactivar esta evaluación?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/surveys/evaluaciones/${id}/desactivar/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        await cargarEvaluaciones();
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error al desactivar evaluación');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleActivar = async (id: number) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/surveys/evaluaciones/${id}/activar/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        await cargarEvaluaciones();
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error al activar evaluación');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleEdit = (evaluacion: Evaluacion) => {
    setEditingEvaluacion(evaluacion);
    setFormData({
      titulo: evaluacion.titulo,
      descripcion: evaluacion.descripcion,
      tipo: evaluacion.tipo,
      estado: evaluacion.estado,
      instrucciones: evaluacion.instrucciones,
      tiempo_limite: evaluacion.tiempo_limite?.toString() || ''
    });
    setShowModal(true);
  };

  const handleEditPregunta = (pregunta: Pregunta) => {
    setEditingPregunta(pregunta);
    setPreguntaForm(pregunta);
  };

  const handleGestionarPreguntas = (evaluacion: Evaluacion) => {
    setEvaluacionSeleccionada(evaluacion);
    cargarPreguntas(evaluacion.id);
    setShowPreguntasModal(true);
  };

  const handleEliminarPregunta = async (preguntaId: number) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar esta pregunta?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/surveys/preguntas/${preguntaId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        if (evaluacionSeleccionada) {
          await cargarPreguntas(evaluacionSeleccionada.id);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error al eliminar pregunta');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const handleReordenarPregunta = async (preguntaId: number, nuevoOrden: number) => {
    if (!evaluacionSeleccionada) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/surveys/preguntas/${preguntaId}/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          orden: nuevoOrden
        })
      });

      if (response.ok) {
        await cargarPreguntas(evaluacionSeleccionada.id);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error al reordenar pregunta');
      }
    } catch (error) {
      setError('Error de conexión');
    }
  };

  const resetForm = () => {
    setFormData({
      titulo: '',
      descripcion: '',
      tipo: 'interna',
      estado: 'activa',
      instrucciones: '',
      tiempo_limite: ''
    });
    setEditingEvaluacion(null);
    setError('');
  };

  const resetPreguntaForm = () => {
    setPreguntaForm({
      orden: preguntas.length + 1,
      texto: '',
      tipo: 'texto',
      es_requerida: true,
      opciones: [],
      escala_min: 1,
      escala_max: 5
    });
    setEditingPregunta(null);
  };

  const agregarOpcion = () => {
    setPreguntaForm({
      ...preguntaForm,
      opciones: [...preguntaForm.opciones, '']
    });
  };

  const actualizarOpcion = (index: number, valor: string) => {
    const nuevasOpciones = [...preguntaForm.opciones];
    nuevasOpciones[index] = valor;
    setPreguntaForm({
      ...preguntaForm,
      opciones: nuevasOpciones
    });
  };

  const eliminarOpcion = (index: number) => {
    const nuevasOpciones = preguntaForm.opciones.filter((_, i) => i !== index);
    setPreguntaForm({
      ...preguntaForm,
      opciones: nuevasOpciones
    });
  };

  const puedeCrearNormativa = () => {
    return usuario.is_superuser;
  };

  const puedeEditarEvaluacion = (evaluacion: Evaluacion) => {
    if (usuario.is_superuser) {
      return evaluacion.tipo === 'normativa';
    }
    return evaluacion.tipo === 'interna';
  };

  if (loading) {
    return <div className="loading">Cargando evaluaciones...</div>;
  }

  return (
    <div className="gestion-evaluaciones">
      <div className="header">
        <h2>Gestión de Evaluaciones</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowModal(true)}
        >
          + Nueva Evaluación
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="filtros">
        <div className="filtro-busqueda">
          <input
            type="text"
            placeholder="Buscar evaluaciones..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="input-busqueda"
          />
        </div>
        
        <div className="filtro-tabs">
          <button 
            className={`tab ${filtroTipo === 'todas' ? 'active' : ''}`}
            onClick={() => setFiltroTipo('todas')}
          >
            Todas
          </button>
          <button 
            className={`tab ${filtroTipo === 'normativa' ? 'active' : ''}`}
            onClick={() => setFiltroTipo('normativa')}
          >
            Normativas
          </button>
          <button 
            className={`tab ${filtroTipo === 'interna' ? 'active' : ''}`}
            onClick={() => setFiltroTipo('interna')}
          >
            Internas
          </button>
        </div>
        
        <div className="filtro-estado">
          <select 
            value={filtroEstado} 
            onChange={(e) => setFiltroEstado(e.target.value as 'todos' | 'activa' | 'inactiva')}
            className="select-estado"
          >
            <option value="todos">Todos los estados</option>
            <option value="activa">Activas</option>
            <option value="inactiva">Inactivas</option>
          </select>
        </div>
      </div>

      <div className="evaluaciones-grid">
        {evaluacionesFiltradas.map(evaluacion => (
          <div key={evaluacion.id} className="evaluacion-card">
            <div className="evaluacion-header">
              <h3>{evaluacion.titulo}</h3>
              <div className="badges">
                <span className={`badge ${evaluacion.tipo}`}>
                  {evaluacion.tipo_display}
                </span>
                <span className={`badge ${evaluacion.estado}`}>
                  {evaluacion.estado_display}
                </span>
              </div>
            </div>

            <div className="evaluacion-info">
              <p className="descripcion">{evaluacion.descripcion}</p>
              <div className="meta-info">
                <span>Preguntas: {evaluacion.total_preguntas}</span>
                <span>Creado por: {evaluacion.creado_por_nombre}</span>
                {evaluacion.empresa_nombre && (
                  <span>Empresa: {evaluacion.empresa_nombre}</span>
                )}
              </div>
            </div>

            <div className="evaluacion-actions">
              <button 
                className="btn-secondary"
                onClick={() => handleGestionarPreguntas(evaluacion)}
              >
                Gestionar Preguntas
              </button>
              
              {puedeEditarEvaluacion(evaluacion) && (
                <>
                  <button 
                    className="btn-secondary"
                    onClick={() => handleEdit(evaluacion)}
                  >
                    Editar
                  </button>
                  
                  {evaluacion.estado === 'activa' ? (
                    <button 
                      className="btn-danger"
                      onClick={() => handleDesactivar(evaluacion.id)}
                    >
                      Desactivar
                    </button>
                  ) : (
                    <button 
                      className="btn-primary"
                      onClick={() => handleActivar(evaluacion.id)}
                    >
                      Activar
                    </button>
                  )}
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Modal para crear/editar evaluación */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{editingEvaluacion ? 'Editar Evaluación' : 'Nueva Evaluación'}</h3>
              <button 
                className="btn-close"
                onClick={() => {
                  setShowModal(false);
                  resetForm();
                }}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="modal-form">
              <div className="form-group">
                <label>Título:</label>
                <input
                  type="text"
                  value={formData.titulo}
                  onChange={(e) => setFormData({...formData, titulo: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Descripción:</label>
                <textarea
                  value={formData.descripcion}
                  onChange={(e) => setFormData({...formData, descripcion: e.target.value})}
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Tipo:</label>
                <select
                  value={formData.tipo}
                  onChange={(e) => setFormData({...formData, tipo: e.target.value as 'normativa' | 'interna'})}
                  disabled={!puedeCrearNormativa() && formData.tipo === 'normativa'}
                >
                  <option value="interna">Interna</option>
                  {puedeCrearNormativa() && (
                    <option value="normativa">Normativa</option>
                  )}
                </select>
              </div>

              <div className="form-group">
                <label>Instrucciones:</label>
                <textarea
                  value={formData.instrucciones}
                  onChange={(e) => setFormData({...formData, instrucciones: e.target.value})}
                  rows={4}
                />
              </div>

              <div className="form-group">
                <label>Tiempo límite (minutos):</label>
                <input
                  type="number"
                  value={formData.tiempo_limite}
                  onChange={(e) => setFormData({...formData, tiempo_limite: e.target.value})}
                  min="1"
                />
              </div>

              <div className="form-group">
                <label>Estado:</label>
                <select
                  value={formData.estado}
                  onChange={(e) => setFormData({...formData, estado: e.target.value as 'activa' | 'inactiva'})}
                >
                  <option value="activa">Activa</option>
                  <option value="inactiva">Inactiva</option>
                </select>
              </div>

              <div className="form-actions">
                <button type="button" onClick={() => {
                  setShowModal(false);
                  resetForm();
                }}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary">
                  {editingEvaluacion ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para gestionar preguntas */}
      {showPreguntasModal && evaluacionSeleccionada && (
        <div className="modal-overlay">
          <div className="modal modal-large">
            <div className="modal-header">
              <h3>Preguntas - {evaluacionSeleccionada.titulo}</h3>
              <button 
                className="btn-close"
                onClick={() => {
                  setShowPreguntasModal(false);
                  setEvaluacionSeleccionada(null);
                  resetPreguntaForm();
                }}
              >
                ×
              </button>
            </div>

            <div className="modal-content">
              {/* Formulario para agregar/editar pregunta */}
              <div className="pregunta-form">
                <h4>{editingPregunta ? 'Editar Pregunta' : 'Nueva Pregunta'}</h4>
                
                <form onSubmit={handleSubmitPregunta}>
                  <div className="form-row">
                    <div className="form-group">
                      <label>Orden:</label>
                      <input
                        type="number"
                        value={preguntaForm.orden}
                        onChange={(e) => setPreguntaForm({...preguntaForm, orden: parseInt(e.target.value)})}
                        min="1"
                        required
                      />
                    </div>
                    
                    <div className="form-group">
                      <label>Tipo:</label>
                      <select
                        value={preguntaForm.tipo}
                        onChange={(e) => setPreguntaForm({...preguntaForm, tipo: e.target.value as any})}
                      >
                        <option value="texto">Texto libre</option>
                        <option value="multiple">Opción múltiple</option>
                        <option value="verdadero_falso">Verdadero/Falso</option>
                        <option value="escala">Escala numérica</option>
                        <option value="fecha">Fecha</option>
                      </select>
                    </div>
                  </div>

                  <div className="form-group">
                    <label>Texto de la pregunta:</label>
                    <textarea
                      value={preguntaForm.texto}
                      onChange={(e) => setPreguntaForm({...preguntaForm, texto: e.target.value})}
                      required
                      rows={2}
                    />
                  </div>

                  <div className="form-group">
                    <label>
                      <input
                        type="checkbox"
                        checked={preguntaForm.es_requerida}
                        onChange={(e) => setPreguntaForm({...preguntaForm, es_requerida: e.target.checked})}
                      />
                      Pregunta requerida
                    </label>
                  </div>

                  {/* Opciones para preguntas múltiples */}
                  {preguntaForm.tipo === 'multiple' && (
                    <div className="form-group">
                      <label>Opciones:</label>
                      {preguntaForm.opciones.map((opcion, index) => (
                        <div key={index} className="opcion-row">
                          <input
                            type="text"
                            value={opcion}
                            onChange={(e) => actualizarOpcion(index, e.target.value)}
                            placeholder={`Opción ${index + 1}`}
                          />
                          <button 
                            type="button"
                            onClick={() => eliminarOpcion(index)}
                            className="btn-danger btn-small"
                          >
                            Eliminar
                          </button>
                        </div>
                      ))}
                      <button 
                        type="button"
                        onClick={agregarOpcion}
                        className="btn-secondary btn-small"
                      >
                        + Agregar opción
                      </button>
                    </div>
                  )}

                  {/* Escala para preguntas numéricas */}
                  {preguntaForm.tipo === 'escala' && (
                    <div className="form-row">
                      <div className="form-group">
                        <label>Valor mínimo:</label>
                        <input
                          type="number"
                          value={preguntaForm.escala_min || 1}
                          onChange={(e) => setPreguntaForm({...preguntaForm, escala_min: parseInt(e.target.value)})}
                        />
                      </div>
                      <div className="form-group">
                        <label>Valor máximo:</label>
                        <input
                          type="number"
                          value={preguntaForm.escala_max || 5}
                          onChange={(e) => setPreguntaForm({...preguntaForm, escala_max: parseInt(e.target.value)})}
                        />
                      </div>
                    </div>
                  )}

                  <div className="form-actions">
                    <button type="button" onClick={resetPreguntaForm}>
                      Cancelar
                    </button>
                    <button type="submit" className="btn-primary">
                      {editingPregunta ? 'Actualizar' : 'Agregar'} Pregunta
                    </button>
                  </div>
                </form>
              </div>

              {/* Lista de preguntas */}
              <div className="preguntas-lista">
                <h4>Preguntas ({preguntas.length})</h4>
                {preguntas.map(pregunta => (
                  <div key={pregunta.id} className="pregunta-item">
                    <div className="pregunta-header">
                      <span className="pregunta-orden">{pregunta.orden}</span>
                      <span className="pregunta-tipo">{pregunta.tipo}</span>
                      {pregunta.es_requerida && <span className="requerida">Requerida</span>}
                    </div>
                    <p className="pregunta-texto">{pregunta.texto}</p>
                    
                    {pregunta.opciones.length > 0 && (
                      <div className="pregunta-opciones">
                        <strong>Opciones:</strong>
                        <ul>
                          {pregunta.opciones.map((opcion, index) => (
                            <li key={index}>{opcion}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {pregunta.tipo === 'escala' && (
                      <div className="pregunta-escala">
                        <strong>Escala:</strong> {pregunta.escala_min} - {pregunta.escala_max}
                      </div>
                    )}
                    
                    <div className="pregunta-actions">
                      <button 
                        className="btn-secondary btn-small"
                        onClick={() => handleEditPregunta(pregunta)}
                      >
                        Editar
                      </button>
                      <button 
                        className="btn-secondary btn-small"
                        onClick={() => handleReordenarPregunta(pregunta.id!, pregunta.orden - 1)}
                        disabled={pregunta.orden === 1}
                      >
                        ↑
                      </button>
                      <button 
                        className="btn-secondary btn-small"
                        onClick={() => handleReordenarPregunta(pregunta.id!, pregunta.orden + 1)}
                        disabled={pregunta.orden === preguntas.length}
                      >
                        ↓
                      </button>
                      <button 
                        className="btn-danger btn-small"
                        onClick={() => handleEliminarPregunta(pregunta.id!)}
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionEvaluaciones;
