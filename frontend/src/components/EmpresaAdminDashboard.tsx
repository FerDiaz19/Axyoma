import React, { useState, useEffect } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionEstructura from './GestionEstructura';
import GestionPlantas from './GestionPlantas';
import { logout } from '../services/authService';
import { obtenerSuscripcionActual } from '../services/suscripcionService';
import '../css/Dashboard.css';
import '../css/GestionPlantas.css';

interface EmpresaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'plantas' | 'empleados' | 'estructura' | 'evaluaciones' | 'reportes'>('plantas');
  const [subscriptionInfo, setSubscriptionInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSubscriptionInfo();
    
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
  }, []);

  const loadSubscriptionInfo = async () => {
    try {
      console.log('🔄 Cargando información de suscripción...');
      const info = await obtenerSuscripcionActual();
      console.log('✅ Información de suscripción recibida:', info);
      setSubscriptionInfo(info);
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
  };

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
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>Panel de Administración - Empresa</h1>
          <div className="empresa-info">
            <span>Cargando...</span>
          </div>
        </header>
        <div className="loading-subscription">
          <p>Verificando estado de suscripción...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Panel de Administración - Empresa</h1>
        <div className="empresa-info">
          <span>{userData?.nombre_empresa || 'Empresa'}</span>
          <span>({userData?.usuario})</span>
          {isEmpresaSuspendida && (
            <span className="status-suspended">⚠️ SUSPENDIDA</span>
          )}
          {subscriptionInfo?.tiene_suscripcion && subscriptionInfo?.estado === 'activa' && (
            <span className="status-active" style={{ color: '#28a745', fontWeight: 'bold' }}>
              ✅ ACTIVA ({subscriptionInfo.dias_restantes} días)
            </span>
          )}
        </div>
        <button onClick={handleLogout} className="logout-btn">
          Cerrar Sesión
        </button>
      </header>

      {/* Información de suscripción activa */}
      {subscriptionInfo?.tiene_suscripcion && subscriptionInfo?.estado === 'activa' && (
        <div className="subscription-active-info" style={{ 
          margin: '20px 0', 
          padding: '15px', 
          backgroundColor: '#d4edda', 
          borderRadius: '5px', 
          border: '1px solid #c3e6cb' 
        }}>
          <h4 style={{ color: '#155724', margin: '0 0 10px 0' }}>✅ Suscripción Activa</h4>
          <div style={{ display: 'flex', gap: '20px', color: '#155724' }}>
            <span>Plan: {subscriptionInfo.suscripcion?.plan_nombre}</span>
            <span>Días restantes: {subscriptionInfo.dias_restantes}</span>
            <span>Vence: {subscriptionInfo.fecha_vencimiento}</span>
          </div>
        </div>
      )}

      {/* Mensaje de advertencia para empresa suspendida */}
      {isEmpresaSuspendida && (
        <div className="suspension-warning">
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
                style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                🔄 Activar Suscripción
              </button>
              <button 
                onClick={loadSubscriptionInfo}
                style={{ padding: '10px 20px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                🔃 Verificar Estado
              </button>
            </div>
          </div>
        </div>
      )}

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
  );
};

export default EmpresaAdminDashboard;
