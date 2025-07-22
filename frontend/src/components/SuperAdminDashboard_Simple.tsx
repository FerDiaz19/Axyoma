import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import '../css/SuperAdminDashboard.css';

interface SuperAdminEstadisticas {
  total_empresas: number;
  total_usuarios: number;
  total_plantas: number;
  empresas_activas: number;
  empresas_suspendidas: number;
  usuarios_activos: number;
  usuarios_suspendidos: number;
}

const SuperAdminDashboard: React.FC = () => {
  const [estadisticas, setEstadisticas] = useState<SuperAdminEstadisticas | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    setError('');
    
    try {
      console.log('🔍 Cargando estadísticas del sistema...');
      
      const response = await fetch('/api/empresas/estadisticas/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });

      console.log('📊 Response status:', response.status);

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Datos cargados:', data);
      
      setEstadisticas(data);
    } catch (error: any) {
      console.error('❌ Error cargando datos:', error);
      setError(error.message || 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando datos del sistema...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-container">
          <h2>❌ Error</h2>
          <p>{error}</p>
          <button onClick={cargarDatos} className="btn btn-primary">
            Reintentar
          </button>
          <button onClick={handleLogout} className="btn btn-secondary">
            Cerrar Sesión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>🏢 Panel Super Administrador</h1>
        <div className="header-actions">
          <button onClick={cargarDatos} className="btn btn-refresh">
            🔄 Actualizar
          </button>
          <button onClick={handleLogout} className="btn btn-logout">
            🚪 Cerrar Sesión
          </button>
        </div>
      </header>

      {estadisticas && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>📊 Estadísticas del Sistema</h3>
            <div className="stat-item">
              <span className="stat-label">Total Empresas:</span>
              <span className="stat-value">{estadisticas.total_empresas || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Usuarios:</span>
              <span className="stat-value">{estadisticas.total_usuarios || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Plantas:</span>
              <span className="stat-value">{estadisticas.total_plantas || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Empresas Activas:</span>
              <span className="stat-value">{estadisticas.empresas_activas || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Empresas Suspendidas:</span>
              <span className="stat-value">{estadisticas.empresas_suspendidas || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Usuarios Activos:</span>
              <span className="stat-value">{estadisticas.usuarios_activos || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Usuarios Suspendidos:</span>
              <span className="stat-value">{estadisticas.usuarios_suspendidos || 0}</span>
            </div>
          </div>
        </div>
      )}

      <div className="debug-info">
        <h4>🔍 Debug Info</h4>
        <p>Token: {localStorage.getItem('token') ? '✅ Presente' : '❌ Ausente'}</p>
        <p>Estado: {loading ? 'Cargando...' : 'Listo'}</p>
        <p>Error: {error || 'Ninguno'}</p>
        <p>Datos: {estadisticas ? '✅ Cargados' : '❌ Sin datos'}</p>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
