import React, { useState, useEffect } from 'react';
import Login from './Login';
import RegistroEmpresa from './RegistroEmpresa';
import SuperAdminDashboard from './SuperAdminDashboard';
import EmpresaAdminDashboard from './EmpresaAdminDashboard';
import PlantaAdminDashboard from './PlantaAdminDashboard';
import SubscriptionAlert from './SubscriptionAlert';
import { logout } from '../services/authService';
import '../css/Dashboard.css';

const Dashboard: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegistro, setShowRegistro] = useState(false);
  const [userData, setUserData] = useState<any>(null);
  const [showSubscriptionAlert, setShowSubscriptionAlert] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

<<<<<<< HEAD
  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setUserData(null);
    setShowSubscriptionAlert(false);
    setIsLoading(false);
    setError(null);
  };

  const fetchUserData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.get('/users/me/');
      const userData = response.data;
      
      console.log('📡 Datos obtenidos del servidor (/users/me/):', userData);
      
      setIsLoggedIn(true);
      setUserData(userData);
      localStorage.setItem('userData', JSON.stringify(userData));
      
      // Verificar si necesita mostrar alerta de suscripción
      checkSubscriptionAlert(userData);
    } catch (error: any) {
      console.error('Error obteniendo datos del usuario:', error);
      setError(`Error cargando datos del usuario: ${error?.response?.status || error?.message || 'Error desconocido'}`);
      // Si hay error, limpiar sesión solo si es error de autenticación
      if (error?.response?.status === 401 || error?.response?.status === 403) {
        handleLogout();
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

=======
>>>>>>> parent of f78dc52 (solucion de errores de login y usuarios de planta)
  useEffect(() => {
    // Verificar si hay una sesión activa
    const token = localStorage.getItem('authToken');
    const userDataStored = localStorage.getItem('userData');
    
<<<<<<< HEAD
    if (token) {
      // Si hay token, obtener datos completos del usuario desde el backend
      fetchUserData();
    } else {
      setIsLoading(false);
=======
    if (token && userDataStored) {
      setIsLoggedIn(true);
      setUserData(JSON.parse(userDataStored));
>>>>>>> parent of f78dc52 (solucion de errores de login y usuarios de planta)
    }
  }, []);

  const handleLoginSuccess = (data: any) => {
    setIsLoggedIn(true);
    setUserData(data);
    localStorage.setItem('userData', JSON.stringify(data));
    
    // Asegurar que el token esté guardado (ya debe estar desde authService.login)
    if (data.token && !localStorage.getItem('authToken')) {
      localStorage.setItem('authToken', data.token);
    }
    
    // Verificar si necesita mostrar alerta de suscripción
    checkSubscriptionAlert(data);
  };

  const checkSubscriptionAlert = (data: any) => {
    // Solo para admins de empresa y planta
    if (data.tipo_dashboard === 'admin-empresa' || data.tipo_dashboard === 'admin-planta') {
      const suscripcion = data.suscripcion;
      const advertencia = data.advertencia;
      
      // Mostrar alerta si:
      // 1. No tiene suscripción
      // 2. Suscripción vencida
      // 3. Empresa suspendida por suscripción
      if (!suscripcion?.tiene_suscripcion || 
          advertencia?.requiere_accion ||
          (suscripcion && (suscripcion.estado === 'sin_suscripcion' || suscripcion.estado === 'vencida'))) {
        setShowSubscriptionAlert(true);
      }
    }
  };

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setUserData(null);
    setShowSubscriptionAlert(false);
    localStorage.removeItem('userData');
  };

  const handleRegistroSuccess = () => {
    setShowRegistro(false);
    alert('Empresa registrada exitosamente. Ahora puedes iniciar sesión.');
  };

  const handleSubscriptionUpdated = () => {
    setShowSubscriptionAlert(false);
    // Recargar datos del usuario para reflejar nueva suscripción
    window.location.reload();
  };

  const handleContinueWithLimitations = () => {
    setShowSubscriptionAlert(false);
  };

  // Obtener información para la alerta de suscripción
  const getSubscriptionAlertInfo = () => {
    if (!userData?.suscripcion) return null;
    
    const suscripcion = userData.suscripcion;
    const empresaId = userData.empresa_id;
    const empresaNombre = userData.nombre_empresa;
    
    let tipoAlerta: 'sin_suscripcion' | 'vencida' | 'por_vencer' = 'sin_suscripcion';
    let diasRestantes = 0;
    
    if (suscripcion.estado === 'vencida') {
      tipoAlerta = 'vencida';
      diasRestantes = suscripcion.dias_vencida || 0;
    } else if (suscripcion.estado === 'por_vencer') {
      tipoAlerta = 'por_vencer';
      diasRestantes = suscripcion.dias_restantes || 0;
    }
    
    return {
      empresaId,
      empresaNombre,
      tipoAlerta,
      diasRestantes
    };
  };

  // Renderizar el dashboard según el tipo de usuario
  const renderDashboard = () => {
    if (!userData?.tipo_dashboard) {
      return <div>Error: Tipo de usuario no válido</div>;
    }

    // Si hay alerta de suscripción, mostrarla primero
    if (showSubscriptionAlert) {
      const alertInfo = getSubscriptionAlertInfo();
      if (alertInfo) {
        return (
          <SubscriptionAlert
            empresaId={alertInfo.empresaId}
            empresaNombre={alertInfo.empresaNombre}
            tipoAlerta={alertInfo.tipoAlerta}
            diasRestantes={alertInfo.diasRestantes}
            onSubscriptionUpdated={handleSubscriptionUpdated}
            onContinueWithLimitations={handleContinueWithLimitations}
          />
        );
      }
    }

    switch (userData.tipo_dashboard) {
      case 'superadmin':
        return <SuperAdminDashboard userData={userData} onLogout={handleLogout} />;
      
      case 'admin-empresa':
        return <EmpresaAdminDashboard userData={userData} />;
      
      case 'admin-planta':
        return <PlantaAdminDashboard userData={userData} />;
      
      default:
        return <div>Error: Tipo de dashboard no reconocido</div>;
    }
  };

  // Mostrar loading mientras se cargan los datos
  if (isLoading) {
    return (
      <div className="loading-container" style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        flexDirection: 'column'
      }}>
        <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔄</div>
        <div>Cargando datos del usuario...</div>
      </div>
    );
  }

  // Mostrar error si hay problemas
  if (error) {
    return (
      <div className="error-container" style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        flexDirection: 'column',
        padding: '2rem'
      }}>
        <div style={{ fontSize: '2rem', marginBottom: '1rem', color: 'red' }}>❌</div>
        <div style={{ marginBottom: '1rem', color: 'red', textAlign: 'center' }}>{error}</div>
        <button onClick={handleLogout} style={{
          padding: '10px 20px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}>
          Cerrar Sesión y Reintentar
        </button>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="auth-container">
        {!showRegistro ? (
          <div>
            <Login 
              onLogin={handleLoginSuccess} 
            />
          </div>
        ) : (
          <div>
            <RegistroEmpresa 
              onRegistroSuccess={handleRegistroSuccess} 
              onSwitchToLogin={() => setShowRegistro(false)}
            />
          </div>
        )}
      </div>
    );
  }

  return renderDashboard();
};

export default Dashboard;
