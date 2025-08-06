import React, { useState, useEffect } from 'react';
import './AsignacionEvaluaciones.css';

interface Empleado {
  id: number;
  nombre: string;
  apellido: string;
  numero_empleado?: string;
  departamento_nombre?: string;
  puesto_nombre?: string;
  planta_nombre?: string;
  empresa_nombre?: string;
  activo: boolean;
}

interface Departamento {
  id: number;
  nombre: string;
}

interface Puesto {
  id: number;
  nombre: string;
}

interface FiltrosDisponibles {
  departamentos: Departamento[];
  puestos: Puesto[];
  plantas: any[];
  total_empleados: number;
}

interface EvaluacionOficial {
  id: number;
  nombre: string;
  descripcion: string;
  tipo_norma: string;
  vigente: boolean;
}

interface EmpleadoConToken {
  empleado_id: number;
  nombre_completo: string;
  token: string;
  numero_empleado?: string;
}

interface AsignacionRespuesta {
  success: boolean;
  message: string;
  asignacion_id: number;
  nombre_asignacion: string;
  evaluacion: string;
  tipo_norma: string;
  fecha_inicio: string;
  fecha_fin: string;
  empleados_asignados: EmpleadoConToken[];
  total_empleados: number;
}

interface AsignacionEvaluacionesProps {
  userData?: {
    nivel_usuario: string;
    empresa_id?: number;
    planta_id?: number;
  };
}

const AsignacionEvaluaciones: React.FC<AsignacionEvaluacionesProps> = ({ userData }) => {
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [filtrosDisponibles, setFiltrosDisponibles] = useState<FiltrosDisponibles | null>(null);
  const [evaluacionesDisponibles, setEvaluacionesDisponibles] = useState<EvaluacionOficial[]>([]);
  const [empleadosSeleccionados, setEmpleadosSeleccionados] = useState<number[]>([]);
  const [evaluacionSeleccionada, setEvaluacionSeleccionada] = useState<number | null>(null);
  const [duracionDias, setDuracionDias] = useState<number>(7);
  const [nombreAsignacion, setNombreAsignacion] = useState<string>('');
  const [filtroActual, setFiltroActual] = useState<{
    departamento?: number;
    puesto?: number;
    busqueda?: string;
  }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tokensGenerados, setTokensGenerados] = useState<EmpleadoConToken[] | null>(null);
  const [mostrarTokens, setMostrarTokens] = useState(false);

  // Obtener token de autenticación
  const getAuthToken = () => {
    return localStorage.getItem('token') || '';
  };

  // Headers para las peticiones API
  const getHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Token ${getAuthToken()}`
  });

  useEffect(() => {
    cargarDatosIniciales();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const cargarDatosIniciales = async () => {
    setLoading(true);
    try {
      await Promise.all([
        cargarEmpleados(),
        cargarFiltrosDisponibles(),
        cargarEvaluacionesDisponibles()
      ]);
    } catch (error) {
      console.error('Error cargando datos iniciales:', error);
      setError('Error al cargar los datos iniciales');
    } finally {
      setLoading(false);
    }
  };

  const cargarEmpleados = async () => {
    try {
      const response = await fetch('/api/evaluaciones/asignacion/empleados/', {
        headers: getHeaders()
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('📋 Empleados cargados:', data);
      setEmpleados(data.results || data);
    } catch (error) {
      console.error('Error cargando empleados:', error);
      setError('Error al cargar empleados');
    }
  };

  const cargarFiltrosDisponibles = async () => {
    try {
      const response = await fetch('/api/evaluaciones/asignacion/empleados/filtros_disponibles/', {
        headers: getHeaders()
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('🔍 Filtros disponibles:', data);
      setFiltrosDisponibles(data);
    } catch (error) {
      console.error('Error cargando filtros:', error);
    }
  };

  const cargarEvaluacionesDisponibles = async () => {
    try {
      const response = await fetch('/api/evaluaciones/oficial/evaluaciones-oficiales/', {
        headers: getHeaders()
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      // Filtrar solo evaluaciones vigentes
      const evaluacionesVigentes = (data.results || data).filter((evaluacion: EvaluacionOficial) => evaluacion.vigente);
      console.log('📊 Evaluaciones disponibles:', evaluacionesVigentes);
      setEvaluacionesDisponibles(evaluacionesVigentes);
    } catch (error) {
      console.error('Error cargando evaluaciones:', error);
      setError('Error al cargar evaluaciones disponibles');
    }
  };

  const aplicarFiltros = async () => {
    try {
      let url = '/api/evaluaciones/asignacion/empleados/';
      const params = new URLSearchParams();

      if (filtroActual.departamento) {
        url = '/api/evaluaciones/asignacion/empleados/por_departamento/';
        params.append('departamento_id', filtroActual.departamento.toString());
      }

      if (filtroActual.puesto) {
        url = '/api/evaluaciones/asignacion/empleados/por_puesto/';
        params.append('puesto_id', filtroActual.puesto.toString());
      }

      if (filtroActual.busqueda) {
        params.append('search', filtroActual.busqueda);
      }

      if (params.toString()) {
        url += `?${params.toString()}`;
      }

      const response = await fetch(url, {
        headers: getHeaders()
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setEmpleados(data.results || data);
    } catch (error) {
      console.error('Error aplicando filtros:', error);
      setError('Error al filtrar empleados');
    }
  };

  useEffect(() => {
    if (filtroActual.departamento || filtroActual.puesto || filtroActual.busqueda) {
      aplicarFiltros();
    } else if (empleados.length === 0) {
      cargarEmpleados();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filtroActual]);

  const toggleSeleccionEmpleado = (empleadoId: number) => {
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
      setEmpleadosSeleccionados(empleados.map(emp => emp.id));
    }
  };

  const crearAsignacion = async () => {
    if (!evaluacionSeleccionada || empleadosSeleccionados.length === 0) {
      setError('Debe seleccionar una evaluación y al menos un empleado');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const fechaActual = new Date().toLocaleDateString('es-MX');
      const nombreFinal = nombreAsignacion.trim() || `Evaluación ${fechaActual}`;

      const payload = {
        evaluacion_id: evaluacionSeleccionada,
        empleados_ids: empleadosSeleccionados,
        duracion_dias: duracionDias,
        nombre_asignacion: nombreFinal
      };

      console.log('🚀 Enviando asignación:', payload);

      const response = await fetch('/api/evaluaciones/asignacion/asignaciones/crear_asignacion/', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Error ${response.status}: ${response.statusText}`);
      }

      const resultado: AsignacionRespuesta = await response.json();
      
      console.log('✅ Asignación creada exitosamente:', resultado);
      
      // Mostrar tokens generados
      setTokensGenerados(resultado.empleados_asignados);
      setMostrarTokens(true);
      
      // Limpiar formulario
      setEmpleadosSeleccionados([]);
      setEvaluacionSeleccionada(null);
      setNombreAsignacion('');
      setDuracionDias(7);

    } catch (error: any) {
      console.error('❌ Error creando asignación:', error);
      setError(error.message || 'Error al crear la asignación');
    } finally {
      setLoading(false);
    }
  };

  const exportarTokens = () => {
    if (!tokensGenerados) return;

    const csvContent = "data:text/csv;charset=utf-8," 
      + "Empleado,Token,Numero_Empleado\n"
      + tokensGenerados.map(emp => 
          `"${emp.nombre_completo}","${emp.token}","${emp.numero_empleado || 'N/A'}"`
        ).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `tokens_evaluacion_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading && empleados.length === 0) {
    return (
      <div className="asignacion-evaluaciones loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Cargando datos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="asignacion-evaluaciones">
      <div className="asignacion-header">
        <h2>🎯 Asignación de Evaluaciones</h2>
        <p>Asigna evaluaciones NOM-030 y NOM-035 a empleados y genera tokens de acceso</p>
        
        {userData && (
          <div className="usuario-info">
            <span>Usuario: {userData.nivel_usuario}</span>
            {userData.empresa_id && <span>Empresa ID: {userData.empresa_id}</span>}
            {userData.planta_id && <span>Planta ID: {userData.planta_id}</span>}
          </div>
        )}
      </div>

      {error && (
        <div className="error-message">
          <span>❌ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Modal de Tokens Generados */}
      {mostrarTokens && tokensGenerados && (
        <div className="modal-overlay">
          <div className="modal-tokens">
            <div className="modal-header">
              <h3>🔑 Tokens de Acceso Generados</h3>
              <button onClick={() => setMostrarTokens(false)}>✕</button>
            </div>
            <div className="modal-body">
              <p><strong>¡Evaluación asignada exitosamente!</strong></p>
              <p>Se han generado {tokensGenerados.length} tokens de acceso únicos:</p>
              <div className="tokens-list">
                {tokensGenerados.map((emp, index) => (
                  <div key={index} className="token-item">
                    <div className="token-empleado">
                      <strong>{emp.nombre_completo}</strong>
                    </div>
                    <div className="token-code">
                      Token: <span className="token-highlight">{emp.token}</span>
                    </div>
                    <div className="token-numero">
                      #{emp.numero_empleado || 'N/A'}
                    </div>
                  </div>
                ))}
              </div>
              <div className="token-instrucciones">
                <p><strong>📋 Instrucciones para los empleados:</strong></p>
                <ol>
                  <li>Ingresar a la página principal del sistema</li>
                  <li>Buscar la sección "Responder Evaluación"</li>
                  <li>Introducir su token personal</li>
                  <li>Completar la evaluación asignada</li>
                </ol>
              </div>
              <div className="modal-actions">
                <button onClick={exportarTokens} className="btn-export">
                  📥 Exportar CSV
                </button>
                <button onClick={() => setMostrarTokens(false)} className="btn-close">
                  ✅ Entendido
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="configuracion-evaluacion">
        <h3>⚙️ Configuración</h3>
        <div className="config-grid">
          <div className="config-item">
            <label>Evaluación:</label>
            <select 
              value={evaluacionSeleccionada || ''} 
              onChange={(e) => setEvaluacionSeleccionada(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">Seleccionar evaluación...</option>
              {evaluacionesDisponibles.map(evaluacion => (
                <option key={evaluacion.id} value={evaluacion.id}>
                  {evaluacion.nombre} ({evaluacion.tipo_norma})
                </option>
              ))}
            </select>
          </div>
          
          <div className="config-item">
            <label>Duración (días):</label>
            <input 
              type="number" 
              value={duracionDias}
              onChange={(e) => setDuracionDias(Number(e.target.value))}
              min="1"
              max="365"
            />
          </div>
          
          <div className="config-item">
            <label>Nombre de asignación:</label>
            <input 
              type="text" 
              value={nombreAsignacion}
              onChange={(e) => setNombreAsignacion(e.target.value)}
              placeholder="Opcional - se generará automáticamente"
            />
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="filtros-empleados">
        <h3>🔍 Filtros</h3>
        <div className="filtros-grid">
          <div className="filtro-item">
            <label>Buscar:</label>
            <input
              type="text"
              placeholder="Nombre, apellido o número..."
              value={filtroActual.busqueda || ''}
              onChange={(e) => setFiltroActual(prev => ({ ...prev, busqueda: e.target.value }))}
            />
          </div>
          
          {filtrosDisponibles && (
            <>
              <div className="filtro-item">
                <label>Departamento:</label>
                <select
                  value={filtroActual.departamento || ''}
                  onChange={(e) => setFiltroActual(prev => ({ 
                    ...prev, 
                    departamento: e.target.value ? Number(e.target.value) : undefined 
                  }))}
                >
                  <option value="">Todos los departamentos</option>
                  {filtrosDisponibles.departamentos.map(dep => (
                    <option key={dep.id} value={dep.id}>{dep.nombre}</option>
                  ))}
                </select>
              </div>

              <div className="filtro-item">
                <label>Puesto:</label>
                <select
                  value={filtroActual.puesto || ''}
                  onChange={(e) => setFiltroActual(prev => ({ 
                    ...prev, 
                    puesto: e.target.value ? Number(e.target.value) : undefined 
                  }))}
                >
                  <option value="">Todos los puestos</option>
                  {filtrosDisponibles.puestos.map(puesto => (
                    <option key={puesto.id} value={puesto.id}>{puesto.nombre}</option>
                  ))}
                </select>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Lista de Empleados */}
      <div className="empleados-section">
        <div className="empleados-header">
          <h3>👥 Empleados ({empleadosSeleccionados.length}/{empleados.length} seleccionados)</h3>
          <button onClick={seleccionarTodos} className="btn-toggle-all">
            {empleadosSeleccionados.length === empleados.length ? 
              '❌ Deseleccionar Todos' : 
              '✅ Seleccionar Todos'
            }
          </button>
        </div>

        {loading ? (
          <div className="loading-empleados">
            <div className="spinner"></div>
            <p>Cargando empleados...</p>
          </div>
        ) : empleados.length === 0 ? (
          <div className="no-empleados">
            <p>📭 No se encontraron empleados</p>
            <p>Verifica que tu empresa tenga empleados registrados.</p>
          </div>
        ) : (
          <div className="empleados-grid">
            {empleados.map(empleado => (
              <div 
                key={empleado.id}
                className={`empleado-card ${empleadosSeleccionados.includes(empleado.id) ? 'selected' : ''}`}
                onClick={() => toggleSeleccionEmpleado(empleado.id)}
              >
                <div className="empleado-checkbox">
                  <input 
                    type="checkbox"
                    checked={empleadosSeleccionados.includes(empleado.id)}
                    onChange={() => toggleSeleccionEmpleado(empleado.id)}
                  />
                </div>
                <div className="empleado-info">
                  <div className="empleado-nombre">
                    {empleado.nombre} {empleado.apellido}
                  </div>
                  <div className="empleado-detalles">
                    <span>#{empleado.numero_empleado || 'Sin número'}</span>
                    <span>📂 {empleado.departamento_nombre || 'Sin departamento'}</span>
                    <span>💼 {empleado.puesto_nombre || 'Sin puesto'}</span>
                  </div>
                  {empleado.planta_nombre && (
                    <div className="empleado-planta">🏭 {empleado.planta_nombre}</div>
                  )}
                  {empleado.empresa_nombre && (
                    <div className="empleado-empresa">🏢 {empleado.empresa_nombre}</div>
                  )}
                </div>
                <div className="empleado-status">
                  {empleado.activo ? '✅ Activo' : '❌ Inactivo'}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Botón de Asignación */}
      <div className="asignacion-actions">
        <button 
          onClick={crearAsignacion}
          className="btn-asignar-principal"
          disabled={!evaluacionSeleccionada || empleadosSeleccionados.length === 0 || loading}
        >
          {loading ? 
            '⏳ Procesando...' : 
            `🎯 Asignar a ${empleadosSeleccionados.length} Empleados y Generar Tokens`
          }
        </button>
        
        {empleadosSeleccionados.length > 0 && evaluacionSeleccionada && (
          <div className="asignacion-preview">
            <p>
              ✅ Se asignará <strong>{evaluacionesDisponibles.find(e => e.id === evaluacionSeleccionada)?.nombre}</strong> 
              {' '}a <strong>{empleadosSeleccionados.length}</strong> empleados por <strong>{duracionDias}</strong> días.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AsignacionEvaluaciones;