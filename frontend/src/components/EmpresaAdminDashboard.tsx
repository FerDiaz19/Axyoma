import React, { useState } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionPlantas from './GestionPlantas';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
import UsuariosPlanta from './UsuariosPlanta';
import AsignacionEvaluacionesDashboard from './AsignacionEvaluacionesDashboard';
import { logout } from '../services/authService';
import '../css/Dashboard.css';
import '../css/GestionPlantas.css';
import '../css/EmpresaAdminDashboard.css';

interface EmpresaAdminDashboardProps {
  userData: any;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData }) => {
  const [activeSection, setActiveSection] = useState('plantas');

  const menuItems = [
    {
      id: 'plantas',
      label: 'Gestión de Plantas',
      icon: '🏭',
      description: 'Administrar plantas de la empresa'
    },
    {
      id: 'departamentos',
      label: 'Departamentos',
      icon: '🏢',
      description: 'Gestionar departamentos'
    },
    {
      id: 'puestos',
      label: 'Puestos',
      icon: '💼',
      description: 'Administrar puestos de trabajo'
    },
    {
      id: 'usuarios-planta',
      label: 'Usuarios de Planta',
      icon: '👤',
      description: 'Ver usuarios asignados a plantas'
    },
    {
      id: 'empleados',
      label: 'Gestión de Empleados',
      icon: '👥',
      description: 'Administrar empleados'
    },
    {
      id: 'evaluaciones',
      label: 'Gestión de Evaluaciones',
      icon: '📊',
      description: 'Gestionar y asignar evaluaciones'
    },
    {
      id: 'reportes',
      label: 'Reportes',
      icon: '📋',
      description: 'Ver reportes y estadísticas'
    }
  ];

  const handleLogout = async () => {
    try {
      await logout();
      window.location.href = '/';
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'plantas':
        return <GestionPlantas empresaId={userData?.empresa?.id} />;
      case 'departamentos':
        return <GestionDepartamentos />;
      case 'puestos':
        return <GestionPuestos />;
      case 'usuarios-planta':
        return <UsuariosPlanta />;
      case 'empleados':
        return <EmpleadosCRUD userData={userData} />;
      case 'evaluaciones':
        return <AsignacionEvaluacionesDashboard empresaId={userData?.empresa?.id} />;
      case 'reportes':
        return (
          <div className="coming-soon">
            <h2>Reportes</h2>
            <p>Módulo de reportes en desarrollo...</p>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Reportes Generados</h3>
                <p className="stat-number">8</p>
              </div>
              <div className="stat-card">
                <h3>Descargas</h3>
                <p className="stat-number">24</p>
              </div>
              <div className="stat-card">
                <h3>Usuarios Activos</h3>
                <p className="stat-number">156</p>
              </div>
            </div>
          </div>
        );
      default:
        return <div>Sección no encontrada</div>;
    }
  };

  return (
    <div className="dashboard empresa-admin-dashboard">
      {/* Sidebar - Always visible */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>🏢 AXYOMA</h2>
            <span className="sidebar-subtitle">Admin Empresa</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <button 
              key={item.id}
              className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => setActiveSection(item.id as any)}
              title={item.description}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-text">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            <span>🚪</span>
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Main content area */}
      <div className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="header-left">
            <h1>Panel de Administración - Empresa</h1>
            <p className="header-subtitle">Gestión integral de la empresa</p>
          </div>
          <div className="header-right">
            <div className="empresa-info">
              <div className="empresa-avatar">
                <span className="avatar-icon">🏢</span>
              </div>
              <div className="empresa-details">
                <span className="empresa-name">{userData?.empresa?.nombre || 'Empresa'}</span>
                <span className="empresa-user">({userData?.username})</span>
              </div>
            </div>
          </div>
        </header>

        {/* Content area */}
        <main className="dashboard-content">
          {renderActiveSection()}
        </main>
      </div>
    </div>
  );
};

export default EmpresaAdminDashboard;
