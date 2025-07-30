import { Route, Routes } from 'react-router-dom';

// Components
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import PlanSelection from './components/PlanSelection';
import RegistroEmpresa from './components/RegistroEmpresa';

const AppRoutes = () => {
  const handleLogin = (userData: any) => {
    // Guardar datos del usuario y redireccionar al dashboard
    localStorage.setItem('userData', JSON.stringify(userData));
    window.location.href = '/dashboard';
  };

  return (
    <Routes>
      <Route index element={<LandingPage />} />
      <Route path="/login" element={<Login onLogin={handleLogin} />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/registro" element={<RegistroEmpresa onRegistroSuccess={() => window.location.href = '/dashboard'} />} />
      <Route path="/plan-selection" element={<PlanSelection empresaId={1} onPlanSelected={() => window.location.href = '/dashboard'} />} />
    </Routes>
  );
};

export default AppRoutes;
