import React, { useState, useEffect } from 'react';
import Login from './Login';
import RegistroEmpresa from './RegistroEmpresa';
import SuperAdminDashboard from './SuperAdminDashboard_NEW';
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

  useEffect(() => {
    // Verificar si hay una sesión activa
    const token = localStorage.getItem('authToken');
    const userDataStored = localStorage.getItem('userData');
    
    if (token && userDataStored) {
      setIsLoggedIn(true);
      setUserData(JSON.parse(userDataStored));
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
        return <EmpresaAdminDashboard userData={userData} onLogout={handleLogout} />;
      
      case 'admin-planta':
        return <PlantaAdminDashboard userData={userData} onLogout={handleLogout} />;
      
      default:
        return <div>Error: Tipo de dashboard no reconocido</div>;
    }
  };

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
