import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionPlantas from './GestionPlantas';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
import EvaluacionesGestion from './EvaluacionesGestion';
import AsignacionEvaluaciones from './AsignacionEvaluaciones';
import GestionSuscripcion from './GestionSuscripcion';
import UsuariosPlantasView from './UsuariosPlantasView';
import { logout } from '../services/authService';
import '../css/SuperAdminDashboard.css';

interface EmpresaAdminDashboardProps {
  userData: any;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData }) => {
  const [activeSection, setActiveSection] = useState('overview');
  const navigate = useNavigate();

  const empresaId = userData?.empresa_id;

  // Debug logs
  console.log('🔍 DEBUG EmpresaAdminDashboard - userData completo:', userData);
  console.log('🔍 DEBUG EmpresaAdminDashboard - empresaId obtenido:', empresaId);
  console.log('🔍 DEBUG EmpresaAdminDashboard - empresa_id directo:', userData?.empresa_id);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('userData');
      navigate('/login');
    }
  };

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <div className="welcome-section">
            <div className="hero-banner">
              <h2>¡Bienvenido al Panel de Administración!</h2>
              <p>Gestiona tu empresa de manera integral desde este panel de control</p>
            </div>
            
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">👥</div>
                <div className="stat-content">
                  <h3>Empleados Activos</h3>
                  <p className="stat-number">156</p>
                  <span className="stat-change positive">+8 este mes</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🏭</div>
                <div className="stat-content">
                  <h3>Plantas Operativas</h3>
                  <p className="stat-number">12</p>
                  <span className="stat-change positive">+2 este trimestre</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-content">
                  <h3>Evaluaciones Completadas</h3>
                  <p className="stat-number">89%</p>
                  <span className="stat-change positive">+5% vs mes anterior</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-content">
                  <h3>Objetivos Alcanzados</h3>
                  <p className="stat-number">94%</p>
                  <span className="stat-change positive">Excelente rendimiento</span>
                </div>
              </div>
            </div>

            <div className="quick-actions">
              <h3>Acciones Rápidas</h3>
              <div className="action-buttons">
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('empleados')}
                >
                  <span className="action-icon">👤</span>
                  <span>Gestionar Empleados</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('plantas')}
                >
                  <span className="action-icon">🏭</span>
                  <span>Ver Plantas</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('evaluaciones')}
                >
                  <span className="action-icon">📋</span>
                  <span>Crear Evaluación</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('asignaciones')}
                >
                  <span className="action-icon">🎯</span>
                  <span>Asignar Evaluaciones</span>
                </button>
              </div>
            </div>
          </div>
        );
      case 'empleados':
        return (
          <EmpleadosCRUD 
            userData={userData}
          />
        );
      case 'plantas':
        return (
          <GestionPlantas 
            empresaId={empresaId || 1}
          />
        );
      case 'usuarios-plantas':
        return (
          <UsuariosPlantasView 
            empresaId={empresaId || 1}
          />
        );
      case 'departamentos':
        return (
          <GestionDepartamentos 
            empresaId={empresaId || 1}
          />
        );
      case 'puestos':
        return (
          <GestionPuestos empresaId={empresaId || 1} />
        );
      case 'evaluaciones':
        return (
          <EvaluacionesGestion 
            userData={userData}
          />
        );
      case 'asignaciones':
        return (
          <AsignacionEvaluaciones 
            userData={userData}
          />
        );
      case 'suscripcion':
        return (
          <GestionSuscripcion 
            empresaId={empresaId || 1}
          />
        );
      default:
        return (
          <div className="welcome-section">
            <div className="hero-banner">
              <h2>¡Bienvenido al Panel de Administración!</h2>
              <p>Gestiona tu empresa de manera integral desde este panel de control</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard superadmin-dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>🏢 AXYOMA</h2>
            <span className="sidebar-subtitle">Panel Empresa</span>
          </div>
        </div>
        <nav className="sidebar-nav">
          <button 
            className={activeSection === 'overview' ? 'active' : ''}
            onClick={() => setActiveSection('overview')}
          >
            <span className="nav-icon">📊</span>
            <span className="nav-text">Dashboard</span>
          </button>
          <button 
            className={activeSection === 'empleados' ? 'active' : ''}
            onClick={() => setActiveSection('empleados')}
          >
            <span className="nav-icon">👥</span>
            <span className="nav-text">Empleados</span>
          </button>
          <button 
            className={activeSection === 'plantas' ? 'active' : ''}
            onClick={() => setActiveSection('plantas')}
          >
            <span className="nav-icon">🏭</span>
            <span className="nav-text">Plantas</span>
          </button>
          <button 
            className={activeSection === 'usuarios-plantas' ? 'active' : ''}
            onClick={() => setActiveSection('usuarios-plantas')}
          >
            <span className="nav-icon">👤</span>
            <span className="nav-text">Usuarios Plantas</span>
          </button>
          <button 
            className={activeSection === 'departamentos' ? 'active' : ''}
            onClick={() => setActiveSection('departamentos')}
          >
            <span className="nav-icon">🏢</span>
            <span className="nav-text">Departamentos</span>
          </button>
          <button 
            className={activeSection === 'puestos' ? 'active' : ''}
            onClick={() => setActiveSection('puestos')}
          >
            <span className="nav-icon">💼</span>
            <span className="nav-text">Puestos</span>
          </button>
          <button 
            className={activeSection === 'evaluaciones' ? 'active' : ''}
            onClick={() => setActiveSection('evaluaciones')}
          >
            <span className="nav-icon">📋</span>
            <span className="nav-text">Evaluaciones</span>
          </button>
          <button 
            className={activeSection === 'asignaciones' ? 'active' : ''}
            onClick={() => setActiveSection('asignaciones')}
          >
            <span className="nav-icon">🎯</span>
            <span className="nav-text">Asignaciones</span>
          </button>
          <button 
            className={activeSection === 'suscripcion' ? 'active' : ''}
            onClick={() => setActiveSection('suscripcion')}
          >
            <span className="nav-icon">💳</span>
            <span className="nav-text">Suscripción</span>
          </button>
        </nav>
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
            <div className="user-info">
              <div className="user-avatar">
                <span className="avatar-icon">👤</span>
              </div>
              <div className="user-details">
                <span className="user-name">
                  {userData?.perfil_usuario?.nombre || userData?.username}
                </span>
                <span className="user-role">Administrador de Empresa</span>
              </div>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <span className="logout-icon">🚪</span>
              Cerrar Sesión
            </button>
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
