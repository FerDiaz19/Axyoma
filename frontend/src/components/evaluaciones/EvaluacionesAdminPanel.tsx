import React, { useState, useEffect, useCallback, useRef } from 'react';
import { evaluacionesOficialesAPI } from '../../services/evaluacionesOficialesAPI';
import evaluacionesAPI from '../../services/evaluacionesService';
import { getEmpleados, type Empleado } from '../../services/empleadoService';
import './EvaluacionesAdminPanel.css';

interface EvaluacionOficial {
  id: number;
  nombre: string;
  descripcion: string;
  tipo_norma: string;
  vigente: boolean;
  total_preguntas: number;
}

interface AsignacionEmpleado {
  asignacion_empleado_id: number;
  empleado: {
    id: number;
    nombre_completo: string;
    numero_empleado: string;
    departamento_nombre: string;
    puesto_nombre: string;
  };
  token_acceso: string;
  status: string;
  fecha_asignacion: string;
  fecha_completado?: string;
  resultado?: {
    puntaje_total: number;
    aprobado: boolean;
    porcentaje_correctas: number;
  };
}

interface AsignacionBase {
  asignacion_id: number;
  evaluacion: {
    titulo: string;
    tipo_normativa: string;
  };
  fecha_inicio: string;
  fecha_fin: string;
  status: boolean;
  asignaciones_empleado: AsignacionEmpleado[];
  total_empleados: number;
  completadas: number;
  pendientes: number;
  expiradas: number;
  desactivadas: number;
}

interface EvaluacionesAdminPanelProps {
  userData: {
    nivel_usuario: string;
    empresa_id?: number;
    planta_id?: number;
    usuario?: string;
    nombre_planta?: string;
  };
}

// Componente simple y compacto para las tarjetas de asignación
const AsignacionCard: React.FC<{
  asignacion: AsignacionBase;
  isExpanded: boolean;
  onToggleExpanded: (id: number) => void;
  onGestionarAsignacion: (id: number, accion: 'activar' | 'desactivar') => void;
  onExportarTokens: (asignacion: AsignacionBase) => void;
}> = ({ asignacion, isExpanded, onToggleExpanded, onGestionarAsignacion, onExportarTokens }) => {

  return (
    <div className="asignacion-card-compact">
      <div className="card-compact-header">
        <div className="evaluacion-title">
          <h4>{asignacion.evaluacion.titulo}</h4>
          <span className="evaluacion-dates">
            {new Date(asignacion.fecha_inicio).toLocaleDateString()} - {new Date(asignacion.fecha_fin).toLocaleDateString()}
          </span>
        </div>
        
        <div className="status-and-progress">
          <span className={`status-compact ${asignacion.status ? 'activa' : 'inactiva'}`}>
            {asignacion.status ? '🟢' : '🔴'}
          </span>
          <div className="progress-mini">
            <div 
              className="progress-fill-mini"
              style={{ 
                width: `${asignacion.total_empleados > 0 ? (asignacion.completadas / asignacion.total_empleados) * 100 : 0}%` 
              }}
            ></div>
          </div>
          <span className="progress-text-mini">
            {asignacion.completadas}/{asignacion.total_empleados}
          </span>
        </div>
      </div>
      
      <div className="card-compact-stats">
        <div className="stat-compact completadas">
          <span className="stat-number-mini">{asignacion.completadas}</span>
          <span className="stat-label-mini">✅</span>
        </div>
        <div className="stat-compact pendientes">
          <span className="stat-number-mini">{asignacion.pendientes}</span>
          <span className="stat-label-mini">⏳</span>
        </div>
        {asignacion.expiradas > 0 && (
          <div className="stat-compact expiradas">
            <span className="stat-number-mini">{asignacion.expiradas}</span>
            <span className="stat-label-mini">⏰</span>
          </div>
        )}
        {asignacion.desactivadas > 0 && (
          <div className="stat-compact desactivadas">
            <span className="stat-number-mini">{asignacion.desactivadas}</span>
            <span className="stat-label-mini">🚫</span>
          </div>
        )}
      </div>
      
      <div className="card-compact-actions">
        <button 
          className="btn-compact btn-info-compact"
          onClick={() => onToggleExpanded(asignacion.asignacion_id)}
          title={isExpanded ? 'Ocultar Empleados' : 'Ver Empleados'}
        >
          {isExpanded ? '🔼' : '🔽'}
        </button>
        
        <button 
          className="btn-compact btn-secondary-compact"
          onClick={() => onExportarTokens(asignacion)}
          title="Exportar Tokens"
        >
          📥
        </button>
        
        {asignacion.status ? (
          <button 
            className="btn-compact btn-warning-compact"
            onClick={() => onGestionarAsignacion(asignacion.asignacion_id, 'desactivar')}
            title="Desactivar"
          >
            ⏸️
          </button>
        ) : (
          <button 
            className="btn-compact btn-success-compact"
            onClick={() => onGestionarAsignacion(asignacion.asignacion_id, 'activar')}
            title="Activar"
          >
            ▶️
          </button>
        )}
      </div>
      
      {/* Detalles expandibles - más compactos */}
      {isExpanded && (
        <div className="empleados-detalle-compact">
          <div className="empleados-grid-compact">
            {asignacion.asignaciones_empleado.map(ae => (
              <div key={ae.asignacion_empleado_id} className="empleado-compact">
                <span className="empleado-nombre-compact">
                  {ae.empleado.nombre_completo}
                </span>
                <span className={`empleado-status-compact ${ae.status.toLowerCase()}`}>
                  {ae.status === 'Completada' || ae.status === 'Terminada' ? '✅' :
                   ae.status === 'Pendiente' || ae.status === 'Activa' ? '⏳' :
                   ae.status === 'Expirada' ? '⏰' : '🚫'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const EvaluacionesAdminPanel: React.FC<EvaluacionesAdminPanelProps> = ({ userData }) => {
  const [activeTab, setActiveTab] = useState<'disponibles' | 'asignadas' | 'resultados'>('disponibles');
  const [evaluacionesOficiales, setEvaluacionesOficiales] = useState<EvaluacionOficial[]>([]);
  const [asignacionesActivas, setAsignacionesActivas] = useState<AsignacionBase[]>([]);
  const [resultadosEvaluaciones, setResultadosEvaluaciones] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Estados para modal de asignación
  const [modalAsignacionAbierto, setModalAsignacionAbierto] = useState(false);
  const [evaluacionParaAsignar, setEvaluacionParaAsignar] = useState<EvaluacionOficial | null>(null);
  const [empleadosDisponibles, setEmpleadosDisponibles] = useState<Empleado[]>([]);
  const [empleadosSeleccionados, setEmpleadosSeleccionados] = useState<number[]>([]);
  const [fechaVencimiento, setFechaVencimiento] = useState('');
  
  // Estado para expandir detalles de asignaciones
  const [asignacionesExpandidas, setAsignacionesExpandidas] = useState<Set<number>>(new Set());

  // Ref para mantener posición de scroll
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const isAdminEmpresa = userData.nivel_usuario === 'admin_empresa';
  const isAdminPlanta = userData.nivel_usuario === 'admin_planta';

  const cargarEvaluacionesOficiales = useCallback(async () => {
    try {
      const evaluaciones = await evaluacionesOficialesAPI.getEvaluaciones();
      // Los datos ya vienen mapeados desde la API
      const evaluacionesConVigencia = evaluaciones.map((ev) => ({
        ...ev,
        vigente: true, // Por defecto todas las evaluaciones oficiales están vigentes
        total_preguntas: 0 // Se puede obtener dinámicamente si es necesario
      }));
      setEvaluacionesOficiales(evaluacionesConVigencia);
    } catch (error) {
      console.error('Error cargando evaluaciones oficiales:', error);
      setEvaluacionesOficiales([]);
    }
  }, []);

  const cargarAsignacionesActivas = useCallback(async () => {
    try {
      // Cargar asignaciones y evaluaciones en paralelo
      const [asignacionesResponse, evaluacionesResponse] = await Promise.all([
        evaluacionesAPI.getAsignaciones(),
        evaluacionesOficialesAPI.getEvaluaciones()
      ]);
      
      const asignaciones = asignacionesResponse.data || [];
      const evaluaciones = evaluacionesResponse || [];
      
      // Crear un mapa de evaluaciones para acceso rápido
      const evaluacionesMap = new Map(evaluaciones.map(ev => [ev.id, ev]));
      
      // Filtrar según el nivel de usuario
      let asignacionesFiltradas = asignaciones;
      
      if (isAdminPlanta && userData.planta_id) {
        // Admin planta solo ve asignaciones de empleados de su planta
        asignacionesFiltradas = asignaciones.filter((asignacion: any) =>
          asignacion.asignaciones_empleado && asignacion.asignaciones_empleado.some((ae: any) => 
            ae.empleado_planta_id === userData.planta_id
          )
        );
      } else if (isAdminEmpresa && userData.empresa_id) {
        // Admin empresa ve todas las asignaciones de empleados de su empresa
        asignacionesFiltradas = asignaciones.filter((asignacion: any) =>
          asignacion.asignaciones_empleado && asignacion.asignaciones_empleado.some((ae: any) => 
            ae.empleado_empresa_id === userData.empresa_id
          )
        );
      }

      // Mapear al formato esperado
      const asignacionesMapeadas = asignacionesFiltradas.map((asignacion: any) => {
        const evaluacionData = evaluacionesMap.get(asignacion.evaluacion);
        
        return {
          asignacion_id: asignacion.asignacion_id,
          evaluacion: {
            titulo: evaluacionData?.nombre || `Evaluación ID: ${asignacion.evaluacion}`,
            tipo_normativa: evaluacionData?.tipo_norma || 'N/A'
          },
          fecha_inicio: asignacion.fecha_inicio,
          fecha_fin: asignacion.fecha_fin,
          status: asignacion.status,
          asignaciones_empleado: asignacion.asignaciones_empleado.map((ae: any) => ({
            asignacion_empleado_id: ae.asignacion_empleado_id,
            empleado: {
              id: ae.empleado,
              nombre_completo: ae.empleado_nombre,
              numero_empleado: ae.empleado_numero || '',
              departamento_nombre: ae.empleado_departamento,
              puesto_nombre: ae.empleado_puesto
            },
            token_acceso: ae.token_acceso,
            status: ae.status,
            fecha_asignacion: asignacion.fecha_inicio,
            fecha_completado: ae.fecha_completado
          })),
          total_empleados: asignacion.asignaciones_empleado?.length || 0,
          completadas: asignacion.asignaciones_empleado?.filter((ae: any) => 
            ae.status === 'Completada' || ae.status === 'Terminada'
          ).length || 0,
          pendientes: asignacion.asignaciones_empleado?.filter((ae: any) => 
            ae.status === 'Pendiente' || ae.status === 'Activa'
          ).length || 0,
          expiradas: asignacion.asignaciones_empleado?.filter((ae: any) => 
            ae.status === 'Expirada'
          ).length || 0,
          desactivadas: asignacion.asignaciones_empleado?.filter((ae: any) => 
            ae.status === 'Desactivada'
          ).length || 0
        };
      });

      setAsignacionesActivas(asignacionesMapeadas);
    } catch (error) {
      console.error('Error cargando asignaciones:', error);
      setAsignacionesActivas([]);
    }
  }, [isAdminPlanta, userData.planta_id, isAdminEmpresa, userData.empresa_id]);

  const cargarResultados = useCallback(async () => {
    try {
      const response = await evaluacionesAPI.getResultadosEvaluacion();
      const resultados = response.data || [];
      setResultadosEvaluaciones(resultados);
    } catch (error) {
      console.error('Error cargando resultados:', error);
      setResultadosEvaluaciones([]);
    }
  }, []);

  const cargarDatosIniciales = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      switch (activeTab) {
        case 'disponibles':
          await cargarEvaluacionesOficiales();
          break;
        case 'asignadas':
          await cargarAsignacionesActivas();
          break;
        case 'resultados':
          await cargarResultados();
          break;
      }
    } catch (error: any) {
      console.error('Error cargando datos:', error);
      setError(error.message || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  }, [activeTab, cargarEvaluacionesOficiales, cargarAsignacionesActivas, cargarResultados]);

  useEffect(() => {
    cargarDatosIniciales();
  }, [cargarDatosIniciales]);

  const abrirModalAsignacion = async (evaluacion: EvaluacionOficial) => {
    try {
      setEvaluacionParaAsignar(evaluacion);
      setModalAsignacionAbierto(true);
      
      // Cargar empleados disponibles
      const empleados = await getEmpleados();
      setEmpleadosDisponibles(empleados.filter(emp => emp.status));
      
      // Establecer fecha de vencimiento por defecto (30 días)
      const fechaDefecto = new Date();
      fechaDefecto.setDate(fechaDefecto.getDate() + 30);
      setFechaVencimiento(fechaDefecto.toISOString().split('T')[0]);
      
    } catch (error) {
      console.error('Error al cargar empleados:', error);
      alert('Error al cargar la lista de empleados');
    }
  };

  const toggleEmpleadoSeleccionado = (empleadoId: number) => {
    setEmpleadosSeleccionados(prev => {
      if (prev.includes(empleadoId)) {
        return prev.filter(id => id !== empleadoId);
      } else {
        return [...prev, empleadoId];
      }
    });
  };

  const seleccionarTodosEmpleados = () => {
    if (empleadosSeleccionados.length === empleadosDisponibles.length) {
      setEmpleadosSeleccionados([]);
    } else {
      setEmpleadosSeleccionados(empleadosDisponibles.map(emp => emp.empleado_id));
    }
  };

  const cerrarModalAsignacion = () => {
    setModalAsignacionAbierto(false);
    setEvaluacionParaAsignar(null);
    setEmpleadosSeleccionados([]);
    setEmpleadosDisponibles([]);
  };

  const enviarAsignaciones = async () => {
    if (!evaluacionParaAsignar || empleadosSeleccionados.length === 0) {
      alert('Debes seleccionar al menos un empleado');
      return;
    }

    try {
      setLoading(true);
      
      const fechaInicio = new Date().toISOString().split('T')[0];
      
      const datosAsignacion = {
        evaluacion: evaluacionParaAsignar.id,
        fecha_inicio: fechaInicio,
        fecha_fin: fechaVencimiento,
        status: true
      };

      const response = await evaluacionesAPI.createAsignacion(datosAsignacion);
      
      // Ahora asignar empleados a esta asignación
      if (response.data.asignacion_id) {
        await evaluacionesAPI.asignarEmpleados(response.data.asignacion_id, {
          empleado_ids: empleadosSeleccionados
        });
      }
      
      alert(`Evaluación "${evaluacionParaAsignar.nombre}" asignada exitosamente a ${empleadosSeleccionados.length} empleados`);
      
      // Cerrar modal y recargar datos
      cerrarModalAsignacion();
      if (activeTab === 'asignadas') {
        await cargarAsignacionesActivas();
      }
      
    } catch (error: any) {
      console.error('Error al crear asignaciones:', error);
      alert(`Error al asignar evaluación: ${error.message || 'Error desconocido'}`);
    } finally {
      setLoading(false);
    }
  };

  const toggleAsignacionExpandida = useCallback((asignacionId: number) => {
    setAsignacionesExpandidas(prev => {
      const nuevas = new Set(prev);
      if (nuevas.has(asignacionId)) {
        nuevas.delete(asignacionId);
      } else {
        nuevas.add(asignacionId);
      }
      return nuevas;
    });
  }, []);

  const gestionarAsignacion = async (asignacionId: number, accion: 'activar' | 'desactivar') => {
    try {
      if (accion === 'activar') {
        await evaluacionesAPI.activarAsignacion(asignacionId);
      } else {
        await evaluacionesAPI.desactivarAsignacion(asignacionId);
      }
      
      await cargarAsignacionesActivas(); // Recargar datos
      
    } catch (error: any) {
      console.error(`Error al ${accion} asignación:`, error);
      alert(`Error al ${accion} la asignación: ${error.message}`);
    }
  };

  const exportarTokens = useCallback((asignacion: AsignacionBase) => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Empleado,Token,Numero_Empleado,Departamento,Puesto,Estado\n"
      + asignacion.asignaciones_empleado.map(ae => 
          `"${ae.empleado.nombre_completo}","${ae.token_acceso}","${ae.empleado.numero_empleado}","${ae.empleado.departamento_nombre}","${ae.empleado.puesto_nombre}","${ae.status}"`
        ).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `tokens_${asignacion.evaluacion.titulo}_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  if (loading) {
    return (
      <div className="evaluaciones-admin-loading">
        <div className="loading-spinner"></div>
        <p>Cargando información de evaluaciones...</p>
      </div>
    );
  }

  return (
    <div className="evaluaciones-admin-panel">
      <div className="panel-header">
        <h2>
          🎯 Gestión de Evaluaciones
          {isAdminPlanta && <span className="panel-scope">- {userData.nombre_planta}</span>}
          {isAdminEmpresa && <span className="panel-scope">- Empresa</span>}
        </h2>
        <p>Sistema completo de gestión de evaluaciones NOM-030 y NOM-035</p>
      </div>

      {error && (
        <div className="error-banner">
          <span>❌ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="panel-tabs">
        <button 
          className={`tab ${activeTab === 'disponibles' ? 'active' : ''}`}
          onClick={() => setActiveTab('disponibles')}
        >
          📋 Evaluaciones Disponibles
          <span className="tab-count">{evaluacionesOficiales.length}</span>
        </button>
        
        <button 
          className={`tab ${activeTab === 'asignadas' ? 'active' : ''}`}
          onClick={() => setActiveTab('asignadas')}
        >
          👥 Asignaciones Activas
          <span className="tab-count">{asignacionesActivas.length}</span>
        </button>
        
        <button 
          className={`tab ${activeTab === 'resultados' ? 'active' : ''}`}
          onClick={() => setActiveTab('resultados')}
        >
          📊 Resultados
          <span className="tab-count">{resultadosEvaluaciones.length}</span>
        </button>
      </div>

      <div className="panel-content">
        {activeTab === 'disponibles' && (
          <div className="evaluaciones-disponibles">
            <div className="section-header">
              <h3>📋 Evaluaciones Oficiales Disponibles</h3>
              <p>Evaluaciones normativas listas para asignar a empleados</p>
            </div>

            {evaluacionesOficiales.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📭</div>
                <h4>No hay evaluaciones disponibles</h4>
                <p>No se encontraron evaluaciones oficiales vigentes</p>
              </div>
            ) : (
              <div className="evaluaciones-grid">
                {evaluacionesOficiales.map(evaluacion => (
                  <div key={evaluacion.id} className="evaluacion-card">
                    <div className="card-header">
                      <div className="evaluacion-tipo">
                        {(evaluacion.tipo_norma?.toLowerCase().includes('030') || 
                          evaluacion.nombre?.toLowerCase().includes('030')) ? '🛡️ NOM-030' : '🧠 NOM-035'}
                      </div>
                      <div className={`vigente-badge ${evaluacion.vigente ? 'vigente' : 'no-vigente'}`}>
                        {evaluacion.vigente ? '✅ Vigente' : '❌ No vigente'}
                      </div>
                    </div>
                    
                    <div className="card-body">
                      <h4>{evaluacion.nombre}</h4>
                      <p className="evaluacion-descripcion">{evaluacion.descripcion}</p>
                      
                      <div className="evaluacion-stats">
                        <span className="stat">
                          📝 {evaluacion.total_preguntas || 0} preguntas
                        </span>
                      </div>
                    </div>
                    
                    <div className="card-actions">
                      <button 
                        className="btn-primary"
                        onClick={() => abrirModalAsignacion(evaluacion)}
                        disabled={!evaluacion.vigente}
                      >
                        👥 Asignar a Empleados
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'asignadas' && (
          <div className="asignaciones-activas">
            <div className="section-header">
              <h3>👥 Asignaciones Activas</h3>
              <p>Evaluaciones asignadas a empleados con seguimiento en tiempo real</p>
            </div>

            {asignacionesActivas.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📭</div>
                <h4>No hay asignaciones activas</h4>
                <p>No se encontraron evaluaciones asignadas a empleados</p>
              </div>
            ) : (
              <div className="asignaciones-grid-compact" ref={scrollContainerRef}>
                {asignacionesActivas.map(asignacion => (
                  <AsignacionCard
                    key={asignacion.asignacion_id}
                    asignacion={asignacion}
                    isExpanded={asignacionesExpandidas.has(asignacion.asignacion_id)}
                    onToggleExpanded={toggleAsignacionExpandida}
                    onGestionarAsignacion={gestionarAsignacion}
                    onExportarTokens={exportarTokens}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'resultados' && (
          <div className="resultados-evaluaciones">
            <div className="section-header">
              <h3>📊 Resultados de Evaluaciones</h3>
              <p>Análisis de resultados y certificaciones obtenidas</p>
            </div>

            <div className="resultados-stats">
              <div className="stats-grid">
                <div key="aprobados" className="stat-card">
                  <div className="stat-icon">✅</div>
                  <div className="stat-content">
                    <span className="stat-number">{resultadosEvaluaciones.filter(r => r.aprobado).length}</span>
                    <span className="stat-label">Aprobados</span>
                  </div>
                </div>
                
                <div key="no-aprobados" className="stat-card">
                  <div className="stat-icon">❌</div>
                  <div className="stat-content">
                    <span className="stat-number">{resultadosEvaluaciones.filter(r => !r.aprobado).length}</span>
                    <span className="stat-label">No Aprobados</span>
                  </div>
                </div>
                
                <div key="promedio" className="stat-card">
                  <div className="stat-icon">📊</div>
                  <div className="stat-content">
                    <span className="stat-number">
                      {resultadosEvaluaciones.length > 0 
                        ? Math.round(resultadosEvaluaciones.reduce((acc, r) => acc + (r.porcentaje_correctas || 0), 0) / resultadosEvaluaciones.length)
                        : 0}%
                    </span>
                    <span className="stat-label">Promedio General</span>
                  </div>
                </div>
                
                <div key="tasa-exito" className="stat-card">
                  <div className="stat-icon">🏆</div>
                  <div className="stat-content">
                    <span className="stat-number">
                      {resultadosEvaluaciones.length > 0 
                        ? Math.round((resultadosEvaluaciones.filter(r => r.aprobado).length / resultadosEvaluaciones.length) * 100)
                        : 0}%
                    </span>
                    <span className="stat-label">Tasa de Éxito</span>
                  </div>
                </div>
              </div>
            </div>

            {resultadosEvaluaciones.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📊</div>
                <h4>Sin resultados disponibles</h4>
                <p>Los resultados aparecerán cuando los empleados completen sus evaluaciones</p>
              </div>
            ) : (
              <div className="resultados-table">
                <div className="table-header">
                  <span>Empleado</span>
                  <span>Evaluación</span>
                  <span>Fecha</span>
                  <span>Puntaje</span>
                  <span>Estado</span>
                </div>
                
                {resultadosEvaluaciones.map(resultado => (
                  <div key={resultado.resultado_id} className="table-row">
                    <div className="empleado-info">
                      <span className="empleado-nombre">
                        {resultado.asignacion_empleado?.empleado?.nombre_completo || 'N/A'}
                      </span>
                      <span className="empleado-numero">
                        #{resultado.asignacion_empleado?.empleado?.numero_empleado}
                      </span>
                    </div>
                    
                    <div className="evaluacion-info">
                      <span className="evaluacion-titulo">
                        {resultado.asignacion_empleado?.asignacion?.evaluacion?.titulo || 'N/A'}
                      </span>
                    </div>
                    
                    <div className="fecha-info">
                      {new Date(resultado.asignacion_empleado?.fecha_completado).toLocaleDateString()}
                    </div>
                    
                    <div className="puntaje-info">
                      <span className="puntaje-numero">
                        {resultado.porcentaje_correctas?.toFixed(1)}%
                      </span>
                      <div className="puntaje-barra">
                        <div 
                          className="puntaje-fill"
                          style={{ width: `${resultado.porcentaje_correctas}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="estado-info">
                      <span className={`estado-badge ${resultado.aprobado ? 'aprobado' : 'no-aprobado'}`}>
                        {resultado.aprobado ? '✅ Aprobado' : '❌ No Aprobado'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Modal de Asignación */}
      {modalAsignacionAbierto && evaluacionParaAsignar && (
        <div className="modal-overlay">
          <div className="modal-content asignacion-modal">
            <div className="modal-header">
              <h3>Asignar Evaluación: {evaluacionParaAsignar.nombre}</h3>
              <button 
                className="modal-close"
                onClick={cerrarModalAsignacion}
                disabled={loading}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="evaluacion-info-modal">
                <p><strong>Tipo:</strong> {evaluacionParaAsignar.tipo_norma}</p>
                <p><strong>Descripción:</strong> {evaluacionParaAsignar.descripcion}</p>
              </div>
              
              <div className="fecha-vencimiento">
                <label>
                  <strong>Fecha de Vencimiento:</strong>
                  <input
                    type="date"
                    value={fechaVencimiento}
                    onChange={(e) => setFechaVencimiento(e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                  />
                </label>
              </div>
              
              <div className="empleados-selector">
                <div className="empleados-header">
                  <h4>Seleccionar Empleados ({empleadosSeleccionados.length} de {empleadosDisponibles.length})</h4>
                  <button 
                    type="button"
                    className="btn-seleccionar-todos"
                    onClick={seleccionarTodosEmpleados}
                    disabled={loading}
                  >
                    {empleadosSeleccionados.length === empleadosDisponibles.length ? 
                      'Deseleccionar Todos' : 'Seleccionar Todos'
                    }
                  </button>
                </div>
                
                <div className="empleados-lista">
                  {empleadosDisponibles.map(empleado => (
                    <div key={empleado.empleado_id} className="empleado-item">
                      <label>
                        <input
                          type="checkbox"
                          checked={empleadosSeleccionados.includes(empleado.empleado_id)}
                          onChange={() => toggleEmpleadoSeleccionado(empleado.empleado_id)}
                          disabled={loading}
                        />
                        <div className="empleado-info">
                          <span className="empleado-nombre">
                            {empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno}
                          </span>
                          <span className="empleado-detalles">
                            {empleado.numero_empleado && `#${empleado.numero_empleado} - `}
                            {empleado.departamento_nombre} - {empleado.puesto_nombre}
                          </span>
                        </div>
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="modal-footer">
              <button 
                className="btn-cancelar"
                onClick={cerrarModalAsignacion}
                disabled={loading}
              >
                Cancelar
              </button>
              <button 
                className="btn-guardar"
                onClick={enviarAsignaciones}
                disabled={loading || empleadosSeleccionados.length === 0}
              >
                {loading ? 'Asignando...' : `Asignar a ${empleadosSeleccionados.length} empleados`}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EvaluacionesAdminPanel;
