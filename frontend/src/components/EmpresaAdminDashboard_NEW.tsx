import React, { useState, useEffect, useCallback } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
import GestionEvaluaciones from './GestionEvaluaciones';
import { logout } from '../services/authService';
import '../css/ModernDashboard.css';

interface EmpresaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'overview' | 'plantas' | 'empleados' | 'estructura' | 'evaluaciones' | 'reportes'>('overview');
  const [subscriptionInfo, setSubscriptionInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadSubscriptionInfo = useCallback(async () => {
    try {
      const empresaId = userData?.empresa_id;
      if (empresaId) {
        const { obtenerInfoSuscripcionEmpresa } = await import('../services/suscripcionService');
        const info = await obtenerInfoSuscripcionEmpresa(empresaId);
        setSubscriptionInfo(info);
      } else {
        throw new Error('No se encontró empresa_id en userData');
      }
    } catch (error) {
      console.error('Error loading subscription info:', error);
      setSubscriptionInfo({ 
        tiene_suscripcion: false, 
        estado: 'sin_suscripcion', 
        requiere_pago: true 
      });
    } finally {
      setLoading(false);
    }
  }, [userData?.empresa_id]);

  useEffect(() => {
    if (userData?.suscripcion) {
      setSubscriptionInfo(userData.suscripcion);
      setLoading(false);
    } else {
      loadSubscriptionInfo();
    }

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'subscription_updated') {
        loadSubscriptionInfo();
        localStorage.removeItem('subscription_updated');
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [userData, loadSubscriptionInfo]);

  const handleLogout = () => {
    logout();
    onLogout();
  };

  const shouldShowSuspended = subscriptionInfo && 
    !subscriptionInfo.tiene_suscripcion && 
    subscriptionInfo.requiere_pago &&
    ['sin_suscripcion', 'pendiente_pago', 'vencida'].includes(subscriptionInfo.estado);

  const isEmpresaSuspendida = userData?.empresa_suspendida || 
                             userData?.advertencia?.tipo === 'empresa_suspendida' ||
                             shouldShowSuspended;

  // Menú de navegación
  const menuItems = [
    { id: 'overview', label: 'Panel General', icon: '📊', description: 'Vista general del sistema' },
    { id: 'plantas', label: 'Plantas', icon: '🏭', description: 'Gestión de plantas industriales' },
    { id: 'empleados', label: 'Empleados', icon: '👥', description: 'Administración de personal' },
    { id: 'estructura', label: 'Estructura', icon: '🏗️', description: 'Departamentos y puestos' },
    { id: 'evaluaciones', label: 'Evaluaciones', icon: '📝', description: 'Gestión de evaluaciones' },
    { id: 'reportes', label: 'Reportes', icon: '📈', description: 'Análisis y reportes' }
  ];

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'overview':
        return <OverviewSection subscriptionInfo={subscriptionInfo} userData={userData} />;
      case 'plantas':
        return <GestionPlantas empresaId={userData?.empresa_id} />;
      case 'empleados':
        return <EmpleadosCRUD />;
      case 'estructura':
        return <GestionEstructura />;
      case 'evaluaciones':
        return <GestionEvaluaciones usuario={userData} />;
      case 'reportes':
        return subscriptionInfo?.tiene_suscripcion ? (
          <ReportesSection />
        ) : (
          <div className="upgrade-needed">
            <div className="upgrade-card">
              <span className="upgrade-icon">🔒</span>
              <h3>Sección Premium</h3>
              <p>Los reportes requieren una suscripción activa.</p>
              <button 
                className="upgrade-btn"
                onClick={() => setActiveSection('overview')}
              >
                Ver Planes
              </button>
            </div>
          </div>
        );
      default:
        return <OverviewSection subscriptionInfo={subscriptionInfo} userData={userData} />;
    }
  };

  if (loading) {
    return (
      <div className="modern-dashboard">
        <div className="loading-container">
          <div className="loading-spinner">🔄</div>
          <h2>Cargando Dashboard</h2>
          <p>Verificando estado de suscripción...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="modern-dashboard">
      {/* Sidebar Navigation */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>🏢 AXYOMA</h2>
            <span className="sidebar-subtitle">Admin Empresa</span>
          </div>
          <div className="user-info">
            <div className="user-avatar">
              {userData?.usuario?.charAt(0).toUpperCase() || 'A'}
            </div>
            <div className="user-details">
              <span className="user-name">{userData?.usuario || 'Admin'}</span>
              <span className="user-role">Administrador de Empresa</span>
            </div>
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
          <div className="subscription-status">
            {subscriptionInfo?.tiene_suscripcion ? (
              <div className="status-card success">
                <span className="status-icon">✅</span>
                <div>
                  <span className="status-text">Suscripción Activa</span>
                  <span className="status-detail">
                    {subscriptionInfo.plan_nombre} - {subscriptionInfo.dias_restantes || 0} días
                  </span>
                </div>
              </div>
            ) : (
              <div className="status-card warning">
                <span className="status-icon">⚠️</span>
                <div>
                  <span className="status-text">Sin Suscripción</span>
                  <span className="status-detail">Funcionalidad limitada</span>
                </div>
              </div>
            )}
          </div>
          
          <button className="logout-btn" onClick={handleLogout}>
            <span>🚪</span>
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="dashboard-main">
        <header className="main-header">
          <div className="header-left">
            <h1 className="page-title">
              {menuItems.find(item => item.id === activeSection)?.label || 'Dashboard'}
            </h1>
            <p className="page-description">
              {menuItems.find(item => item.id === activeSection)?.description || 'Panel de administración'}
            </p>
          </div>
          <div className="header-right">
            <div className="empresa-badge">
              <span className="badge-icon">🏢</span>
              <span className="badge-text">{userData?.nombre_empresa || 'Mi Empresa'}</span>
            </div>
          </div>
        </header>

        <div className="main-content">
          {isEmpresaSuspendida ? (
            <div className="suspension-warning">
              <div className="warning-card">
                <div className="warning-icon">🚫</div>
                <div className="warning-content">
                  <h3>Acceso Limitado</h3>
                  <p>
                    Su empresa no tiene una suscripción activa. 
                    Para acceder a todas las funcionalidades, debe activar una suscripción.
                  </p>
                  <button 
                    className="activate-btn"
                    onClick={() => setActiveSection('overview')}
                  >
                    <span>💳</span>
                    Activar Suscripción
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="content-area">
              {renderActiveSection()}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

// Componente Overview
const OverviewSection: React.FC<{subscriptionInfo: any, userData: any}> = ({ subscriptionInfo, userData }) => {
  return (
    <div className="overview-section">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🏢</div>
          <div className="stat-info">
            <h3>{userData?.nombre_empresa || 'Mi Empresa'}</h3>
            <p>Empresa Principal</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">💼</div>
          <div className="stat-info">
            <h3>{subscriptionInfo?.plan_nombre || 'Sin Plan'}</h3>
            <p>Plan Actual</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-info">
            <h3>{subscriptionInfo?.dias_restantes || 0}</h3>
            <p>Días Restantes</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-info">
            <h3>{subscriptionInfo?.tiene_suscripcion ? 'Activa' : 'Inactiva'}</h3>
            <p>Estado</p>
          </div>
        </div>
      </div>

      {!subscriptionInfo?.tiene_suscripcion && (
        <div className="upgrade-prompt">
          <h3>🚀 Desbloquea todo el potencial de Axyoma</h3>
          <p>Activa una suscripción para acceder a todas las funcionalidades premium.</p>
          <div className="features-list">
            <div className="feature-item">
              <span>📊</span>
              <span>Reportes avanzados</span>
            </div>
            <div className="feature-item">
              <span>👥</span>
              <span>Gestión ilimitada de empleados</span>
            </div>
            <div className="feature-item">
              <span>🔐</span>
              <span>Seguridad empresarial</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Componente Reportes
const ReportesSection: React.FC = () => {
  return (
    <div className="reportes-section">
      <h3>📈 Reportes y Análisis</h3>
      <p>Aquí podrás acceder a todos los reportes de tu empresa.</p>
    </div>
  );
};

export default EmpresaAdminDashboard;
