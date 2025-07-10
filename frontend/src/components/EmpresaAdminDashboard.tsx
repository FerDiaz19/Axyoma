import React, { useState, useEffect, useCallback } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
<<<<<<< HEAD
import GestionEvaluaciones from './GestionEvaluaciones';
=======
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
>>>>>>> parent of 2766511 (si)
import { logout } from '../services/authService';
import '../css/ModernDashboard.css';
import '../css/Dashboard.css'; // Mantener estilos originales como fallback

interface EmpresaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'plantas' | 'empleados' | 'estructura' | 'evaluaciones' | 'reportes'>('plantas');
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

  // Menú de navegación - manteniendo estructura original
  const menuItems = [
    { id: 'plantas', label: 'Gestión de Plantas', icon: '🏭', description: 'Gestión de plantas industriales' },
    { id: 'empleados', label: 'Gestión de Empleados', icon: '👥', description: 'Administración de personal' },
    { id: 'estructura', label: 'Estructura Organizacional', icon: '🏗️', description: 'Departamentos y puestos' },
    { id: 'evaluaciones', label: 'Gestión de Evaluaciones', icon: '📝', description: 'Gestión de evaluaciones' },
    { id: 'reportes', label: 'Reportes', icon: '📈', description: 'Análisis y reportes' }
  ];

  const renderActiveSection = () => {
    // Mostrar advertencia de suspensión si es necesario
    if (isEmpresaSuspendida && activeSection === 'reportes') {
      return (
        <div className="suspension-warning">
          <div className="warning-card">
            <div className="warning-icon">🚫</div>
            <div className="warning-content">
              <h3>Acceso Restringido a Reportes</h3>
              <p>
                Su empresa no tiene una suscripción activa. 
                Los reportes requieren una suscripción para acceder.
              </p>
            </div>
          </div>
        </div>
      );
    }

    switch (activeSection) {
      case 'plantas':
        return <GestionPlantas empresaId={userData?.empresa_id} />;
      case 'empleados':
        return <EmpleadosCRUD userData={userData} />;
      case 'estructura':
        return <GestionEstructura />;
      case 'evaluaciones':
        return (
          <GestionEvaluaciones 
            usuario={userData}
          />
        );
      case 'reportes':
        return subscriptionInfo?.tiene_suscripcion ? (
          <ReportesSection />
        ) : (
          <div className="upgrade-needed">
            <div className="upgrade-card">
              <span className="upgrade-icon">🔒</span>
              <h3>Sección Premium</h3>
              <p>Los reportes requieren una suscripción activa.</p>
            </div>
          </div>
        );
      default:
        return <GestionPlantas empresaId={userData?.empresa_id} />;
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

<<<<<<< HEAD
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
=======
        {/* Content area */}
        <main className="dashboard-content">
          {/* Información de suscripción activa */}
          {subscriptionInfo?.tiene_suscripcion && subscriptionInfo?.estado === 'activa' && (
            <div className="subscription-alert">
              <div className="warning-content">
                <h3>✅ Suscripción Activa</h3>
                <div style={{ display: 'flex', gap: '20px', color: '#155724' }}>
                  <span>Plan: {subscriptionInfo.suscripcion?.plan_nombre}</span>
                  <span>Días restantes: {subscriptionInfo.dias_restantes}</span>
                  <span>Vence: {subscriptionInfo.fecha_vencimiento}</span>
                </div>
              </div>
            </div>
          )}

          {/* Mensaje de advertencia para empresa suspendida */}
          {isEmpresaSuspendida && (
            <div className="subscription-warning">
              <div className="warning-content">
                <h3>⚠️ {getSuspensionMessage()}</h3>
                <p>
                  {subscriptionInfo?.estado === 'sin_suscripcion' && 
                    'Para acceder a todas las funcionalidades, debe activar una suscripción.'}
                  {subscriptionInfo?.estado === 'pendiente_pago' && 
                    'Complete el pago para activar su suscripción y acceder a todas las funcionalidades.'}
                  {subscriptionInfo?.estado === 'vencida' && 
                    'Su suscripción ha vencido. Renueve su plan para continuar usando el sistema.'}
                  {!subscriptionInfo?.estado && 
                    'Las funcionalidades están limitadas. Contacte con soporte para reactivar su suscripción.'}
                </p>
                <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                  <button 
                    className="renewal-button" 
                    onClick={() => window.location.href = '/plan-selection'}
                  >
                    🔄 Activar Suscripción
                  </button>
                  <button 
                    onClick={loadSubscriptionInfo}
                    className="action-button"
                    style={{ backgroundColor: '#6c757d' }}
                  >
                    🔃 Verificar Estado
                  </button>
                </div>
              </div>
            </div>
          )}
        {activeSection === 'plantas' && (
          <GestionPlantas empresaId={userData?.empresa_id} />
        )}
        {activeSection === 'departamentos' && <GestionDepartamentos />}
        {activeSection === 'puestos' && <GestionPuestos />}
        {activeSection === 'estructura' && <GestionEstructura />}
        {activeSection === 'empleados' && <EmpleadosCRUD userData={userData} />}
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
            {isEmpresaSuspendida ? (
              <div className="subscription-expired">
                <h2>❌ {getSuspensionMessage()}</h2>
                <p>
                  {subscriptionInfo?.estado === 'sin_suscripcion' && 
                    'Para acceder a reportes y estadísticas, debe activar una suscripción.'}
                  {subscriptionInfo?.estado === 'pendiente_pago' && 
                    'Complete el pago de su suscripción para acceder a reportes y estadísticas.'}
                  {subscriptionInfo?.estado === 'vencida' && 
                    'Su suscripción ha vencido. Renueve su plan para acceder a reportes y estadísticas.'}
                  {!subscriptionInfo?.estado && 
                    'Su suscripción ha expirado. Para acceder a estadísticas y reportes, debe renovar su plan.'}
                </p>
                <div className="expired-message">
                  <h3>🚫 Funciones No Disponibles:</h3>
                  <ul>
                    <li>• Reportes detallados</li>
                    <li>• Estadísticas avanzadas</li>
                    <li>• Análisis de rendimiento</li>
                    <li>• Exportación de datos</li>
                  </ul>
                  <button className="renewal-button" onClick={() => window.location.href = '/plan-selection'}>
                    � Activar Suscripción
                  </button>
>>>>>>> parent of 2766511 (si)
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
                    onClick={() => setActiveSection('plantas')}
                  >
                    <span>💳</span>
                    Ver Gestión de Plantas
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

// Componente Reportes
const ReportesSection: React.FC = () => {
  return (
    <div className="reportes-section">
      <h3>📈 Reportes y Análisis</h3>
      <p>Aquí podrás acceder a todos los reportes de tu empresa.</p>
      <div className="coming-soon">
        <h4>� Próximamente</h4>
        <p>Esta sección estará disponible en futuras actualizaciones.</p>
      </div>
    </div>
  );
};

export default EmpresaAdminDashboard;
