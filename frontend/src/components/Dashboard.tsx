import React, { useState, useEffect, useCallback } from 'react';
import api from '../api';
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

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setUserData(null);
    setShowSubscriptionAlert(false);
  };

  const fetchUserData = useCallback(async () => {
    try {
      const response = await api.get('/users/me/');
      const userData = response.data;
      
      console.log('📡 Datos obtenidos del servidor (/users/me/):', userData);
      
      setIsLoggedIn(true);
      setUserData(userData);
      localStorage.setItem('userData', JSON.stringify(userData));
      
      // Verificar si necesita mostrar alerta de suscripción
      checkSubscriptionAlert(userData);
    } catch (error) {
      console.error('Error obteniendo datos del usuario:', error);
      // Si hay error, limpiar sesión
      handleLogout();
    }
  }, []);

  useEffect(() => {
    // Verificar si hay una sesión activa
    const token = localStorage.getItem('authToken');
    
    if (token) {
      // Si hay token, obtener datos completos del usuario desde el backend
      fetchUserData();
    }
  }, [fetchUserData]);

  const handleLoginSuccess = (data: any) => {
    // Guardar el token
    if (data.token) {
      localStorage.setItem('authToken', data.token);
    }
    
    // Obtener datos completos del usuario desde el servidor
    fetchUserData();
  };

  const checkSubscriptionAlert = (data: any) => {
    // Solo para admins de empresa (no superusers)
    if (!data.is_superuser && data.empresa) {
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

    // Determinar el tipo de dashboard basado en los datos disponibles
    console.log('🔍 Dashboard - userData completo:', userData);
    console.log('🔍 Dashboard - nivel_usuario:', userData?.perfil?.nivel_usuario);
    console.log('🔍 Dashboard - is_superuser:', userData?.is_superuser);
    console.log('🔍 Dashboard - empresa:', userData?.empresa);
    
    if (userData?.is_superuser) {
      console.log('✅ Dirigiendo a SuperAdminDashboard');
      return <SuperAdminDashboard userData={userData} onLogout={handleLogout} />;
    } else if (userData?.perfil?.nivel_usuario === 'admin_planta') {
      console.log('✅ Dirigiendo a PlantaAdminDashboard');
      return <PlantaAdminDashboard userData={userData} />;
    } else if (userData?.empresa) {
      console.log('✅ Dirigiendo a EmpresaAdminDashboard');
      return <EmpresaAdminDashboard userData={userData} />;
    } else {
      // Dashboard por defecto para usuarios normales
      console.log('✅ Dirigiendo a EmpresaAdminDashboard (default)');
      return <EmpresaAdminDashboard userData={userData} />;
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
