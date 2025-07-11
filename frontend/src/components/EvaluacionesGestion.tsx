import React, { useState, useEffect } from 'react';
import evaluacionesAPI, { TipoEvaluacion, Pregunta } from '../services/evaluacionesService';
import '../css/Evaluaciones.css';

interface EvaluacionesGestionProps {
  userData?: any;
}

const EvaluacionesGestion: React.FC<EvaluacionesGestionProps> = ({ userData }) => {
  const [tipos, setTipos] = useState<TipoEvaluacion[]>([]);
  const [preguntas, setPreguntasState] = useState<Pregunta[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Estados para gestión de normativas
  const [selectedNormativa, setSelectedNormativa] = useState<TipoEvaluacion | null>(null);
  const [showNormativaDetail, setShowNormativaDetail] = useState(false);
  const [showPreguntaForm, setShowPreguntaForm] = useState(false);
  const [preguntaForm, setPreguntaForm] = useState({
    texto_pregunta: '',
    tipo_respuesta: 'multiple' as 'multiple' | 'si_no' | 'escala' | 'texto',
    opciones_respuesta: ['', ''],
    es_obligatoria: true,
    orden: 1
  });

  // Estados para crear evaluación personalizada
  const [showCreateEvaluacion, setShowCreateEvaluacion] = useState(false);
  const [evaluacionForm, setEvaluacionForm] = useState({
    nombre: '',
    descripcion: '',
    activo: true
  });

  // Estados para editar evaluación
  const [showEditEvaluacion, setShowEditEvaluacion] = useState(false);
  const [editingEvaluacion, setEditingEvaluacion] = useState<TipoEvaluacion | null>(null);

  const isSuperAdmin = userData?.nivel_usuario === 'superadmin';
  const isAdminEmpresa = userData?.nivel_usuario === 'admin-empresa';
  const isAdminPlanta = userData?.nivel_usuario === 'admin-planta';
  
  // Permisos para gestionar evaluaciones
  const canCreateEvaluaciones = isSuperAdmin || isAdminEmpresa || isAdminPlanta;
  const canModifyNormativas = isSuperAdmin; // Solo SuperAdmin puede modificar normativas
  const canAddQuestions = isSuperAdmin || isAdminEmpresa || isAdminPlanta;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const tiposRes = await evaluacionesAPI.getTipos();
      setTipos(tiposRes.data);
    } catch (err: any) {
      setError('Error al cargar datos: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const loadPreguntas = async (tipoEvaluacion?: string) => {
    try {
      const params = tipoEvaluacion ? { tipo_evaluacion: tipoEvaluacion } : undefined;
      const response = await evaluacionesAPI.getPreguntas(params);
      setPreguntasState(response.data);
    } catch (err: any) {
      setError('Error al cargar preguntas: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleSelectNormativa = (tipo: TipoEvaluacion) => {
    setSelectedNormativa(tipo);
    setShowNormativaDetail(true);
    loadPreguntas(tipo.nombre);
  };

  const canManageEvaluationType = (tipo: TipoEvaluacion) => {
    // SuperAdmin puede gestionar todas las evaluaciones
    if (isSuperAdmin) return true;
    
    // Admins de empresa y planta solo pueden gestionar evaluaciones internas (no normativas oficiales)
    if (isAdminEmpresa || isAdminPlanta) {
      return !tipo.normativa_oficial;
    }
    
    return false;
  };

  const handleCreatePregunta = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedNormativa) {
      setError('No hay normativa seleccionada');
      return;
    }

    try {
      const nuevaPregunta = {
        ...preguntaForm,
        tipo_evaluacion: selectedNormativa.id
      };
      
      console.log('Enviando pregunta:', nuevaPregunta);
      await evaluacionesAPI.createPregunta(nuevaPregunta);
      
      // Recargar preguntas
      loadPreguntas(selectedNormativa.nombre);
      
      // Limpiar formulario
      setPreguntaForm({
        texto_pregunta: '',
        tipo_respuesta: 'multiple',
        opciones_respuesta: ['', ''],
        es_obligatoria: true,
        orden: preguntas.length + 1
      });
      
      setShowPreguntaForm(false);
      setError('');
      alert('Pregunta creada exitosamente');
    } catch (err: any) {
      console.error('Error al crear pregunta:', err);
      setError('Error al crear pregunta: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleAddOpcion = () => {
    setPreguntaForm({
      ...preguntaForm,
      opciones_respuesta: [...preguntaForm.opciones_respuesta, '']
    });
  };

  const handleRemoveOpcion = (index: number) => {
    const nuevasOpciones = preguntaForm.opciones_respuesta.filter((_, i) => i !== index);
    setPreguntaForm({
      ...preguntaForm,
      opciones_respuesta: nuevasOpciones
    });
  };

  const updateOpcion = (index: number, valor: string) => {
    const nuevasOpciones = [...preguntaForm.opciones_respuesta];
    nuevasOpciones[index] = valor;
    setPreguntaForm({
      ...preguntaForm,
      opciones_respuesta: nuevasOpciones
    });
  };

  const getIconoNormativa = (nombre: string) => {
    switch (nombre) {
      case 'NOM-030': return '⚠️';
      case 'NOM-035': return '🧠';
      case '360': return '🎯';
      default: return '📋';
    }
  };

  const closeError = () => setError('');

  const handleCreateEvaluacion = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!evaluacionForm.nombre.trim()) {
      setError('El nombre de la evaluación es requerido');
      return;
    }

    try {
      const nuevaEvaluacion = {
        nombre: evaluacionForm.nombre,
        descripcion: evaluacionForm.descripcion,
        normativa_oficial: false, // Siempre false para evaluaciones creadas por empresas/plantas
        activo: evaluacionForm.activo
      };
      
      console.log('Creando evaluación personalizada:', nuevaEvaluacion);
      
      // Llamar al endpoint para crear el tipo de evaluación
      const response = await evaluacionesAPI.createTipo(nuevaEvaluacion);
      
      // Limpiar formulario
      setEvaluacionForm({
        nombre: '',
        descripcion: '',
        activo: true
      });
      
      setShowCreateEvaluacion(false);
      setError('');
      
      // Recargar datos
      await loadData();
      
      // Mostrar mensaje de éxito
      alert(`Evaluación "${response.data.nombre}" creada exitosamente. Ahora puedes agregar preguntas personalizadas.`);
      
    } catch (err: any) {
      console.error('Error al crear evaluación:', err);
      setError('Error al crear evaluación: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleEditEvaluacion = (evaluacion: TipoEvaluacion) => {
    setEditingEvaluacion(evaluacion);
    setEvaluacionForm({
      nombre: evaluacion.nombre,
      descripcion: evaluacion.descripcion,
      activo: evaluacion.activo
    });
    setShowEditEvaluacion(true);
  };

  const handleUpdateEvaluacion = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!editingEvaluacion || !evaluacionForm.nombre.trim()) {
      setError('Datos de evaluación incompletos');
      return;
    }

    try {
      const datosActualizados = {
        nombre: evaluacionForm.nombre,
        descripcion: evaluacionForm.descripcion,
        activo: evaluacionForm.activo
      };
      
      console.log('Actualizando evaluación:', datosActualizados);
      
      await evaluacionesAPI.updateTipo(editingEvaluacion.id, datosActualizados);
      
      // Limpiar estados
      setEditingEvaluacion(null);
      setEvaluacionForm({
        nombre: '',
        descripcion: '',
        activo: true
      });
      
      setShowEditEvaluacion(false);
      setError('');
      
      // Recargar datos
      await loadData();
      
      alert('Evaluación actualizada exitosamente');
      
    } catch (err: any) {
      console.error('Error al actualizar evaluación:', err);
      setError('Error al actualizar evaluación: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteEvaluacion = async (evaluacion: TipoEvaluacion) => {
    if (!canManageEvaluationType(evaluacion)) {
      setError('No tienes permisos para eliminar esta evaluación');
      return;
    }

    const confirmDelete = window.confirm(
      `¿Estás seguro de que quieres eliminar la evaluación "${evaluacion.nombre}"?\n\nEsta acción eliminará también todas las preguntas asociadas y no se puede deshacer.`
    );

    if (!confirmDelete) return;

    try {
      await evaluacionesAPI.deleteTipo(evaluacion.id);
      
      // Recargar datos
      await loadData();
      
      alert('Evaluación eliminada exitosamente');
      
    } catch (err: any) {
      console.error('Error al eliminar evaluación:', err);
      setError('Error al eliminar evaluación: ' + (err.response?.data?.detail || err.message));
    }
  };

  if (loading) {
    return (
      <div className="evaluaciones-gestion">
        <div className="loading">Cargando evaluaciones...</div>
      </div>
    );
  }

  return (
    <div className="evaluaciones-gestion">
      <div className="page-header">
        <h2>Gestión de Evaluaciones</h2>
        <p>
          {isSuperAdmin ? 
            'Administra todas las evaluaciones normativas y personalizadas' : 
            'Gestiona evaluaciones internas y personalizadas de tu organización'
          }
        </p>
      </div>

      {error && (
        <div className="error-message">
          <span>{error}</span>
          <button onClick={closeError} className="close-error">×</button>
        </div>
      )}

      {!showNormativaDetail ? (
        <div className="tabs-container">
          <div className="tabs">
            <button className="tab active">
              {isSuperAdmin ? 'Todas las Evaluaciones' : 'Evaluaciones Disponibles'}
            </button>
            {canCreateEvaluaciones && (
              <button 
                className="tab"
                onClick={() => setShowCreateEvaluacion(true)}
              >
                + Crear Evaluación Personalizada
              </button>
            )}
          </div>
          <div className="tab-content">
            <div className="evaluaciones-grid">
              {tipos.map(tipo => (
                <div
                  key={tipo.id}
                  className={`evaluacion-card ${!canManageEvaluationType(tipo) ? 'readonly' : ''}`}
                >
                  <div className="card-header">
                    <h4>
                      {getIconoNormativa(tipo.nombre)} {tipo.nombre}
                    </h4>
                    <div className="card-badges">
                      <span className={`status-badge ${tipo.normativa_oficial ? 'activa' : 'borrador'}`}>
                        {tipo.normativa_oficial ? 'Oficial' : 'Personalizada'}
                      </span>
                      {!canManageEvaluationType(tipo) && (
                        <span className="readonly-badge">Solo lectura</span>
                      )}
                    </div>
                  </div>
                  <div className="card-content">
                    <p><strong>Descripción:</strong> {tipo.descripcion}</p>
                    <p><strong>Estado:</strong> {tipo.activo ? 'Activa' : 'Inactiva'}</p>
                    {tipo.normativa_oficial && !isSuperAdmin && (
                      <p className="warning-text">
                        <strong>Nota:</strong> Solo puedes ver y usar las preguntas de esta evaluación normativa. No puedes modificarla.
                      </p>
                    )}
                  </div>
                  <div className="card-actions">
                    <button 
                      className="btn-primary"
                      onClick={() => handleSelectNormativa(tipo)}
                    >
                      {canManageEvaluationType(tipo) ? 'Gestionar Preguntas' : 'Ver Preguntas'}
                    </button>
                    {canManageEvaluationType(tipo) && !tipo.normativa_oficial && (
                      <div className="card-secondary-actions">
                        <button 
                          className="btn-info"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEditEvaluacion(tipo);
                          }}
                        >
                          Editar
                        </button>
                        <button 
                          className="btn-danger"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteEvaluacion(tipo);
                          }}
                        >
                          Eliminar
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {tipos.length === 0 && (
              <div className="empty-state">
                <p>No hay normativas disponibles.</p>
                <button 
                  className="btn-primary"
                  onClick={() => window.location.reload()}
                >
                  Recargar
                </button>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="normativa-detail">
          <div className="detail-header">
            <button 
              className="btn-secondary"
              onClick={() => {
                setShowNormativaDetail(false);
                setSelectedNormativa(null);
                setPreguntasState([]);
              }}
            >
              ← Volver
            </button>
            <h3 className="detail-title">
              {getIconoNormativa(selectedNormativa?.nombre || '')} {selectedNormativa?.nombre} - 
              {canManageEvaluationType(selectedNormativa!) ? ' Gestión de Preguntas' : ' Consulta de Preguntas'}
              {selectedNormativa?.normativa_oficial && !isSuperAdmin && (
                <span className="readonly-indicator"> (Solo lectura)</span>
              )}
            </h3>
            {canAddQuestions && canManageEvaluationType(selectedNormativa!) && (
              <button 
                className="btn-primary"
                onClick={() => setShowPreguntaForm(true)}
              >
                + Agregar Pregunta
              </button>
            )}
          </div>

          <div className="preguntas-container">
            <div className="preguntas-stats">
              <div className="stat-card">
                <h4>Total de Preguntas</h4>
                <span className="stat-number">{preguntas.length}</span>
              </div>
              <div className="stat-card">
                <h4>Preguntas Obligatorias</h4>
                <span className="stat-number">{preguntas.filter(p => p.es_obligatoria).length}</span>
              </div>
              <div className="stat-card">
                <h4>Tipos de Respuesta</h4>
                <span className="stat-number">{new Set(preguntas.map(p => p.tipo_respuesta)).size}</span>
              </div>
            </div>

            <div className="preguntas-list">
              {preguntas.map((pregunta, index) => (
                <div key={pregunta.id} className="pregunta-card">
                  <div className="pregunta-header">
                    <span className="pregunta-numero">#{index + 1}</span>
                    <span className={`tipo-badge ${pregunta.tipo_respuesta}`}>
                      {pregunta.tipo_respuesta}
                    </span>
                    {pregunta.es_obligatoria && (
                      <span className="obligatoria-badge">Obligatoria</span>
                    )}
                  </div>
                  <div className="pregunta-content">
                    <h4>{pregunta.texto_pregunta}</h4>
                    {pregunta.opciones_respuesta.length > 0 && (
                      <div className="opciones-preview">
                        <strong>Opciones:</strong>
                        <ul>
                          {pregunta.opciones_respuesta.map((opcion, i) => (
                            <li key={i}>{opcion}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  <div className="pregunta-actions">
                    {canManageEvaluationType(selectedNormativa!) && (
                      <>
                        <button className="btn-info">Editar</button>
                        <button className="btn-danger">Eliminar</button>
                      </>
                    )}
                    {!canManageEvaluationType(selectedNormativa!) && (
                      <span className="readonly-text">Solo lectura</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {preguntas.length === 0 && (
              <div className="empty-state">
                <p>No hay preguntas para esta {selectedNormativa?.normativa_oficial ? 'normativa' : 'evaluación'}.</p>
                {canAddQuestions && canManageEvaluationType(selectedNormativa!) && (
                  <button 
                    className="btn-primary"
                    onClick={() => setShowPreguntaForm(true)}
                  >
                    Crear Primera Pregunta
                  </button>
                )}
                {!canManageEvaluationType(selectedNormativa!) && (
                  <p className="info-text">
                    Esta es una evaluación normativa oficial. No puedes agregar preguntas, pero puedes usar las existentes en tus evaluaciones.
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {showPreguntaForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Agregar Nueva Pregunta</h3>
              <button 
                className="modal-close"
                onClick={() => setShowPreguntaForm(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleCreatePregunta} className="pregunta-form">
              <div className="form-group">
                <label>Texto de la Pregunta</label>
                <textarea
                  value={preguntaForm.texto_pregunta}
                  onChange={(e) => setPreguntaForm({...preguntaForm, texto_pregunta: e.target.value})}
                  required
                  placeholder="Escribe aquí la pregunta..."
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Tipo de Respuesta</label>
                <select
                  value={preguntaForm.tipo_respuesta}
                  onChange={(e) => setPreguntaForm({...preguntaForm, tipo_respuesta: e.target.value as any})}
                  required
                >
                  <option value="multiple">Opción múltiple</option>
                  <option value="si_no">Sí/No</option>
                  <option value="escala">Escala (1-5)</option>
                  <option value="texto">Texto libre</option>
                </select>
              </div>

              {(preguntaForm.tipo_respuesta === 'multiple' || preguntaForm.tipo_respuesta === 'si_no' || preguntaForm.tipo_respuesta === 'escala') && (
                <div className="form-group">
                  <label>Opciones de Respuesta</label>
                  {preguntaForm.opciones_respuesta.map((opcion, index) => (
                    <div key={index} className="opcion-input">
                      <input
                        type="text"
                        value={opcion}
                        onChange={(e) => updateOpcion(index, e.target.value)}
                        placeholder={`Opción ${index + 1}`}
                        required
                      />
                      {preguntaForm.opciones_respuesta.length > 2 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveOpcion(index)}
                          className="btn-danger"
                        >
                          Eliminar
                        </button>
                      )}
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={handleAddOpcion}
                    className="btn-secondary"
                  >
                    + Agregar Opción
                  </button>
                </div>
              )}

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={preguntaForm.es_obligatoria}
                    onChange={(e) => setPreguntaForm({...preguntaForm, es_obligatoria: e.target.checked})}
                  />
                  Pregunta obligatoria
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-success">
                  Crear Pregunta
                </button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowPreguntaForm(false)}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para crear evaluación personalizada */}
      {showCreateEvaluacion && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Crear Evaluación Personalizada</h3>
              <button 
                className="modal-close"
                onClick={() => setShowCreateEvaluacion(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleCreateEvaluacion} className="evaluacion-form">
              <div className="form-group">
                <label>Nombre de la Evaluación</label>
                <input
                  type="text"
                  value={evaluacionForm.nombre}
                  onChange={(e) => setEvaluacionForm({...evaluacionForm, nombre: e.target.value})}
                  required
                  placeholder="Ej: Evaluación de Clima Laboral 2024"
                />
              </div>

              <div className="form-group">
                <label>Descripción</label>
                <textarea
                  value={evaluacionForm.descripcion}
                  onChange={(e) => setEvaluacionForm({...evaluacionForm, descripcion: e.target.value})}
                  placeholder="Describe el propósito y alcance de esta evaluación..."
                  rows={4}
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={evaluacionForm.activo}
                    onChange={(e) => setEvaluacionForm({...evaluacionForm, activo: e.target.checked})}
                  />
                  Activar evaluación inmediatamente
                </label>
              </div>

              <div className="form-info">
                <p><strong>Nota:</strong> Una vez creada la evaluación, podrás agregar preguntas personalizadas y usar preguntas de evaluaciones normativas existentes.</p>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-success">
                  Crear Evaluación
                </button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowCreateEvaluacion(false)}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para editar evaluación personalizada */}
      {showEditEvaluacion && editingEvaluacion && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Editar Evaluación: {editingEvaluacion.nombre}</h3>
              <button 
                className="modal-close"
                onClick={() => {
                  setShowEditEvaluacion(false);
                  setEditingEvaluacion(null);
                }}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleUpdateEvaluacion} className="evaluacion-form">
              <div className="form-group">
                <label>Nombre de la Evaluación</label>
                <input
                  type="text"
                  value={evaluacionForm.nombre}
                  onChange={(e) => setEvaluacionForm({...evaluacionForm, nombre: e.target.value})}
                  required
                  placeholder="Ej: Evaluación de Clima Laboral 2024"
                />
              </div>

              <div className="form-group">
                <label>Descripción</label>
                <textarea
                  value={evaluacionForm.descripcion}
                  onChange={(e) => setEvaluacionForm({...evaluacionForm, descripcion: e.target.value})}
                  placeholder="Describe el propósito y alcance de esta evaluación..."
                  rows={4}
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={evaluacionForm.activo}
                    onChange={(e) => setEvaluacionForm({...evaluacionForm, activo: e.target.checked})}
                  />
                  Evaluación activa
                </label>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-success">
                  Actualizar Evaluación
                </button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => {
                    setShowEditEvaluacion(false);
                    setEditingEvaluacion(null);
                  }}
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

export default EvaluacionesGestion;
