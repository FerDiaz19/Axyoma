import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';


import EvaluacionesDashboard from './evaluaciones/EvaluacionesDashboard';
import AsignacionesDashboard from './evaluaciones/AsignacionesDashboard';

import { logout } from '../services/authService';
import '../css/Dashboard.css';
import '../css/PlantaAdminDashboard.css';

interface PlantaAdminDashboardProps {
  userData: any;
}

type ActiveSection = 'departamentos' | 'puestos' | 'empleados' | 'evaluaciones' | 'asignaciones';

const PlantaAdminDashboard: React.FC<PlantaAdminDashboardProps> = ({ userData }) => {
  const [activeSection, setActiveSection] = useState<ActiveSection>('departamentos');
  const navigate = useNavigate();

  const menuItems = [
    {
      id: 'departamentos' as ActiveSection,
      label: 'Departamentos',
      icon: <svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1" />
      </svg>,
      description: 'Gestionar departamentos de la planta'
    },
    {
      id: 'puestos' as ActiveSection,
      label: 'Puestos',
      icon: <svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m8 6V8a2 2 0 00-2-2H10a2 2 0 00-2 2v6m8 0a2 2 0 01-2 2H10a2 2 0 01-2-2m8 0V8a2 2 0 00-2-2H10a2 2 0 00-2 2v6" />
      </svg>,
      description: 'Administrar puestos de trabajo'
    },
    {
      id: 'empleados' as ActiveSection,
      label: 'Empleados',
      icon: <svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
      </svg>,
      description: 'Gestión de empleados'
    },
    {
      id: 'evaluaciones' as ActiveSection,
      label: 'Evaluaciones',
      icon: <svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>,
      description: 'Gestionar evaluaciones'
    },
    {
      id: 'asignaciones' as ActiveSection,
      label: 'Asignar Evaluaciones',
      icon: <svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>,
      description: 'Asignar evaluaciones a empleados'
    }
  ];

const handleLogout = () => {
  try {
    console.log("🚪 Iniciando cierre de sesión...");

    logout(); // Limpia el token

    console.log("✅ Sesión cerrada, redirigiendo a página principal...");

    // Navegamos al inicio
    navigate('/', { replace: true });

    // Forzamos recarga para reiniciar el estado de la app
    setTimeout(() => {
      window.location.reload();
    }, 50); // Pequeña pausa para asegurar que el navigate se complete
  } catch (error) {
    console.error("❌ Error durante el cierre de sesión:", error);
    window.location.href = '/';
  }
};

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'departamentos':
        return <GestionDepartamentos />;
      case 'puestos':
        return <GestionPuestos />;
      case 'empleados':
        return <EmpleadosCRUD userData={userData} />;

      case 'evaluaciones':
        return <EvaluacionesDashboard userData={userData} />
      case 'asignaciones':
        return <AsignacionesDashboard userData={userData} />

      default:
        return <div>Sección no encontrada</div>;
    }
  };

  return (
    <div className="dashboard planta-admin-dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '2rem', height: '2rem', marginRight: '10px', verticalAlign: 'middle' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg> AXYOMA
            </h2>
            <span className="sidebar-subtitle">Admin Planta</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => setActiveSection(item.id)}
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

      {/* Main content */}
      <div className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="header-left">
            <h1>Panel de Administración - Planta</h1>
            <p className="header-subtitle">Gestión de planta industrial</p>
          </div>
          <div className="header-right">
            <div className="planta-info">
              <div className="planta-avatar">
                <span className="avatar-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" style={{ width: '1.5rem', height: '1.5rem' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </span>
              </div>
              <div className="planta-details">
                <span className="planta-name">{userData?.nombre_planta || 'Mi Planta'}</span>
                <span className="planta-user">({userData?.usuario})</span>
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

export default PlantaAdminDashboard;
