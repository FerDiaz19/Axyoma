import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from '../services/authService';
import '../css/Dashboard.css';

interface EmpleadoDashboardProps {
  userData: any;
}

const EmpleadoDashboard: React.FC<EmpleadoDashboardProps> = ({ userData }) => {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState('perfil');

  const handleLogout = () => {
    try {
      console.log("🚪 Iniciando cierre de sesión...");
      
      logout(); // Limpia el token
      
      console.log("✅ Sesión cerrada, redirigiendo a página principal...");
      navigate('/', { replace: true });

      // Forzamos recarga para reiniciar el estado de la app soy gay jiji
      setTimeout(() => {
        window.location.reload();
      }, 50);
    } catch (error) {
      console.error("❌ Error durante el cierre de sesión:", error);
      window.location.href = '/';
    }
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'perfil':
        return (
          <div className="dashboard-section">
            <h2>Mi Perfil</h2>
            <div className="profile-info">
              <div className="user-details">
                <h3>Información Personal</h3>
                <p><strong>Nombre:</strong> {userData.nombre_completo || userData.usuario}</p>
                <p><strong>Usuario:</strong> {userData.usuario}</p>
                <p><strong>Rol:</strong> Empleado</p>
              </div>
            </div>
          </div>
        );
      case 'evaluaciones':
        return (
          <div className="dashboard-section">
            <h2>Mis Evaluaciones</h2>
            <p>Próximamente podrás ver tus evaluaciones asignadas aquí.</p>
          </div>
        );
      default:
        return <div>Sección no encontrada</div>;
    }
  };

  return (
    <div className="dashboard empleado-dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>👤 AXYOMA</h2>
            <span className="sidebar-subtitle">Panel de Empleado</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button 
            className={activeSection === 'perfil' ? 'active' : ''}
            onClick={() => setActiveSection('perfil')}
          >
            <span className="nav-icon">👤</span>
            <span className="nav-text">Mi Perfil</span>
          </button>
          <button 
            className={activeSection === 'evaluaciones' ? 'active' : ''}
            onClick={() => setActiveSection('evaluaciones')}
          >
            <span className="nav-icon">📝</span>
            <span className="nav-text">Mis Evaluaciones</span>
          </button>
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
            <h1>Panel de Empleado</h1>
            <p className="header-subtitle">Bienvenido, {userData.nombre_completo || userData.usuario}</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar">
                <span className="avatar-icon">👤</span>
              </div>
              <div className="user-details">
                <span className="user-name">{userData.nombre_completo || userData.usuario}</span>
                <span className="user-role">Empleado</span>
              </div>
            </div>
          </div>
        </header>

        {/* Content area */}
        <main className="dashboard-content">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default EmpleadoDashboard;
