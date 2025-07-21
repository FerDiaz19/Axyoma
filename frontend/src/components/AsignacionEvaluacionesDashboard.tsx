import React, { useState, useEffect, useCallback } from 'react';
import api from '../api';
import EvaluacionesActivas from './EvaluacionesActivas';

interface Evaluacion {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_evaluacion_nombre: string;
  total_preguntas: number;
  estado: string;
  fecha_inicio: string;
  fecha_fin: string;
  empresa_nombre?: string;
  es_normativa: boolean;
}

interface Empleado {
  empleado_id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  genero: string;
  antiguedad?: number;
  status: boolean;
  puesto: number;
  departamento: number;
  planta: number;
  // Nombres descriptivos
  departamento_nombre?: string;
  puesto_nombre?: string;
  planta_nombre?: string;
}

interface TokenGenerado {
  empleado_id: number;
  empleado_nombre: string;
  empleado_apellido: string;
  empleado_email: string;
  token_generado: string;
  evaluacion_titulo?: string;
  fecha_asignacion?: string;
  usado?: boolean;
}

interface AsignacionEvaluacionesDashboardProps {
  empresaId?: number;
}

const AsignacionEvaluacionesDashboard: React.FC<AsignacionEvaluacionesDashboardProps> = ({ empresaId }) => {
  const [evaluaciones, setEvaluaciones] = useState<Evaluacion[]>([]);
  const [evaluacionSeleccionada, setEvaluacionSeleccionada] = useState<number | null>(null);
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [empleadosSeleccionados, setEmpleadosSeleccionados] = useState<number[]>([]);
  const [tokensGenerados, setTokensGenerados] = useState<TokenGenerado[]>([]);
  const [paso, setPaso] = useState<'seleccionar' | 'empleados' | 'tokens'>('seleccionar');
  const [vistaActiva, setVistaActiva] = useState<'evaluaciones' | 'activas' | 'tokens'>('evaluaciones');
  const [filtros, setFiltros] = useState({
    departamento: '',
    puesto: '',
    planta: ''
  });
  const [loading, setLoading] = useState(false);
  const [loadingEvaluaciones, setLoadingEvaluaciones] = useState(true);

  // Cargar evaluaciones disponibles
  const cargarEvaluaciones = async () => {
    try {
      console.log('🚀 Iniciando carga de evaluaciones...');
      setLoadingEvaluaciones(true);
      const response = await api.get('/evaluaciones/evaluaciones/');
      console.log('🔍 API Response:', response);
      console.log('🔍 Response data:', response.data);
      console.log('🔍 Auth token:', localStorage.getItem('authToken'));
      const data = response.data;
      const evaluacionesArray = Array.isArray(data) ? data : (data.results || []);
      console.log('📊 Evaluaciones procesadas:', evaluacionesArray);
      setEvaluaciones(evaluacionesArray);
    } catch (error) {
      console.error('❌ Error al cargar evaluaciones:', error);
      setEvaluaciones([]);
    } finally {
      setLoadingEvaluaciones(false);
    }
  };

  useEffect(() => {
    cargarEvaluaciones();
  }, []);  // Cargar empleados cuando se selecciona una evaluación
  const cargarEmpleados = useCallback(async () => {
    if (!evaluacionSeleccionada) return;
    
    try {
      setLoading(true);
      console.log('🔄 Cargando empleados para evaluación:', evaluacionSeleccionada);
      
      const queryParams = new URLSearchParams();
      
      if (filtros.departamento) queryParams.append('departamento', filtros.departamento);
      if (filtros.puesto) queryParams.append('puesto', filtros.puesto);
      if (filtros.planta) queryParams.append('planta', filtros.planta);

      // Usar el endpoint de empleados general, no específico de evaluación
      const url = `/empleados/?${queryParams}`;
      console.log('🌐 URL empleados:', url);
      
      const response = await api.get(url);
      console.log('✅ Empleados cargados:', response.data.length);
      setEmpleados(response.data);
    } catch (error: any) {
      console.error('❌ Error al cargar empleados:', error);
      console.error('❌ Error response:', error.response?.data);
      console.error('❌ Error status:', error.response?.status);
      setEmpleados([]);
      alert('Error al cargar empleados. Verifica la conexión.');
    } finally {
      setLoading(false);
    }
  }, [evaluacionSeleccionada, filtros]);

  useEffect(() => {
    if (evaluacionSeleccionada) {
      cargarEmpleados();
    }
  }, [evaluacionSeleccionada, cargarEmpleados]);

  // Cargar tokens desde el backend
  const cargarTokensGenerados = async () => {
    try {
      setLoading(true);
      const response = await api.get('/evaluaciones/tokens/');
      console.log('Tokens del backend:', response.data);
      
      // Transformar los datos del backend al formato esperado
      const tokensFormateados = response.data.map((token: any) => ({
        empleado_id: token.asignacion?.empleado?.empleado_id || 0,
        empleado_nombre: token.asignacion?.empleado?.nombre || '',
        empleado_apellido: token.asignacion?.empleado?.apellido_paterno || '',
        empleado_email: token.asignacion?.empleado?.email || '',
        token_generado: token.token,
        evaluacion_titulo: token.asignacion?.evaluacion?.titulo || '',
        fecha_asignacion: token.fecha_creacion,
        usado: token.usado
      }));
      
      setTokensGenerados(tokensFormateados);
    } catch (error) {
      console.error('Error al cargar tokens:', error);
      setTokensGenerados([]);
    } finally {
      setLoading(false);
    }
  };

  const crearEvaluacion360 = async () => {
    try {
      setLoading(true);
      
      const nuevaEvaluacion = {
        titulo: `Evaluación 360° Personalizada - ${new Date().toLocaleDateString()}`,
        descripcion: 'Evaluación 360° personalizada creada por la empresa',
        tipo_evaluacion: 3, // Asumiendo que 3 es el ID para evaluaciones 360°
        estado: 'borrador',
        fecha_inicio: new Date().toISOString().split('T')[0],
        fecha_fin: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 30 días después
        empresa: empresaId,
        normativa_oficial: false // Es personalizada
      };

      const response = await api.post('/evaluaciones/', nuevaEvaluacion);
      
      if (response.status === 201) {
        alert('✅ Evaluación 360° personalizada creada exitosamente');
        cargarEvaluaciones(); // Recargar la lista
      }
    } catch (error) {
      console.error('Error al crear evaluación 360°:', error);
      alert('❌ Error al crear la evaluación. Verifica los permisos.');
    } finally {
      setLoading(false);
    }
  };

  const seleccionarEvaluacion = (evaluacionId: number) => {
    setEvaluacionSeleccionada(evaluacionId);
    setPaso('empleados');
  };

  const toggleEmpleado = (empleadoId: number) => {
    setEmpleadosSeleccionados(prev => 
      prev.includes(empleadoId) 
        ? prev.filter(id => id !== empleadoId)
        : [...prev, empleadoId]
    );
  };

  const seleccionarTodos = () => {
    if (empleadosSeleccionados.length === empleados.length) {
      setEmpleadosSeleccionados([]);
    } else {
      setEmpleadosSeleccionados(empleados.map(emp => emp.empleado_id));
    }
  };

  const asignarEvaluacion = async () => {
    if (!evaluacionSeleccionada || empleadosSeleccionados.length === 0) {
      alert('Selecciona al menos un empleado');
      return;
    }

    try {
      setLoading(true);
      
      const payload = {
        evaluacion_id: evaluacionSeleccionada,
        empleados_ids: empleadosSeleccionados,
        fecha_inicio: new Date().toISOString(),
        fecha_fin: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
      };
      
      console.log('🚀 Enviando asignación:', payload);
      
      const response = await api.post(`/evaluaciones/asignaciones/asignar_masivo/`, payload);
      
      console.log('✅ Respuesta del servidor:', response.data);
      
      if (response.data.tokens && response.data.tokens.length > 0) {
        // Transformar tokens para el formato esperado por el frontend
        const tokensFormateados = response.data.tokens.map((token: any) => ({
          empleado_id: token.asignacion?.empleado?.empleado_id || 0,
          empleado_nombre: token.asignacion?.empleado?.nombre || '',
          empleado_apellido: token.asignacion?.empleado?.apellido_paterno || '',
          empleado_email: token.asignacion?.empleado?.email || 'N/A',
          token_generado: token.token,
          evaluacion_titulo: 'Evaluación asignada',
          fecha_asignacion: token.fecha_creacion,
          usado: token.usado || false
        }));
        
        setTokensGenerados(tokensFormateados);
        setPaso('tokens');
        
        alert(`✅ Evaluación asignada exitosamente a ${response.data.tokens.length} empleados`);
      } else {
        alert('⚠️ No se pudieron generar tokens. Verifica que los empleados no tengan evaluaciones activas.');
      }
      
    } catch (error: any) {
      console.error('❌ Error al asignar evaluación:', error);
      console.error('❌ Response data:', error.response?.data);
      
      let errorMessage = 'Error al asignar evaluación';
      
      if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      } else if (error.response?.status === 403) {
        errorMessage = 'Sin permisos para asignar esta evaluación';
      } else if (error.response?.status === 404) {
        errorMessage = 'Evaluación no encontrada';
      }
      
      alert(`❌ ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const reiniciar = () => {
    setEvaluacionSeleccionada(null);
    setEmpleados([]);
    setEmpleadosSeleccionados([]);
    setTokensGenerados([]);
    setPaso('seleccionar');
    setFiltros({ departamento: '', puesto: '', planta: '' });
  };

  const filtrarEvaluacionesDisponibles = () => {
    // Mostrar TODAS las evaluaciones disponibles
    console.log('🔍 Evaluaciones a filtrar:', evaluaciones);
    console.log('🔍 Total evaluaciones:', evaluaciones.length);
    
    evaluaciones.forEach(e => {
      console.log(`- ${e.titulo}: normativa=${e.es_normativa}, tipo=${e.tipo_evaluacion_nombre}`);
    });
    
    // Retornar todas las evaluaciones sin filtrar
    return evaluaciones;
  };  const copiarToken = (token: string) => {
    navigator.clipboard.writeText(token);
    alert('Token copiado al portapapeles');
  };

  return (
    <div className="asignacion-evaluaciones-dashboard">
      <div className="dashboard-header">
        <h2>Gestión de Evaluaciones</h2>
        <p>Gestiona evaluaciones normativas, personalizadas y tokens de acceso</p>
      </div>

      {/* Pestañas de navegación */}
      <div className="tabs-navigation">
        <button 
          className={`tab-button ${vistaActiva === 'evaluaciones' ? 'active' : ''}`}
          onClick={() => {
            setVistaActiva('evaluaciones');
            reiniciar(); // Reset al cambiar de vista
          }}
        >
          � Gestión de Evaluaciones
        </button>
        <button 
          className={`tab-button ${vistaActiva === 'activas' ? 'active' : ''}`}
          onClick={() => setVistaActiva('activas')}
        >
          🎯 Evaluaciones Activas
        </button>
        <button 
          className={`tab-button ${vistaActiva === 'tokens' ? 'active' : ''}`}
          onClick={() => {
            setVistaActiva('tokens');
            cargarTokensGenerados();
          }}
        >
          🔑 Tokens de Acceso
        </button>
      </div>

      {/* Vista de Gestión de Evaluaciones */}
      {vistaActiva === 'evaluaciones' && (
        <>
          {paso === 'seleccionar' && (
            <div className="evaluaciones-section">
              <div className="section-header">
                <h3>� Evaluaciones Disponibles</h3>
                <p>Gestiona evaluaciones normativas (NOM-030, NOM-035) y crea evaluaciones 360° personalizadas</p>
                <div className="actions-header">
                  <button 
                    onClick={crearEvaluacion360}
                    className="btn-primary"
                    disabled={loading}
                  >
                    ➕ Crear Evaluación 360° Personalizada
                  </button>
                </div>
              </div>
              
              {loadingEvaluaciones ? (
                <div className="loading">Cargando evaluaciones...</div>
              ) : (
                <div className="evaluaciones-grid">
                  {Array.isArray(evaluaciones) && filtrarEvaluacionesDisponibles().length > 0 ? (
                    filtrarEvaluacionesDisponibles().map((evaluacion) => (
                      <div 
                        key={evaluacion.id} 
                        className={`evaluacion-card ${
                          evaluacion.es_normativa 
                            ? `evaluacion-${evaluacion.tipo_evaluacion_nombre.toLowerCase().replace('-', '')}` 
                            : 'evaluacion-360-personal'
                        }`}
                        onClick={() => seleccionarEvaluacion(evaluacion.id)}
                      >
                        <div className="evaluacion-header">
                          <h4>{evaluacion.titulo}</h4>
                          <div className="badge-container">
                            {evaluacion.es_normativa ? (
                              <span className={`badge badge-normativa badge-${evaluacion.tipo_evaluacion_nombre.toLowerCase()}`}>
                                {evaluacion.tipo_evaluacion_nombre}
                              </span>
                            ) : (
                              <>
                                <span className="badge badge-360">360°</span>
                                <span className="badge badge-personalizada">PERSONALIZADA</span>
                              </>
                            )}
                          </div>
                        </div>
                        <p>{evaluacion.descripcion}</p>
                        <div className="evaluacion-info">
                          <small>Tipo: {evaluacion.tipo_evaluacion_nombre}</small>
                          <small>Preguntas: {evaluacion.total_preguntas}</small>
                          {!evaluacion.es_normativa && evaluacion.empresa_nombre && (
                            <small>Empresa: {evaluacion.empresa_nombre}</small>
                          )}
                        </div>
                        <div className="evaluacion-meta">
                          <span className={`estado ${evaluacion.estado.toLowerCase()}`}>
                            {evaluacion.estado}
                          </span>
                          <span className="fecha">
                            {new Date(evaluacion.fecha_inicio).toLocaleDateString()} - 
                            {new Date(evaluacion.fecha_fin).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="no-evaluaciones">
                      <div className="empty-state">
                        <h4>� No hay evaluaciones disponibles</h4>
                        <p>Las evaluaciones normativas (NOM-030, NOM-035) estarán disponibles una vez configuradas.</p>
                        <div className="empty-actions">
                          <button 
                            onClick={crearEvaluacion360}
                            className="btn-primary"
                            disabled={loading}
                          >
                            ➕ Crear Evaluación 360° Personalizada
                          </button>
                          <p className="help-text">
                            Puedes crear evaluaciones 360° personalizadas para obtener feedback 
                            integral de supervisores, pares y subordinados.
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {paso === 'empleados' && (
            <div className="empleados-section">
              <div className="section-header">
                <h3>Seleccionar Empleados</h3>
                <button onClick={reiniciar} className="btn-secondary">
                  Volver a Evaluaciones
                </button>
              </div>

              <div className="filtros-section">
                <h4>Filtros</h4>
                <div className="filtros-grid">
                  <input
                    type="text"
                    placeholder="Departamento"
                    value={filtros.departamento}
                    onChange={(e) => setFiltros({...filtros, departamento: e.target.value})}
                  />
                  <input
                    type="text"
                    placeholder="Puesto"
                    value={filtros.puesto}
                    onChange={(e) => setFiltros({...filtros, puesto: e.target.value})}
                  />
                  <input
                    type="text"
                    placeholder="Planta"
                    value={filtros.planta}
                    onChange={(e) => setFiltros({...filtros, planta: e.target.value})}
                  />
                </div>
              </div>

              <div className="empleados-controls">
                <button 
                  onClick={seleccionarTodos}
                  className="btn-outline"
                >
                  {empleadosSeleccionados.length === empleados.length ? 'Deseleccionar Todos' : 'Seleccionar Todos'}
                </button>
                <span className="seleccion-count">
                  {empleadosSeleccionados.length} de {empleados.length} empleados seleccionados
                </span>
                <button 
                  onClick={asignarEvaluacion}
                  disabled={empleadosSeleccionados.length === 0 || loading}
                  className="btn-primary"
                >
                  {loading ? 'Asignando...' : 'Asignar Evaluación'}
                </button>
              </div>

              {loading ? (
                <div className="loading">Cargando empleados...</div>
              ) : empleados.length > 0 ? (
                <div className="empleados-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Seleccionar</th>
                        <th>Nombre</th>
                        <th>Género</th>
                        <th>Departamento</th>
                        <th>Puesto</th>
                        <th>Planta</th>
                      </tr>
                    </thead>
                    <tbody>
                      {empleados.map((empleado, index) => (
                        <tr key={`empleado-${empleado.empleado_id}-${index}`}>
                          <td>
                            <input
                              type="checkbox"
                              checked={empleadosSeleccionados.includes(empleado.empleado_id)}
                              onChange={() => toggleEmpleado(empleado.empleado_id)}
                            />
                          </td>
                          <td>{empleado.nombre} {empleado.apellido_paterno}</td>
                          <td>{empleado.genero}</td>
                          <td>{empleado.departamento_nombre || `Depto ${empleado.departamento}`}</td>
                          <td>Puesto {empleado.puesto}</td>
                          <td>Planta {empleado.planta}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-state">
                  <h4>👥 No se encontraron empleados</h4>
                  <p>No hay empleados disponibles para asignar a esta evaluación.</p>
                  <p>Verifica que existan empleados registrados en el sistema.</p>
                  <button onClick={cargarEmpleados} className="btn-primary">
                    🔄 Recargar Empleados
                  </button>
                </div>
              )}
            </div>
          )}

          {paso === 'tokens' && (
            <div className="tokens-section">
              <div className="section-header">
                <h3>Tokens Generados</h3>
                <button onClick={reiniciar} className="btn-secondary">
                  Nueva Asignación
                </button>
              </div>

              <div className="success-message">
                <h4>¡Evaluación asignada exitosamente!</h4>
                <p>Se han generado {tokensGenerados.length} tokens para los empleados seleccionados.</p>
              </div>

              <div className="tokens-table">
                <table>
                  <thead>
                    <tr>
                      <th>Empleado</th>
                      <th>Email</th>
                      <th>Token</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tokensGenerados.map((token, index) => (
                      <tr key={`generated-token-${token.empleado_id}-${token.token_generado}-${index}`}>
                        <td>{token.empleado_nombre} {token.empleado_apellido}</td>
                        <td>{token.empleado_email}</td>
                        <td className="token-cell">
                          <code>{token.token_generado}</code>
                        </td>
                        <td>
                          <button 
                            onClick={() => copiarToken(token.token_generado)}
                            className="btn-copy"
                          >
                            Copiar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {/* Vista de Evaluaciones Activas */}
      {vistaActiva === 'activas' && (
        <EvaluacionesActivas />
      )}

      {/* Vista de Tokens */}
      {vistaActiva === 'tokens' && (
        <div className="tokens-section">
          <div className="section-header">
            <h3>🔑 Gestión de Tokens de Acceso</h3>
            <p>Visualiza y gestiona todos los tokens de acceso generados para las evaluaciones</p>
          </div>

          <div className="tokens-info">
            <div className="info-card">
              <h4>📊 Estado de Tokens</h4>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-number">{tokensGenerados.length}</span>
                  <span className="stat-label">Tokens Generados</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{tokensGenerados.filter(t => !t.usado).length}</span>
                  <span className="stat-label">Sin Usar</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{tokensGenerados.filter(t => t.usado).length}</span>
                  <span className="stat-label">Completados</span>
                </div>
              </div>
            </div>
          </div>

          {tokensGenerados.length > 0 ? (
            <div className="tokens-table">
              <table>
                <thead>
                  <tr>
                    <th>Empleado</th>
                    <th>Email</th>
                    <th>Evaluación</th>
                    <th>Token</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {tokensGenerados.map((token, index) => (
                    <tr key={`token-${token.empleado_id}-${token.token_generado}-${index}`}>
                      <td>{token.empleado_nombre} {token.empleado_apellido}</td>
                      <td>{token.empleado_email}</td>
                      <td>{token.evaluacion_titulo || 'N/A'}</td>
                      <td className="token-cell">
                        <code>{token.token_generado}</code>
                      </td>
                      <td>
                        <span className={`status-badge ${token.usado ? 'completed' : 'pending'}`}>
                          {token.usado ? 'Completado' : 'Pendiente'}
                        </span>
                      </td>
                      <td>{token.fecha_asignacion ? new Date(token.fecha_asignacion).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <button 
                          onClick={() => copiarToken(token.token_generado)}
                          className="btn-copy"
                        >
                          Copiar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="empty-state">
              <h4>📝 No hay tokens generados</h4>
              <p>Los tokens aparecerán aquí una vez que asignes evaluaciones a los empleados.</p>
              <button 
                onClick={() => setVistaActiva('evaluaciones')}
                className="btn-primary"
              >
                Asignar Primera Evaluación
              </button>
            </div>
          )}
        </div>
      )}

      <style>{`
        .asignacion-evaluaciones-dashboard {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
        }

        .dashboard-header {
          margin-bottom: 30px;
        }

        .dashboard-header h2 {
          color: #2c3e50;
          margin-bottom: 10px;
        }

        .tabs-navigation {
          display: flex;
          gap: 10px;
          margin-bottom: 30px;
          border-bottom: 2px solid #e9ecef;
        }

        .tab-button {
          padding: 12px 20px;
          border: none;
          background: transparent;
          color: #6c757d;
          cursor: pointer;
          border-bottom: 3px solid transparent;
          transition: all 0.3s ease;
          font-weight: 500;
        }

        .tab-button:hover {
          color: #007bff;
          background: #f8f9fa;
        }

        .tab-button.active {
          color: #007bff;
          border-bottom-color: #007bff;
          background: #f8f9fa;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 20px;
          flex-wrap: wrap;
          gap: 15px;
        }

        .section-header h3 {
          margin: 0;
          color: #2c3e50;
        }

        .section-header p {
          margin: 5px 0 0 0;
          color: #6c757d;
          font-size: 0.9rem;
        }

        .actions-header {
          display: flex;
          gap: 10px;
        }

        .evaluacion-nom030 {
          border-left: 4px solid #28a745;
        }

        .evaluacion-nom035 {
          border-left: 4px solid #dc3545;
        }

        .evaluacion-360 {
          border-left: 4px solid #6f42c1;
        }

        .evaluacion-360-personal {
          border-left: 4px solid #6f42c1;
          background: linear-gradient(135deg, #f8f9ff 0%, #e8d5ff 100%);
        }

        .badge-nom-030 {
          background: #d4edda;
          color: #155724;
        }

        .badge-nom-035 {
          background: #f8d7da;
          color: #721c24;
        }

        .badge-container {
          display: flex;
          gap: 5px;
          flex-wrap: wrap;
        }

        .badge-360 {
          background: #e8d5ff;
          color: #6f42c1;
        }

        .empty-state {
          text-align: center;
          padding: 60px 20px;
          background: #f8f9fa;
          border-radius: 8px;
          border: 2px dashed #dee2e6;
        }

        .empty-state h4 {
          color: #6c757d;
          margin-bottom: 15px;
        }

        .empty-state p {
          color: #868e96;
          margin-bottom: 20px;
        }

        .empty-actions {
          margin-top: 25px;
        }

        .help-text {
          font-size: 0.85rem;
          color: #6c757d;
          font-style: italic;
          margin-top: 10px;
        }

        .tokens-info {
          margin-bottom: 30px;
        }

        .info-card {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          border: 1px solid #dee2e6;
        }

        .info-card h4 {
          margin: 0 0 15px 0;
          color: #2c3e50;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 20px;
        }

        .stat-item {
          text-align: center;
        }

        .stat-number {
          display: block;
          font-size: 2rem;
          font-weight: bold;
          color: #007bff;
          margin-bottom: 5px;
        }

        .stat-label {
          font-size: 0.85rem;
          color: #6c757d;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .status-badge {
          padding: 3px 8px;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 500;
          text-transform: uppercase;
        }

        .status-badge.completed {
          background: #d4edda;
          color: #155724;
        }

        .status-badge.pending {
          background: #fff3cd;
          color: #856404;
        }

        .filtros-tipo {
          display: flex;
          gap: 10px;
        }

        .btn-filtro {
          padding: 8px 16px;
          border: 1px solid #ddd;
          background: white;
          color: #6c757d;
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .btn-filtro:hover {
          background: #f8f9fa;
        }

        .btn-filtro.active {
          background: #007bff;
          color: white;
          border-color: #007bff;
        }

        .evaluaciones-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }

        .evaluacion-card {
          background: white;
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 20px;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
        }

        .evaluacion-card:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          transform: translateY(-2px);
        }

        .evaluacion-card.normativa {
          border-left: 4px solid #28a745;
        }

        .evaluacion-card.personalizada {
          border-left: 4px solid #007bff;
        }

        .evaluacion-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 10px;
        }

        .evaluacion-header h4 {
          margin: 0;
          color: #2c3e50;
          flex: 1;
        }

        .badge {
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: bold;
          text-transform: uppercase;
        }

        .badge-normativa {
          background: #d4edda;
          color: #155724;
        }

        .badge-personalizada {
          background: #d1ecf1;
          color: #0c5460;
        }

        .evaluacion-info {
          display: flex;
          flex-direction: column;
          gap: 5px;
          margin: 10px 0;
        }

        .evaluacion-info small {
          color: #6c757d;
        }

        .evaluacion-meta {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 15px;
          padding-top: 15px;
          border-top: 1px solid #eee;
        }

        .estado {
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .estado.activa {
          background: #d4edda;
          color: #155724;
        }

        .fecha {
          font-size: 0.8rem;
          color: #6c757d;
        }

        .filtros-section {
          margin-bottom: 20px;
          padding: 15px;
          background: #f8f9fa;
          border-radius: 6px;
        }

        .filtros-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 10px;
          margin-top: 10px;
        }

        .filtros-grid input {
          padding: 8px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
        }

        .empleados-controls {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          gap: 15px;
        }

        .seleccion-count {
          color: #6c757d;
          font-weight: 500;
        }

        .empleados-table, .tokens-table {
          background: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .empleados-table table, .tokens-table table {
          width: 100%;
          border-collapse: collapse;
        }

        .empleados-table th, .tokens-table th,
        .empleados-table td, .tokens-table td {
          padding: 12px;
          text-align: left;
          border-bottom: 1px solid #eee;
        }

        .empleados-table th, .tokens-table th {
          background: #f8f9fa;
          font-weight: 600;
          color: #495057;
        }

        .token-cell code {
          background: #f8f9fa;
          padding: 4px 8px;
          border-radius: 4px;
          font-family: monospace;
          font-size: 0.9rem;
        }

        .success-message {
          background: #d4edda;
          border: 1px solid #c3e6cb;
          color: #155724;
          padding: 15px;
          border-radius: 6px;
          margin-bottom: 20px;
        }

        .success-message h4 {
          margin: 0 0 5px 0;
        }

        .coming-soon {
          text-align: center;
          padding: 40px 20px;
          background: #f8f9fa;
          border-radius: 8px;
          margin-top: 20px;
        }

        .no-evaluaciones, .no-tokens {
          text-align: center;
          padding: 40px 20px;
          color: #6c757d;
        }

        .status.activo {
          background: #d4edda;
          color: #155724;
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 0.8rem;
        }

        .status.usado {
          background: #f8d7da;
          color: #721c24;
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 0.8rem;
        }

        .loading {
          text-align: center;
          padding: 40px 20px;
          color: #6c757d;
        }

        .btn-primary {
          background: #007bff;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 500;
        }

        .btn-primary:hover {
          background: #0056b3;
        }

        .btn-primary:disabled {
          background: #6c757d;
          cursor: not-allowed;
        }

        .btn-secondary {
          background: #6c757d;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 500;
        }

        .btn-secondary:hover {
          background: #545b62;
        }

        .btn-outline {
          background: transparent;
          color: #007bff;
          border: 1px solid #007bff;
          padding: 10px 20px;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 500;
        }

        .btn-outline:hover {
          background: #007bff;
          color: white;
        }

        .btn-copy {
          background: #28a745;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.8rem;
        }

        .btn-copy:hover {
          background: #218838;
        }
      `}</style>
    </div>
  );
};

export default AsignacionEvaluacionesDashboard;
