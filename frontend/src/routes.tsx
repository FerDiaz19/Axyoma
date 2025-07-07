import { Route, Routes } from 'react-router-dom';

// Components
import Dashboard from './components/Dashboard';
import PlanSelection from './components/PlanSelection';

const AppRoutes = () => (
    <Routes>
        <Route index element={<Dashboard />} />
        <Route path="/plan-selection" element={<PlanSelection empresaId={1} onPlanSelected={() => window.location.href = '/'} />} />
    </Routes>
);

export default AppRoutes;
