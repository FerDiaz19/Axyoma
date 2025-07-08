import React, { useState, useEffect, useCallback } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
import { logout } from '../services/authService';
import '../css/Dashboard.css';
import '../css/GestionPlantas.css';
import '../css/EmpresaAdminDashboard.css';

interface EmpresaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'plantas' | 'departamentos' | 'puestos' | 'empleados' | 'estructura' | 'evaluaciones' | 'reportes'>('plantas');
  const [subscriptionInfo, setSubscriptionInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadSubscriptionInfo = useCallback(async () => {
    try {
      console.log('🔄 Cargando información de suscripción...');
      // Usar empresa_id de userData si está disponible
      const empresaId = userData?.empresa_id;
      if (empresaId) {
        const { obtenerInfoSuscripcionEmpresa } = await import('../services/suscripcionService');
        const info = await obtenerInfoSuscripcionEmpresa(empresaId);
        console.log('✅ Información de suscripción recibida:', info);
        setSubscriptionInfo(info);
      } else {
        throw new Error('No se encontró empresa_id en userData');
      }
    } catch (error) {
      console.error('❌ Error loading subscription info:', error);
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
    // Usar la información de suscripción que viene del login en lugar de hacer una nueva llamada
    if (userData?.suscripcion) {
      console.log('🔄 Usando información de suscripción del login:', userData.suscripcion);
      setSubscriptionInfo(userData.suscripcion);
      setLoading(false);
    } else {
      // Solo como fallback si no hay información en userData
      loadSubscriptionInfo();
    }
    
    // Verificar si hay un parámetro que indique que se debe refrescar
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('refresh') === 'true') {
      // Limpiar el parámetro y refrescar datos
      window.history.replaceState({}, document.title, window.location.pathname);
      setTimeout(() => {
        loadSubscriptionInfo();
      }, 500);
    }
    
    // Agregar listener para eventos de storage (para sincronizar entre tabs)
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

  // Verificar si la empresa está suspendida o sin suscripción
  const shouldShowSuspended = subscriptionInfo && 
    !subscriptionInfo.tiene_suscripcion && 
    subscriptionInfo.requiere_pago &&
    ['sin_suscripcion', 'pendiente_pago', 'vencida'].includes(subscriptionInfo.estado);

  const isEmpresaSuspendida = userData?.empresa_suspendida || 
                             userData?.advertencia?.tipo === 'empresa_suspendida' ||
                             shouldShowSuspended;

  const getSuspensionMessage = () => {
    if (!subscriptionInfo) return 'Verificando estado de suscripción...';
    
    switch (subscriptionInfo.estado) {
      case 'sin_suscripcion':
        return 'No tiene una suscripción activa';
      case 'pendiente_pago':
        return 'Suscripción pendiente de pago';
      case 'vencida':
        return `Suscripción vencida ${subscriptionInfo.dias_vencida ? `hace ${subscriptionInfo.dias_vencida} días` : ''}`;
      case 'activa':
        return 'Suscripción activa';
      default:
        return subscriptionInfo.mensaje || 'Estado de suscripción no disponible';
    }
  };

  if (loading) {
    return <div className="loading">🔄 Cargando información de la empresa...</div>;
  }

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
          <button 
            className={activeSection === 'plantas' ? 'active' : ''}
            onClick={() => setActiveSection('plantas')}
          >
            <span className="nav-icon">🏭</span>
            <span className="nav-text">Gestión de Plantas</span>
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
            className={activeSection === 'estructura' ? 'active' : ''}
            onClick={() => setActiveSection('estructura')}
          >
            <span className="nav-icon">🏗️</span>
            <span className="nav-text">Estructura Organizacional</span>
          </button>
          <button 
            className={activeSection === 'empleados' ? 'active' : ''}
            onClick={() => setActiveSection('empleados')}
          >
            <span className="nav-icon">👥</span>
            <span className="nav-text">Gestión de Empleados</span>
          </button>
          <button 
            className={activeSection === 'evaluaciones' ? 'active' : ''}
            onClick={() => setActiveSection('evaluaciones')}
          >
            <span className="nav-icon">📊</span>
            <span className="nav-text">Evaluaciones</span>
          </button>
          <button 
            className={activeSection === 'reportes' ? 'active' : ''}
            onClick={() => setActiveSection('reportes')}
          >
            <span className="nav-icon">📋</span>
            <span className="nav-text">Reportes</span>
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
            <div className="empresa-info">
              <div className="empresa-avatar">
                <span className="avatar-icon">🏢</span>
              </div>
              <div className="empresa-details">
                <span className="empresa-name">{userData?.nombre_empresa || 'Empresa'}</span>
                <span className="empresa-user">({userData?.usuario})</span>
              </div>
              {isEmpresaSuspendida && (
                <span className="status-suspended">⚠️ SUSPENDIDA</span>
              )}
              {subscriptionInfo?.tiene_suscripcion && subscriptionInfo?.estado === 'activa' && (
                <span className="status-active">
                  ✅ ACTIVA ({subscriptionInfo.dias_restantes} días)
                </span>
              )}
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <span className="logout-icon">🚪</span>
              Cerrar Sesión
            </button>
          </div>
        </header>

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
                </div>
              </div>
            ) : (
              <>
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
              </>
            )}
          </div>
        )}
        </main>
      </div>
    </div>
  );
};

export default EmpresaAdminDashboard;
