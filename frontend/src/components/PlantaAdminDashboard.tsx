import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';

import EvaluacionesDashboard from './evaluaciones/EvaluacionesDashboard';

// import EvaluacionesGestion from './EvaluacionesGestion';
// import AsignacionEvaluaciones from './AsignacionEvaluaciones';

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
      icon: '🏢',
      description: 'Gestionar departamentos de la planta'
    },
    {
      id: 'puestos' as ActiveSection,
      label: 'Puestos',
      icon: '💼',
      description: 'Administrar puestos de trabajo'
    },
    {
      id: 'empleados' as ActiveSection,
      label: 'Empleados',
      icon: '👥',
      description: 'Gestión de empleados'
    },
    {
      id: 'evaluaciones' as ActiveSection,
      label: 'Evaluaciones',
      icon: '📝',
      description: 'Gestionar evaluaciones'
    },
    {
      id: 'asignaciones' as ActiveSection,
      label: 'Asignar Evaluaciones',
      icon: '🎯',
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

      // case 'asignaciones':
      //   return <AsignacionEvaluaciones userData={{ nivel_usuario: 'admin_planta' }} />;
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
            <h2>🏭 AXYOMA</h2>
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
                <span className="avatar-icon">🏭</span>
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
