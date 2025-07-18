import React, { useState, useEffect } from 'react';
import evaluacionesAPI, { EvaluacionCompleta, TipoEvaluacion, Pregunta } from '../services/evaluacionesService';
import '../css/Evaluaciones.css';

interface EvaluacionesGestionProps {
  userData?: any;
}

const EvaluacionesGestion: React.FC<EvaluacionesGestionProps> = ({ userData }) => {
  const [evaluaciones, setEvaluaciones] = useState<EvaluacionCompleta[]>([]);
  const [tipos, setTipos] = useState<TipoEvaluacion[]>([]);
  const [preguntas, setPreguntas] = useState<Pregunta[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'evaluaciones'>('evaluaciones');
  
  // Estados para crear evaluación
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    titulo: '',
    descripcion: '',
    tipo_evaluacion: '',
    fecha_inicio: '',
    fecha_fin: '',
    es_anonima: true,
    preguntas_seleccionadas: [] as number[]
  });

  // Estados para gestión de normativas
  const [selectedNormativa, setSelectedNormativa] = useState<string>('');
  const [showNormativaDetail, setShowNormativaDetail] = useState(false);
  const [showPreguntaForm, setShowPreguntaForm] = useState(false);
  const [preguntaForm, setPreguntaForm] = useState({
    texto_pregunta: '',
    tipo_respuesta: 'multiple' as 'multiple' | 'si_no' | 'escala' | 'texto',
    opciones_respuesta: ['', ''],
    es_obligatoria: true,
    orden: 1
  });

  const normativas = [
    { 
      id: 'nom-030', 
      nombre: 'NOM-030', 
      titulo: 'Servicios Preventivos de Seguridad y Salud en el Trabajo',
      descripcion: 'Normativa oficial para servicios preventivos de seguridad y salud en el trabajo',
      icono: '⚠️'
    },
    { 
      id: 'nom-035', 
      nombre: 'NOM-035', 
      titulo: 'Factores de Riesgo Psicosocial en el Trabajo',
      descripcion: 'Normativa oficial para identificación y prevención de factores de riesgo psicosocial',
      icono: '🧠'
    },
    { 
      id: 'evaluacion-360', 
      nombre: 'Evaluación 360°', 
      titulo: 'Evaluación de Competencias 360 Grados',
      descripcion: 'Evaluación integral de competencias desde múltiples perspectivas',
      icono: '🎯'
    }
  ];

  const isSuperAdmin = userData?.nivel_usuario === 'superadmin';
  const isAdminEmpresa = userData?.nivel_usuario === 'admin-empresa';

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [evaluacionesRes, tiposRes] = await Promise.all([
        evaluacionesAPI.getEvaluaciones(),
        evaluacionesAPI.getTipos()
      ]);
      
      setEvaluaciones(evaluacionesRes.data);
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
      setPreguntas(response.data);
    } catch (err: any) {
      setError('Error al cargar preguntas: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleCreateEvaluacion = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const data = {
        ...formData,
        tipo_evaluacion: parseInt(formData.tipo_evaluacion),
        preguntas_seleccionadas: formData.preguntas_seleccionadas.map((id, index) => ({
          pregunta_id: id,
          orden: index + 1,
          es_obligatoria: true
        }))
      };
      
      await evaluacionesAPI.createEvaluacion(data);
      setShowCreateForm(false);
      setFormData({
        titulo: '',
        descripcion: '',
        tipo_evaluacion: '',
        fecha_inicio: '',
        fecha_fin: '',
        es_anonima: true,
        preguntas_seleccionadas: []
      });
      await loadData();
    } catch (err: any) {
      setError('Error al crear evaluación: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleActivarEvaluacion = async (id: number) => {
    try {
      await evaluacionesAPI.activarEvaluacion(id);
      await loadData();
    } catch (err: any) {
      setError('Error al activar evaluación: ' + (err.response?.data?.detail || err.message));
    }
  };

  const crearPreguntasOficiales = async () => {
    if (!isSuperAdmin) return;
    
    setLoading(true);
    try {
      const response = await evaluacionesAPI.crearPreguntasOficiales();
      alert(`✅ ${response.data.message}`);
      await loadPreguntas();
    } catch (err: any) {
      setError('Error al crear preguntas: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const togglePreguntaSeleccionada = (preguntaId: number) => {
    const selected = formData.preguntas_seleccionadas;
    if (selected.includes(preguntaId)) {
      setFormData({
        ...formData,
        preguntas_seleccionadas: selected.filter(id => id !== preguntaId)
      });
    } else {
      setFormData({
        ...formData,
        preguntas_seleccionadas: [...selected, preguntaId]
      });
    }
  };

  const handleCreatePregunta = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const data = {
        ...preguntaForm,
        opciones_respuesta: preguntaForm.tipo_respuesta === 'multiple' ? preguntaForm.opciones_respuesta.filter((op: string) => op.trim()) : [],
        tipo_evaluacion: parseInt(selectedNormativa) || 1
      };
      
      await evaluacionesAPI.createPregunta(data);
      setPreguntaForm({
        texto_pregunta: '',
        tipo_respuesta: 'multiple',
        opciones_respuesta: ['', ''],
        es_obligatoria: true,
        orden: 1
      });
      setShowPreguntaForm(false);
      if (selectedNormativa) {
        loadPreguntas(selectedNormativa);
      }
      setError('');
    } catch (err: any) {
      setError('Error al crear pregunta: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleTipoPreguntaChange = (tipo: string) => {
    setPreguntaForm(prev => ({
      ...prev,
      tipo_respuesta: tipo as 'multiple' | 'si_no' | 'escala' | 'texto',
      opciones_respuesta: tipo === 'multiple' ? ['', ''] : 
                         tipo === 'si_no' ? ['Sí', 'No'] : 
                         tipo === 'escala' ? ['1', '2', '3', '4', '5'] : []
    }));
  };

  const addOpcion = () => {
    setPreguntaForm(prev => ({
      ...prev,
      opciones_respuesta: [...prev.opciones_respuesta, '']
    }));
  };

  const removeOpcion = (index: number) => {
    setPreguntaForm(prev => ({
      ...prev,
      opciones_respuesta: prev.opciones_respuesta.filter((_: string, i: number) => i !== index)
    }));
  };

  const updateOpcion = (index: number, value: string) => {
    setPreguntaForm(prev => ({
      ...prev,
      opciones_respuesta: prev.opciones_respuesta.map((op: string, i: number) => i === index ? value : op)
    }));
  };

  const renderEvaluaciones = () => (
    <div className="evaluaciones-section">
      <div className="section-header">
        <h3>📊 Evaluaciones</h3>
        {isAdminEmpresa && (
          <button 
            onClick={() => setShowCreateForm(true)}
            className="btn-primary"
          >
            ➕ Nueva Evaluación
          </button>
        )}
      </div>

      <div className="evaluaciones-grid">
        {evaluaciones.map(evaluacion => (
          <div key={evaluacion.id} className="evaluacion-card">
            <div className="card-header">
              <h4>{evaluacion.titulo}</h4>
              <span className={`status-badge ${evaluacion.estado}`}>
                {evaluacion.estado.toUpperCase()}
              </span>
            </div>
            
            <div className="card-content">
              <p><strong>Tipo:</strong> {evaluacion.tipo_evaluacion_nombre}</p>
              <p><strong>Descripción:</strong> {evaluacion.descripcion}</p>
              <p><strong>Fecha inicio:</strong> {new Date(evaluacion.fecha_inicio).toLocaleDateString()}</p>
              <p><strong>Fecha fin:</strong> {new Date(evaluacion.fecha_fin).toLocaleDateString()}</p>
              <p><strong>Preguntas:</strong> {evaluacion.total_preguntas}</p>
              <p><strong>Respuestas:</strong> {evaluacion.total_respuestas}</p>
              <p><strong>Anónima:</strong> {evaluacion.es_anonima ? 'Sí' : 'No'}</p>
            </div>
            
            <div className="card-actions">
              {evaluacion.estado === 'borrador' && isAdminEmpresa && (
                <button 
                  onClick={() => handleActivarEvaluacion(evaluacion.id)}
                  className="btn-success"
                >
                  🚀 Activar
                </button>
              )}
              <button className="btn-info">
                📈 Ver Resultados
              </button>
            </div>
          </div>
        ))}
      </div>

      {evaluaciones.length === 0 && (
        <div className="empty-state">
          <p>No hay evaluaciones creadas</p>
          {isAdminEmpresa && (
            <button 
              onClick={() => setShowCreateForm(true)}
              className="btn-primary"
            >
              Crear mi primera evaluación
            </button>
          )}
        </div>
      )}
    </div>
  );

  const renderPreguntas = () => (
    <div className="preguntas-section">
      <div className="section-header">
        <h3>❓ Banco de Preguntas</h3>
        <div className="header-actions">
          <select 
            onChange={(e) => loadPreguntas(e.target.value || undefined)}
            className="tipo-filter"
          >
            <option value="">Todos los tipos</option>
            {tipos.map(tipo => (
              <option key={tipo.id} value={tipo.nombre}>
                {tipo.nombre}
              </option>
            ))}
          </select>
          
          {isSuperAdmin && (
            <button 
              onClick={crearPreguntasOficiales}
              className="btn-secondary"
              disabled={loading}
            >
              🏛️ Crear Preguntas Oficiales
            </button>
          )}
        </div>
      </div>

      <div className="preguntas-list">
        {preguntas.map(pregunta => (
          <div key={pregunta.id} className="pregunta-card">
            <div className="pregunta-header">
              <span className="tipo-badge">{pregunta.tipo_evaluacion_nombre}</span>
              <span className="empresa-badge">
                {pregunta.empresa_nombre || 'OFICIAL'}
              </span>
            </div>
            
            <div className="pregunta-content">
              <p className="pregunta-texto">{pregunta.texto_pregunta}</p>
              <div className="pregunta-meta">
                <span>Tipo: {pregunta.tipo_respuesta}</span>
                <span>Orden: {pregunta.orden}</span>
                <span>Obligatoria: {pregunta.es_obligatoria ? 'Sí' : 'No'}</span>
              </div>
              
              {pregunta.opciones_respuesta.length > 0 && (
                <div className="opciones">
                  <strong>Opciones:</strong>
                  <ul>
                    {pregunta.opciones_respuesta.map((opcion, index) => (
                      <li key={index}>{opcion}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {preguntas.length === 0 && (
        <div className="empty-state">
          <p>No hay preguntas disponibles</p>
          {isSuperAdmin && (
            <button 
              onClick={crearPreguntasOficiales}
              className="btn-primary"
            >
              Crear Preguntas Oficiales
            </button>
          )}
        </div>
      )}
    </div>
  );

  const renderCreateForm = () => (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>➕ Nueva Evaluación</h3>
          <button 
            onClick={() => setShowCreateForm(false)}
            className="close-btn"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleCreateEvaluacion} className="create-form">
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
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Tipo de Evaluación:</label>
              <select
                value={formData.tipo_evaluacion}
                onChange={(e) => {
                  setFormData({...formData, tipo_evaluacion: e.target.value});
                  if (e.target.value) {
                    const tipo = tipos.find(t => t.id.toString() === e.target.value);
                    if (tipo) loadPreguntas(tipo.nombre);
                  }
                }}
                required
              >
                <option value="">Seleccionar tipo</option>
                {tipos.map(tipo => (
                  <option key={tipo.id} value={tipo.id}>
                    {tipo.nombre} - {tipo.descripcion}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={formData.es_anonima}
                  onChange={(e) => setFormData({...formData, es_anonima: e.target.checked})}
                />
                Evaluación Anónima
              </label>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Fecha de Inicio:</label>
              <input
                type="datetime-local"
                value={formData.fecha_inicio}
                onChange={(e) => setFormData({...formData, fecha_inicio: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label>Fecha de Fin:</label>
              <input
                type="datetime-local"
                value={formData.fecha_fin}
                onChange={(e) => setFormData({...formData, fecha_fin: e.target.value})}
                required
              />
            </div>
          </div>

          {preguntas.length > 0 && (
            <div className="form-group">
              <label>Seleccionar Preguntas:</label>
              <div className="preguntas-selector">
                {preguntas.map(pregunta => (
                  <div key={pregunta.id} className="pregunta-checkbox">
                    <label>
                      <input
                        type="checkbox"
                        checked={formData.preguntas_seleccionadas.includes(pregunta.id)}
                        onChange={() => togglePreguntaSeleccionada(pregunta.id)}
                      />
                      {pregunta.texto_pregunta}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="form-actions">
            <button type="button" onClick={() => setShowCreateForm(false)} className="btn-secondary">
              Cancelar
            </button>
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Creando...' : 'Crear Evaluación'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // Función para manejar selección de normativa
  const handleSelectNormativa = (normativa: any) => {
    setSelectedNormativa(normativa.id);
    setShowNormativaDetail(true);
    loadPreguntas(normativa.id);
  };

  const handleBackToEvaluaciones = () => {
    setShowNormativaDetail(false);
    setSelectedNormativa('');
    setShowPreguntaForm(false);
  };

  // Función principal de render
  const renderMainContent = () => {
    if (showNormativaDetail && selectedNormativa) {
      return renderNormativaDetail();
    }
    
    return renderEvaluacionesList();
  };

  const renderEvaluacionesList = () => (
    <div className="evaluaciones-main">
      <div className="section-header">
        <h3>📋 Gestión de Evaluaciones</h3>
        <p className="section-description">
          Gestiona las evaluaciones oficiales y sus preguntas. Haz clic en "Editar" para gestionar las preguntas de cada evaluación.
        </p>
      </div>

      <div className="evaluaciones-grid">
        {normativas.map(normativa => (
          <div key={normativa.id} className="evaluacion-card">
            <div className="evaluacion-icon">{normativa.icono}</div>
            <div className="evaluacion-info">
              <h4>{normativa.nombre}</h4>
              <h5>{normativa.titulo}</h5>
              <p>{normativa.descripcion}</p>
            </div>
            <div className="evaluacion-stats">
              <div className="stat">
                <span className="stat-number">
                  {preguntas.filter(p => p.tipo_evaluacion === parseInt(normativa.id) || p.tipo_evaluacion?.toString() === normativa.id).length}
                </span>
                <span className="stat-label">Preguntas</span>
              </div>
            </div>
            <div className="evaluacion-actions">
              <button 
                onClick={() => handleSelectNormativa(normativa)}
                className="btn-primary"
              >
                ✏️ Editar Preguntas
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Evaluaciones creadas por empresas */}
      {evaluaciones.length > 0 && (
        <div className="evaluaciones-empresa-section">
          <h4>📊 Evaluaciones Creadas</h4>
          <div className="evaluaciones-empresa-grid">
            {evaluaciones.map(evaluacion => (
              <div key={evaluacion.id} className="evaluacion-empresa-card">
                <div className="evaluacion-empresa-header">
                  <h5>{evaluacion.titulo}</h5>
                  <span className={`status ${evaluacion.estado}`}>
                    {evaluacion.estado}
                  </span>
                </div>
                <p>{evaluacion.descripcion}</p>
                <div className="evaluacion-empresa-stats">
                  <span>{evaluacion.total_preguntas} preguntas</span>
                  <span>{evaluacion.total_respuestas} respuestas</span>
                </div>
                <div className="evaluacion-empresa-actions">
                  <button className="btn-info btn-sm">👁️ Ver</button>
                  <button className="btn-warning btn-sm">✏️ Editar</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Botón para crear evaluación personalizada */}
      {(isSuperAdmin || isAdminEmpresa) && (
        <div className="add-evaluacion-section">
          <button 
            onClick={() => setShowCreateForm(true)}
            className="btn-secondary add-evaluacion-btn"
          >
            ➕ Crear Evaluación Personalizada
          </button>
        </div>
      )}
    </div>
  );

  const renderNormativaDetail = () => {
    const normativa = normativas.find(n => n.id === selectedNormativa);
    const preguntasNormativa = preguntas.filter(p => 
      p.tipo_evaluacion === parseInt(selectedNormativa) || 
      p.tipo_evaluacion?.toString() === selectedNormativa
    );

    return (
      <div className="normativa-detail">
        <div className="detail-header">
          <button 
            onClick={handleBackToEvaluaciones}
            className="btn-back"
          >
            ← Volver a Evaluaciones
          </button>
          <div className="detail-title">
            <span className="detail-icon">{normativa?.icono}</span>
            <div>
              <h3>{normativa?.nombre}</h3>
              <p>{normativa?.titulo}</p>
            </div>
          </div>
          <button 
            onClick={() => setShowPreguntaForm(true)}
            className="btn-primary"
          >
            ➕ Agregar Pregunta
          </button>
        </div>

        <div className="preguntas-container">
          <div className="preguntas-header">
            <h4>Preguntas de {normativa?.nombre}</h4>
            <span className="preguntas-count">{preguntasNormativa.length} preguntas</span>
          </div>

          {preguntasNormativa.length === 0 ? (
            <div className="empty-preguntas">
              <div className="empty-icon">📝</div>
              <h5>No hay preguntas creadas</h5>
              <p>Comienza creando la primera pregunta para esta normativa</p>
              <button 
                onClick={() => setShowPreguntaForm(true)}
                className="btn-primary"
              >
                Crear primera pregunta
              </button>
            </div>
          ) : (
            <div className="preguntas-list">
              {preguntasNormativa.map((pregunta, index) => (
                <div key={pregunta.id} className="pregunta-card">
                  <div className="pregunta-header">
                    <span className="pregunta-numero">#{index + 1}</span>
                    <span className="pregunta-tipo">{pregunta.tipo_respuesta?.toUpperCase()}</span>
                    {pregunta.es_obligatoria && <span className="pregunta-required">*</span>}
                  </div>
                  
                  <div className="pregunta-content">
                    <p className="pregunta-texto">{pregunta.texto_pregunta}</p>
                    
                    {pregunta.opciones_respuesta && pregunta.opciones_respuesta.length > 0 && (
                      <div className="pregunta-opciones">
                        <strong>Opciones:</strong>
                        <ul>
                          {pregunta.opciones_respuesta.map((opcion: string, idx: number) => (
                            <li key={idx}>{opcion}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  
                  <div className="pregunta-actions">
                    <button className="btn-warning btn-sm">✏️ Editar</button>
                    <button className="btn-danger btn-sm">🗑️ Eliminar</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {showPreguntaForm && renderPreguntaForm()}
      </div>
    );
  };

  const renderPreguntaForm = () => (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>➕ Crear Nueva Pregunta</h3>
          <button 
            onClick={() => setShowPreguntaForm(false)}
            className="modal-close"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleCreatePregunta} className="pregunta-form">
          <div className="form-group">
            <label htmlFor="normativa">Normativa</label>
            <select
              id="normativa"
              value={selectedNormativa}
              onChange={(e) => setSelectedNormativa(e.target.value)}
              required
            >
              <option value="">Seleccionar normativa</option>
              {normativas.map(normativa => (
                <option key={normativa.id} value={normativa.id}>
                  {normativa.nombre}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="texto">Texto de la pregunta</label>
            <textarea
              id="texto"
              value={preguntaForm.texto_pregunta}
              onChange={(e) => setPreguntaForm(prev => ({...prev, texto_pregunta: e.target.value}))}
              placeholder="Escriba la pregunta..."
              required
              rows={3}
            />
          </div>

          <div className="form-group">
            <label htmlFor="tipo">Tipo de pregunta</label>
            <select
              id="tipo"
              value={preguntaForm.tipo_respuesta}
              onChange={(e) => handleTipoPreguntaChange(e.target.value)}
              required
            >
              <option value="multiple">Opción múltiple</option>
              <option value="si_no">Sí/No</option>
              <option value="escala">Escala (1-5)</option>
              <option value="texto">Texto libre</option>
            </select>
          </div>

          {preguntaForm.tipo_respuesta === 'multiple' && (
            <div className="form-group">
              <label>Opciones de respuesta</label>
              {preguntaForm.opciones_respuesta.map((opcion: string, index: number) => (
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
                      onClick={() => removeOpcion(index)}
                      className="btn-danger btn-sm"
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
              <button 
                type="button"
                onClick={addOpcion}
                className="btn-secondary btn-sm"
              >
                ➕ Agregar opción
              </button>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="orden">Orden</label>
            <input
              type="number"
              id="orden"
              value={preguntaForm.orden}
              onChange={(e) => setPreguntaForm(prev => ({...prev, orden: parseInt(e.target.value)}))}
              min="1"
              required
            />
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={preguntaForm.es_obligatoria}
                onChange={(e) => setPreguntaForm(prev => ({...prev, es_obligatoria: e.target.checked}))}
              />
              Pregunta requerida
            </label>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creando...' : 'Crear Pregunta'}
            </button>
            <button 
              type="button" 
              onClick={() => setShowPreguntaForm(false)}
              className="btn-secondary"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  return (
    <div className="evaluaciones-gestion">
      <div className="page-header">
        <h2>📊 Sistema de Evaluaciones</h2>
        <p>Gestión de evaluaciones NOM-035, NOM-030 y 360°</p>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError('')} className="close-error">✕</button>
        </div>
      )}

      <div className="evaluaciones-container">
        <div className="evaluaciones-content">
          {loading && <div className="loading">Cargando...</div>}
          
          {renderMainContent()}
        </div>
      </div>

      {showCreateForm && renderCreateForm()}
    </div>
  );
};

export default EvaluacionesGestion;
