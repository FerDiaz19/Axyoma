import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
import EvaluacionesGestion from './EvaluacionesGestion';
import GestionSuscripcion from './GestionSuscripcion';
import { logout } from '../services/authService';
import '../css/Dashboard.css';
import '../css/GestionPlantas.css';
import '../css/EmpresaAdminDashboard.css';

interface EmpresaAdminDashboardProps {
  userData: any;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData }) => {
  console.log('Renderizando EmpresaAdminDashboard', { userData });
  const [activeSection, setActiveSection] = useState('suscripcion');
  const [empresaId, setEmpresaId] = useState<number | null>(null);
  console.log('Sección activa inicial:', activeSection);
  const navigate = useNavigate();

  useEffect(() => {
    const getEmpresaId = async () => {
      try {
        // Intentar extraer empresa_id del userData
        if (userData?.empresa_id) {
          console.log('Empresa ID obtenido de userData:', userData.empresa_id);
          setEmpresaId(userData.empresa_id);
          return;
        }
        
        // Si no está en userData, intentar obtener de profile_id
        if (userData?.profile_id) {
          console.log('Usando profile_id como empresa_id:', userData.profile_id);
          setEmpresaId(userData.profile_id);
          return;
        }
        
        // Si todo falla, consultar a la API
        console.log('Intentando obtener empresa_id desde API...');
        // Importar dinámicamente para evitar dependencias circulares
        const { obtenerPerfilUsuario } = await import('../services/userService');
        const perfil = await obtenerPerfilUsuario(userData?.user_id);
        if (perfil && perfil.empresa_id) {
          console.log('Empresa ID obtenido desde API:', perfil.empresa_id);
          setEmpresaId(perfil.empresa_id);
          return;
        }
        
        // Como último recurso, intentar obtenerlo desde localStorage
        const storedEmpresaId = localStorage.getItem('empresaId');
        if (storedEmpresaId) {
          console.log('Empresa ID obtenido desde localStorage:', storedEmpresaId);
          setEmpresaId(parseInt(storedEmpresaId));
          return;
        }
        
        console.warn('No se pudo determinar el empresa_id. Usando valor predeterminado 1 para pruebas.');
        setEmpresaId(1); // Valor por defecto para pruebas
      } catch (error) {
        console.error('Error al obtener empresa_id:', error);
        // Como fallback, usar ID 1 para pruebas
        setEmpresaId(1);
      }
    };
    
    getEmpresaId();
  }, [userData]);

  // Lista de elementos del menú
  const menuItems = [
    {
      id: 'suscripcion',
      label: 'Plan de Suscripción',
      icon: '💎',
      description: 'Gestionar suscripción'
    },
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
      id: 'estructura',
      label: 'Estructura Organizacional',
      icon: '🏗️',
      description: 'Ver estructura completa'
    },
    {
      id: 'empleados',
      label: 'Gestión de Empleados',
      icon: '👥',
      description: 'Administrar empleados'
    },
    {
      id: 'evaluaciones',
      label: 'Evaluaciones',
      icon: '📊',
      description: 'Gestionar evaluaciones'
    },
    {
      id: 'reportes',
      label: 'Reportes',
      icon: '📋',
      description: 'Ver reportes y estadísticas'
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
    console.log('Sección activa:', activeSection);
    switch (activeSection) {
      case 'suscripcion':
        console.log('Renderizando sección de suscripción con empresaId:', empresaId);
        return empresaId ? <GestionSuscripcion empresaId={empresaId} /> : <div className="loading">Cargando suscripción...</div>;
      case 'plantas':
        return <GestionPlantas empresaId={userData?.empresa_id} />;
      case 'departamentos':
        return <GestionDepartamentos />;
      case 'puestos':
        return <GestionPuestos />;
      case 'estructura':
        return <GestionEstructura />;
      case 'empleados':
        return <EmpleadosCRUD userData={userData} />;
      case 'evaluaciones':
        return <EvaluacionesGestion userData={{ nivel_usuario: 'admin_empresa' }} />;
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
                <span className="empresa-name">{userData?.nombre_empresa || 'Empresa'}</span>
                <span className="empresa-user">({userData?.usuario})</span>
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
