import React, { useState, useEffect } from 'react';
import { obtenerEstadisticasBD, tablas, type EstadisticasBD } from '../services/adminBDService';
import ExportacionCSV from './ExportacionCSV';
import GestionRespaldos from './GestionRespaldos';
import '../css/GestionBD.css';

const GestionBD: React.FC = () => {
  const [estadisticas, setEstadisticas] = useState<EstadisticasBD | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'exportacion' | 'respaldos'>('exportacion');

  // Filtrar tablas - remover evaluaciones y encuestas
  const tablasDisponibles = tablas.filter(tabla => 
    !['evaluaciones', 'encuestas'].includes(tabla.nombre)
  );

  useEffect(() => {
    cargarEstadisticas();
  }, []);

  const cargarEstadisticas = async () => {
    setLoading(true);
    try {
      const stats = await obtenerEstadisticasBD();
      setEstadisticas(stats);
    } catch (error) {
      console.error('Error cargando estadísticas:', error);
      alert('Error al cargar estadísticas de la base de datos');
    } finally {
      setLoading(false);
    }
  };

  const getIcono = (tablaNombre: string) => {
    switch (tablaNombre) {
      case 'empresas': return '🏢';
      case 'plantas': return '🏭';
      case 'departamentos': return '🏢';
      case 'puestos': return '💼';
      case 'empleados': return '👤';
      case 'usuarios': return '👥';
      default: return '📊';
    }
  };

  const getContadorTabla = (tablaNombre: string): number => {
    if (!estadisticas) return 0;
    switch (tablaNombre) {
      case 'empresas': return estadisticas.empresas;
      case 'plantas': return estadisticas.plantas;
      case 'departamentos': return estadisticas.departamentos;
      case 'puestos': return estadisticas.puestos;
      case 'empleados': return estadisticas.empleados;
      case 'usuarios': return estadisticas.usuarios;
      default: return 0;
    }
  };

  return (
    <div className="gestion-bd">
      <div className="gestion-bd-header">
        <div className="header-content">
          <h2 className="gestion-bd-title">
            <span className="title-icon">🗄️</span>
            Gestión de Base de Datos
          </h2>
          <p className="gestion-bd-subtitle">
            Exporta datos en CSV y gestiona respaldos de la base de datos
          </p>
        </div>
        <button 
          onClick={cargarEstadisticas} 
          className="btn-refresh"
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner">⏳</span>
              Cargando...
            </>
          ) : (
            <>
              <span>🔄</span>
              Actualizar
            </>
          )}
        </button>
      </div>

      {/* Sistema de Pestañas */}
      <div className="tabs-container">
        <div className="tabs-header">
          <button 
            className={`tab-button ${activeTab === 'exportacion' ? 'active' : ''}`}
            onClick={() => setActiveTab('exportacion')}
          >
            <span className="tab-icon">📤</span>
            Exportación CSV
          </button>
          <button 
            className={`tab-button ${activeTab === 'respaldos' ? 'active' : ''}`}
            onClick={() => setActiveTab('respaldos')}
          >
            <span className="tab-icon">💾</span>
            Respaldos de BD
          </button>
        </div>
      </div>

      {/* Contenido de las pestañas */}
      {activeTab === 'exportacion' ? (
        // Contenido de Exportación CSV
        loading ? (
          <div className="loading-container">
            <div className="loading-spinner">⏳</div>
            <p>Cargando estadísticas de la base de datos...</p>
          </div>
        ) : estadisticas ? (
        <>
          {/* Resumen de estadísticas */}
          <div className="stats-summary">
            <div className="stats-summary-card">
              <h3>📊 Resumen del Sistema</h3>
              <div className="stats-grid-mini">
                <div className="stat-mini">
                  <span className="stat-mini-number">{estadisticas.empresas + estadisticas.plantas + estadisticas.departamentos + estadisticas.puestos + estadisticas.empleados + estadisticas.usuarios}</span>
                  <span className="stat-mini-label">Total Registros</span>
                </div>
                <div className="stat-mini">
                  <span className="stat-mini-number">{tablas.length}</span>
                  <span className="stat-mini-label">Tablas Disponibles</span>
                </div>
                <div className="stat-mini">
                  <span className="stat-mini-number">CSV</span>
                  <span className="stat-mini-label">Formato Export</span>
                </div>
              </div>
            </div>
          </div>

          {/* Grid de tarjetas de exportación */}
          <div className="exportacion-section">
            <h3 className="section-title">
              <span className="section-icon">📤</span>
              Exportación de Datos
            </h3>
            <p className="section-description">
              Selecciona las tablas que deseas exportar en formato CSV para análisis externo
            </p>
            
            <div className="exportacion-cards-grid">
              {tablasDisponibles.map((tabla) => (
                <div key={tabla.nombre} className="export-card">
                  <div className="export-card-header">
                    <div className="export-card-icon">
                      {getIcono(tabla.nombre)}
                    </div>
                    <div className="export-card-info">
                      <h4 className="export-card-title">{tabla.nombre}</h4>
                      <div className="export-card-count">
                        <span className="count-number">{getContadorTabla(tabla.nombre)}</span>
                        <span className="count-label">registros</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="export-card-body">
                    <p className="export-card-description">
                      {tabla.descripcion}
                    </p>
                  </div>
                  
                  <div className="export-card-footer">
                    <ExportacionCSV 
                      tablaNombre={tabla.nombre}
                      descripcion={tabla.descripcion}
                      className="export-card-btn"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
        ) : (
          <div className="error-container">
            <div className="error-icon">❌</div>
            <h3>Error al cargar datos</h3>
            <p>No se pudieron cargar las estadísticas de la base de datos</p>
            <button onClick={cargarEstadisticas} className="btn-retry">
              🔄 Reintentar
            </button>
          </div>
        )
      ) : (
        // Contenido de Respaldos de BD
        <GestionRespaldos />
      )}
    </div>
  );
};

export default GestionBD;