import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Login from './Login';
import RegistroEmpresa from './RegistroEmpresa';
import SuperAdminDashboard from './SuperAdminDashboard';
import EmpresaAdminDashboard from './EmpresaAdminDashboard';
import PlantaAdminDashboard from './PlantaAdminDashboard';
// import EmpleadoDashboard from './EmpleadoDashboard'; // Importar el dashboard de empleado
// ⬆️ Descomenta la línea de abajo si el archivo existe en otra ruta o crea el archivo si no existe
import EmpleadoDashboard from './EmpleadoDashboard'; // Asegúrate de que este archivo exista en src/components/
import SubscriptionAlert from './SubscriptionAlert';
import { logout } from '../services/authService';
import '../css/Dashboard.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
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

    // Redirigir al landing page
    navigate('/', { replace: true });

    // Forzar recarga para reiniciar completamente la app
    setTimeout(() => {
      window.location.reload();
    }, 50);
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
    // Añadir diagnóstico para ver qué está recibiendo el sistema
    console.log('🧪 Dashboard: userData recibido:', userData);
    console.log('🧪 Tipo de usuario detectado:', userData?.nivel_usuario);
    console.log('🧪 Tipo de dashboard detectado:', userData?.tipo_dashboard);

    if (!userData) {
      return <div className="error-container">No hay información de usuario disponible</div>;
    }

    // Validación mejorada del nivel de usuario
    const tipoUsuario = userData.nivel_usuario?.toLowerCase();
    const tipoDashboard = userData.tipo_dashboard?.toLowerCase();

    try {
      // Validar tipos conocidos
      if (tipoUsuario === 'superadmin' || tipoUsuario === 'super_admin' || tipoUsuario === 'super-admin') {
        return <SuperAdminDashboard userData={userData} onLogout={handleLogout} />;
      }

      if (tipoUsuario === 'admin_empresa' || tipoUsuario === 'admin-empresa' || tipoDashboard === 'admin-empresa') {
        return <EmpresaAdminDashboard userData={userData} />;
      }

      if (tipoUsuario === 'admin_planta' || tipoUsuario === 'admin-planta' || tipoDashboard === 'admin-planta') {
        return <PlantaAdminDashboard userData={userData} />;
      }

      if (tipoUsuario === 'empleado') {
        return <EmpleadoDashboard userData={userData} />;
      }

      // Si llegamos aquí, el tipo no es válido
      console.error('❌ ERROR: Tipo de usuario no reconocido:', {
        nivel_usuario: userData.nivel_usuario,
        tipo_dashboard: userData.tipo_dashboard
      });

      return (
        <div className="error-container">
          <h2>Error: Tipo de usuario no válido</h2>
          <p>Nivel de usuario recibido: <strong>{userData.nivel_usuario || 'No definido'}</strong></p>
          <p>Tipo dashboard recibido: <strong>{userData.tipo_dashboard || 'No definido'}</strong></p>
          <p>Por favor contacte al administrador del sistema con esta información.</p>
          <button onClick={handleLogout} className="error-logout-btn">
            Cerrar sesión e intentar nuevamente
          </button>
        </div>
      );
    } catch (err) {
      console.error('❌ Error renderizando dashboard:', err);
      return (
        <div className="error-container">
          <h2>Error inesperado</h2>
          <p>Ha ocurrido un error al cargar la interfaz. Por favor intente nuevamente.</p>
          <p>Detalles: {(err as Error).message}</p>
          <button onClick={handleLogout} className="error-logout-btn">
            Cerrar sesión e intentar nuevamente
          </button>
        </div>
      );
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
