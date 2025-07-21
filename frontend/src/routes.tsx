import { Route, Routes } from 'react-router-dom';

// Components
import Dashboard from './components/Dashboard';
import PlanSelection from './components/PlanSelection';
import RegistroEmpresa from './components/RegistroEmpresa';
import LoginEmpleado from './components/LoginEmpleado';
import TokenLogin from './components/TokenLogin';

const AppRoutes = () => (
    <Routes>
        <Route index element={<Dashboard />} />
        <Route path="/registro" element={<RegistroEmpresa onRegistroSuccess={() => window.location.href = '/'} />} />
        <Route path="/plan-selection" element={<PlanSelection empresaId={1} onPlanSelected={() => window.location.href = '/'} />} />
        <Route path="/empleado" element={<LoginEmpleado />} />
        <Route path="/token-login" element={<TokenLogin />} />
    </Routes>
);

export default AppRoutes;
