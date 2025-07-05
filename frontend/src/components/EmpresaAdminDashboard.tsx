import React, { useState } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
import { logout } from '../services/authService';
import '../css/Dashboard.css';
import '../css/GestionPlantas.css';

interface EmpresaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'plantas' | 'empleados' | 'estructura' | 'evaluaciones' | 'reportes'>('plantas');

  const handleLogout = () => {
    logout();
    onLogout();
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Panel de Administración - Empresa</h1>
        <div className="empresa-info">
          <span>{userData?.nombre_empresa || 'Empresa'}</span>
          <span>({userData?.usuario})</span>
        </div>
        <button onClick={handleLogout} className="logout-btn">
          Cerrar Sesión
        </button>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={activeSection === 'plantas' ? 'active' : ''}
          onClick={() => setActiveSection('plantas')}
        >
          Gestión de Plantas
        </button>
        <button 
          className={activeSection === 'estructura' ? 'active' : ''}
          onClick={() => setActiveSection('estructura')}
        >
          Estructura Organizacional
        </button>
        <button 
          className={activeSection === 'empleados' ? 'active' : ''}
          onClick={() => setActiveSection('empleados')}
        >
          Gestión de Empleados
        </button>
        <button 
          className={activeSection === 'evaluaciones' ? 'active' : ''}
          onClick={() => setActiveSection('evaluaciones')}
        >
          Evaluaciones
        </button>
        <button 
          className={activeSection === 'reportes' ? 'active' : ''}
          onClick={() => setActiveSection('reportes')}
        >
          Reportes
        </button>
      </nav>

      <main className="dashboard-content">
        {activeSection === 'plantas' && (
          <GestionPlantas empresaId={userData?.empresa_id} />
        )}
        {activeSection === 'estructura' && <GestionEstructura />}
        {activeSection === 'empleados' && <EmpleadosCRUD />}
        {activeSection === 'evaluaciones' && (
          <div className="coming-soon">
            <h2>Evaluaciones</h2>
            <p>Módulo de evaluaciones en desarrollo...</p>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Evaluaciones Activas</h3>
                <p className="stat-number">5</p>
              </div>
              <div className="stat-card">
                <h3>Evaluaciones Completadas</h3>
                <p className="stat-number">12</p>
              </div>
              <div className="stat-card">
                <h3>Empleados Evaluados</h3>
                <p className="stat-number">45</p>
              </div>
            </div>
          </div>
        )}
        {activeSection === 'reportes' && (
          <div className="coming-soon">
            <h2>Reportes y Estadísticas</h2>
            <p>Módulo de reportes en desarrollo...</p>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Empleados</h3>
                <p className="stat-number">45</p>
              </div>
              <div className="stat-card">
                <h3>Departamentos</h3>
                <p className="stat-number">8</p>
              </div>
              <div className="stat-card">
                <h3>Plantas</h3>
                <p className="stat-number">3</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default EmpresaAdminDashboard;
