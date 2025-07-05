import React, { useState, useEffect } from 'react';
import Login from './Login';
import RegistroEmpresa from './RegistroEmpresa';
import SuperAdminDashboard from './SuperAdminDashboard';
import EmpresaAdminDashboard from './EmpresaAdminDashboard';
import PlantaAdminDashboard from './PlantaAdminDashboard';
import { logout } from '../services/authService';
import '../css/Dashboard.css';

const Dashboard: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegistro, setShowRegistro] = useState(false);
  const [userData, setUserData] = useState<any>(null);

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
  };

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setUserData(null);
    localStorage.removeItem('userData');
  };

  const handleRegistroSuccess = () => {
    setShowRegistro(false);
    alert('Empresa registrada exitosamente. Ahora puedes iniciar sesión.');
  };

  // Renderizar el dashboard según el tipo de usuario
  const renderDashboard = () => {
    if (!userData?.tipo_dashboard) {
      return <div>Error: Tipo de usuario no válido</div>;
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
              onLoginSuccess={handleLoginSuccess} 
              onSwitchToRegister={() => setShowRegistro(true)}
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
